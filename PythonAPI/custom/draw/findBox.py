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

def queryRoad(s):
    prefix = s[0]
    if prefix != "r" : 
        return -1
    
    num = eval(s[1:])
    if not isinstance(num, (int)):
        return -1

    return num

def validFormat(s):

    coordT = s.split(",")
    posX=0.0
    posY=0.0
    szX=0.0
    szY=0.0
    w =0.0

    if len(coordT) != 5:
        return []


    posX = eval(coordT[0])
    if not isinstance(posX, (int, float)):
        return []

    posY = eval(coordT[1])
    if not isinstance(posY, (int, float)):
        return []

    szX = eval(coordT[2])
    if not isinstance(szX, (int, float)):
        return []

    szY = eval(coordT[3])
    if not isinstance(szY, (int, float)):
        return []

    w = eval(coordT[4])
    if not isinstance(w, (int, float)):
        return []

    return [posX, posY, szX, szY, w]

def draw(coord, debug):

    x = coord[0]
    y = coord[1]
    hdg = coord[2]
    l = coord[3]
    w = coord[4]

    xy = carla.Location(x, y, 3)


    print(math.sin(hdg))
    print(math.cos(hdg))

    end = carla.Location(math.cos(hdg) * l, math.sin(hdg)* l)

    # extent = carla.Vector3D(halfX, halfY, 0)
    rot = carla.Rotation()

    # box = carla.BoundingBox(center, extent)

    debug.draw_arrow(xy, xy + end , thickness=0.5, life_time = lifeTime)

    debug.draw_point(xy, size=0.1, color = yellow, life_time = lifeTime)
    debug.draw_point(end, size=0.1, color = yellow, life_time = lifeTime)
    # debug.draw_point(center, size = 0.1, color = red, life_time = lifeTime)
    # debug.draw_box(box, rot, thickness=0.5, color = red, life_time = lifeTime)
    
    print("  Box drawn!")

def main():
    try:
        client = carla.Client('localhost', 2000)
        client.set_timeout(5.0)

        world = client.get_world()

        debug = world.debug

        s = ""


        while not s == "exit":
            s = input("Enter position and size \"posX, posY, Hdg, Length, width\" :")
            
            n = queryRoad(s)
            if n != -1:
                with open("roadCoords.txt") as fp:
                    for i, line in enumerate(fp):
                        if i == n:
                            s = line
            
            coord = validFormat(s)
            if len(coord) != 0:

                draw(coord, debug)

            elif not s == "exit":
                print("--incorrect Formatting!")

    finally:
        pass


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('\nExit by user.')
    finally:
        print('\nExit.')