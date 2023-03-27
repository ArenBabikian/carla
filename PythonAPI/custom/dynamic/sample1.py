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
from datetime import datetime


def main():

    #add argument support here, if necessary

    actor_list = []
    client = carla.Client('localhost', 2000)
    client.set_timeout(2.0)
    # print(client.get_available_maps())
    try:

        world = client.get_world()
        map = world.get_map()

        settings = world.get_settings()
        settings.no_rendering_mode = True
        world.apply_settings(settings)

        # xodr_str = map.to_opendrive()
        # dt = datetime.now().strftime("%H-%M-%S")
        # dir_name = "Interface/maps/"
        # out_name = "mapAt" + dt + "-1.xodr"

        # f = open(dir_name + out_name, "a")
        # f.write(xodr_str)
        # f.close()


        #list blueprints that we can use for adding new actors into the simulation.
        veh_bp_lib = world.get_blueprint_library().filter('vehicle')

        #
        # veh_bp = random.choice(veh_bp_lib)
        veh_bp = veh_bp_lib[0]

        # Now we need to give an initial transform to the vehicle. We choose a
        # random transform from the list of recommended spawn points of the map.
        sp1 = world.get_map().get_spawn_points()[0]
        # print([sp1.location.x, sp1.location.y, sp1.location.z])
        # print([sp1.rotation.pitch, sp1.rotation.yaw, sp1.rotation.roll])

        #[-6.446169853210449, -79.05502319335938, 1.842996597290039]
        # l1 = carla.Location(sp1.location.x, sp1.location.y, sp1.location.z)
        l1 = carla.Location(-10, -75, 2)
        r1 = carla.Rotation(0.0, 90.0, 0.0)
        # tr1 = carla.Transform(l1, r1)
        tr1 = map.get_waypoint(l1).transform

        l2 = carla.Location(00, sp1.location.y, sp1.location.z)
        r2 = carla.Rotation(0.0, 90.0, 0.0)
        tr2 = carla.Transform(l2, r2)
        # tr2 = map.get_waypoint(l2).transform



        # So let's tell the world to spawn the vehicle.
        veh1 = world.spawn_actor(veh_bp, tr1)
        actor_list.append(veh1)
        veh2 = world.spawn_actor(veh_bp, tr2)
        actor_list.append(veh2)

        # out_name = "mapAt" + dt + "-2.xodr"
        # f = open(dir_name + out_name, "a")
        # f.write(xodr_str)
        # f.close()

        print('created 2 vehicles')

        

        veh1.set_autopilot(True)
        veh2.set_autopilot(True)

        # out_name = "mapAt" + dt + "-3.xodr"
        # f = open(dir_name + out_name, "a")
        # f.write(xodr_str)
        # f.close()

        # # Let's add now a "depth" camera attached to the vehicle. Note that the
        # # transform we give here is now relative to the vehicle.
        # camera_bp = blueprint_library.find('sensor.camera.depth')
        # camera_transform = carla.Transform(carla.Location(x=1.5, z=2.4))
        # camera = world.spawn_actor(camera_bp, camera_transform, attach_to=vehicle)
        # actor_list.append(camera)
        # print('created %s' % camera.type_id)

        # # Now we register the function that will be called each time the sensor
        # # receives an image. In this example we are saving the image to disk
        # # converting the pixels to gray-scale.
        # cc = carla.ColorConverter.LogarithmicDepth
        # camera.listen(lambda image: image.save_to_disk('_out/%06d.png' % image.frame_number, cc))

        # # Oh wait, I don't like the location we gave to the vehicle, I'm going
        # # to move it a bit forward.
        # location = vehicle.get_location()
        # location.x += 40
        # vehicle.set_location(location)
        # print('moved vehicle to %s' % location)

        # # But the city now is probably quite empty, let's add a few more
        # # vehicles.
        # transform.location += carla.Location(x=40, y=-3.2)
        # transform.rotation.yaw = -180.0
        # for _ in range(0, 10):
        #     transform.location.x += 8.0

        #     bp = random.choice(blueprint_library.filter('vehicle'))

        #     # This time we are using try_spawn_actor. If the spot is already
        #     # occupied by another object, the function will return None.
        #     npc = world.try_spawn_actor(bp, transform)
        #     if npc is not None:
        #         actor_list.append(npc)
        #         npc.set_autopilot()
        #         print('created %s' % npc.type_id)

        x = input("Press Enter to destroy actors.")
        print(x)

    finally:

        for actor in actor_list:
            actor.destroy()
        print('Actors Destroyed.')


if __name__ == '__main__':
    main()