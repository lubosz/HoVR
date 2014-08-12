from balanceboard import PyBalanceBoard
import bpy
from bpy import data as D
from bpy import context as C
from mathutils import *
from math import *

def poll(bb, own):
    if bb.isConnected:
        
        count = 0
        while (count < 10):
           bb.poll()
           count = count + 1
        
        ##print(bb.topLeft)
        #print(bb.topRight)
        
        #try:
            #left = (bb.topLeft + bb.bottomLeft) / bb.getTotal()
            #right = (bb.topRight + bb.bottomRight) / bb.getTotal()
            #top = (bb.topRight + bb.topLeft) / bb.getTotal()
            #bottom = (bb.bottomRight + bb.bottomLeft) / bb.getTotal()

        #except ZeroDivisionError:
        #    left = 0
        #    right = 0
        #    top = 0
        #    bottom = 0
        
        left = (bb.topLeft + bb.bottomLeft) / 2
        right = (bb.topRight + bb.bottomRight) / 2
        top = (bb.topRight + bb.topLeft) / 2
        bottom = (bb.bottomRight + bb.bottomLeft) / 2
        
        if 'initialLeft' in own:
            left -= own['initialLeft']
            right -= own['initialRight']
            top -= own['initialTop']
            bottom -= own['initialBottom']
        
        #print ("L/R", left, right)
        #print ("TL/BL/T", bb.topLeft, bb.bottomLeft, bb.getTotal())
        
        #bb.printSensors()
        
        #calibrate
        if not 'initialLeft' in own and left != 0:
            calibrateScale = 1.2
            own['initialLeft'] = left * calibrateScale
            own['initialRight'] = right * calibrateScale
            own['initialTop'] = top * calibrateScale
            own['initialBottom'] = bottom * calibrateScale
        
        
        
        if not 'moveinit' in own:
            own['moveinit'] = 1
            own['mx'] = 0.0
            own['my'] = 0.0
            own['accel'] = 0.05     # Acceleration
            own['maxspd'] = 35.0    # Top speed
            own['friction'] = 0.75   # Friction percentage; set to 0.0 for immediate stop
            own['movelocal'] = 1    # Move on local axis?
            own['treshold'] = 0.5
            
            own['rotAccel'] = 0.0015
            own['initRot'] = Matrix(own.worldOrientation)
            own['initPos'] = Vector(own.worldPosition)
        

        
        LR = right-left
        if abs(LR) > own['treshold']:
            acceleration = (LR * own['accel'])
            own['my'] += acceleration
        
        if own['my'] > 0:
        #if right > left:
        #if True:    
            TB = top - bottom
        else:
            TB = bottom - top
        
        if abs(TB) > own['treshold'] * 0.8:
            rotation = TB * own['rotAccel']
            own.applyRotation([0,0,rotation], True)
        
        #print("L %f R %f T %f B %f" % (left, right, top, bottom))
            
        # Clamping
        if own['my'] > own['maxspd']:
            own['my'] = own['maxspd']
        elif own['my'] < -own['maxspd']:
            own['my'] = -own['maxspd']
        
        # Actual movement
          
        own.setLinearVelocity([
            own['my'], 
            own['mx'], 
            own.getLinearVelocity()[2]], 
            own['movelocal'])
        
        
        TB2 = bottom - top
            
        scene = bge.logic.getCurrentScene()
        #scene.objects["Boardvis"].applyRotation([0.1,0,0], True)
        boardRot = scene.objects["Boardvis"].localOrientation.to_euler()
        
        scene.objects["Boardvis"].localOrientation = Euler([TB2*0.02,LR*0.01,boardRot.z], 'XYZ')
        
        #LR*0.03
        #scene.objects["Boardvis"].localOrientation = Euler([boardRot.x,LR*0.01,boardRot.z], 'XYZ')

cont = bge.logic.getCurrentController()
own = cont.owner

if 'startConnect' in own:    
    poll(bge.logic.bb, own)
else:
    own['startConnect'] = True
    print ("Connecting to Balance Board")
    bge.logic.bb = PyBalanceBoard()
    bge.logic.bb.connect()
