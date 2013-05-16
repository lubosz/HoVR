from bge import logic as g
from bge import render as r
from mathutils import *
from math import *
import bgl

cont = g.getCurrentController()
own = cont.owner
scene = g.getCurrentScene()
objects = scene.objects

width = r.getWindowWidth()
height = r.getWindowHeight()

rf = g.getRandomFloat

viewport = bgl.Buffer(bgl.GL_INT, 4)
bgl.glGetIntegerv(bgl.GL_VIEWPORT, viewport);
pixels = bgl.Buffer(bgl.GL_FLOAT, [1])

SAMPLES = 10
ADAPT = 0.99
g.xpoint = []
g.ypoint = []

    
def init():
    
    #http://www.cgafaq.info/wiki/Evenly_distributed_points_on_sphere
    
    dlong = pi*(3-sqrt(5))
    dz = 1.0/SAMPLES
    long = 0
    z = 1 - dz/2
    
    for i in range(SAMPLES):
       
        g.xpoint.append([])
        g.ypoint.append([])
        
        r = sqrt(1-z)
        
        g.xpoint[i] = viewport[0] + ((cos(long)*r)*0.5+0.5)*width
        g.ypoint[i] = viewport[1] + ((sin(long)*r)*0.5+0.5)*height
                
        z = z - dz
        long = long + dlong   
        
    g.reileigh = 2.5
    g.turbidity = 2.0
    g.worldscale = 1.0
    
    g.contrast = 6.5
    g.bias = 2.0
    g.lumamount = 0.3
    
    g.initialized = 1
    

    
def getlum():
    
    g.readL = 0
    if hasattr(g,"initialized"):
        for j in range(SAMPLES):
            bgl.glReadPixels(int(g.xpoint[j]),int(g.ypoint[j]), 1, 1, bgl.GL_LUMINANCE, bgl.GL_FLOAT, pixels)
            g.readL += pixels[0]            
    g.readL /= SAMPLES
    
def setlum():
    
    Lum = g.readL
    
    adapt = 0.8
    time = 1/(60)
    own["L"] = own["L"] + (Lum - own["L"]) * (1 - exp(-time * adapt)); 
    
    g.luminance = own["L"]
    
    #objects["skybox"].color = [own["L"],1.0,1.0,1.0]
    #objects["ground"].color = [own["L"],1.0,1.0,1.0]
