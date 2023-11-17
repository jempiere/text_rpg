""" Client Management """
from dataclasses import dataclass




@dataclass
class Client:
    control: bool = False
    age: int = inf
    server: object
    renderer: object

    def host(self,port='127.0.0.1'):
        """ """
        ...
        
    def render(self):
        """ """
        ...

def promoteMinion(minion: Client):
    """Set the passed minion as the master"""
    ...


