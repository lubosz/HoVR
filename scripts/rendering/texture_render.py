from bge import logic as g
from bge import texture
from mathutils import *
from math import *
import bgl

cont = g.getCurrentController()
own = cont.owner
scene = g.getCurrentScene()
objlist = scene.objects

texsize = 64 #refraction tex dimensions

activecam = scene.active_camera
rendercam = objlist['rendercam1']
flare = objlist['flare1']

#setting lens nad projection to watercamera
#rendercam.lens = activecam.lens
#rendercam.projection_matrix = activecam.projection_matrix

#disable visibility for the water surface during texture rendering
own.visible = False
flare.visible = False

###REFRACTION####################

#initializing camera for refraction pass
#rendercam.position = activecam.position
#rendercam.orientation = activecam.orientation


#rendering the refraction texture in tex channel 1
if not hasattr(g, 'tex'):
	g.tex = texture.Texture(own, 0, 0)
	g.tex.source = texture.ImageRender(scene,rendercam)
	g.tex.source.capsize = [texsize,texsize]
	g.tex.source.background = [100,100,100,0]

g.tex.refresh(True)

g.blurtex.refresh(True)

own.visible = True
flare.visible = True
