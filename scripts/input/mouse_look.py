#Blender Game Engine 2.55 Simple Camera Look
#Created by Mike Pan: mikepan.com

# Use mouse to look around
# W,A,S,D key to walk around
# E and C key to ascend and decend

from bge import logic as G
from bge import render as R
from bge import events
from mathutils import *

scene = G.getCurrentScene()

yaw = scene.objects["Board"]

speed = 0.08				# walk speed
sensitivity = 0.002		# mouse sensitivity
smooth = 0.9	#		# mouse smoothing (0.0 - 0.99)

cont = G.getCurrentController()

#owner = scene.cameras["Camera"]
#cam.worldOrientation = rot

owner = cont.owner
Mouse = cont.sensors["Mouse"]

w = R.getWindowWidth()//2
h = R.getWindowHeight()//2
screen_center = (w, h)

# center mouse on first frame, create temp variables
if "oldX" not in owner:

	R.setMousePosition(w + 1, h + 1)
	
	owner["oldX"] = 0.0
	owner["oldY"] = 0.0

else:
	
	scrc = Vector(screen_center)
	mpos = Vector(Mouse.position)
	
	x = scrc.x-mpos.x
	y = scrc.y-mpos.y

	
	# Smooth movement
	owner['oldX'] = (owner['oldX']*smooth + x*(1.0-smooth))
	owner['oldY'] = (owner['oldY']*smooth + y*(1.0-smooth))
	
	x = owner['oldX']* sensitivity
	y = owner['oldY']* sensitivity
	 
	# set the values
	yaw.applyRotation([0, 0, x], False)
	owner.applyRotation([0, -y, 0], True)
	
	# Center mouse in game window
	R.setMousePosition(*screen_center)
	

