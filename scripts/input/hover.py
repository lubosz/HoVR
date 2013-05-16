from bge import logic as G
from bge import events
from mathutils import *
from math import sin
import time

keyboard = G.keyboard.events

cont = G.getCurrentController()
owner = cont.owner

if not "underwater" in owner:
    owner["underwater"] = False

vel = owner.getLinearVelocity()

#water
if owner.worldPosition.z < 0.7:
    upmov = 0.2
elif owner.worldPosition.z > 10.0:
    upmov = -0.02
else:
    upmov = 0.15
    
#upmov *= 2 * sin(time.time()*8.0))/2.0
    
owner.setLinearVelocity([vel[0], vel[1], vel[2]+upmov], False)

#if owner.worldPosition.z < 0.9:
#    print ("water!")
    

if owner.worldPosition.z > 2.0:
    owner["underwater"] = False

if not owner["underwater"] and owner.worldPosition.z < 0.9:
#if not owner["underwater"]:

    sound = cont.actuators["dive-in"]
    print(sound.mode)
    
    sound.startSound()
    owner["underwater"] = True
#sound.setGain(dist)
