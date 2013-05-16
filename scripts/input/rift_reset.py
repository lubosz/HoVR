from bge import logic as G
from bge import events
from rift import PyRift

keyboard = G.keyboard.events

if keyboard[events.SPACEKEY] == 1:
    print ("Reset Rift")
    bge.logic.rift.reset()
