import glob
import os
import sys

try:
    sys.path.append(glob.glob('C:/Applications/CARLA_0.9.5/PythonAPI/carla/dist/carla-*%d.%d-%s.egg' % (
        sys.version_info.major,
        sys.version_info.minor,
        'win-amd64' if os.name == 'nt' else 'linux-x86_64'))[0])
except IndexError:
    pass

import carla

import argparse
import math
import random
import time

red = carla.Color(255, 0, 0)
green = carla.Color(0, 255, 0)
blue = carla.Color(47, 210, 231)
cyan = carla.Color(0, 255, 255)
yellow = carla.Color(255, 255, 0)
orange = carla.Color(255, 162, 0)
white = carla.Color(255, 255, 255)

'''
PARAMETERS
'''
# loc = carla.Location(-50, 0, 0)
# loc = carla.Location(-60, 0, 0)
# loc = carla.Location(-100, 0, 0)
loc = carla.Location(-100, 0, 0)

seed = os.getpid()
distance = 15
depth = 10
thresh = 90 # +/- degrees
adjacents = True

lifeTime = 20
'''
END PARAMETERS
'''


def draw_waypoint_info(debug, w, lt=5):
    w_loc = w.transform.location
    debug.draw_string(w_loc + carla.Location(z=0.5), "lane: " + str(w.lane_id), False, yellow, lt)
    debug.draw_string(w_loc + carla.Location(z=1.0), "road: " + str(w.road_id), False, blue, lt)
    debug.draw_string(w_loc + carla.Location(z=-.5), str(w.lane_change), False, red, lt)

def drawWP(debug, w, color = red, size = 0.1, lt = lifeTime, persistentLines = False):
	debug.draw_point(w.transform.location + carla.Location(z=0.25), 
		size = size, color = color, life_time = lt, persistent_lines = persistentLines)

def drawWPUnion(debug, w0, w1, color = red, size = 0.1, lt = lifeTime, persistentLines = False):
	debug.draw_line(
        w0.transform.location + carla.Location(z=0.25),
        w1.transform.location + carla.Location(z=0.25),
        thickness=size, color=color, life_time=lt, persistent_lines=False)

def drawVector(debug, w, color = cyan, length = 3, size = 0.1, arrowSize = 5,
	lt = lifeTime, persistentLines = False):
	
	 
	begin = w.transform.location + carla.Location(z=0.25)


	yawInRad = math.radians(w.transform.rotation.yaw)
	xCal = begin.x + math.cos(yawInRad) * length
	yCal = begin.y + math.sin(yawInRad) * length
	zCal = begin.z
	end = carla.Location(x=xCal, y = yCal, z = zCal)

	debug.draw_arrow( begin, end,
        thickness=size, arrow_size=arrowSize, color=color, life_time=lt, persistent_lines=False)

def drawAdjacents(m, debug, w):
	rAdjLoc = getAdjacentLoc(w, True)
	lAdjLoc = getAdjacentLoc(w, False)
	# drawWP(debug, rAdjWp, color = yellow)
	# debug.draw_point(rAdjLoc + carla.Location(z=0.25), color = orange, life_time=lifeTime)
	# debug.draw_point(lAdjLoc + carla.Location(z=0.25), color = orange, life_time=lifeTime)
	# debug.draw_line(
	# lAdjLoc + carla.Location(z=0.25),
	# rAdjLoc + carla.Location(z=0.25), color=yellow, life_time=lifeTime)

	# wLoc = w.transform.location
	# rAdjWp = m.get_waypoint(rAdjLoc)
	# if wLoc.distance(rAdjWp.transform.location) > thresh:
	# 	drawWP(debug, rAdjWp, color = yellow)
	# 	drawWPUnion(debug, w, rAdjWp, color = yellow)

	# lAdjWp = m.get_waypoint(lAdjLoc)
	# if wLoc.distance(lAdjWp.transform.location) > thresh:
	# 	drawWP(debug, lAdjWp, color = yellow)
	# 	drawWPUnion(debug, w, lAdjWp, color = yellow)


	wYaw = w.transform.rotation.yaw
	# print("Wtr:")
	# print("loc, x= " + str(wTr.location.x) + " y= " + str(wTr.location.y)
	# 	+ " z= " + str(wTr.location.z) )
	# print("rot, x= " + str(wTr.rotation.pitch) + " y= " + str(wTr.rotation.yaw)
	# 	+ " z= " + str(wTr.rotation.roll) )
	rAdjWp = m.get_waypoint(rAdjLoc)

	# print("rAdjWp:")
	# print("loc, x= " + str(rAdjWp.transform.location.x) + " y= " + str(rAdjWp.transform.location.y)
	# 	+ " z= " + str(rAdjWp.transform.location.z) )
	# print("rot, x= " + str(rAdjWp.transform.rotation.pitch) + " y= " + str(rAdjWp.transform.rotation.yaw)
	# 	+ " z= " + str(rAdjWp.transform.rotation.roll) )

	if (wYaw - rAdjWp.transform.rotation.yaw + 90) % 360 > thresh * 2:
		# print((wYaw - rAdjWp.transform.rotation.yaw + 90) % 360)
		drawWP(debug, rAdjWp, color = yellow)
		drawWPUnion(debug, w, rAdjWp, color = yellow)
		drawVector(debug, rAdjWp, color = yellow)

	lAdjWp = m.get_waypoint(lAdjLoc)
	# print("lAdjWp:")
	# print("loc, x= " + str(lAdjWp.transform.location.x) + " y= " + str(lAdjWp.transform.location.y)
	# 	+ " z= " + str(lAdjWp.transform.location.z) )
	# print("rot, x= " + str(lAdjWp.transform.rotation.pitch) + " y= " + str(lAdjWp.transform.rotation.yaw)
	# 	+ " z= " + str(lAdjWp.transform.rotation.roll) )

	if (wYaw - lAdjWp.transform.rotation.yaw + 90) % 360 > thresh * 2:
		# print((wYaw - lAdjWp.transform.rotation.yaw + 90) % 360)
		drawWP(debug, lAdjWp, color = yellow)
		drawWPUnion(debug, w, lAdjWp, color = yellow)
		drawVector(debug, lAdjWp, color = green)


def addIfNotDup(wp, allTr, allWP):
	for i in allWP:
		if i.transform == wp.transform:
			return 
	# if wp.transform in allWP:
	# 	return True
	# else:
	allTr.append(wp.transform)
	allWP.append(wp)
	return 

def getAdjacentLoc(w, isRight = True):
	lnWidth = w.lane_width
	tr = w.transform
	yawInRad = math.radians(tr.rotation.yaw)

	if isRight:
		yawInRad += math.pi/2
	else:
		yawInRad -= math.pi/2
    # pitch_in_rad = math.radians(tr.rotation.pitch)
   
	xCal = tr.location.x + math.cos(yawInRad) * lnWidth
	yCal = tr.location.y + math.sin(yawInRad) * lnWidth
	zCal = tr.location.z
	return carla.Location(x=xCal, y = yCal, z = zCal)

def getNextWaypoints(debug, w):
	potentialTr = list()
	potentialW = list()

	nextWPs = w.next(distance)
	# print(len(nextWPs))
	# print(nextWPs[0].transform == nextWPs[1].transform)
	if len(nextWPs) != 0:
		potentialTr.append(nextWPs[0].transform)
		potentialW.append(nextWPs[0])

		for wp in nextWPs[1:]: 
			addIfNotDup(wp, potentialTr, potentialW)
				

	# for p in potentialW:
	# 	print("loc, x= " + str(p.transform.location.x) + " y= " + str(p.transform.location.y)
	# 		+ " z= " + str(p.transform.location.z) )
	# 	print("rot, x= " + str(p.transform.rotation.pitch) + " y= " + str(p.transform.rotation.yaw)
	# 		+ " z= " + str(p.transform.rotation.roll) )
	# 	print("id = " + str(p.id))
	# 	print("is_intersection = " + str(p.is_intersection))
	# 	# print("is_junction = " + str(p.is_junction))
	# 	print("lane_width = " + str(p.lane_width))
	# 	print("road_id = " + str(p.road_id))
	# 	print("section_id = " + str(p.section_id))
	# 	print("lane_id = " + str(p.lane_id))
	# 	print("s = " + str(p.s))
	# 	print("lane_change = " + str(p.lane_change))
	# 	print("lane_type = " + str(p.lane_type))
	# 	print("right_lane_marking = " + str(p.right_lane_marking))
	# 	print("left_lane_marking = " + str(p.left_lane_marking))
	# 	print()

	# # RIGHT
	# print("rmark= ", w.right_lane_marking.type, "+", w.right_lane_marking.lane_change)
	# print("lmark= ", w.left_lane_marking.type, "+", w.left_lane_marking.lane_change)
	if w.lane_change & carla.LaneChange.Right:
		# print("Right")
		right_w = w.get_right_lane()
		if right_w and right_w.lane_type == carla.LaneType.Driving:	
			for wp in right_w.next(distance): 
				addIfNotDup(wp, potentialTr, potentialW)

    # LEFT
	if w.lane_change & carla.LaneChange.Left:
		# print("Left")
		left_w = w.get_left_lane()
		if left_w and left_w.lane_type == carla.LaneType.Driving:
			for wp in left_w.next(distance): 
				addIfNotDup(wp, potentialTr, potentialW)
			# potentialW = potentialW.union(left_w.next(distance))

	# all potential WPs found
	for wp in potentialW:
		drawWPUnion(debug, w, wp)

	# print("wps ", len(potentialW), ", trs ", len(potentialTr))

	return potentialW

def WPdfs(debug, wpList):
	allNxtLvlWp = list()
	allNxtLvlTr = list()
	for wp in wpList:
		nextWPs = getNextWaypoints(debug, wp)
		for nextWP in nextWPs:
			addIfNotDup(nextWP, allNxtLvlTr, allNxtLvlWp)
		# allNextLevel.extend(nextWPs)
	return allNxtLvlWp

def main():
	try:
		client = carla.Client('localhost', 2000)
		client.set_timeout(5.0)

		world = client.get_world()

		settings = world.get_settings()
		settings.no_rendering_mode = False
		world.apply_settings(settings)

		m = world.get_map()
		debug = world.debug

		random.seed(seed)
		print("Seed: ", seed)
		print("Initial location: ", loc)

		initWp = m.get_waypoint(loc)
		currentWPs = [initWp]
		drawWP(debug, initWp, size = 0.2)
		drawAdjacents(m, debug, initWp)
		drawVector(debug, initWp)




		for i in range(0, depth):

			#GET NEXT WAYPOINTS
			potentialWPs= WPdfs(debug, currentWPs)
			print(len(currentWPs), "--", len(potentialWPs))
			currentWPs = []
			currentWPs = potentialWPs

			for p in currentWPs:
				# print(type(p))
				drawWP(debug, p)
				drawAdjacents(m, debug, p)
				drawVector(debug, p)


			# see if adjacent object is a road, draw it

	
		
		# choose a random waypoint to be the next
		# next_w = random.choice(potential_w)
		# potential_w.remove(next_w)

		# # Render some nice information, notice that you can't see the strings if you are using an editor camera
		# draw_waypoint_info(debug, current_w, trail_life_time)
		# draw_waypoint_union(debug, current_w, next_w, cyan if current_w.is_intersection else green, trail_life_time)
		# draw_transform(debug, current_w.transform, white, trail_life_time)

		# # print the remaining waypoints
		# for p in potential_w:
		#     debug.draw_string(p.transform.location, str(p.lane_id), False, orange, trail_life_time)
		#     draw_waypoint_union(debug, current_w, p, red, trail_life_time)
		#     draw_transform(debug, p.transform, white, trail_life_time)

		
		# x = input("Press Enter to end.")
		# print(x)
		print("Will Die in", lifeTime*2, "seconds")
		time.sleep(lifeTime*2)

	finally:
		pass


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('\nExit by user.')
    finally:
        print('\nExit.')