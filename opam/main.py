import numpy as np
from os import getcwd
import logging

from opam.map import Map
from opam.core import Core

if __name__ == '__main__':
    #Generate map objest

    logging.basicConfig(level=logging.DEBUG)
    core = Core()

    map_path = getcwd() + '/data/maps/'
    core.load_maps(map_path, pix_per_meter=100)
    episode_path = getcwd() + '/data/episodes/'
    core.load_episodes(episode_path, 3)

    test_map = core.maps.popitem()[1]
    test_map.compute_visitation_counts()
    # test_map.display_map()
    test_map.display_visitation_counts()