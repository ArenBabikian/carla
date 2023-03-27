import argparse
import os
import subprocess
from pathlib import Path

# import carla



def main():
    # print("hi")
    os.environ["PYTHONPATH"] = ""
    print(os.environ["PYTHONPATH"])
    # import carla
    # print(carla.Client('localhost', 2000))

    argparser = argparse.ArgumentParser(description=__doc__)

    argparser.add_argument(
        '-v', '--version',
        metavar='A',
        default='0.9.13',
        help='path to openscenario')
    argparser.add_argument(
        '-lq', '--low-quality',
        action='store_true',
        help='worst quality')
    argparser.add_argument(
        '--fps',
        metavar='A',
        default='normal',
        help='fps')
    args = argparser.parse_args()

    directory = Path().home().parent.parent / "Applications" / "CARLA_{}".format(args.version) / "WindowsNoEditor"
    dir_str = str(directory)

    # file_dir = Path(__file__).parent.resolve()
    # ini_path = file_dir / "CarlaSettings.ini"
    # settings_path = "-carla-settings=\"{}\"".format(str(ini_path))

    print("cd {}".format(dir_str))
    os.chdir(dir_str)

    cmd = ["CarlaUE4.exe"]
    if args.fps == 'low':
        cmd.append("-fps=20")
    if args.low_quality:
        cmd.append("-quality-level=Low")
    
    print(*cmd)
    subprocess.run(cmd, check=False)


if __name__ == '__main__':
    main()
