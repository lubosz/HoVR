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

attribute vec4 Tangent;
varying vec4 fragPos;
varying vec3 T, B, N; //tangent binormal normal
varying vec3 viewPos, worldPos;
varying float timer;
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
    gl_TexCoord[0] = gl_MultiTexCoord0;
	vec3 pos = vec3(gl_Vertex);
	
	T   = m3(ModelMatrix)*Tangent.xyz;
	B   = m3(ModelMatrix)*cross(gl_Normal, Tangent.xyz);
	N   = m3(ModelMatrix)*gl_Normal; 

    worldPos = vec3(ModelMatrix*gl_Vertex);
    fragPos = ftransform();
    viewPos = pos - m3(ModelMatrix)*gl_ModelViewMatrixInverse[3].xyz;
    gl_Position = ftransform();
    //timer = gl_Color.r*2.0;
}

"""

FragmentShader = """

varying vec4 fragPos; //fragment coordinates
varying vec3 T, B, N; //tangent binormal normal
varying vec3 viewPos;
varying vec3 worldPos;
uniform float timer;
uniform sampler2D reflectionSampler,refractionSampler, depthSampler, normalSampler;
uniform vec3 cameraPos;

//----------------
//tweakables

vec2 windDir = vec2(0.5, -0.8); //wind direction XY
float windSpeed = 0.2; //wind speed

float visibility = 28.0;

float scale = 1.0; //overall wave scale

vec2 bigWaves = vec2(0.3, 0.3); //strength of big waves
vec2 midWaves = vec2(0.3, 0.15); //strength of middle sized waves
vec2 smallWaves = vec2(0.15, 0.1); //strength of small waves

vec3 waterColor = vec3(0.2,0.4,0.5); //color of the water
float waterDensity = 0.0; //water density (0.0-1.0)
    
float choppy = 0.15; //wave choppyness
float aberration = 0.002; //chromatic aberration amount
float bump = 2.6; //overall water surface bumpyness
float reflBump = 0.04; //reflection distortion amount
float refrBump = 0.03; //refraction distortion amount

vec3 sunPos = vec3(gl_ModelViewMatrixInverse*gl_LightSource[0].position);
float sunSpec = 1000.0; //Sun specular hardness

float scatterAmount = 3.5; //amount of sunlight scattering of waves
vec3 scatterColor = vec3(0.0,1.0,0.95);// color of the sunlight scattering
//----------------

vec3 tangentSpace(vec3 v)
{
	vec3 vec;
	vec.xy=v.xy;
	vec.z=sqrt(1.0-dot(vec.xy,vec.xy));
	vec.xyz= normalize(vec.x*T+vec.y*B+vec.z*N);
	return vec;
}

float fresnel_dielectric(vec3 Incoming, vec3 Normal, float eta)
{
    /* compute fresnel reflectance without explicitly computing
       the refracted direction */
    float c = abs(dot(Incoming, Normal));
    float g = eta * eta - 1.0 + c * c;
    float result;

    if(g > 0.0) {
        g = sqrt(g);
        float A =(g - c)/(g + c);
        float B =(c *(g + c)- 1.0)/(c *(g - c)+ 1.0);
        result = 0.5 * A * A *(1.0 + B * B);
    }
    else
        result = 1.0;  /* TIR (no refracted component) */

    return result;
}


void main() {
    vec2 fragCoord = (fragPos.xy/fragPos.w)*0.5+0.5;
    fragCoord = clamp(fragCoord,0.002,0.998);

	//normal map
	vec2 nCoord = vec2(0.0); //normal coords
    vec2 coo = ((gl_TexCoord[0].st)/1106.208)-0.5;
    float depth = texture2D(depthSampler,coo).r;
    float coast = smoothstep(0.3,0.7,depth);
    float coast1 = smoothstep(0.49,0.5,depth);
     
    choppy = choppy * (coast)+0.05;
    bump = -bump*clamp(1.0-coast+0.0,0.0,1.0);
    bump = bump*clamp(1.0-coast1+0.0,0.0,1.0);
    
    //scale = scale - (coast*0.1);
    //scale = scale * (coast*0.1+0.9);
    float time = timer - (coast)*80.0; //hmmm
    //timer = timer * (coast*0.5+0.5)*1.5;
    //smallWaves.x = smallWaves.x + (0.1*coast);
    //smallWaves.y = smallWaves.y + (0.1*coast);
    //bigWaves.x = bigWaves.x - (0.1*(1.0-coast));
    //bigWaves.y = bigWaves.y + (0.1*(1.0-coast));
    
    vec3 mudext = vec3(1.0, 0.7, 0.5);//mud extinction
    float atmosphere = length(cameraPos-worldPos)/200.0;
    
    vec3 atmopherefog = clamp(1.0-exp(-atmosphere/mudext),0.0,1.0);
    
  	nCoord = worldPos.xy * (scale * 0.04) + windDir * time * (windSpeed*0.04);
	vec3 normal0 = 2.0 * texture2D(normalSampler, nCoord + vec2(-time*0.015,-time*0.005)).rgb - 1.0;
	nCoord = worldPos.xy * (scale * 0.1) + windDir * time * (windSpeed*0.08)-(normal0.xy/normal0.zz)*choppy;
	vec3 normal1 = 2.0 * texture2D(normalSampler, nCoord + vec2(+time*0.020,+time*0.015)).rgb - 1.0;
 
 	nCoord = worldPos.xy * (scale * 0.25) + windDir * time * (windSpeed*0.07)-(normal1.xy/normal1.zz)*choppy;
	vec3 normal2 = 2.0 * texture2D(normalSampler, nCoord + vec2(-time*0.04,-time*0.03)).rgb - 1.0;
	nCoord = worldPos.xy * (scale * 0.5) + windDir * time * (windSpeed*0.09)-(normal2.xy/normal2.z)*choppy;
	vec3 normal3 = 2.0 * texture2D(normalSampler, nCoord + vec2(+time*0.03,+time*0.04)).rgb - 1.0;
  
  	nCoord = worldPos.xy * (scale* 1.0) + windDir * time * (windSpeed*0.4)-(normal3.xy/normal3.zz)*choppy;
	vec3 normal4 = 2.0 * texture2D(normalSampler, nCoord + vec2(-time*0.02,+time*0.1)).rgb - 1.0;  
    nCoord = worldPos.xy * (scale * 2.0) + windDir * time * (windSpeed*0.7)-(normal4.xy/normal4.zz)*choppy;
    vec3 normal5 = 2.0 * texture2D(normalSampler, nCoord + vec2(+time*0.1,-time*0.06)).rgb - 1.0;

	
	
	vec3 normal = normalize(normal0 * bigWaves.x + normal1 * bigWaves.y +
                            normal2 * midWaves.x + normal3 * midWaves.y +
						    normal4 * smallWaves.x + normal5 * smallWaves.y);

    //normal.x = -normal.x; //in case you need to invert Red channel
    //normal.y = -normal.y; //in case you need to invert Green channel
   
    vec3 nVec = tangentSpace(normal*bump); //converting normals to tangent space    
    vec3 vVec = normalize(viewPos);
    vec3 lVec = normalize(sunPos);
    
    //normal for light scattering
	vec3 lNormal = normalize(normal0 * bigWaves.x*0.5 + normal1 * bigWaves.y*0.5 +
                            normal2 * midWaves.x*0.1 + normal3 * midWaves.y*0.1 +
						    normal4 * smallWaves.x*0.1 + normal5 * smallWaves.y*0.1);
    lNormal = tangentSpace(lNormal*bump);
    vec3 pNormal = tangentSpace(vec3(0.0));
    
	vec3 lR = reflect(lVec, lNormal);
    vec3 llR = reflect(lVec, pNormal);
    
    float sunFade = clamp((sunPos.z+10.0)/20.0,0.0,1.0);
    float scatterFade = clamp((sunPos.z+50.0)/200.0,0.0,1.0);
    vec3 sunext = vec3(0.45, 0.55, 0.68);//sunlight extinction
    
	float s = clamp((dot(lR, vVec)*2.0-1.2), 0.0,1.0);
    float lightScatter = clamp((clamp(dot(-lVec,lNormal)*0.7+0.3,0.0,1.0)*s)*scatterAmount,0.0,1.0)*sunFade *clamp(1.0-exp(-(sunPos.z/500.0)),0.0,1.0);
    scatterColor = mix(vec3(scatterColor)*vec3(1.0,0.4,0.0), scatterColor, clamp(1.0-exp(-(sunPos.z/500.0)*sunext),0.0,1.0));

    //fresnel term
    float ior = 1.33;
    ior = (cameraPos.z>0.0)?(1.333/1.0):(1.0/1.333); //air to water; water to air
    float eta = max(ior, 0.00001);
    float fresnel = fresnel_dielectric(-vVec,nVec,eta);
    
    //texture edge bleed removal
    float fade = 12.0;
    vec2 distortFade = vec2(0.0);
    distortFade.s = clamp(fragCoord.s*fade,0.0,1.0);
    distortFade.s -= clamp(1.0-(1.0-fragCoord.s)*fade,0.0,1.0);
    distortFade.t = clamp(fragCoord.t*fade,0.0,1.0);
    distortFade.t -= clamp(1.0-(1.0-fragCoord.t)*fade,0.0,1.0); 
    
    vec3 reflection = texture2D(reflectionSampler, fragCoord+(nVec.st*vec2(reflBump,reflBump*(6.0))*distortFade)).rgb;
    
    vec3 luminosity = vec3(0.30, 0.59, 0.11);
	float reflectivity = pow(dot(luminosity, reflection.rgb*2.0),3.0);

	float reflectivity1 = pow(dot(luminosity, reflection.rgb),3.0);
        
    vec3 R = reflect(vVec, nVec);

    float specular = clamp(pow(atan(max(dot(R, lVec),0.0)*1.55),1000.0)*reflectivity*8.0,0.0,1.0);
    
    vec3 specColor = mix(vec3(1.0,0.5,0.2), vec3(1.0,1.0,1.0), clamp(1.0-exp(-(sunPos.z/500.0)*sunext),0.0,1.0));

    vec2 rcoord = reflect(vVec,nVec).st;
    vec3 refraction = vec3(0.0);
    
    refraction.r = texture2D(refractionSampler, (fragCoord-(nVec.st*refrBump*distortFade))*1.0).r;
    refraction.g = texture2D(refractionSampler, (fragCoord-(nVec.st*refrBump*distortFade))*1.0-(rcoord*aberration)).g;
    refraction.b = texture2D(refractionSampler, (fragCoord-(nVec.st*refrBump*distortFade))*1.0-(rcoord*aberration*2.0)).b;
    
      
    float waterSunGradient = dot(normalize(cameraPos-worldPos), -normalize(sunPos));
    waterSunGradient = clamp(pow(waterSunGradient*0.7+0.3,2.0),0.0,1.0);  
    vec3 waterSunColor = vec3(0.0,1.0,0.85)*waterSunGradient;
    waterSunColor = (cameraPos.z<0.0)?waterSunColor*0.5:waterSunColor*0.25;//below or above water?
   
    float waterGradient = dot(normalize(cameraPos-worldPos), vec3(0.0,0.0,-1.0));
    waterGradient = clamp((waterGradient*0.5+0.5),0.2,1.0);
    vec3 watercolor = (vec3(0.0078, 0.5176, 0.700)+waterSunColor)*waterGradient*1.5;
    vec3 waterext = vec3(0.6, 0.8, 1.0);//water extinction
    
    watercolor = mix(watercolor*0.3*sunFade, watercolor, clamp(1.0-exp(-(sunPos.z/500.0)*sunext),0.0,1.0));
    
    float fog = length(cameraPos-worldPos)/visibility; 
    fog = (cameraPos.z<0.0)?fog:1.0;
    fog = clamp(pow(fog,1.0),0.0,1.0);
    
    float darkness = visibility*2.0;
    darkness = clamp((cameraPos.z+darkness)/darkness,0.0,1.0);
    
    fresnel = clamp(fresnel,0.0,1.0);
        
    vec3 color = mix(mix(refraction,scatterColor,lightScatter),reflection,fresnel*0.6);
    color = (cameraPos.z<0.0)?mix(clamp(refraction*1.2,0.0,1.0),reflection,fresnel):color;   
    color = (cameraPos.z<0.0)?mix(color, watercolor*darkness*scatterFade, clamp(fog/ waterext,0.0,1.0)):color;
    
    //color = mix(color,atmopherefog*0.8,atmopherefog.b);
    
    //gl_FragColor = vec4(vec3(color*0.001+(specColor*specular)),1.0);
    gl_FragColor = vec4(vec3(color+(specColor*specular)),1.0);
}
"""

mesh = own.meshes[0]
if 'shader' not in own:
	for mat in mesh.materials:
		own['shader'] = mat.getShader()
		if own['shader'] != None:		
			if not own['shader'].isValid():
				own['shader'].setSource(VertexShader, FragmentShader, 1)
own['shader'].setAttrib(g.SHD_TANGENT)
own['shader'].setUniformDef('ModelMatrix', g.MODELMATRIX)
own['shader'].setUniformDef('cameraPos', g.CAM_POS)
own['shader'].setSampler('reflectionSampler',0)
own['shader'].setSampler('refractionSampler',1)
own['shader'].setSampler('normalSampler',2)
own['shader'].setSampler('depthSampler',3)
own['shader'].setUniform1f('timer',own['timer']*3)

