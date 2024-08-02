"""
Crossover Base Class

This script defines the Crossover base class, which provides an interface for
implementing crossover methods in genetic algorithms.

Classes:
    Crossover: A base class for crossover operations.
"""

class Crossover:
    """
    A base class for implementing crossover methods in genetic algorithms.
    
    Methods:
        cross(parent1, parent2): Performs the crossover operation on two parents.
    """
    
    def cross(self, parent1, parent2):
        """
        Performs the crossover operation on two parents.
        
        Parameters:
            parent1: The first parent individual.
            parent2: The second parent individual.
        
        Raises:
            NotImplementedError: If the method is not implemented in the subclass.
        """
        raise NotImplementedError("Crossover method not implemented!")
