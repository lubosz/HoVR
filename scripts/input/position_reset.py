from bge import logic as G
from bge import render as R
from bge import events
from mathutils import *

cont = G.getCurrentController()
owner = cont.owner

owner.worldPosition = owner['initPos']

owner.setLinearVelocity([0, 0, 0], 1)
owner['my'] = 0
owner['mx'] = 0
owner.worldOrientation = owner['initRot']

#print ("reset world pos", owner['initPos'])
#print ("world rot", owner['initRot'])
