import numpy as np
from math import ceil, isnan
from PIL import Image
from typing import Any, DefaultDict, Dict, List, NamedTuple, Optional, Set, Tuple, Union
import logging

from utils.annotation import make_gaussian, make_gaussian, bresenham_line


class Map:
    """Class containing all information relevant to a single environment

    Parameters
    ----------
    env_name
        Name of the environment
    map
        Binary map of the environment
    pix_per_meter
        Number of pixels per meter
    agent_radius
        Radius of the agents in meters
    obstacle
        Value of the obstacle pixels in the map
    free
        Value of the free pixels in the map

    Attributes
    ----------
    env_name
        See above
    map
        See above
    pix_per_meter
        See above
    agent_radius
        Radius of the agents in pixels
    obstacle
        See above
    free
        See above
    map_size
        Size of the map in pixels
    episodes
        List of episodes for the environment
    visitation_counts
        Number of times each pixel has been visited based 
        on episode data
    predicted_occupancy
        Dictionary where the keys are the model names
        and the values are the predicted occupancy maps
    _max_agent_radius 
        Maximum radius of the agents in pixels
    _min_agent_radius
        Minimum radius of the agents in pixels
    _agent_diameter  
        Diameter of the agents in pixels
    _agent_mask
        Array defining the shape of the agent
    """

    def __init__(self, 
        env_name: str,
        map: np.ndarray, 
        pix_per_meter: int = 10, 
        agent_radius: float = 1.5,
        obstacle: int = 0,
        free: int = 1
        )-> None:

        self.env_name = env_name
        self.map = np.asarray(map)
        self.pix_per_meter = pix_per_meter
        self.agent_radius = agent_radius*(pix_per_meter/10)
        self.obstacle = obstacle
        self.free = free
        self.map_size = self.map.shape
        self.episodes = None
        self.visitation_counts = np.zeros(self.map.shape)
        self.predicted_occupancy = {}
        self._max_agent_radius = ceil(self.agent_radius)
        self._min_agent_radius = round(self.agent_radius)
        self._agent_diameter = self._max_agent_radius + self._min_agent_radius
        self._agent_mask = np.rint(make_gaussian(self._agent_diameter, fwhm=self._agent_diameter))

    def compute_visitation_counts(self)-> None:
        """Compute the number of times each pixel has been visited by the agents"""
        logging.debug('Computing visitation counts for '+self.env_name+"...")
        if self.episodes:
            for paths in self.episodes:
                self._check_path_lengths(paths)
                for path in paths:
                    pixel_path = self._raytrace_path(path)
                    swept_area = self._swept_area(pixel_path)
                    self.visitation_counts += swept_area

    def _swept_area(self, path: List[List[float]])-> np.ndarray:
        """Compute the swept area of the agent for a given path
        
        Parameters
        ----------
        path
            List of pixel positions of the agent
            
        Returns
        -------
        np.ndarray
            Array of the same size as the map, where the each pixel visited
            by the agent is set to 1, and the rest are set to 0
        """
        logging.debug('Computing swept area for '+self.env_name+"...")
        swept_area = np.zeros(self.map.shape)

        if self._is_path_valid(path):
            for pos in path:
                min_col = pos[1] - self._max_agent_radius
                max_col = pos[1] + self._min_agent_radius
                min_row = pos[0] - self._max_agent_radius
                max_row = pos[0] + self._min_agent_radius
                swept_area[min_row:max_row, min_col:max_col] += self._agent_mask

        return (swept_area>0).astype(int)

    def _is_path_valid(self, path: List[List[float]])-> bool:
        """Check if a path goes through obstacles

        Parameters
        ----------
            path
                List of pixel positions of the agent
        
        Returns
        -------
            bool
                True if the path is valid, False otherwise
        """
        for pos in path:
            if self.map[pos[0], pos[1]] == self.obstacle:
                return False
        return True

    def _check_path_lengths(self, paths: List[List[List[float]]])-> None:
        """Check if the paths are of the same length

        Parameters
        ----------
            paths
                List of paths for the agents

        Raises
        ------
            ValueError 
                If the paths are not of the same length
        """
        it = iter(paths)
        path_len = len(next(it))
        if not all(len(p) == path_len for p in it):
            raise ValueError('Paths of varying lengths')

    def _path_world_to_pixel(self, path: List[List[float]])-> List[List[float]]:
        """Convert a path from world coordinates to pixel coordinates.
        
        Parameters
        ----------
            path
                List of agent positions in world coordinates
            
        Returns
        -------
            List[List[float]]  
                List of agent positions in pixel coordinates
        """
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

    def _raytrace_path(self, path: List[List[float]])-> List[List[float]]:
        """Raytrace a path to find all the pixels visited by the agent.

        Parameters 
        ----------
            path
                List of agent positions in world coordinates
        
        Returns
        -------
            List[List[float]]
                List of all agent positions in pixel coordinates
        """
        coarse_pixel_path = self._path_world_to_pixel(path)
        pixel_path = []

        for i in range(1, len(coarse_pixel_path)):
            prev_pixel = np.asarray([coarse_pixel_path[i-1]])
            next_pixel = np.asarray([coarse_pixel_path[i]])
            pixel_path.extend(bresenham_line(prev_pixel, next_pixel, -1))

        return pixel_path

    def display_map(self)-> None:
        """Display the map"""
        im = np.asarray(self.map)
        im = im / np.max(im)
        im *= 255
        
        image = Image.fromarray(im.astype(np.uint8))
        image.show()

    def display_visitation_counts(self)-> None:
        """Display the visitation counts"""
        im = np.copy(self.map) 
        normalized_vis_counts = self.visitation_counts / np.max(self.visitation_counts)
        im[self.visitation_counts>0] = normalized_vis_counts[self.visitation_counts>0]*255
        image = Image.fromarray(im.astype(np.uint8))
        image.show()   

    def display_occupancy_predictions(self, model_name: str)-> None:
        """Display the occupancy predictions of the model

        Parameters
        ----------
            model_name
                Name of the model used to predict occupancy
        """
        im = np.copy(self.map) 
        preds = self.predicted_occupancy[model_name]
        normalized_vis_counts = preds / np.max(preds)
        im[preds>0] = normalized_vis_counts[preds>0]*255
        image = Image.fromarray(im.astype(np.uint8))
        image.show()   

    def get_segmentation_mask(self, 
        num_classes: int, 
        class_distribution: List[float]
        )-> np.ndarray:
        """Get the segmentation mask of the map based on the visitation counts.
        
        Parameters
        ----------
            num_classes
                Number of classes in the segmentation mask
            class_distribution
                List defininng the distribution of the classes in 
                the segmentation mask."""

        #TODO: Check class_distribution is valid (non-negative, sum to 1)
        #TODO: Check num_classes is valid (>= 2)
        #TODO: Check visitation_counts is not empty
        #TODO: Check num_classes == len(class_distribution)
        pass
    


