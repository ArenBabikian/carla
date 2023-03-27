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
import xml.dom.minidom
import findBox

red = carla.Color(255, 0, 0)
yellow = carla.Color(255, 255, 0)

lifeTime = 10


def main():
    try:
        client = carla.Client('localhost', 2000)
        client.set_timeout(5.0)

        world = client.get_world()

        debug = world.debug

        doc = xml.dom.minidom.parse("maps/Town03.xodr")
        roads = doc.getElementsByTagName("road")

        for r in roads[3:4]:
            pv = r.getElementsByTagName("planView")[0]
            g = pv.getElementsByTagName("geometry")[0]
            posX = eval(g.getAttribute("x"))
            posY = eval(g.getAttribute("y"))
            szX = eval(g.getAttribute("length"))
            szY = eval(g.getAttribute("hdg"))
            coord = [posX, posY, szX, szY]
            print("drawing", r.getAttribute("name"), ": (", posX, ", ", posY, ")")
            findBox.draw(coord, debug)

            # loc = carla.Location(eval(x), eval(y), 2)
            # print("drawing", r.getAttribute("name"), ": (", eval(x), ", ", eval(y), ")")
            # debug.draw_point(loc, size = 0.2, color = red, life_time = lifeTime)

        time.sleep(lifeTime)
            

    finally:
        pass


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('\nExit by user.')
    finally:
        print('\nExit.')