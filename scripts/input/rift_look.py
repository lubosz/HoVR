import bpy
from bpy import data as D
from bpy import context as C
from mathutils import *
from math import *
from rift import PyRift
from mathutils import Quaternion
from bge import logic as G

def rotateCam(rift):
    
    cont = G.getCurrentController()
    owner = cont.owner
    
    scene = G.getCurrentScene()
 
    rift.poll()
        
    rotation = Quaternion((rift.rotation[0], 
        rift.rotation[1], 
        rift.rotation[2], 
        rift.rotation[3]))

    eu = rotation.to_euler()
    
    #ativecam
    fix = Euler((-1.57, 0, 3*1.57), 'XYZ')
    rot = Euler((-eu.z, eu.y, -eu.x), 'XYZ')
    
    #owner
    #fix = Euler((0, 2*-1.57, -1.57), 'XYZ')
    #rot = Euler((-eu.x, eu.z, eu.y), 'XYZ')
    
    rot.rotate(fix)
     
    #cam = scene.active_camera
    cam = scene.cameras["Camera"]
    cam.localOrientation = rot
    
    #camrot = Euler((cam.worldOrientation.x, rot.y, cam.worldOrientation.z), 'XYZ')
    
    #cam.worldOrientation = camrot
    
    #owner.worldOrientation = camrot
    

    #yawrot = rot
    
    #yaw = scene.objects["Empty"]
    #yaw.worldOrientation = yawrot
    
    #owner.applyRotation([0, 0, x], False)
	#yaw.applyRotation([y, 0, 0], True)
    


try:  
    rotateCam(bge.logic.rift)
except AttributeError:
    bge.logic.rift = PyRift()




