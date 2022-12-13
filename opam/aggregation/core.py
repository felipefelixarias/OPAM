import numpy as np
from json import load, dump
from os import listdir
from typing import Any, DefaultDict, Dict, List, NamedTuple, Optional, Set, Tuple, Union, BinaryIO
from PIL import Image

from opam.environment import Environment
from opam.simulation.orca import Orca

class Aggregator:
    def __init__(self):
        """Class for annotating multiple maps, loading/simulating episodes
        and generating training data for machine learning models.
        
        Attributes
        ----------
        maps
            Dictionary of maps, where the key is the map name and the value 
            is the Map object
        episodes
            Dictionary of episodes, where the key is the map name and the 
            value is a list of episodes for that map
        images
            Dictionary of images, where the key is the map name and the value
            is a a dictionary of images for that map, where the key is the
            image name and the value is the image
        models
            Dictionary of models, where the key is the model name and the value
            is the model object
        self.labels
            Dictionary of labels, where the key is the name of the model the 
            labels are for and the value is a list of labels
        self.features
            Dictionary of features, where the key is the name of the model the
            features are for and the value is a list of features       
        """
        self.maps = {}
        self.episodes = {}
        self.images = {}
        self.models = {}
        self.labels = {}
        self.features = {}

    def load_maps(self, 
        map_path: str, 
        pix_per_meter: int = 10
        )-> None:
        """Load maps from the map_path directory.
        
        Parameters
        ----------
        map_path
            Path to the directory containing the maps
        pix_per_meter
            Number of pixels per meter in the maps
        
        """

        for map_name in listdir(map_path):
            map = Image.open(map_path + map_name)
            map = np.asarray(map)
            self.maps[map_name[:-4]] = Environment(map_name[:-4], map, pix_per_meter)

    def load_episodes(self, 
        episodes_path: str, 
        num_episodes: int = 1
        )-> None:
        """Load episodes from the episodes_path directory.

        Parameters
        ---------- 
        episodes_path
            Path to the directory containing the episodes
        num_episodes
            Number of episodes to load from each file
        """
        for map_name in self.maps.keys():
            found_episode = False
            for episode_file_name in listdir(episodes_path):
                if episode_file_name.startswith(map_name):
                    found_episode = True
                    file = open(episodes_path + episode_file_name, 'r')
                    ep_list = self._process_episodes(file, num_episodes)
                    self.maps[map_name].episodes = ep_list
                    self.episodes[map_name] = ep_list
                    print("Loaded " + str(len(ep_list)) + " episodes for " + map_name)
        
            if not found_episode:
                print('No episode found for map: ' + map_name)

    def _process_episodes(self, 
        file: BinaryIO, 
        num_episodes: int
        ) -> List[List[List[float]]]:
        """Process the episode file and return a list of episodes.

        Parameters
        ----------
        file
            File object to read the episode data from
        num_episodes
            Number of episodes to save from the file

        Returns
        -------
        List[List[float]]   
            List of episodes
        """

        episodes = load(file)
        ep_list =[]

        if num_episodes == 0:
            num_episodes = len(episodes['episodes'])

        for i, episode in enumerate(episodes['episodes']):
            if i >= num_episodes:
                break
            ped_list = []
            for ped in episode['pedestrians']:
                ped_list.append(ped['path'])
            ep_list.append(ped_list)
        
        return ep_list

    #TODO: Add code to simulate episodes over the maps, this may only be useful 
    # for users that don't have data and adds the orca dependency
    def simulate_episodes(
        self, 
        num_episodes: int, 
        map_name: str, 
        **kwargs: dict
        ) -> None:
        """Simulate episodes over a map and save the data to a the episodes dictionary.
        
        Parameters
        ----------
        num_episodes
            Number of episodes to simulate.
        map_name
            Name of the map to simulate episodes over.
        **kwargs
            Keyword arguments to pass to the ORCA class.
        """

        orca = orca(self.maps[map_name].map, self.maps[map_name].pix_per_meter, **kwargs)
        orca.process_map()
        orca.add_agents()
        self.episodes[map_name] = orca.get_episode_data()
        