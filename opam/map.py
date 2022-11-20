import numpy as np
from math import ceil, isnan
from PIL import Image
from utils.annotation import make_gaussian, make_gaussian, bresenham_line


class Map:

    def __init__(self, env_name, map, pix_per_meter=10, agent_radius=1.5):
        self.env_name = env_name
        self.map_size = map.shape
        self.pix_per_meter = pix_per_meter
        self.agent_radius = agent_radius*(pix_per_meter/10)
        self.map = np.asarray(map)
        self.episodes = None
        self.visitation_counts = np.zeros(self.map.shape)
        self.predicted_occupancy = np.zeros(self.map.shape)
        self.distilled_predicted_occupancy = np.zeros(self.map.shape)
        #Assume map is binary, where 1 is free space and 0 is obstacle
        self.obstacle = 0
        self.free = 1
        self.max_agent_radius = ceil(self.agent_radius)
        self.min_agent_radius = round(self.agent_radius)
        self.agent_diameter = self.max_agent_radius + self.min_agent_radius
        self.agent_mask = np.rint(make_gaussian(self.agent_diameter, fwhm=self.agent_diameter))

    def compute_visitation_counts(self):
        #Assume episodes is of shape (Num Eps, Num Agents, Length of Ep)
        for paths in self.episodes:
            self.check_path_lengths(paths)
            for path in paths:
                pixel_path = self.raytrace_path(path)
                swept_area = self.swept_area(pixel_path)
                self.visitation_counts += swept_area

    def swept_area(self, path):
        swept_area = np.zeros(self.map.shape)

        if self.is_path_valid(path):
            for pos in path:
                min_col = pos[1] - self.max_agent_radius
                max_col = pos[1] + self.min_agent_radius
                min_row = pos[0] - self.max_agent_radius
                max_row = pos[0] + self.min_agent_radius
                swept_area[min_row:max_row, min_col:max_col] += self.agent_mask

        return (swept_area>0).astype(int)

    def is_path_valid(self, path):
        for pos in path:
            if self.map[pos[0], pos[1]] == self.obstacle:
                return False
        return True

    def check_path_lengths(self, paths):
        it = iter(paths)
        path_len = len(next(it))
        if not all(len(p) == path_len for p in it):
            raise ValueError('Paths of varying lengths')

    def path_world_to_pixel(self, path):
        #Assume center of map is at (0,0)
        offset_x = self.map.shape[1]//2
        offset_y = self.map.shape[0]//2
        pixel_path = []

        for pos in path:
            if isnan(pos[0]) or isnan(pos[1]):
                continue
            x_pos = offset_x + round(pos[0]*self.pix_per_meter)
            y_pos = offset_y + round(pos[1]*self.pix_per_meter)
            pixel_path.append([y_pos, x_pos])

        return pixel_path

    def raytrace_path(self, path):
        coarse_pixel_path = self.path_world_to_pixel(path)
        pixel_path = []

        for i in range(1, len(coarse_pixel_path)):
            prev_pixel = np.asarray([coarse_pixel_path[i-1]])
            next_pixel = np.asarray([coarse_pixel_path[i]])
            pixel_path.extend(bresenham_line(prev_pixel, next_pixel, -1))

        return pixel_path

    def display_map(self):
        im = np.asarray(self.map)
        im = im / np.max(im)
        im *= 255
        
        image = Image.fromarray(im.astype(np.uint8))
        image.show()

    def display_visitation_counts(self):
        im = np.copy(self.map) 
        normalized_vis_counts = self.visitation_counts / np.max(self.visitation_counts)
        im[self.visitation_counts>0] = normalized_vis_counts[self.visitation_counts>0]*255
        image = Image.fromarray(im.astype(np.uint8))
        image.show()   

    def display_criticality_image(self):
        pass

    def get_segmentation_mask(self):
        pass
    


