from bge import logic as g
from bpy import data as D

cont = g.getCurrentController()
own = cont.owner

VertexShader = D.texts["ground_water.vert"].as_string()
FragmentShader = D.texts["ground_water.frag"].as_string()

mesh = own.meshes[0]
if 'shader' not in own:
	for mat in mesh.materials:
		own['shader'] = mat.getShader()
		if own['shader'] != None:		
			if not own['shader'].isValid():
				own['shader'].setSource(VertexShader, FragmentShader, 1)
own['shader'].setAttrib(g.SHD_TANGENT)
own['shader'].setSampler('NormalSampler',0)
own['shader'].setSampler('TextureSampler',1)
own['shader'].setUniformDef('ModelMatrix', g.MODELMATRIX)

#pprint(type(own))
#own['shader'].setSampler('foamSampler',2)
#own['shader'].setUniformDef('cameraPos', g.CAM_POS)
#own['shader'].setUniform1f('timer',own['timer']*3)

#print(dir(own.color), own.color)
#print(dir(own))
