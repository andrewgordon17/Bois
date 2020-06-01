import math
import numpy as np
import pdb

#a list of possible movement functions




def no_move(scan_data, mem): #don't move at all
	return [0.0,0.0]

def up_move(scan_data, mem): #take a step up. Just useful for testing
	return [0.0,0.1]

#function so that bois with no neighbors can execute a widening spiral
#input i is the number of turns since a neighbor has been seen
def lonely_move(i):
	x = math.floor(0.5*(-1 + math.sqrt(4*i + 1)))
	m = (x**2 + x + (x+1)**2 + (x+1))/2
	if i<= m:
		if x%2 == 1.0:
			return [1.0,0.0]
		return [-1.0, 0.0]
	else:
		if x%2 == 1.0:
			return [0.0, 1.0]
		return [0.0, -1.0]



#inputs a list of points in a plane, outputs the equation of a line (in Ax+By+C=0 format)
# that minimizes distance between those points and that line
def line_of_best_fit(pts):
	xs = np.array([pt[0] for pt in pts])
	ys = np.array([pt[1] for pt in pts])
	sumx = sum([pt[0] for pt in pts])
	sumxx = sum([pt[0]*pt[0] for pt in pts])
	sumxy = sum([pt[0]*pt[1] for pt in pts])
	sumy = sum([pt[1] for pt in pts])
	sumyy = sum([pt[1]*pt[1] for pt in pts])
	n = len(pts)

	sumax = sum([abs(pt[0]) for pt in pts])
	sumay = sum([abs(pt[1]) for pt in pts])

	#terrible edge cases
	if sumxx == 0.0 and sumyy == 0.0:
		#BAD
		return (0,0,0)
	if sumxx == 0.0:
		return (1,0,0)
	if sumyy == 0.0:
		return (0,1,0)
	if round(sumx*sumx,6) == round(n*sumxx,6) and round(sumy*sumy,6) == round(n*sumyy,6):
		return (0,0,0)

	#decide which normalization is a better fit, then solve
	if np.std(xs) > np.std(ys): #(sumx*sumx - sumxx) < (sumy*sumy - sumyy):
		c = (-1*sumy + (sumx * sumxy)/sumxx)/(n-sumx*sumx/sumxx)
		a = (-sumxy - (c*sumx))/sumxx
		l = (round(a,2),1,c)
		if l[0] != 0 and abs(l[0]) < 1:
			l = (1, 1/l[0], c/l[0])
		#print(str(-1*l[0]/l[1]))
		return l
	else:
		c = (-1*sumx + (sumy * sumxy)/sumyy)/(n-sumy*sumy/sumyy)
		b = (-sumxy - (c*sumy))/sumyy
		l = (1,round(b,2),c)
		#pdb.set_trace()
		if l[1] != 0 and abs(l[1]) < 1:
			l = (1/l[1], 1, c/l[1])
		#print(str(-1*l[0]/l[1]))
		return l






#inputs a line (in y=mx + b format) and a circle of radius r
#computes the length of the line that is inside the circle
#throws an error if they don't meet
def chord_endpoints(m, b, r):
	end0x = (-2*m*b - math.sqrt(4*m*m*b*b - 4*(1+m*m)*(b*b-r*r)))/(2+2*m*m)
	end0y = m* end0x + b
	end1x = (-2*m*b - math.sqrt(4*m*m*b*b - 4*(1+m*m)*(b*b-r*r)))/(2+2*m*m)
	end1y = m* end1x + b
	return ([end0x,end0y], [end1x,end1y])

#inputs a list of points on an interval (numbers)
#returns the spot on the interval farthest from any other point
def largest_gap(pts, interval):
	gap = (-1, pts[0]-interval[0])
	for i in range(len(pts) - 1):
		if pts[i+1] - pts[i] > gap[1]:
			gap= (i,pts[i+1] - pts[i])
	if interval[1] - pts[-1] > gap[1]:
		gap = (len(pts), interval[1] - pts[-1])
	return gap[0]


#attempt at evenly spacing. Particles are repulsed by others proportional to their distance (squared?)
def spread_dist_repulse(scan_data, mem): 
	neighbors = scan_data.neighbors
	vector = [0.0,0.0]
	for neighbor in neighbors:
		dist = math.sqrt(neighbor[0]**2 + neighbor[1]**2)
		if dist == 0.0:
			continue
		inv_dist = scan_data.radius*.25*(dist**(-1))#compute coeff organically?
		vector[0] = vector[0] - (inv_dist*neighbor[0])
		vector[1] = vector[1] - (inv_dist*neighbor[1])
	return vector

#movement function that lines the bois up.
#Briefly, each boi finds the line of best fit and moves to it, 
#	spacing out along that line when possible
def line_find_best_fit(scan_data, mem):
	END_CONST = 3
	neighbors = scan_data.neighbors
	rad = scan_data.radius
	#pdb.set_trace()
	if len(neighbors) < 1:#if no neighbors, return to central zone if out of it, else [TODO]
		#if len(scan_data.oob) > 0:
			# if scan_data.oob[0] == 'R':
			# 	return [-1*rad, 0.0]
			# if scan_data.oob[0] == 'L':
			# 	return [rad, 0.0]
			# if scan_data.oob[0] == 'U':
			# 	return [0.0, -1*rad]
			# if scan_data.oob[0] == 'D':
			# 	return [0.0, rad]
		#if mem.lonely_count == 0 and len(mem.turns)>0:
			#return [-1*mem.turns[-1][0], -1*mem.turns[-1][1]]
		spiral_dir = lonely_move(mem.lonely_count)
		return [rad*spiral_dir[0], rad*spiral_dir[1]]

	if len(neighbors) == 1:

		if neighbors[0][0] == 0.0:
			if neighbors[0][1] == 0.0:
				return [0.0,0.0]#BAD
			return [0.0, -1*math.copysign(rad, neighbors[0][1])]
		slope = neighbors[0][1]/neighbors[0][0]
		new_x = -1*math.copysign(rad/math.sqrt(slope*slope + 1), neighbors[0][0])
		return [new_x, slope* new_x]
		
		# dist = math.sqrt(neighbors[0][0]**2 + neighbors[0][1]**2)
		# if dist == 0.0:
		# 	return [0.0,0.0]
		# scale = rad/dist
		# return [-1*scale*neighbors[0][0], -1*scale*neighbors[0][1]]

	#find the line of best fit for neighbors	

	line = line_of_best_fit(neighbors)
	#pdb.set_trace()
	
	#Find location on line of best fit that is most spaced out:
		#we now have a chord in a circle of radius RADIUS. We find the new location by projecting all the neighbors
		#onto the chord, and finding the biggest gap among the projections
	if line[0] == 0.0 and line[1] == 0.0:
		#BAD
		return [0.0,0.0]

	#treat vertical lines separately
	if line[1]==0:
		unit = [0,1]
		mid = [-line[2]/line[0], 0]
		length = 2*math.sqrt(rad*rad - (line[2]/line[0])*(line[2]/line[0]))
	else: #use coordinates y=mx+b
		m = -1*line[0]/line[1]
		b = -1*line[2]/line[1]
		disc = 4*m*m*b*b -4*(1+m*m)*(b*b-rad*rad)
		if disc < 0:
			pdb.set_trace()
		length = math.sqrt(disc/(1+m*m)) #the length of the chord


		#the midpoint of the chord
		if m==0:
			mid= [0, 1*b]
		else:
			mid = [-1*b/(m+m**(-1)), b/(m*m+1)]

		#a unit vector in the direction of the chord
		scale = math.sqrt(1 + m**2)
		unit = [1/scale, m/scale]

	projections = []
	for n in neighbors:
		n_shift = [n[0] - mid[0], n[1] - mid[1]]#shift our coordinates so the center of the chord is (0,0)
		projections.append(n_shift[0]*unit[0] + n_shift[1]*unit[1])#dot product to see position of orthogonal projection
	projections.sort()

	

	gap = largest_gap(projections, (-length/2, length/2))#finds the index to the left of the largest gap

	if gap == -1:
		# if all(i > 0 for i in projections) or all(i < 0 for i in projections):#if I'm at an endpoint
		# 	if len(projections) >= SOME_CONSTANT: #if my line is thick enough, expand
		# 		d = (projections[0] - length)/2
		# 		vector = [mid[0] + d*unit[0], mid[1] + d*unit[1]]
		# 	else: #if not, stay put
		# 		vector = mid
		# else:#if I'm not at an endpoint, expand
		# 	d = (projections[0] - length)/2
		# 	vector = [mid[0] + d*unit[0], mid[1] + d*unit[1]]
		if len(projections)<END_CONST:
			vector = mid #?
		else:
			d = max(-length/2, projections[END_CONST-1]- rad)
			vector = [mid[0] + d*unit[0], mid[1] + d*unit[1]]
	elif gap == len(projections):
		# if all(i > 0 for i in projections) or all(i < 0 for i in projections):#if I'm at an endpoint
		# 	if len(projections) >= SOME_CONSTANT: #if my line is thick enough, expand
		# 		d = (projections[-1] + length)/2
		# 		vector = [mid[0] + d*unit[0], mid[1] + d*unit[1]]
		# 	else: #if not, stay put
		# 		vector = mid
		# else:
		# 	d = (projections[-1] + length)/2
		# 	vector = [mid[0] + d*unit[0], mid[1] + d*unit[1]]
		if len(projections)<END_CONST:
			vector = mid #?
		else:
			d = min(length/2, projections[-1*END_CONST]+ rad)
			vector = [mid[0] + d*unit[0], mid[1] + d*unit[1]]
	else:
		d = (projections[gap+1] + projections[gap])/2
		vector = [mid[0] + d*unit[0], mid[1] + d*unit[1]]

	return vector



	





