use futures::stream::StreamExt;
use lazy_static::lazy_static;
use libp2p::{
    self, gossipsub, mdns, noise, swarm::NetworkBehaviour, swarm::SwarmEvent, tcp, yamux,
};
use pyo3::prelude::*;
use ringbuffer::{AllocRingBuffer, RingBuffer};
use std::collections::hash_map::DefaultHasher;
use std::error::Error;
use std::hash::{Hash, Hasher};
use std::sync::{Arc, Mutex};
use std::time::Duration;
use tokio::{io, io::AsyncBufReadExt, select};
use tracing_subscriber::EnvFilter;

lazy_static! {
    static ref NETWORKER: Arc<Mutex<Option<Box<Networker>>>> = Arc::new(Mutex::new(None));
}

macro_rules! networker {
    // A rust macro to lock the NETWORKER mutex, and unwrap the Option inside.
    () => {
        NETWORKER
            .lock()
            .unwrap()
            .as_mut()
            .expect("Networker not initialized")
    };
}

struct Networker {
    inbound: AllocRingBuffer<String>,
    outbound: AllocRingBuffer<String>,
    events: AllocRingBuffer<String>,
    network_name: String,
}
impl Networker {
    fn new(network_name: String) -> Self {
        Self {
            inbound: AllocRingBuffer::new(1024),
            outbound: AllocRingBuffer::new(1024),
            events: AllocRingBuffer::new(1024),
            network_name,
        }
    }

    fn get_messages() -> Vec<String> {
        networker!().inbound.drain().collect()
    }
    fn push_message(data: String) {
        networker!().outbound.enqueue(data);
    }
    fn get_events() -> Vec<String> {
        networker!().events.drain().collect()
    }
}
#[derive(NetworkBehaviour)]
struct MyBehaviour {
    gossipsub: gossipsub::Behaviour,
    mdns: mdns::tokio::Behaviour,
}

async fn start_network() -> Result<(), Box<dyn Error>> {
    let _ = tracing_subscriber::fmt()
        .with_env_filter(EnvFilter::from_default_env())
        .try_init();

    let mut swarm = libp2p::SwarmBuilder::with_new_identity()
        .with_tokio()
        .with_tcp(
            tcp::Config::default(),
            noise::Config::new,
            yamux::Config::default,
        )?
        .with_quic()
        .with_behaviour(|key| {
            // To content-address message, we can take the hash of message and use it as an ID.
            let message_id_fn = |message: &gossipsub::Message| {
                let mut s = DefaultHasher::new();
                message.data.hash(&mut s);
                gossipsub::MessageId::from(s.finish().to_string())
            };

            // Set a custom gossipsub configuration
            let gossipsub_config = gossipsub::ConfigBuilder::default()
                .heartbeat_interval(Duration::from_secs(10)) // This is set to aid debugging by not cluttering the log space
                .validation_mode(gossipsub::ValidationMode::Strict) // This sets the kind of message validation. The default is Strict (enforce message signing)
                .message_id_fn(message_id_fn) // content-address messages. No two messages of the same content will be propagated.
                .build()
                .map_err(|msg| io::Error::new(io::ErrorKind::Other, msg))?; // Temporary hack because `build` does not return a proper `std::error::Error`.

            // build a gossipsub network behaviour
            let gossipsub = gossipsub::Behaviour::new(
                gossipsub::MessageAuthenticity::Signed(key.clone()),
                gossipsub_config,
            )?;

            let mdns =
                mdns::tokio::Behaviour::new(mdns::Config::default(), key.public().to_peer_id())?;
            Ok(MyBehaviour { gossipsub, mdns })
        })?
        .with_swarm_config(|c| c.with_idle_connection_timeout(Duration::from_secs(60)))
        .build();

    // Create a Gossipsub topic
    let topic = gossipsub::IdentTopic::new("test-net"); //networker!().network_name.clone());
                                                        // subscribes to our topic
    swarm.behaviour_mut().gossipsub.subscribe(&topic)?;

    // Listen on all interfaces and whatever port the OS assigns
    swarm.listen_on("/ip4/0.0.0.0/udp/0/quic-v1".parse()?)?;
    swarm.listen_on("/ip4/0.0.0.0/tcp/0".parse()?)?;

    loop {
        select! {
            //TODO: Make this less than 1000
            _ = tokio::time::sleep(Duration::from_millis(1000)) => {
                let mut nw1 = NETWORKER.lock().unwrap();
                let nw = nw1.as_mut().unwrap();
                let mut outbound = nw.outbound.drain();
                while let Some(data) = outbound.next() {
                    if let Err(e) =  swarm.behaviour_mut().gossipsub.publish(topic.clone(), data.as_bytes()) {
                        nw.events.enqueue(format!("PublishError;{e:?}"));
                    }
                }
            }
            event = swarm.select_next_some() => match event {
                SwarmEvent::Behaviour(MyBehaviourEvent::Mdns(mdns::Event::Discovered(list))) => {
                    for (peer_id, multiaddr) in list {
                        networker!().events.enqueue(format!("Discovered;{};{}", peer_id, multiaddr));
                        swarm.behaviour_mut().gossipsub.add_explicit_peer(&peer_id);
                    }
                },
                SwarmEvent::Behaviour(MyBehaviourEvent::Mdns(mdns::Event::Expired(list))) => {
                    for (peer_id, multiaddr) in list {
                        networker!().events.enqueue(format!("Expired;{};{}", peer_id, multiaddr));
                        swarm.behaviour_mut().gossipsub.remove_explicit_peer(&peer_id);
                    }
                },
                SwarmEvent::Behaviour(MyBehaviourEvent::Gossipsub(gossipsub::Event::Message {
                    propagation_source: peer_id,
                    message_id,
                    message,
                })) => {
                    networker!().inbound.enqueue(format!("Message;{};{};{}", peer_id, message_id, String::from_utf8_lossy(&message.data)));
                },
                SwarmEvent::ConnectionEstablished { peer_id, connection_id, endpoint, num_established, concurrent_dial_errors, established_in } => {
                    networker!().events.enqueue(format!("ConnectionEstablished;{peer_id};{connection_id};{num_established}"));
                },
                SwarmEvent::ConnectionClosed { peer_id, connection_id, endpoint, num_established, cause } => {
                    networker!().events.enqueue(format!("ConnectionClosed;{peer_id};{connection_id};{num_established}"));
                },
                SwarmEvent::IncomingConnection { connection_id, local_addr, send_back_addr } => {
                    networker!().events.enqueue(format!("IncomingConnection;{connection_id};{local_addr};{send_back_addr}"));
                },
                SwarmEvent::IncomingConnectionError { connection_id, local_addr, send_back_addr, error } => {
                    networker!().events.enqueue(format!("IncomingConnectionError;{connection_id};{local_addr};{send_back_addr};{error}"));
                },
                SwarmEvent::OutgoingConnectionError { connection_id, peer_id, error } => {
                    if peer_id.is_some() {
                        let peer_id = peer_id.unwrap();
                        networker!().events.enqueue(format!("OutgoingConnectionError;{connection_id};{peer_id};{error}"));
                    }
                    networker!().events.enqueue(format!("OutgoingConnectionError;{connection_id};;{error}"));
                },
                SwarmEvent::NewListenAddr { address, .. } => {
                    networker!().events.enqueue(format!("NewListenAddr;{address}"));
                },
                SwarmEvent::ExpiredListenAddr { listener_id, address } => {
                    networker!().events.enqueue(format!("ExpiredListenAddr;{address}"));
                },
                SwarmEvent::ListenerClosed { listener_id, addresses, reason } => {
                    networker!().events.enqueue(format!("ListenerClosed"));
                }
                SwarmEvent::ListenerError { listener_id, error } => {
                    networker!().events.enqueue(format!("ListenerError;{error}"));
                },
                SwarmEvent::Dialing { peer_id, connection_id } => {
                    networker!().events.enqueue(format!("Dialing;{connection_id}"));
                },
                SwarmEvent::NewExternalAddrCandidate { address } => {
                    networker!().events.enqueue(format!("NewExternalAddrCandidate;{address}"));
                },
                SwarmEvent::ExternalAddrConfirmed { address } => {
                    networker!().events.enqueue(format!("ExternalAddrConfirmed;{address}"));
                },
                SwarmEvent::ExternalAddrExpired { address } => {
                    networker!().events.enqueue(format!("ExternalAddrExpired;{address}"));
                },
                _ => {},

            }
        }
    }
}

#[pyfunction]
fn get_messages() -> Vec<String> {
    Networker::get_messages()
}

#[pyfunction]
fn push_message(data: String) {
    Networker::push_message(data);
}

#[pyfunction]
fn get_events() -> Vec<String> {
    Networker::get_events()
}

#[pyfunction]
fn init(network_name: String) {
    //TODO: Warn game dev if they're double initializing.
    let net = Networker::new(network_name);
    NETWORKER.lock().unwrap().get_or_insert(Box::new(net));

    use std::thread;
    thread::spawn(move || {
        tokio::runtime::Builder::new_multi_thread()
            .enable_all()
            .build()
            .unwrap()
            .block_on(start_network())
            .unwrap();
    });
}

#[pymodule]
fn libp2py(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(init, m)?)?;
    m.add_function(wrap_pyfunction!(get_events, m)?)?;
    m.add_function(wrap_pyfunction!(get_messages, m)?)?;
    m.add_function(wrap_pyfunction!(push_message, m)?)?;
    Ok(())
}
