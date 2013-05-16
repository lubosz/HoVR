from bge import logic as g
from bge import render as r
import bgl

cont = g.getCurrentController()
own = cont.owner
scene = g.getCurrentScene()
sun = scene.objects['Lamp']

own['fade'] = (((sun.position[2]+70)/90.0))

VertexShader = """

varying vec4 fragPos;
varying float timer;


void main() 
{
	vec3 pos = vec3(gl_Vertex);

    fragPos = ftransform();
    gl_Position = ftransform();
    gl_TexCoord[0] = gl_MultiTexCoord0;
}

"""

FragmentShader = """

varying vec4 fragPos; //fragment coordinates
uniform vec3 sunPos;
uniform sampler2D texSampler;

float sunfade = clamp(((pow((sunPos.z+70.0)/100.0,2.0))),0.0,1.0);
float sunfade1 = clamp((((sunPos.z-1000.0)/250.0)),0.0,1.0);
    
float threshold = 0.55 + 0.36*sunfade + (0.045*sunfade1); //highlight threshold;
float gain = 8.0; //highlight gain;

vec3 treshold(in sampler2D tex, in vec2 coords)
{
	vec3 col = texture2D(tex,coords).rgb;

	vec3 lumcoeff = vec3(0.299,0.587,0.114);
	float lum = dot(col.rgb, lumcoeff);
	float thresh = max((lum-threshold)*gain, 0.0);
	return mix(vec3(0.0),col,thresh);
}

vec2 texel = vec2(1.0/512.0,1.0/512.0);
float glowsize = 0.3;

vec3 blur(in sampler2D tex, in vec2 coords)
{
	vec3 col = vec3(0.0);
	float kernel[25];
	vec2 offset[25];
	
	vec2 wh = vec2(texel.x, texel.y) * glowsize;
	
	offset[0] = vec2(-2.0,-2.0)*wh;
	offset[1] = vec2(-1.0,-2.0)*wh;
	offset[2] = vec2( 0.0,-2.0)*wh;
	offset[3] = vec2( 1.0,-2.0)*wh;
	offset[4] = vec2( 2.0,-2.0)*wh;

	offset[5] = vec2(-2.0,-1.0)*wh;
	offset[6] = vec2(-1.0,-1.0)*wh;
	offset[7] = vec2( 0.0,-1.0)*wh;
	offset[8] = vec2( 1.0,-1.0)*wh;
	offset[9] = vec2( 2.0,-1.0)*wh;

	offset[10] = vec2(-2.0, 0.0)*wh;
	offset[11] = vec2(-1.0, 0.0)*wh;
	offset[12] = vec2( 0.0, 0.0)*wh;
	offset[13] = vec2( 1.0, 0.0)*wh;
	offset[14] = vec2( 2.0, 0.0)*wh;

	offset[15] = vec2(-2.0, 1.0)*wh;
	offset[16] = vec2(-1.0, 1.0)*wh;
	offset[17] = vec2( 0.0, 1.0)*wh;
	offset[18] = vec2( 1.0, 1.0)*wh;
	offset[19] = vec2( 2.0, 1.0)*wh;

	offset[20] = vec2(-2.0, 2.0)*wh;
	offset[21] = vec2(-1.0, 2.0)*wh;
	offset[22] = vec2( 0.0, 2.0)*wh;
	offset[23] = vec2( 1.0, 2.0)*wh;
	offset[24] = vec2( 2.0, 2.0)*wh;

	kernel[0] = 1.0/256.0;   kernel[1] = 4.0/256.0;   kernel[2] = 6.0/256.0;   kernel[3] = 4.0/256.0;   kernel[4] = 1.0/256.0;
	kernel[5] = 4.0/256.0;   kernel[6] = 16.0/256.0;  kernel[7] = 24.0/256.0;  kernel[8] = 16.0/256.0;  kernel[9] = 4.0/256.0;
	kernel[10] = 6.0/256.0;  kernel[11] = 24.0/256.0; kernel[12] = 36.0/256.0; kernel[13] = 24.0/256.0; kernel[14] = 6.0/256.0;
	kernel[15] = 4.0/256.0;  kernel[16] = 16.0/256.0; kernel[17] = 24.0/256.0; kernel[18] = 16.0/256.0; kernel[19] = 4.0/256.0;
	kernel[20] = 1.0/256.0;  kernel[21] = 4.0/256.0;  kernel[22] = 6.0/256.0;  kernel[23] = 4.0/256.0;  kernel[24] = 1.0/256.0;

	for( int i=0; i<25; i++ )
	{
		vec3 tmp = treshold(tex, coords + offset[i]).rgb;
		col += tmp * kernel[i];
	}
	
	return col;
}

void main() 
{
    vec2 TEXCOORD = gl_TexCoord[0].st;

    vec3 col = treshold(texSampler,TEXCOORD).rgb;
    
	gl_FragColor.rgb = col;
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
		shader.setUniform3f('sunPos', sun.position[0],sun.position[1],sun.position[2])
