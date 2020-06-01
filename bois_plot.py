from matplotlib import pyplot as plt
from matplotlib import animation
from bois_classes import Swarm
from movement_functions import *

#This code creates a swarm and graphs its progress in matplotlib

#Variables that affect the swarm
NUMBER_OF_BOIS = 500
BOI_SIZE = .005
RADIUS = .2 #Radius a Boi can see
SHOW_RADIUS = False #when True shows the radius as a circle around each Boi

#Variables that affect the display
NUM_STEPS = 2000 #required for the animation function. SHould be larger than NUMBER_OF_BOIS
NUM_PER_ANIMATE =500 #The number of Bois that update position each frame
INTERVAL = 2000 #the time between frames, in ms

#The parameters for the window where the bois appear at the start
X_LIM = (-1,2)
Y_LIM = (-1,2)
#the parameters for the window that is plotted
X_AX_LIM = (-4,5)
Y_AX_LIM = (-4,5)


fig = plt.figure()

ax = plt.axes(xlim=X_AX_LIM, ylim=Y_AX_LIM)


patches = []
for i in range(NUMBER_OF_BOIS):
	
	if SHOW_RADIUS:
		outer = plt.Circle((X_LIM[0], Y_LIM[0]), RADIUS, fill=False)
		patches.append((plt.Circle((X_LIM[0], Y_LIM[0]), BOI_SIZE),outer))
	else:
		patches.append(plt.Circle((X_LIM[0], Y_LIM[0]), BOI_SIZE))

swm = Swarm(num=NUMBER_OF_BOIS, mf=line_find_best_fit, xwin = X_LIM, ywin = Y_LIM, radius = RADIUS, edge_behavior = ['WARN'])

def init():
	if SHOW_RADIUS:
		for i in range(NUMBER_OF_BOIS):
			patches[i][0].center = (swm.bois[i].xpos, swm.bois[i].ypos)
			patches[i][0].center = (swm.bois[i].xpos, swm.bois[i].ypos)
			ax.add_patch(patches[i][0])
			ax.add_patch(patches[i][1])
		return tuple(patches)
	else:
		for i in range(NUMBER_OF_BOIS):
			patches[i].center = (swm.bois[i].xpos, swm.bois[i].ypos)
			ax.add_patch(patches[i])
		return tuple(patches)

def animate(i):
	i = (NUM_PER_ANIMATE*i)%NUMBER_OF_BOIS
	edited = []
	for j in range(NUM_PER_ANIMATE):
		idx = (i+j)%NUMBER_OF_BOIS
		swm.turn(swm.bois[idx])
		if SHOW_RADIUS:
			patches[idx][0].center = (swm.bois[idx].xpos, swm.bois[idx].ypos)
			edited.append(patches[idx][0])
			patches[idx][1].center = (swm.bois[idx].xpos, swm.bois[idx].ypos)
			edited.append(patches[idx][1])
		else:
			patches[idx].center = (swm.bois[idx].xpos, swm.bois[idx].ypos)
			edited.append(patches[idx])
	return tuple(edited)

anim = animation.FuncAnimation(fig, animate, 
                               init_func=init, 
                               frames=NUM_STEPS, 
                               interval=INTERVAL,
                               blit=False)
plt.show()


