#Space Discover: Genetic Algorithms - Training File 

#Importing the libraries
import numpy as np
from environment import Environment

#Creating the bots
class Route():
    
    def __init__(self, dnaLength):
        self.dnaLength = dnaLength
        self.dna = list()
        self.distance = 0 # Measures the distance travelled by the bot
        
        # Initializing the random DNA
        for i in range(self.dnaLength - 1): # The last gene will always be 0
            # dna =  3, 1, 2
            rnd = np.random.randint(1, self.dnaLength) # upper bound is exluded
            while rnd in self.dna:
                rnd = np.random.randint(1, self.dnaLength) # upper bound is exluded
            self.dna.append(rnd)
        self.dna.append(0)
        #dna = 3, 1, 2, 0
        
    # BUilding the crossover method:
    """
    This part is a little bit tricky since we want the genes to be unique in
    the DNA.
    """
    def mix(self, dna1, dna2):
        self.dna = dna1.copy()
        
        for i in range(self.dnaLength - 1):
            if np.random.rand() > 0.5:
                # We perform a crossover
                # We need to find the index where dna2[i] is located in dna
                idx = self.dna.index(dna2[i])
                # Then we need to replace the gene of dna at position idx 
                # with the one  at position i
                self.dna[idx] = self.dna[i]
                # We then replace the gene of dna at postion previous with 
                # the one of dna2 at the same position
                self.dna[i] = dna2[i]
                
        # Random Partial Mutations 1:
        for i in range(self.dnaLength - 1):
            if np.random.rand() <= 0.1:
                previous = self.dna[i]
                rnd = np.random.randint(1, self.dnaLength)
                idx = self.dna.index(rnd)
                self.dna[idx] = previous
                self.dna[i] = rnd
                
            # Random Partial Mutations 2:
            elif np.random.rand() <= 0.1:
                rnd = np.random.randint(1, self.dnaLength)
                prevIdx = self.dna.index(rnd)
                self.dna.insert(i, rnd)
                
                if i >= prevIdx:
                    self.dna.pop(prevIdx)
                else:
                    self.dna.pop(prevIdx + 1)
        
#Initializing the main code   
populationSize = 50
mutationRate = 0.1 # Probability that the new bot is a complete mutant
nSelected = 5 # number of bots we select during the selection process  

env = Environment()             
dnaLength = len(env.planets)     
population = list()

#Creating the first population
for i in range(populationSize):
    route = Route(dnaLength)
    population.append(route)
    
#Starting the main loop
generation = 0
bestDist = np.inf
while True:
    generation += 1
    
    #Evaluating the population
    for route in population:
        env.reset()
        
        for i in range(dnaLength):
            action = route.dna[i]
            
            route.distance += env.step(action, 'none')
            
    #Sorting the population
    sortedPop = sorted(population, key = lambda x: x.distance)
    population.clear()

    if sortedPop[0].distance < bestDist:
        bestDist = sortedPop[0].distance
        
    # Adding best previous bots to the population
    # This step is not mandatory in genetic algorithm
    # This step is done to retain the best bots as they are because if 
    # we don't do this, the crossover might end up creating worst bots.
    for i in range(nSelected):
        best = sortedPop[i]
        best.distance = 0
        population.append(best)
    
    # Filling in the rest of the population
    left = populationSize - nSelected
    
    for i in range(left):
        newRoute = Route(dnaLength)
        if np.random.rand() <= mutationRate:
            population.append(newRoute)
        else:
            idx1 = np.random.randint(5, populationSize)
            idx2 = np.random.randint(5, populationSize)
            while idx1 == idx2:
                idx1 = np.random.randint(5, populationSize)

            dna1 = sortedPop[idx1].dna
            dna2 = sortedPop[idx2].dna
            
            newRoute.mix(dna1, dna2)
            
            population.append(newRoute)
            
    #Displaying the results
    env.reset()
    
    for i in range(dnaLength):
        action = sortedPop[0].dna[i]
        _ = env.step(action, 'normal')
    
    # We display the rocket every 100 generations
    if generation % 100 == 0:
        env.reset()
        
        for i in range(dnaLength):
            action = sortedPop[0].dna[i]
            _ = env.step(action, 'beautiful')
    
    print('Generation: ' + str(generation) + ' Shortest distance: {:.2f}'.format(bestDist) + ' light years')
        
        
     
          
     



                         




               
               