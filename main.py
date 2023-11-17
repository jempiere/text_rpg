import eloy 
from mafia import systems as s

def main():
    roleCounts = s.setRules()
    players = s.createPlayers(roleCounts)

main()
