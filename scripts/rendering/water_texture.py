from bge import logic as g
from bge import texture
from mathutils import *
from math import *
import bgl
#import bpy
rf = g.getRandomFloat

cont = g.getCurrentController()
own = cont.owner
scene = g.getCurrentScene()
objlist = scene.objects

reflsize = 512 #reflection tex dimensions
refrsize = 512 #refraction tex dimensions
offset = 0.2 #geometry clipping offset

#texture background color
bgR = 0.1
bgG = 0.2
bgB = 0.8
bgA = 0.0

activecam = scene.active_camera
viewer = activecam
cam = objlist['Camera']

#if 'initcam' not in own:
#	cam = bpy.data.cameras.new('rendercamera')
#	cam_ob = bpy.data.objects.new('watercamera', cam)
#	bpy.context.scene.objects.link(cam_ob)
#	own['initcam'] = 1

watercamera = objlist['watercamera'] #camera used for rendering the water
lens = objlist['lens']

#setting lens and projection to watercamera
watercamera.lens = activecam.lens
watercamera.projection_matrix = activecam.projection_matrix

#rotation and mirror matrices
m1=Matrix(own.orientation)
m2=Matrix(own.orientation)
m2.invert()

r180 = Matrix.Rotation(radians(180),3,'Y')
unmir = Matrix.Scale(-1,3,Vector([1,0,0]))

#disable visibility for the water surface during texture rendering
own.visible = False
lens.visible = False

###REFLECTION####################

#initializing camera for reflection pass
pos = (viewer.position - own.position)*m1
pos = own.position + pos*r180*unmir*m2

ori = Matrix(viewer.orientation)
ori.transpose()
ori = ori*m1*r180*unmir*m2
ori.transpose()

#delay reduction using delta offset
if 'oldori' not in own:
	own['oldori'] = ori
	own['oldpos'] = pos
	own['deltaori'] = own['oldori']-ori
	own['deltapos'] = own['oldpos']-pos
    
own['deltaori'] = own['oldori']-ori
own['deltapos'] = own['oldpos']-pos

#orienting and positioning the reflection rendercamera
watercamera.orientation = ori - own['deltaori']
watercamera.position = pos - own['deltapos']

#storing the old orientation and position of the camera
own['oldori'] = ori
own['oldpos'] = pos

#culling front faces as the camera is scaled to -1
bgl.glCullFace(bgl.GL_FRONT)

#plane equation
normal = own.getAxisVect((0.0, 0.0, 1.0)) #plane normals Z=front

D = -own.position.project(normal).magnitude #closest distance from center to plane
V = (activecam.position-own.position).normalized().dot(normal) #VdotN to get frontface/backface

#invert normals when backface
if V<0:
	normal = -normal
	cam['resettimer'] = 0
	cam['randomtime'] = (rf()*5)*2.0-1.0

     
#making a clipping plane buffer
plane = bgl.Buffer(bgl.GL_DOUBLE, [4], [-normal[0], -normal[1], -normal[2], -D+offset])
bgl.glClipPlane(bgl.GL_CLIP_PLANE0,plane)
bgl.glEnable(bgl.GL_CLIP_PLANE0)

#rendering the reflection texture in tex channel 0
if not hasattr(g, 'reflection'):
	g.reflection = texture.Texture(own, 0, 0)
	g.reflection.source = texture.ImageRender(scene,watercamera)
	g.reflection.source.capsize = [reflsize,reflsize]
	g.reflection.source.background = [int(bgR*255),int(bgG*255),int(bgB*255),int(bgA*255)]

g.reflection.refresh(True)

#restoring face culling to normal and disabling the geometry clipping
bgl.glCullFace(bgl.GL_BACK)
bgl.glDisable(bgl.GL_CLIP_PLANE0)

###REFRACTION####################

#initializing camera for refraction pass
pos = viewer.position
ori = Matrix(viewer.orientation)

#delay reduction using delta offset
if 'oldori1' not in own:
	own['oldori1'] = own.orientation
	own['oldpos1'] = own.position
	own['deltaori1'] = own['oldori1']-viewer.orientation
	own['deltapos1'] = own['oldpos1']-viewer.position

    
own['deltaori1'] = own['oldori1']-ori
own['deltapos1'] = own['oldpos1']-pos

#orienting and positioning the refraction rendercamera
watercamera.orientation = ori - own['deltaori1']
watercamera.position = pos - own['deltapos1']

#storing the old orientation and position of the camera
own['oldori1'] = ori
own['oldpos1'] = pos

#making another clipping plane buffer
plane = bgl.Buffer(bgl.GL_DOUBLE, [4], [normal[0], normal[1], normal[2], -D+offset])
bgl.glClipPlane(bgl.GL_CLIP_PLANE1,plane)
bgl.glEnable(bgl.GL_CLIP_PLANE1)

#rendering the refraction texture in tex channel 1
if not hasattr(g, 'refraction'):
	g.refraction = texture.Texture(own, 0, 1)
	g.refraction.source = texture.ImageRender(scene,watercamera)
	g.refraction.source.capsize = [refrsize,refrsize]
	g.refraction.source.background = [int(bgR*255),int(bgG*255),int(bgB*255),int(bgA*255)]

g.refraction.refresh(True)

#disabling the geometry clipping
bgl.glDisable(bgl.GL_CLIP_PLANE1) 
#restoreing visibility for the water surface
own.visible = True
lens.visible = True

#objlist["water"].color = [own["timer"],1.0,1.0,1.0]
#objlist["ground"].color = [own["timer"],1.0,1.0,1.0]
