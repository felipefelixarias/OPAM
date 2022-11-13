import numpy as np
from opam import Map

env_names = ['empty', 'simple', 'complex']

if __name__ == '__main__':
    #Generate map objest
    for env_name in env_names:
        print('Generating map object for environment: ' + env_name)
