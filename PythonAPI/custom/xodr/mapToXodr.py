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

import random
import time


def main():

    #add argument support here, if necessary

    map_names = ["Town05"]
    client = carla.Client('localhost', 2000)
    client.set_timeout(15.0)
    client.get_world().get_settings().no_rendering_mode = True

    try:
        for map_name in map_names :
            client.load_world(map_name)
            world = client.get_world()
            m = world.get_map()
            xodr_str = m.to_opendrive()
            out_name = map_name + ".xodr"

            f = open("maps/all/"+ out_name, "w+")
            f.write(xodr_str)
            f.close()
            print("Done: " + map_name)


    finally:

        # for actor in actor_list:
        #     actor.destroy()
        print('Done.')


if __name__ == '__main__':
    main()