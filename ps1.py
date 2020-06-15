###########################
# 6.00.2x Problem Set 1: Space Cows 

from ps1_partition import get_partitions
import time

#================================
# Part A: Transporting Space Cows
#================================

def load_cows(filename):
    """
    Read the contents of the given file.  Assumes the file contents contain
    data in the form of comma-separated cow name, weight pairs, and return a
    dictionary containing cow names as keys and corresponding weights as values.

    Parameters:
    filename - the name of the data file as a string

    Returns:
    a dictionary of cow name (string), weight (int) pairs
    """

    cow_dict = dict()

    f = open(filename, 'r')
    
    for line in f:
        line_data = line.split(',')
        cow_dict[line_data[0]] = int(line_data[1])
    return cow_dict


# Problem 1
def greedy_cow_transport(cows,limit=10):
    
    """
    Uses a greedy heuristic to determine an allocation of cows that attempts to
    minimize the number of spaceship trips needed to transport all the cows. The
    returned allocation of cows may or may not be optimal.
    The greedy heuristic should follow the following method:

    1. As long as the current trip can fit another cow, add the largest cow that will fit
        to the trip
    2. Once the trip is full, begin a new trip to transport the remaining cows

    Does not mutate the given dictionary of cows.

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)
    
    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """
    # TODO: Your code here
    masterList = []
    cowDict = dict(cows)
    cowNames = list(cowDict.keys())
    cowWeights = list(cowDict.values())
    remainingWeight = limit
    while cowNames != []:
        remainingWeight = limit
        weightToAdd = 0
        thisTrip = []
        while remainingWeight >= min(cowWeights):
            L = len(cowNames)
            weightToAdd = 0
            cowToAdd = None
            for x in range(L):
                if cowWeights[x] > weightToAdd and cowWeights[x] <= remainingWeight:
                    cowToAdd = cowNames[x]
                    weightToAdd = cowWeights[x]
            remainingWeight -= weightToAdd
            thisTrip.append(cowToAdd)
            cowNames.remove(cowToAdd)
            cowWeights.remove(weightToAdd)
            if cowNames!= []:
                if remainingWeight < min(cowWeights):
                    masterList.append(thisTrip)
            else:
                if thisTrip != []:
                    masterList.append(thisTrip)
                return masterList

# Problem 2
def brute_force_cow_transport(cows,limit=10):
    
    
    """
    Finds the allocation of cows that minimizes the number of spaceship trips
    via brute force.  The brute force algorithm should follow the following method:

    1. Enumerate all possible ways that the cows can be divided into separate trips
    2. Select the allocation that minimizes the number of trips without making any trip
        that does not obey the weight limitation
            
    Does not mutate the given dictionary of cows.

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)
    
    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """
    def brute_force_cow_transport(cows,limit=10):
        possibleJourneySets = []
        for item in get_partitions(cows):
            journeySet = []
            for entry in range(len(item)):
                totalWeight = 0
                journey = []
                for cow in item[entry]:
                    totalWeight += cows.get(cow)
                    ourney.append(cow)
                if totalWeight <= limit:
                    journeySet.append(journey)
                if item == journeySet:
                    possibleJourneySets.append(journeySet)
        workingLength = len(possibleJourneySets[0])
        workingPosition = 0
        for number in range(len(possibleJourneySets)):
            if len(possibleJourneySets[number]) < workingLength:
                workingLength = len(possibleJourneySets[number])
                workingPosition = number
        return possibleJourneySets[workingPosition]

        
# Problem 3
def compare_cow_transport_algorithms(cows,limit = 10):
    """
    Using the data from ps1_cow_data.txt and the specified weight limit, run your
    greedy_cow_transport and brute_force_cow_transport functions here. Use the
    default weight limits of 10 for both greedy_cow_transport and
    brute_force_cow_transport.
    
    Print out the number of trips returned by each method, and how long each
    method takes to run in seconds.

    Returns:
    Does not return anything.
    """
    print('Running Greedy Algorithm')
    start = time.time()
    x = (greedy_cow_transport(cows, limit))
    print(x)
    print('number of trips = ', x)
    end = time.time()
    print('Finished greedy algorithm. Time = ',end-start)
    
    print('Running BruteForce Algorithm')
    start = time.time()
    x = (brute_force_cow_transport(cows, limit))
    print(x)
    print('number of trips = ', x)
    print('Finished greedy algorithm. Time = ',end-start)
"""
Here is some test data for you to see the results of your algorithms with. 
Do not submit this along with any of your answers. Uncomment the last two
lines to print the result of your problem.
"""

cows = load_cows("ps1_cow_data.txt")
limit=10
cows2 = {'Maggie': 3, 'Herman': 7, 'Betsy': 9, 'Oreo': 6, 'Moo Moo': 3, 'Milkshake': 2, 'Millie': 5, 'Lola': 2, 'Florence': 2, 'Henrietta': 9}
cows3 = {'Lilly': 24, 'Coco': 10, 'Betsy': 65, 'Willow': 35, 'Daisy': 50, 'Dottie': 85, 'Rose': 50, 'Abby': 38, 'Patches': 12, 'Buttercup': 72}
compare_cow_transport_algorithms(cows)
compare_cow_transport_algorithms(cows2)
compare_cow_transport_algorithms(cows3,100)
