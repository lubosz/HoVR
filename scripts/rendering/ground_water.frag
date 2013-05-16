varying vec3 WorldNormal;
varying vec3 WorldTangent;
varying vec3 WorldBinormal;
varying vec3 WorldSpacePos, eyePos;
varying vec3 LightVec;
varying vec4 fragPos;
varying mat3 WorldToTangent;
uniform sampler2D NormalSampler, TextureSampler,foamSampler;
//varying vec3 Pos;
uniform float timer;

bool causticFringe = false;

float choppy = 0.8;
float refractAmount = 0.4;
float aberration = 0.04;
float visibility = 28.0; //water visibility

float waterLevel = 0.0;

vec2 windDir = vec2(0.5, -0.8); //wind direction XY
float windSpeed = 0.2; //wind speed

float scale = 1.0; //overall wave scale

vec2 bigWaves = vec2(0.3, 0.3); //strength of big waves
vec2 midWaves = vec2(0.3, 0.15); //strength of middle sized waves
vec2 smallWaves = vec2(0.15, 0.1); //strength of small waves

vec3 tangentSpace(vec3 v)
{
	vec3 vec;
	vec.xy=v.xy;
	vec.z=sqrt(1.0-dot(vec.xy,vec.xy));
	vec.xyz= normalize(vec.x*WorldTangent+vec.y*WorldBinormal+vec.z*WorldNormal);
	return vec;
}

vec3 intercept(vec3 lineP,
               vec3 lineN,
               vec3 planeN,
               float  planeD)
{
  
	float distance = (planeD - dot(planeN, lineP)) /dot(lineN, planeN);
	return lineP + lineN * distance;
}

vec3 perturb1(sampler2D tex, vec2 coords, float bend)
{
	//normal map
	vec2 nCoord = vec2(0.0); //normal coords
    bend *= choppy;
  	nCoord = coords * (scale * 0.05) + windDir * timer * (windSpeed*0.04);
	vec3 normal0 = 2.0 * texture2D(tex, nCoord + vec2(-timer*0.015,-timer*0.05)).rgb - 1.0;
	nCoord = coords * (scale * 0.1) + windDir * timer * (windSpeed*0.08)-normal0.xy*bend;
	vec3 normal1 = 2.0 * texture2D(tex, nCoord + vec2(+timer*0.020,+timer*0.015)).rgb - 1.0;
 
 	nCoord = coords * (scale * 0.25) + windDir * timer * (windSpeed*0.07)-normal1.xy*bend;
	vec3 normal2 = 2.0 * texture2D(tex, nCoord + vec2(-timer*0.04,-timer*0.03)).rgb - 1.0;
	nCoord = coords * (scale * 0.5) + windDir * timer * (windSpeed*0.09)-normal2.xy*bend;
	vec3 normal3 = 2.0 * texture2D(tex, nCoord + vec2(+timer*0.03,+timer*0.04)).rgb - 1.0;
  
  	nCoord = coords * (scale* 1.0) + windDir * timer * (windSpeed*0.4)-normal3.xy*bend;
	vec3 normal4 = 2.0 * texture2D(tex, nCoord + vec2(-timer*0.2,+timer*0.1)).rgb - 1.0;  
    nCoord = coords * (scale * 2.0) + windDir * timer * (windSpeed*0.7)-normal4.xy*bend;
    vec3 normal5 = 2.0 * texture2D(tex, nCoord + vec2(+timer*0.1,-timer*0.06)).rgb - 1.0;


	vec3 normal = normalize(normal0 * bigWaves.x + normal1 * bigWaves.y +
                            normal2 * midWaves.x + normal3 * midWaves.y +
						    normal4 * smallWaves.x + normal5 * smallWaves.y);
    return normal;
}

vec3 perturb(sampler2D tex, vec2 coords, float bend)
{
bend *= choppy;
vec3 col = vec3(0.0);
vec2 nCoord = vec2(0.0); //normal coords

nCoord = coords * (scale * 0.04) + windDir * timer * (windSpeed*0.03);
col += texture2D(tex,nCoord + vec2(-timer*0.005,-timer*0.01)).rgb*0.20;
nCoord = coords * (scale * 0.1) + windDir * timer * (windSpeed*0.05)-(col.xy/col.zz)*bend;
col += texture2D(tex,nCoord + vec2(+timer*0.01,+timer*0.005)).rgb*0.20;

nCoord = coords * (scale * 0.25) + windDir * timer * (windSpeed*0.1)-(col.xy/col.zz)*bend;
col += texture2D(tex,nCoord + vec2(-timer*0.02,-timer*0.03)).rgb*0.20;
nCoord = coords * (scale * 0.5) + windDir * timer * (windSpeed*0.2)-(col.xy/col.zz)*bend;
col += texture2D(tex,nCoord + vec2(+timer*0.03,+timer*0.02)).rgb*0.15;

nCoord = coords * (scale* 1.0) + windDir * timer * (windSpeed*1.0)-(col.xy/col.zz)*bend;
col += texture2D(tex, nCoord + vec2(-timer*0.06,+timer*0.08)).rgb*0.15;
nCoord = coords * (scale * 2.0) + windDir * timer * (windSpeed*1.3)-(col.xy/col.zz)*bend;
col += texture2D(tex,nCoord + vec2(+timer*0.08,-timer*0.06)).rgb*0.10;

return col;
}

void main() {


    float waterSunGradient = dot(normalize(eyePos-WorldSpacePos), -normalize(LightVec));
    waterSunGradient = clamp(pow(waterSunGradient*0.7+0.3,2.0),0.0,1.0);
    
    float waterGradient = dot(normalize(eyePos-WorldSpacePos), vec3(0.0,0.0,-1.0));
    waterGradient = clamp((waterGradient*0.5+0.5),0.2,1.0);
    
    vec3 waterSunColor = vec3(0.0,1.0,0.85)*waterSunGradient;
    waterSunColor = (eyePos.z-waterLevel<0.0)?waterSunColor*0.5:waterSunColor*0.25;//below or above water?
    
    vec3 waterColor = (vec3(0.0078, 0.5176, 0.700)+waterSunColor)*waterGradient*1.5;
    
    vec3 mudext = vec3(1.0, 0.7, 0.5);//mud extinction
    vec3 waterext = vec3(0.6, 0.8, 1.0);//water extinction
    vec3 sunext = vec3(0.45, 0.55, 0.7);//sunlight extinction
    
    vec3 fragCoord = vec3(fragPos.xyz);

	vec2 TexCoord = gl_TexCoord[0].st;
	vec3 normal = tangentSpace(vec3(0.0,0.0,0.0));
	
	vec3 EV = normalize(eyePos-WorldSpacePos);
	vec3 LV	= normalize(LightVec-WorldSpacePos);
	
	vec3 waterEyePos = intercept(WorldSpacePos, eyePos-WorldSpacePos, vec3(0.0,0.0,1.0),waterLevel);
    
    vec3 diffuse = texture2D(TextureSampler,gl_TexCoord[0].st*0.05).rgb;      
    //vec3 diffuse = texture2D(TextureSampler,gl_TexCoord[0].st).rgb;
    
    vec3 nothing = vec3(0);
    
    if (diffuse.x == 0.0) {
        diffuse = vec3(1.0);
    }

	float NdotL = max(dot(normal,LV),0.0);


    float sunFade = clamp((LightVec.z+10.0)/20.0,0.0,1.0);
    float scatterFade = clamp((LightVec.z+50.0)/200.0,0.0,1.0);
    vec3 sunLight = mix(vec3(1.0,0.5,0.2), vec3(1.0,1.0,1.0), clamp(1.0-exp(-(LightVec.z/500.0)*sunext),0.0,1.0));
    sunLight *= NdotL*sunFade;
    
    
    //sky illumination
    float skyBright = max(dot(normal,vec3(0.0,0.0,1.0))*0.5+0.5,0.0);   
    vec3 skyLight = mix(vec3(1.0,0.5,0.0)*0.05, vec3(0.2,0.5,1.0)*1.5, clamp(1.0-exp(-(LightVec.z/500.0)*sunext),0.0,1.0));
    skyLight *= skyBright;

    //ground illumination
    float groundBright = max(dot(normal,vec3(0.0,0.0,-1.0))*0.5+0.5,0.0);   
    vec3 groundLight = vec3(0.3,0.3,0.3)*1.0*clamp(1.0-exp(-(LightVec.z/500.0)),0.0,1.0);
    groundLight *= groundBright;
 
    float underwaterFresnel = pow(clamp(1.0-dot(normal,EV),0.0,1.0),2.0)*clamp(1.0-exp(-(LightVec.z/500.0)),0.0,1.0);
 
    //water fogging
       
	float topfog = length(waterEyePos-WorldSpacePos)/visibility;
    topfog = clamp(topfog,0.0,1.0);
    
    float underfog = length(eyePos-WorldSpacePos)/visibility;
    underfog = clamp(underfog,0.0,1.0);

	float depth = waterEyePos.z-WorldSpacePos.z;//water depth

    float far = length(eyePos-WorldSpacePos)/1000.0;
    float shorecut = ((eyePos.z)-waterLevel<0.0)?smoothstep(-5.0*max(far,0.0001),-4.0*max(far,0.0001),depth):smoothstep(-0.001,0.001,depth);
    
    float shorewetcut = smoothstep(-0.18,-0.000,depth+0.01);
    
    
    
    depth /= visibility;  
    depth = clamp(depth,0.0,1.0);
    

    
    float fog = (eyePos.z-waterLevel<0.0)?underfog:topfog;//below or above water?
    fog = pow(fog,1.0);
    fog = fog*shorecut;
    
    float darkness = visibility*1.5;
    darkness = mix(1.0,clamp((eyePos.z+darkness)/darkness,0.0,1.0),shorecut);
    float fogdarkness = visibility*2.0;
    fogdarkness = mix(1.0,clamp((eyePos.z+fogdarkness)/fogdarkness,0.0,1.0),shorecut)*scatterFade;
    

    //caustics
    vec3 causticPos = intercept(WorldSpacePos, LightVec-WorldSpacePos, vec3(0.0,0.0,1.0),waterLevel);
    float causticdepth = length(causticPos-WorldSpacePos); //caustic depth
    causticdepth = 1.0-clamp(causticdepth/visibility,0.0,1.0);
    causticdepth = clamp(causticdepth,0.0,1.0);
    
    vec3 normalMap = perturb(NormalSampler,causticPos.st,causticdepth);
    vec3 causticnorm = tangentSpace(normalMap*2.0-1.0);
    
    float fresnel = pow(clamp(dot(LV,causticnorm),0.0,1.0),2.0); 
 
    float causticR = 1.0-perturb(NormalSampler,causticPos.st,causticdepth).z;
        
    vec3 caustics = clamp(pow(vec3(causticR)*5.5,vec3(5.5*causticdepth)),0.0,1.0)*NdotL*sunFade*causticdepth;
    
    if(causticFringe)
    {
    float causticG = 1.0-perturb(NormalSampler,causticPos.st+(1.0-causticdepth)*aberration,causticdepth).z;
    float causticB = 1.0-perturb(NormalSampler,causticPos.st+(1.0-causticdepth)*aberration*2.0,causticdepth).z;
    caustics = clamp(pow(vec3(causticR,causticG,causticB)*5.5,vec3(5.5*causticdepth)),0.0,1.0)*NdotL*sunFade*causticdepth;
    }
    
    
    vec3 underwaterSunLight = clamp((sunLight+0.9)-(1.0-caustics),0.0,1.0)*causticdepth+(sunLight*caustics);
    
    underwaterSunLight = mix(underwaterSunLight, underwaterSunLight*waterColor, clamp((1.0-causticdepth)/waterext,0.0,1.0));
    skyLight = mix(skyLight, skyLight*waterColor, clamp((depth)/waterext,0.0,1.0));
    groundLight = mix(groundLight, groundLight*waterColor, clamp((depth)/waterext,0.0,1.0));

    sunLight = mix(sunLight,mix(underwaterSunLight,(waterColor*0.8+0.4)*sunFade,underwaterFresnel),shorecut);

    vec3 color = vec3(sunLight+skyLight*0.7+groundLight*0.8)*darkness;

    waterColor = mix(waterColor*0.3*sunFade, waterColor, clamp(1.0-exp(-(LightVec.z/500.0)*sunext),0.0,1.0));

    vec3 foo = (diffuse * 0.2 + 0.8) * color *
               mix(vec3(1.2,0.95,0.58) * 0.8,
                   vec3(1.1,0.85,0.5) * 0.8,
                   shorewetcut);

    //adding water color fog
    vec3 fogging = mix(foo, 
                       waterColor * fogdarkness, 
                       clamp(fog / waterext, 0.0, 1.0));

    
    
    //vec3 light = ((diffuse*0.2+0.8)*vec3(1.0,0.85,0.55)*(NdotL+skyLight+groundLight));
    
    gl_FragColor =  vec4(fogging,1.0) ;
    
    //gl_FragColor = vec4(LightVec,1);
    //gl_FragColor = vec4(shorewetcut, 1);
    //gl_FragColor = texture2D(TextureSampler,gl_TexCoord[0].st);
    //gl_FragColor = texture2D(NormalSampler,gl_TexCoord[0].st);
   
   
}
