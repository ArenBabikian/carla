import glob
import os
import sys

try:
    sys.path.append(glob.glob('../carla/dist/carla-*%d.%d-%s.egg' % (
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

    actor_list = []
    client = carla.Client('localhost', 2000)
    client.set_timeout(5.0)
    try:

        world = client.get_world()
        settings = carla.WorldSettings(synchronous_mode=False)
        print(world.get_settings())
        world.apply_settings(settings)
        print(world.get_settings())

        spectator = world.get_spectator()
        

        map = world.get_map()
        #list blueprints that we can use for adding new actors into the simulation.
        veh_bp_lib = world.get_blueprint_library().filter('vehicle')

        #
        # veh_bp = random.choice(veh_bp_lib)
        veh_bp = veh_bp_lib[0]

        # Now we need to give an initial transform to the vehicle. We choose a
        # random transform from the list of recommended spawn points of the map.
        sp1 = map.get_spawn_points()[0]
        # print([sp1.location.x, sp1.location.y, sp1.location.z])
        # print([sp1.rotation.pitch, sp1.rotation.yaw, sp1.rotation.roll])

        #[-6.446169853210449, -79.05502319335938, 1.842996597290039]
        # l1 = carla.Location(sp1.location.x, sp1.location.y, sp1.location.z)
        l1 = carla.Location(-10, -75, 2)
        r1 = carla.Rotation(0.0, 90.0, 0.0)
        # tr1 = carla.Transform(l1, r1)
        tr1 = map.get_waypoint(l1).transform

        veh1 = world.try_spawn_actor(veh_bp, tr1)
        print(veh1)
        actor_list.append(veh1)


        world.tick()
        world_snapshot = world.wait_for_tick()
        print(world_snapshot)
        actor_snapshot = world_snapshot.find(veh1.id)

        # Set spectator at given transform (vehicle transform)
        spectator.set_transform(actor_snapshot.get_transform())

        veh1.set_autopilot(True)

        print('created 1 vehicle')

        x = input("Press Enter to destroy actors.")
        print(x)

    finally:

        for actor in actor_list:
            actor.destroy()
        print('Actors Destroyed.')


if __name__ == '__main__':
    main()