import bge

w = bge.render.getWindowWidth()
h = bge.render.getWindowHeight()

#print (w,h)

#shader.setUniform2f("screensize", w, h)

def toNextPOT(num):
    pot = 2;
    while num > pot:
        pot = pot * 2
    return pot

co = bge.logic.getCurrentController()

own = co.owner

#own['screen_width'] = w
#own['screen_height'] = h

own['screen_width'] = toNextPOT(w)
own['screen_height'] = toNextPOT(h)

#print (w,h)
#print (toNextPOT(w), toNextPOT(h))

#for act in co.actuators:
#    print (act.name, type(act))
#    #print (dir(act))

#distortion = co.actuators["riftDistortion"]

#print (dir(distortion))

#print(own['foo'] )

#own['foo'] = own['foo'] - 0.01p
