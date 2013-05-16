from bge import logic as g
from bge import render as r
from mathutils import *
from math import *
import bgl

cont = g.getCurrentController()
own = cont.owner
scene = g.getCurrentScene()
sun = scene.objects['Lamp']
camera = scene.objects['Camera']


sunpoint = sun.position

obj, point, normal = camera.rayCast(sunpoint,None,99999,"sky")
hit = 0

if obj:
    hit = 1
else:
    hit = 0

own["hit"] = hit*0.4+own["hit"]*0.6
hit = own["hit"]

VertexShader = """

varying vec3 normal, viewPos, sunPos, wPos;
uniform vec3 sunVec, cameraPos, exaustVec;
uniform mat4 ModelMatrix;

mat3 m3( mat4 m )
{
	mat3 result;
	
	result[0][0] = m[0][0]; 
	result[0][1] = m[0][1]; 
	result[0][2] = m[0][2]; 

	result[1][0] = m[1][0]; 
	result[1][1] = m[1][1]; 
	result[1][2] = m[1][2]; 
	
	result[2][0] = m[2][0]; 
	result[2][1] = m[2][1]; 
	result[2][2] = m[2][2]; 
	
	return result;
}

void main()
{	
    wPos = vec3(ModelMatrix * gl_Vertex);
	normal = m3(ModelMatrix)*gl_Normal;
    viewPos = wPos - cameraPos.xyz;
    sunPos = wPos - sunVec;
    gl_Position = ftransform();
}

"""

FragmentShader = """

varying vec3 normal, viewPos, sunPos, wPos, sunVec;
uniform vec3 posStep, cameraPos;
uniform float hit;
void main (void)
{					
	vec3 N = normalize(normal);
	vec3 L = normalize(sunPos);

    vec3 E = normalize(viewPos);
	vec3 R = reflect(L, E);

    float sunFade = clamp((-sunPos.z+50.0)/300.0,0.0,1.0);
    vec3 sunext = vec3(0.45, 0.55, 0.68);//sunlight extinction
    
    //mix(vec3(1.0,0.5,0.2), vec3(1.0,1.0,1.0), clamp(1.0-exp(-(sunPos.z/500.0)*sunext),0.0,1.0));
 
	float sunflare = pow( max(dot(R, E), 0.0), 4.0 )*0.5;
    sunflare += pow( max(dot(R, E), 0.0), 100.0 )*0.1;
    sunflare = atan(sunflare,2.0);
    float depth = (cameraPos.z<0.0)?0.0:1.0;

    vec3 color = mix(vec3(1.0,0.5,0.2), vec3(1.0,1.0,1.0), clamp(((-sunPos.z+50.0)/300.0)*sunext,0.0,1.0));

	gl_FragColor = vec4(sunflare*color*sunFade*hit*depth,1.0);			
}
"""

mesh = own.meshes[0]
for mat in mesh.materials:
	shader = mat.getShader()
	if shader != None:
		if not shader.isValid():
			shader.setSource(VertexShader, FragmentShader, 1)
		shader.setUniformDef('ModelMatrix', g.MODELMATRIX)
		shader.setUniformDef('cameraPos', g.CAM_POS)
		shader.setUniform3f('sunVec', sun.position[0],sun.position[1],sun.position[2])
		shader.setUniform1f('hit', hit)
