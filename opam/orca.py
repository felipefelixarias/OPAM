import rvo2
import numpy as np 

class Orca:
      """Simulator for pedestrians using the RVO2 library
      
      Parameters
      ----------
      map
            Binary traversability map of environment
      pix_per_meter
            Number of pixels per meter in the map
      time_step
            Time step for simulation
      nieghbor_dist
            The maximum distance each agent considers to avoid
            collisions with other agents. Must be positve and
            not too small.
      max_neighbors
            The maximum number of other agents each agent takes
            into account in order to avoid collisions. Must be
            positive and not too small.
      time_horizon
            The minimum amount of time for which the velocity of
            each agent is safe with respect to the other agents.
            A longer time horizon will lead to agents that respond
            to the presence of other agents faster but have less
            freedom in choosing their velocities. Must be positive
            and not too small.
      time_horizon_obst
            The minimum amount of time for which the velocity of
            each agent is safe with respect to static obstacles.
            A longer time horizon will lead to agents that respond
            to the presence of obstacles faster but have less
            freedom in choosing their velocities. Must be positive
            and not too small.
      radius
            The radius of each agent. Must be positive.
      max_speed
            The maximum speed of each agent. Must be positive.
      num_agents
            The Number of agents to simulate

      Attributes
      ----------
      map
            See above
      time_step
            See above
      neighbor_dist
            See above
      max_neighbors
            See above
      time_horizon      
            See above
      time_horizon_obst
            See above
      radius
            See above
      max_speed  
            See above
      num_agents
            See above
      agents
            List of agents in the simulation
      obstacles
            List of obstacles in the simulation
      sim   
            RVO2 simulator object

      """
      def __init__(
            self, 
            map: np.ndarray,
            pix_per_meter: float,
            time_step: float = 1/60,
            neighbor_dist: float = 1.5,
            max_neighbors: int = 5,
            time_horizon: float = 1.5,
            time_horizon_obst: float = 2.0,
            radius: float = 0.4,
            max_speed: float = 2.0,
            num_agents: int = 5
            ) -> None:
            self.map = map
            self.time_step = time_step
            self.neighbor_dist = neighbor_dist
            self.max_neighbors = max_neighbors
            self.time_horizon = time_horizon
            self.time_horizon_obst = time_horizon_obst
            self.radius = radius
            self.max_speed = max_speed
            self.num_agents = num_agents
            self.agents = []
            self.obstacles = []


            self.sim = rvo2.PyRVOSimulator(
                  self.time_step,
                  self.neighbor_dist,
                  self.max_neighbors,
                  self.time_horizon,
                  self.time_horizon_obst,
                  self.radius,
                  self.max_speed)

      def process_map(self):
      
            """Process the map into a format that RVO2 can use.
            Finds objects in the map and adds them to the RVO2
            simulator object.
            """

            # Obstacles are also supported.
            o1 = self.sim.addObstacle([(0.1, 0.1), (-0.1, 0.1), (-0.1, -0.1), (-0.1, -0.1)])
            self.sim.processObstacles()

      def get_episode_data(self):
            """Get positions of agents across episode and return
            a list of the positions for each agent at each timestep.

            Returns
            -------
            episode_data
                  List of lists of agent positions at each timestep
            """

            #Assume agents have already been added to the simulator

      def add_agents(self):
            """Add agents to the simulation
            """
            a0 = self.sim.addAgent((0, 0))
            a1 = self.sim.addAgent((1, 0))
            a2 = self.sim.addAgent((1, 1))
            a3 = self.sim.addAgent((0, 1))

            self.agents = [a0, a1, a2, a3]
      

      def recreate_example(self):
            """Recreate the example from the RVO2 library"""
            self.sim.setAgentPrefVelocity(self.agents[0], (1, 1))
            self.sim.setAgentPrefVelocity(self.agents[1], (-1, 1))
            self.sim.setAgentPrefVelocity(self.agents[2], (-1, -1))
            self.sim.setAgentPrefVelocity(self.agents[3], (1, -1))

            print('Simulation has %i agents and %i obstacle vertices in it.' %
                  (self.sim.getNumAgents(), self.sim.getNumObstacleVertices()))

            print('Running simulation')

            for step in range(20):
                  self.sim.doStep()

                  positions = ['(%5.3f, %5.3f)' % self.sim.getAgentPosition(agent_no)
                              for agent_no in self.agents]
                  print('step=%2i  t=%.3f  %s' % (step, self.sim.getGlobalTime(), '  '.join(positions)))


#TODO: Get positions of agents and overlay them on the small_square image.

orca = Orca(map=np.zeros((10,10)), pix_per_meter=10)

orca.recreate_example()