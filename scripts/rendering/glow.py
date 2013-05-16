##############################################################
# Water surface GLSL shader for BGE v1.0
# by Martins Upitis (martinsh) (devlog-martinsh.blogspot.com)
##############################################################

from bge import logic as g
from bge import render as r
import bgl

cont = g.getCurrentController()
own = cont.owner

VertexShader = """

varying vec4 fragPos;
varying float timer;


void main() 
{
	vec3 pos = vec3(gl_Vertex);

    fragPos = ftransform();
    gl_Position = ftransform();
}

"""

FragmentShader = """

varying vec4 fragPos; //fragment coordinates

uniform sampler2D texSampler;

float threshold = 0.0; //highlight threshold;
float gain = 1.0; //highlight gain;

vec3 treshold(in sampler2D tex, in vec2 coords)
{
	vec3 col = texture2D(tex,coords).rgb;

	vec3 lumcoeff = vec3(0.299,0.587,0.114);
	float lum = dot(col.rgb, lumcoeff);
	float thresh = max((lum-threshold)*gain, 0.0);
	return mix(vec3(0.0),col,thresh);
}



void main() 
{
    vec2 TEXCOORD = (fragPos.xy/fragPos.w)*0.5+0.5;
 
    float sparklesize = 128.0;
    int samples = 8;
    float sparklefade = 1.1;
    
    vec3 anamorph = vec3(0.0);
    float s;

	for (int i = -samples; i < samples; ++i) 
	{
        s = clamp(pow(1.0/abs(float(i)),sparklefade),0.0,1.0);
		anamorph += treshold(texSampler, clamp(vec2(TEXCOORD.x + float(i)*(1.0/sparklesize),TEXCOORD.y - float(i)*(1.0/sparklesize)),0.02,0.98)).rgb*s;
	}

	for (int i = -samples; i < samples; ++i) 
	{
        s = clamp(pow(1.0/abs(float(i)),sparklefade),0.0,1.0);
		anamorph += treshold(texSampler, clamp(vec2(TEXCOORD.x - float(i)*(1.0/sparklesize),TEXCOORD.y - float(i)*(1.0/sparklesize)),0.02,0.98)).rgb*s;
	}

	for (int i = -samples; i < samples; ++i) 
	{
        s = clamp(pow(1.0/abs(float(i)),sparklefade),0.0,1.0);
		anamorph += treshold(texSampler, clamp(vec2(TEXCOORD.x,TEXCOORD.y+ float(i)*(1.0/sparklesize)),0.02,0.98)).rgb*s;
	}
/*
	for (int i = -samples; i < samples; ++i) 
	{
        s = clamp(pow(1.0/abs(float(i)),sparklefade),0.0,1.0);
		anamorph += treshold(texSampler, vec2(TEXCOORD.x + float(i)*(1.0/sparklesize),TEXCOORD.y)).rgb*s;
	}
*/
	gl_FragColor.rgb = anamorph;
    //gl_FragColor.rgb = texture2D(texSampler,TEXCOORD).rgb;
	gl_FragColor.a = 1.0;
}

"""

mesh = own.meshes[0]
for mat in mesh.materials:
	shader = mat.getShader()
	if shader != None:
		if not shader.isValid():
			shader.setSource(VertexShader, FragmentShader, 1)
		shader.setSampler('texSampler',0)
