import glob
import os
import sys

try:
    sys.path.append(glob.glob('../../carla/dist/carla-*%d.%d-%s.egg' % (
        sys.version_info.major,
        sys.version_info.minor,
        'win-amd64' if os.name == 'nt' else 'linux-x86_64'))[0])
except IndexError:
    pass

import carla

import random
import time


def main():

    client = carla.Client('127.0.0.1', 2000)
    client.set_timeout(2.0)

    world = client.get_world()
    actor_list = world.get_actors()

    for actor in actor_list:
        actor.destroy()
    print('Actors Destroyed.')


if __name__ == '__main__':
    main()