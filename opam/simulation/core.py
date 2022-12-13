import numpy as np

from opam.environment.core import Environment

class Simulator:
    """Parent class for simulators

    Parameters
    ----------
    environment
        Environment object to simulate in

    Attributes
    ----------
    environment
        See above
    """
    def __init__(self, environment: type[Environment]) -> None:
        self.environment = environment

    def step(self) -> None:
        """Simulate one step"""
        raise NotImplementedError

    def reset(self) -> None:
        """Reset the simulation"""
        raise NotImplementedError
