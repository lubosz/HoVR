from bge import logic as g
from bge import texture
from mathutils import *
from math import *
import bgl

cont = g.getCurrentController()
own = cont.owner
scene = g.getCurrentScene()
objlist = scene.objects

texsize = 128 #refraction tex dimensions

activecam = scene.active_camera
rendercam = objlist['rendercam']
blur = objlist['blur']

#setting lens nad projection to watercamera
rendercam.lens = activecam.lens
rendercam.projection_matrix = activecam.projection_matrix

#disable visibility for the water surface during texture rendering
own.visible = False

###REFRACTION####################

#initializing camera for refraction pass
pos = activecam.position
ori = Matrix(activecam.orientation)

#delay reduction using delta offset
if 'oldori1' not in own:
	own['oldori1'] = activecam.orientation
	own['oldpos1'] = activecam.position
	own['deltaori1'] = own['oldori1']-activecam.orientation
	own['deltapos1'] = own['oldpos1']-activecam.position

    
own['deltaori1'] = own['oldori1']-ori
own['deltapos1'] = own['oldpos1']-pos

#orienting and positioning the refraction rendercamera
rendercam.orientation = ori - own['deltaori1']*1
rendercam.position = pos - own['deltapos1']*1

#storing the old orientation and position of the camera
own['oldori1'] = ori
own['oldpos1'] = pos

#rendering the refraction texture in tex channel 1
if not hasattr(g, 'blurtex'):
	g.blurtex = texture.Texture(own, 0, 0)
	g.blurtex.source = texture.ImageRender(scene,rendercam)
	g.blurtex.source.capsize = [texsize,texsize]
	g.blurtex.source.background = [100,100,100,0]

#own.visible = False
g.blurtex.refresh(True)
own.visible = True

