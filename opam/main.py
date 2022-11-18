import numpy as np
from os import getcwd

from map import Map
from core import Core

if __name__ == '__main__':
    #Generate map objest

    core = Core()

    map_path = getcwd() + '/data/maps/'
    core.load_maps(map_path)
    episode_path = getcwd() + '/data/episodes/'
    core.load_episodes(episode_path)

    test_map = core.maps.popitem()[1]
    test_map.display_map()