from bge import logic as G
from bge import events

keyboard = G.keyboard.events

cont = G.getCurrentController()
owner = cont.owner

# KEY BINDINGS

kbleft = events.AKEY # Replace these with others, if you wish
kbright = events.DKEY # An example would be 'events.WKEY, DKEY, SKEY, and AKEY
kbup = events.WKEY
kbdown = events.SKEY # 

##################

if not 'moveinit' in owner:
    owner['moveinit'] = 1
    owner['mx'] = 0.0
    owner['my'] = 0.0
    
    #
    #
    #
    # ~~SETTINGS~~ #
    #
    #
    #
    # Tweak these settings to fit your needs
    
    owner['accel'] = 2.0      # Acceleration
    owner['maxspd'] = 5.0    # Top speed
    owner['friction'] = 0.75   # Friction percentage; set to 0.0 for immediate stop
    owner['movelocal'] = 1    # Move on local axis?
    
if keyboard[kbleft]:
    owner['mx'] += owner['accel']
elif keyboard[kbright]:
    owner['mx'] -= owner['accel']
else:
    owner['mx'] *= owner['friction']
    
if keyboard[kbup]:
    owner['my'] += owner['accel']
elif keyboard[kbdown]:
    owner['my'] -= owner['accel']
else:
    owner['my'] *= owner['friction']
    
# Clamping
    
if owner['mx'] > owner['maxspd']:
    owner['mx'] = owner['maxspd']
elif owner['mx'] < -owner['maxspd']:
    owner['mx'] = -owner['maxspd']
    
if owner['my'] > owner['maxspd']:
    owner['my'] = owner['maxspd']
elif owner['my'] < -owner['maxspd']:
    owner['my'] = -owner['maxspd']
    
# Actual movement
    
owner.setLinearVelocity([owner['my'], owner['mx'], owner.getLinearVelocity()[2]], owner['movelocal'])
