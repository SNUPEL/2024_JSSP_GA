"""
Mutation Base Class

This script defines the Mutation base class, which provides an interface for
implementing mutation methods in genetic algorithms.

Classes:
    Mutation: A base class for mutation operations.

Functions:
    mutate(individual): Performs the mutation operation on an individual.
"""

class Mutation:
    """
    A base class for implementing mutation methods in genetic algorithms.
    
    Methods:
        mutate(individual): Performs the mutation operation on an individual.
    """
    
    def mutate(self, individual):
        """
        Performs the mutation operation on an individual.
        
        Parameters:
            individual: The individual to mutate.
        
        Raises:
            NotImplementedError: If the method is not implemented in the subclass.
        """
        raise NotImplementedError("Mutation method not implemented!")
