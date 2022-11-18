import numpy as np
from json import load, dump
from os import listdir
from PIL import Image

from map import Map

class Core:
    def __init__(self):
        self.maps = {}
        self.episodes = {}
        self.images = {}
        self.model = None
        self.distilled_model = None
        self.labels = None
        self.features = None

    def load_maps(self, map_path, pix_per_meter=10):

        for map_name in listdir(map_path):
            map = Image.open(map_path + map_name)
            map = np.asarray(map)
            self.maps[map_name[:-4]] = Map(map_name[:-4], map, pix_per_meter)

    def load_episodes(self, episodes_path):

        for map_name in self.maps.keys():
            found_episode = False
            for episode_file_name in listdir(episodes_path):
                if episode_file_name.startswith(map_name):
                    found_episode = True
                    file = open(episodes_path + episode_file_name, 'r')
                    ep_list = self.process_episodes(file)
                    self.maps[map_name].episodes = ep_list
            if not found_episode:
                print('No episode found for map: ' + map_name)

    def process_episodes(self, file):
        episodes = load(file)
        ep_list =[]

        for episode in episodes['episodes']:
            ped_list = []
            for ped in episode['pedestrians']:
                # path = np.asarray(ped['path'])
                ped_list.append(ped['path'])
            ep_list.append(ped_list)
        
        self.episodes[file.name[:-5]] = ep_list

        return ep_list