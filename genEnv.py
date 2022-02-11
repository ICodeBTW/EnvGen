import os.path
import sys


def relative_path(folder_path):
    return os.path.relpath(folder_path)


def generate_env_file(folder_path,ITBU,env):
     with open("environment_variables.txt","w") as fp:
        fp.write('FOLDER_PATH="{}"\n'.format(folder_path))
        fp.write('ITBU="{}"\n'.format(ITBU))
        fp.write('ENV="{}"\n'.format(env))

     print("Genration Complete")

