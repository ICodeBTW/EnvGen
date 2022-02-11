import os.path
import sys
import pandas as pd

def relative_path(folder_path):
    return os.path.relpath(folder_path)


def generate_env_file(folder_path,ITBU,env):
     with open("environment_variables.txt","w") as fp:
        fp.write('FOLDER_PATH="{}"\n'.format(folder_path))
        fp.write('ITBU="{}"\n'.format(ITBU))
        fp.write('ENV="{}"\n'.format(env))

     print("Genration Complete")

def generate_csv_file(data):
    df = pd.DataFrame(data,)
    print(df)
    df.to_csv("assets.csv",index=False, header=False)
