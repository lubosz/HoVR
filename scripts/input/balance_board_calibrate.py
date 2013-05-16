from balanceboard import PyBalanceBoard
import bpy
from bpy import data as D
from bpy import context as C
from mathutils import *
from math import *

cont = bge.logic.getCurrentController()
own = cont.owner

def poll(bb, own):
    if bb.isConnected:
        
        count = 0
        while (count < 10):
           bb.poll()
           count = count + 1
           
        left = (bb.topLeft + bb.bottomLeft) / 2
        right = (bb.topRight + bb.bottomRight) / 2
        top = (bb.topRight + bb.topLeft) / 2
        bottom = (bb.bottomRight + bb.bottomLeft) / 2
        
        #calibrate
        calibrateScale = 1.2
        own['initialLeft'] = left * calibrateScale
        own['initialRight'] = right * calibrateScale
        own['initialTop'] = top * calibrateScale
        own['initialBottom'] = bottom * calibrateScale
        
        print("calibrating", own['initialLeft'], own['initialRight'], own['initialTop'], own['initialBottom'])

if 'startConnect' in own:    
    poll(bge.logic.bb, own)
else:
    own['startConnect'] = True
    print ("Connecting to Balance Board")
    bge.logic.bb = PyBalanceBoard()
    bge.logic.bb.connect()
