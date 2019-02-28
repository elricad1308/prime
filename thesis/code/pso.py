#!/usr/bin/env python3

"""Implements the PSO algorithm.

This module implements a simple version of the PSO algorithm, as
proposed by Kennedy & Eberhart (1995).

Attributes:
  DESIRED_MINIMUM (float): The stop condition of the algorithm. The
    execution will continue until the output value is lesser than this
    value.
  GLOBAL_CONSTANT (float): A constant that indicates how much
    a particle is influenced by the results found by the best particle
    in the population (the 'leader'). Lesser values will result in
    individualistic particles that ignore the leader. Greater values
    will result in highly influenced particles that follow the leader
    closely.
  INDIVIDUAL_CONSTANT (float): A constant that indicates how
    much a particle takes into consideration its previous performances.
    Lesser values will result in memory-less particles that forget
    their previous results. Greater values will result in consistent
    particles that keep their performance constant.
  INERTIA_WEIGHT (float): The weight of a particle. As the name
    suggests, it is the 'friction' of the particles that prevents them
    from moving too fast.
  ITERATIONS (int): The number of iterations that the algorithm will
    perform before it stops.
  PARTICLE_SIZE (int): The magnitude of this particle i.e. the number
    of values that the particle contains. For example, the number of
    variables in a multiple-variable function, or the number of cities
    in a TSP problem.
  POPULATION_SIZE (int): The number of particles used by the algorithm.
    Each particle will move through the search space looking for a
    feasible solution.
  VELOCITY_MAX (float): The maximum speed at which a particle can move.
    This parameter is used as a 'speed limit' that particles cannot
    exceed.
"""

import copy
import math
import random
import sys
import threading
import time

import algorithms
import datastructures
import rython

DESIRED_MINIMUM = 3
GLOBAL_CONSTANT = 7.0 # 5.0
INDIVIDUAL_CONSTANT = 3.0 # 5.0
INERTIA_WEIGHT = 2.50 # 0.75
ITERATIONS = 10 # 50
PARTICLE_SIZE = 2
POPULATION_SIZE = 25 # 5
VELOCITY_MAX = 0.50 # 1.0

class Particle(object):
    """Implement a Particle.
    
    Particles are the core units in the PSO algorithm: they are simple
    entities with no knowledge of the problem they are 'solving': they
    just move around their search space. The interaction between
    individual particles as a whole its what leads to the emergence of
    'intelligent' behaviour.
    
    Attributes:
      best_fitness (float): the fitness value achieved by the Particle
        when it found its best values. It is stored so that it doesn't
        need to be computed again.
      current_fitness (float): the fitness value achieved by the 
        Particle with its current set of values.
      graph (GRAPH): the graph to be colored by the Particle.
      particle_id (int): the unique identifier of the particle.
      personal_best (list of float): the list used to store the best
        values achieved by the particle.
      size (int): the number of values stored in every particle.
      sync (boolean): a flag used to synchronize particles in parallel
        execution.
      values (list of float): the list used to store the current values
        of the particle.
      velocities (list of float): the list of the velocities used to
        move the particle.
      MAX_VALUE (float): The lower bound for the particles' values.
        Together with MIN_VALUE delimits the search space in which
        the particles will move.
      MIN_VALUE (float): The upper bound for the particles' values.
        Together with MAX_VALUE delimits the search space in which
        the particles will move.
    """    
    MAX_VALUE = 5.0
    MIN_VALUE = 0.0
    
    def __init__(self, particle_id, size):
        """Create a new, particle.
        
        All particles have a list for their values and velocities.
        Additionaly, a list called 'personalBest' is used for keep the
        record of the best performance of the particle so far. Also,
        since the fitness computation represents the main load in
        computational cost for evolutionary algorithms [Eiben &
        Schoenauer, 2002], we use two variables called 'currentFitness'
        and 'bestFitness' to keep the values for the current and best
        iterations, respectively.
        
        Args:
          particle_id (int): The unique identifier for this particle.
            This is usually the index of the particle within the
            structure that stores the particles in the algorithm.
          size (int): The magnitude of this particle i.e. the number
            of values that the particle contains. For example, the
            number of variables in a multiple-variable function, or
            the number of cities in a TSP problem.
        """
        self.values = list()
        self.velocities = list()
        self.personal_best = list()
        
        self.particle_id = particle_id
        self.size = size
        self.graph = None
        self.best_coloring = None
        self.sync = False
                
        # Initializes the fitness as an arbitrary bad value. 
        self.best_fitness = -(2**63)
        self.current_fitness = self.best_fitness
        
        # Initialise values to random numbers within the range.
        for index in range(self.size):
            self.values.append(random.uniform(
              Particle.MIN_VALUE, Particle.MAX_VALUE)
            )
            self.velocities.append(0);
        
        # Since there is no previous values, the current value is the best
        self.personal_best = self.values[:]
    
    def __repr__(self):
        """Get a JSON representation of the particle.
        
        Returns:
          str: a JSON string containing all the relevent information
            of the particle.
        """
        ids = '"particle_id":' + str(self.particle_id)        
        sizes = '"size":' + str(self.size)
        
        curfit = '"current_fitness":' + str(self.current_fitness)
        str_vals = ",".join([str(v) for v in self.values])
        vals = '"values":[' + str_vals + ']'
        
        besfit = '"best_fitness":' + str(self.best_fitness)
        str_bests = ",".join([str(b) for b in self.personal_best])
        bests = '"personal_best":[' + str_bests + ']'
        
        str_vels = ",".join([str(vl) for vl in self.velocities])
        vels = '"velocities":[' + str_vels + ']'
        
        return '{' + ",".join(
            [ids, sizes, curfit, vals, besfit, bests, vels]) +'}'
    
    def calculate_velocity(self, globalBest):
        """Calculate the new velocity for this particle.
        
        The velocity of a particle determines how 'fast' a particle
        moves through its search space. Velocities are simply numbers
        that are added (or substraced) from the particle's values. The
        velocities are calculated using a formula that determines the
        level of influence that the leader exert over this particle, 
        as well as its previous performances.
        
        Args:
          globalBest (lisf of float): the current values of the leader.      
        """
        self.sync = False
        
        for index in range(self.size):
            # The formula is composed of 3 terms
            term1 = INERTIA_WEIGHT * self.velocities[index]
            
            term2 = (
              INDIVIDUAL_CONSTANT * random.uniform(0, 1) *
              (self.personal_best[index] - self.values[index])
            )
            
            term3 = (
              GLOBAL_CONSTANT * random.uniform(0, 1) *
              (globalBest[index] - self.values[index])
            )
            
            newVelocity = term1 + term2 + term3
            
            # Adjust the velocity so it doesn't exceed the maximum allowed            
            if newVelocity < 0:
                self.velocities[index] = -(newVelocity % VELOCITY_MAX)
            else:
                self.velocities[index] = newVelocity % VELOCITY_MAX

    def evaluate_fitness(self):
        """Evaluate the fitness for this particle.
        
        In a numerical particle. the fitness is usually the evaluation
        of some function, which depends of the problem to solve. You
        can change the content of this method to fit your needs.
        """
        fitness = 0.0
        # TO-DO: Write your fitness evaluation code here:
        
        if self.graph is not None:
            try:
                fitness = 1.0 / algorithms.sdr_widgerson(
                  self.graph, self.values[0], self.values[1]
                )
            except RuntimeError:
                fitness = 1 / (2 ** 63)
        else:
            raise RuntimeError("Particle graph has not been set!")
            
        # END TO-DO
        self.current_fitness = fitness
        
        # Check if we've got a better result
        if fitness > self.best_fitness:
            # Update the best performance accordingly
            self.best_fitness = fitness
            self.personal_best = self.values[:]
            self.best_coloring = copy.deepcopy(self.graph)
            
        self.sync = True
    
    def move(self):
        """Move the particle.
        
        In a numerical particle, movement is determined by the
        velocities vector by adding it to the values vector. Since
        velocities is a vector, it also determines the direction the
        particle will follow.        
        """
        for index in range(self.size):
            self.values[index] = self.values[index] + self.velocities[index]
            
            # Adjust values to keep particle inside boundaries.
            if self.values[index] < Particle.MIN_VALUE:
                self.values[index] = (-self.values[index] % Particle.MAX_VALUE)
            elif self.values[index] > Particle.MAX_VALUE:
                self.values[index] = (self.values[index] % Particle.MAX_VALUE)


class PSO(object):
    """Implement the PSO algorithm, as proposed by Kennedy and Eberhart
    in 1995.
    
    PSO (Particle Swarm Optimization) is a meta-heuristic inspered by
    the choreography of a bird flock, in which a set of entities called
    'particles' (a 'swarm') performs multidimensional search. The 
    particles of the swarm do not posses any kind of problem-solving 
    skills: they just move around the search space; its the interaction
    between them which eventually leads to the emergence of 
    'intelligent' behaviour.
    
    Attributes:
      iteration (int): the current iteration of the algorithm.
      leader (int): the index used to identify the current leader.
      population (list of Particle): the population of particles used
        by the algorithm.
    """
    
    def __init__(self, graph):
        """Initialize the structure of the algorithm.
        
        The population is stored in a list called 'population', which
        is filled with randomly-created particles. Then we proceed to
        look for the leader.
        
        Args:
          graph (GRAPH): the GRAPH datastructure that the swarm will
            attempt to color.
        """
        self.population = list()
        self.leader = -1
        self.iteration = 0
        
        for index in range(POPULATION_SIZE):
            p = Particle(index, PARTICLE_SIZE)
            p.graph = copy.deepcopy(graph)
            self.population.append(p)
        
        self.find_leader()
    
    def concurrent_run(self, particle):
        """Allows particles to work in parallel.
        
        This method allows particles to find their leader, calculate
        their velocities, move themselves, and evaluate the objective
        function in parallel.
        
        Args:
          particle (Particle): the particle that will execute its
          evaluation method.
        """        
        # Store the leader values.
        leader_vals = self.population[self.leader].values[:]
        
        # Calculate velocity and move the particle
        particle.calculate_velocity(leader_vals)
        particle.move()
        particle.evaluate_fitness()
    
    def create_log_entry(self, i):
        """Create a log entry record.
        
        Log entries are designed to be writed to a CSV file, therefore
        the lines produced by this method will have the following
        structure:
        
        iteration, best, worst, mean, std
        
        Args:
          i (int): The current iteration. It will figure as the first
            first element in every row.
            
        Returns:
          str: a string with the statistical information about the
            current iteration.
        """        
        fitness_vector = self.get_fitness_vector()
        
        best = min(fitness_vector)
        worst = max(fitness_vector)
        mean = rython.mean(fitness_vector)
        std = rython.std(fitness_vector)
        
        return "{0},{1},{2},{3},{4}\n".format(i, 1.0/best, 1.0/worst, 1.0/mean, std)
    
    def find_leader(self):
        """Iterate over all the swarm to find the leader.
        
        The leader of a swarm is the particle with the highest fitness.
        """
        # Initialize the leader fitness as an arbitrarly bad value
        leaderFitness = -(2**63)
        
        for number in range(POPULATION_SIZE):
            if self.population[number].current_fitness > leaderFitness:
                leaderFitness = self.population[number].current_fitness
                self.leader = number
       
    def get_fitness_vector(self):
        """Get the fitness of all particles in the swarm.
        
        This method will create a new list that contains the fitness
        for all the particles in the population. The list then can be
        used to perform statistical tests using the library 'rython'.
        
        Returns:
          list of float: a list storing the fitness values of all the
            particles in the swarm.
        """
        vector = list()
        
        for particle in self.population:            
            vector.append(particle.current_fitness)
            
        return vector
    
    def is_synchronized(self):
        """Determine if the algorithm is synchronized.
        
        In order to choose the leader, all particles must be 
        synchronized. This method checks the flags for all the 
        particles and act as as a redezvous barrier.
        
        Returns:
          bool: True if and only if all particles are synchronized.
            False otherwise.
        """
        sync_state = True
        
        for particle in self.population:
            sync_state = (sync_state and particle.sync)
            
            if not sync_state:
                break;
            
        return sync_state
    
    def print_leader(self):
        """Print the information for the best particle found so far.
        
        Returns:
          str: the information of the leader.
        """
        return "Best particle found:\n{0}".format(
            repr(self.population[self.leader]))
    
    def run(self, seed=None, csv_file=None, json_file=None):
        """Execute the algorithm.
        
        This method will iterate the algorithm, making all the steps
        necessary automatically. There is no need to do anything else.
        
        Attributes:
          seed (int, optional): The seed for the pseudo-random number
            generator. If not given, system's current time will be used
            as seed. Defaults to None.
          csv_file (String, optional): the name of the output file that
            will save the results of the experiment. If given,it must
            include extension. If not given, the output will not be
            saved. Defaults to None.
          json_file (String, optional): the name of the output file
            that will save the resulting coloring of the experiment. If
            given, it must include extension. If not given, the
            resulting coloring will not be saved. Defaults to None.
        """
        start = time.time()
        
        # Sets seed (if not provided).
        if seed is None:
            seed = int(start)
        
        random.seed(seed)
        
        # Appends the CSV file 'header' and initial values
        if csv_file is not None:
            # This list will store each iteration's result.
            output = list()
            output.append("iteration,best,worst,mean,std\n")
            output.append(self.create_log_entry(0))
        
        for iteration in range(ITERATIONS):
            self.iteration += 1
            printer("Iteration [{0} / {1}] completed.".format(
                iteration, ITERATIONS))
            
            for particle in self.population:                
                # Launch a new thread to move particles in parallel
                t = threading.Thread(
                    target=self.concurrent_run, args=(particle,))
                t.start()
                
            # Waits until all particles are synchronized
            while not self.is_synchronized():
                pass
                
            # Find new leader
            self.find_leader()
            
            # Register the results of this iteration
            if csv_file is not None:
                output.append(self.create_log_entry(iteration + 1))
            
            # Check if we've attained the desired minimum
            best = 1.0/self.population[self.leader].current_fitness
            if best <= DESIRED_MINIMUM:
                break
        
        printer("Iteration [{0} / {1}] completed.".format(
            ITERATIONS, ITERATIONS))
        
        # Prints the best solution
        self.find_leader()
        leader = self.population[self.leader]
        
        # Writes the output to a file
        if csv_file is not None:
            with open(csv_file, 'w') as f:
                for line in output:
                    f.write(line)
                
                f.write(self.print_leader())
                f.write("\nAlgorithm stoped after {0} iterations.".format(
                    self.iteration))
                f.write("\nThis experiment's seed is {0}".format(seed))
                f.write("\nAlgorithm completed after {0} seconds.".format(
                    str(time.time() - start)))
        
        if json_file is not None:
            datastructures.to_json(leader.best_coloring, json_file)
        
        print("Done.\n")


# --------------------------------------------------------------------
#                             Module methods
# --------------------------------------------------------------------

def printer(msg):
    """Prints a message to the standard output.
    
    This method simulates a progress bar and is used to give the user
    an idea of how much time the algorithm will take to complete.
    
    Args:
      msg (str): the message to print in the standard output.
    """
    sys.stdout.write("\r" + msg)
    sys.stdout.flush()

def print_usage():
    """Print a small manual of how to use the module."""
    print("USAGE: python[3] pso.py [<seed>] [<filename>]")
    print("  where:")
    print("\t[<seed>]\tOPTIONAL - seed for the random generator")
    print("\t[<filename>]\tOPTIONAL - name for the output file")
