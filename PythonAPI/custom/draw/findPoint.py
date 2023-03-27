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
yellow = carla.Color(255, 255, 0)

lifeTime = 10

def validFormat(s):

	coordT = s.split(",")
	x=0.0
	y=0.0
	z=0.0

	if len(coordT) <2 or len(coordT) > 3:
		return []


	x = eval(coordT[0])
	if not isinstance(x, (int, float)):
		return []

	y = eval(coordT[1])
	if not isinstance(y, (int, float)):
		return []

	z = 1

	if len(coordT) == 3 :

		z = eval(coordT[2])
		if not isinstance(z, (int, float)):
			return []

	return [x, y, z]


def main():
	try:
		client = carla.Client('localhost', 2000)
		client.set_timeout(5.0)

		world = client.get_world()

		m = world.get_map()
		debug = world.debug

		s = ""


		while not s == "exit":
			s = input("Enter a position \"x, y(, z)\" :")

			coord = validFormat(s)
			if len(coord) != 0:


				loc = carla.Location(coord[0], coord[1], coord[2])

				w = m.get_waypoint(loc)
				w_loc = w.transform.location

				debug.draw_point(loc, size = 0.2, color = red, life_time = lifeTime)
				debug.draw_point(w_loc + carla.Location(z=1), size = 0.1, color = yellow, life_time = lifeTime)
				debug.draw_line(loc, w_loc + carla.Location(z=1), thickness=0.2, color= red, life_time=lifeTime)

				print(f"  point [{coord[0]}, {coord[1]}] drawn at [{w_loc.x}, {w_loc.y}]!")

			elif not s == "exit":
				print("--incorrect Formatting!")

		

		




		# for i in range(0, depth):

		# 	#GET NEXT WAYPOINTS
		# 	potentialWPs= WPdfs(debug, currentWPs)
		# 	print(len(currentWPs), "--", len(potentialWPs))
		# 	currentWPs = []
		# 	currentWPs = potentialWPs

		# 	for p in currentWPs:
		# 		# print(type(p))
		# 		drawWP(debug, p)
		# 		drawAdjacents(m, debug, p)
		# 		drawVector(debug, p)


			# see if adjacent object is a road, draw it


		# print("Will Die in", lifeTime*2, "seconds")
		# time.sleep(lifeTime*2)

	finally:
		pass


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('\nExit by user.')
    finally:
        print('\nExit.')