import numpy as np
import math
from movement_functions import *
import pdb
#This document contains the defintions of objects. In short
#A Swarm contains a list of boi objects. When it's turn method
#	is called, it gives a boi in its list local data (A Scan_data object)
#A Boi is one of the individual units that tries to organize
#	It contains its position, an object containing memory of prior movements (A Boi_memory object)
#	and a function for how it converts Scan_data and Boi_memory into a new direction to move
#

DEFAULT_SIZE = 1
DEFAULT_COLOR = (255,255,255)


#class containing information a boi passes to it's movefunction
class Boi_memory:
	def __init__(self):
		self.turns = []
		self.lonely_count = -1

#class describing a boi
class Boi:
	#create the class by possibly specifying a size and color
	def __init__(self, id, xpos = 0.0, ypos = 0.0, size=DEFAULT_SIZE, color = DEFAULT_COLOR, movefun=no_move):
		self.size = size
		self.color = color
		self.xpos = xpos
		self.ypos = ypos
		self.id = id
		self.movefun = movefun
		self.mem = Boi_memory()

	def move(self, sd):
		if len(sd.neighbors) == 0:
			self.mem.lonely_count = self.mem.lonely_count +1
		else:
			self.mem.lonely_count = -1
		direction = self.movefun(sd, self.mem)
		return direction

#class for information a swarm passes to a boi on its turn
class Scan_data:
	def __init__(self, neighbors, radius=-1):
		self.neighbors = neighbors
		self.radius = radius
		self.oob = []
		
#class that aggregates multiple bois, and gives them local information
class Swarm:
	#create the class by making a bunch of random bois
	def __init__(self, num, mf, xwin, ywin, radius, edge_behavior=[]):
		self.xwin = xwin
		self.ywin = ywin
		self.bois = []
		self.edge_behavior = edge_behavior
		self.radius = radius
		
		
		for i in range(num):
			xpos = np.random.normal((xwin[1]+xwin[0])/2.0, (xwin[1]-xwin[0])/6.0)
		 	ypos = np.random.normal((ywin[1]+ywin[0])/2.0, (ywin[1]-ywin[0])/6.0)
		 	self.bois.append(Boi(i, xpos=xpos, ypos=ypos, movefun=mf))
		

	#returns all neighbors in nearby (square) radius. If things are slow this coud be done faster
	def scan(self, id, xpos, ypos):
		neighbors = []
		for boi in self.bois:
			#if abs(boi.xpos - xpos) <= SCAN_RADIUS and abs(boi.ypos-ypos) <= SCAN_RADIUS and boi.id != id:
			if math.sqrt((boi.xpos-xpos)**2 + (boi.ypos-ypos)**2) < self.radius and boi.id != id:
				neighbors.append((boi.xpos - xpos, boi.ypos - ypos))
		return neighbors

	def turn(self, boi):
		
		if 'REPULSE' in self.edge_behavior:
			if boi.xpos == self.xwin[0]:
				boi.xpos += .05 * (self.xwin[1]-self.xwin[0])
			if boi.xpos == self.xwin[1]:
				boi.xpos -= .05 * (self.xwin[1]-self.xwin[0])
			if boi.ypos == self.ywin[0]:
				boi.ypos += .05 * (self.ywin[1]-self.ywin[0])
			if boi.ypos == self.ywin[1]:
				boi.ypos -= .05 * (self.ywin[1]-self.ywin[0])

		neighbors = self.scan(boi.id, boi.xpos, boi.ypos)
		sd = Scan_data(neighbors, self.radius)
		if 'WARN' in self.edge_behavior:
			if boi.xpos >= self.xwin[1]:
				sd.oob.append('R')
			if boi.ypos >= self.ywin[1]:
				sd.oob.append('U')
			if boi.xpos <= self.xwin[0]:
				sd.oob.append('L')
			if boi.ypos <= self.ywin[0]:
				sd.oob.append('D')
		direction = boi.move(sd)
		boi.xpos += direction[0]
		boi.ypos += direction[1]
		boi.mem.turns.append(direction)
		if 'STOP' in self.edge_behavior:
			if boi.xpos >= self.xwin[1]:
				boi.xpos = self.xwin[1]
			if boi.ypos >= self.ywin[1]:
				boi.ypos = self.ywin[1]
			if boi.xpos <= self.xwin[0]:
				boi.xpos = self.xwin[0]
			if boi.ypos <= self.ywin[0]:
				boi.ypos = self.ywin[0]

