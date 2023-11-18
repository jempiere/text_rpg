import esper
from dataclasses import dataclass
from typing import List
import libp2py
import time
from serde import serde
from serde.json import to_json, from_json

libp2py.init("myapp")

_classnames = {}


def component(cls):
    cls = serde(dataclass(cls))
    _classnames[cls.__name__] = cls
    return cls


def sendSerialized():
    entities = esper._entities
    for entity in entities:
        json = f"{entity};"
        components = entities[entity]
        comma = False
        for component in components:
            if not comma:
                comma = True
            else:
                json += ";"
            data = f"{component.__name__}:{to_json(components[component])}"
            json += data
        libp2py.push_message(json)


def receiveSerialized():
    for json in libp2py.get_messages():
        data = json.split(";")
        entity = data[0]
        if entity in esper._entities:
            esper.delete_entity(entity)
        esper._entities[entity] = {}
        components = data[1:]
        for component in components:
            name, data = component.split(":", 1)
            cls = _classnames[name]
            obj = from_json(cls, data)
            esper.add_component(entity, obj)


def netcodeHandler():
    # for msg in libp2py.get_events():
    #     print(msg)
    for msg in libp2py.get_messages():
        print(msg)

    time.sleep(0.3)


@component
class Test:
    test: str = "test"


# @serde
# @dataclass
@component
class Player:
    name: str
    age: int


esper.create_entity(Test())
esper.create_entity(Player(name="Eloy", age=18))
esper.create_entity(Player(name="20", age=30), Test())

sendSerialized()
