import glob
import os
import sys

import argparse
import math
import random
import time
import xml.etree.ElementTree as ET


def main():
    doc = ET.parse("maps/Town03.xodr").getroot()
    roads = doc.iter("road")
    print("Root tag is ", doc.tag)

    for r in roads:
        # geoms = r.getElementsByTagName("planView")[0].getElementsByTagName("geometry")
        # print(r.getAttribute("name"),  ": ", len(geoms), "geometries")

        geoms = r.getElementsByTagName("planView")[0].attributes.values()
        print(r.getAttribute("name"),  ": ", geoms)



        # if len(rtype) != 0 :
        #     speed = r.getElementsByTagName("type")
        #     print(", ", len(speed))
            
        # g = pv.getElementsByTagName("geometry")[0]
        # posX = eval(g.getAttribute("x"))
        # posY = eval(g.getAttribute("y"))
        # szX = eval(g.getAttribute("length"))
        # szY = eval(g.getAttribute("hdg"))
        # coord = [posX, posY, szX, szY]
        # print("drawing", r.getAttribute("name"), ": (", posX, ", ", posY, ")")
        # _findBox.draw(coord, debug)

        # loc = carla.Location(eval(x), eval(y), 2)
        # print("drawing", r.getAttribute("name"), ": (", eval(x), ", ", eval(y), ")")
        # debug.draw_point(loc, size = 0.2, color = red, life_time = lifeTime)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('\nExit by user.')
    finally:
        print('\nExit.')