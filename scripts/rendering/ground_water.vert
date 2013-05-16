attribute vec4 Tangent;
varying vec3 WorldSpacePos, eyePos;
varying vec3 LightVec;
varying mat3 WorldToTangent;
uniform mat4 ModelMatrix;
uniform vec3 cameraPos;
varying vec3 WorldNormal, WorldTangent, WorldBinormal;
uniform sampler2D NormalSampler,foamSampler;
//varying vec3 Pos;
varying float timer;
varying vec4 fragPos;

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

void main() {
     		
	WorldSpacePos = vec3(ModelMatrix*gl_Vertex);  
	eyePos = vec3(ModelMatrix*gl_ModelViewMatrixInverse[3]);
	LightVec = vec3(ModelMatrix*(gl_ModelViewMatrixInverse*gl_LightSource[0].position));
    fragPos = ftransform();
	
	WorldTangent    = m3(ModelMatrix) * Tangent.xyz;
	WorldBinormal   = m3(ModelMatrix) * cross(gl_Normal, Tangent.xyz);
	WorldNormal     = m3(ModelMatrix) * gl_Normal; 
	
    gl_TexCoord[0].st = gl_Vertex.xy;
	gl_TexCoord[1] = ftransform();
	gl_FrontColor = gl_Color;
	
	//Pos = vec3(gl_ModelViewMatrix*gl_Vertex);
	//timer = gl_Color.r*2.0;
	gl_Position = ftransform();

    #ifdef __GLSL_CG_DATA_TYPES
	    gl_ClipVertex = gl_ModelViewMatrix * gl_Vertex;
    #endif

}
