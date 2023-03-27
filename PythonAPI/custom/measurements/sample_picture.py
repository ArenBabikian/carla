import carla
import itertools

def fix_map(client):
    cur_world = client.get_world().get_map().name

    if cur_world != "Town03":
        client.load_world("Town03")
        client = carla.Client('localhost', 2000)
        client.set_timeout(2.0)


def fix_spectator_angle(world):
    loc = carla.Location(x=241.930847, y=36.851646, z=15.790533)
    rot = carla.Rotation(pitch=-54.941986, yaw=160.377472, roll=0.000051)
    world.get_spectator().set_transform(carla.Transform(loc, rot))


def fix_spectator_top(world):
    loc = carla.Location(x=231.176941, y=34.014755, z=20.030090)
    rot = carla.Rotation(pitch=-88.857727, yaw=0.969636, roll=-179.999939)
    world.get_spectator().set_transform(carla.Transform(loc, rot))

def spawn_vehicle(world, color, loc_vehicle):

    bp_vehicle = world.get_blueprint_library().find("vehicle.bmw.grandtourer")
    bp_vehicle.set_attribute("color", color)
    tr_vehicle = world.get_map().get_waypoint(loc_vehicle).transform
    tr_vehicle.location = tr_vehicle.location + carla.Location(0,0,5)
    world.spawn_actor(bp_vehicle, tr_vehicle)

def spawn_pedestrian(world):

    bp_ped = world.get_blueprint_library().find("walker.pedestrian.0001")
    loc_ped = carla.Location(228, 45, 5)
    rot_ped = carla.Rotation(0, 0, 0)

    tr_ped = carla.Transform(loc_ped, rot_ped)
    world.spawn_actor(bp_ped, tr_ped)


def spawn_actors(world):

    #environment vehicle
    color = '127,0,0'
    color = '128,64,0'
    loc = carla.Location(230, 41, 0)
    veh = spawn_vehicle(world, color, loc)

    #ego vehicle
    color = '0,0,127'
    loc = carla.Location(235,35, 0)
    spawn_vehicle(world, color, loc)


def main():
    actors_list = []
    client = carla.Client('localhost', 2000)
    client.set_timeout(3.0)
    world = client.get_world()

    try:
        fix_map(client)
        world.set_weather(getattr(carla.WeatherParameters, 'CloudyNoon'))

        spawn_actors(world)
        spawn_pedestrian(world)
        # spawn_arrows(world) #TODO Implement this
        print("Actors spawned!")
        
        fix_spectator_angle(world)
        # take_snapshot()
        input("Move to TOP view?")

        fix_spectator_top(world)
        # take_snapshot()
        
        input("press ENTER to finish.")
        

    finally:
        vehicles = world.get_actors().filter('vehicle.*')
        pedestrians = world.get_actors().filter('walker.*')
        for actor in itertools.chain(vehicles, pedestrians):
            print(actor)
            actor.destroy()
        print('Actors Destroyed.')





if __name__ == '__main__':
    main()


'Default', 'ClearNoon', 'CloudyNoon', 'WetNoon', 'WetCloudyNoon', 'MidRainyNoon', 'HardRainNoon', 'SoftRainNoon', 'ClearSunset', 'CloudySunset', 'WetSunset', 'WetCloudySunset', 'MidRainSunset', 'HardRainSunset', 'SoftRainSunset'