# Problem Set 3: Simulating the Spread of Disease and Virus Population Dynamics 

import random
import pylab as plt

''' 
Begin helper code
'''
class NoChildException(Exception):
    """
    NoChildException is raised by the reproduce() method in the SimpleVirus
    and ResistantVirus classes to indicate that a virus particle does not
    reproduce. You can use NoChildException as is, you do not need to
    modify/add any code.
    """
'''
End helper code
'''
#
# PROBLEM 1
#
# random.seed(0)

class SimpleVirus(object):
    """
    Representation of a simple virus (does not model drug effects/resistance).
    """
    def __init__(self, maxBirthProb, clearProb):
        """
        Initialize a SimpleVirus instance, saves all parameters as attributes
        of the instance.        
        maxBirthProb: Maximum reproduction probability (a float between 0-1)        
        clearProb: Maximum clearance probability (a float between 0-1).
        """
        self.maxBirthProb = maxBirthProb
        self.clearProb = clearProb

    def getMaxBirthProb(self):
        """
        Returns the max birth probability.
        """
        return self.maxBirthProb

    def getClearProb(self):
        """
        Returns the clear probability.
        """
        return self.clearProb

    def doesClear(self):
        """ Stochastically determines whether this virus particle is cleared from the
        patient's body at a time step. 
        returns: True with probability self.getClearProb and otherwise returns
        False.
        """
        if self.getClearProb() >= random.random():
            return True
        else:
            return False
    
    def reproduce(self, popDensity):
        """
        Stochastically determines whether this virus particle reproduces at a
        time step. Called by the update() method in the Patient and
        TreatedPatient classes. The virus particle reproduces with probability
        self.maxBirthProb * (1 - popDensity).
        
        If this virus particle reproduces, then reproduce() creates and returns
        the instance of the offspring SimpleVirus (which has the same
        maxBirthProb and clearProb values as its parent).         

        popDensity: the population density (a float), defined as the current
        virus population divided by the maximum population.         
        
        returns: a new instance of the SimpleVirus class representing the
        offspring of this virus particle. The child should have the same
        maxBirthProb and clearProb values as this virus. Raises a
        NoChildException if this virus particle does not reproduce.               
        """
        if self.maxBirthProb * (1 - popDensity) >= random.random():
            return SimpleVirus(self.getMaxBirthProb(), self.getClearProb())
        else:
            raise NoChildException


class Patient(object):
    """
    Representation of a simplified patient. The patient does not take any drugs
    and his/her virus populations have no drug resistance.
    """    

    def __init__(self, viruses, maxPop):
        """
        Initialization function, saves the viruses and maxPop parameters as
        attributes.

        viruses: the list representing the virus population (a list of
        SimpleVirus instances)

        maxPop: the maximum virus population for this patient (an integer)
        """
        self.viruses = viruses
        self.maxPop = maxPop

    def getViruses(self):
        """
        Returns the viruses in this Patient.
        """
        return self.viruses

    def getMaxPop(self):
        """
        Returns the max population.
        """
        return self.maxPop

    def getTotalPop(self):
        """
        Gets the size of the current total virus population. 
        returns: The total virus population (an integer)
        """
        return len(self.getViruses())      

    def update(self):
        """
        Update the state of the virus population in this patient for a single
        time step. update() should execute the following steps in this order:
        
        - Determine whether each virus particle survives and updates the list
        of virus particles accordingly.   
        
        - The current population density is calculated. This population density
          value is used until the next call to update() 
        
        - Based on this value of population density, determine whether each 
          virus particle should reproduce and add offspring virus particles to 
          the list of viruses in this patient.                    

        returns: The total virus population at the end of the update (an
        integer)
        """
        # Get updated list after some viruses potentially clear
        workingList = self.getViruses()
        updateList = []
        for pathogen in workingList:
            if pathogen.doesClear() == False:
                updateList.append(pathogen)
        
        # Calculate population density
        popDensity = len(updateList) / self.getMaxPop()
        
        # Populate a list of viruses that are created in this time step
        newGerms = []
        for pathogen in updateList:
            try:
                newGerms.append(pathogen.reproduce(popDensity))
            except NoChildException:
                continue
        
        # Add the new viruses to the updated list
        for pathogen in newGerms:
            updateList.append(pathogen)
        
        # Set self.viruses to updated list
        self.viruses = updateList    
        
        # Return total virus population
        return(len(updateList))
#
# PROBLEM 2
#
def simulationWithoutDrug(numViruses, maxPop, maxBirthProb, clearProb,
                          numTrials):
    """
    Run the simulation and plot the graph for problem 3 (no drugs are used,
    viruses do not have any drug resistance).    
    For each of numTrials trial, instantiates a patient, runs a simulation
    for 300 timesteps, and plots the average virus population size as a
    function of time.

    numViruses: number of SimpleVirus to create for patient (an integer)
    maxPop: maximum virus population for patient (an integer)
    maxBirthProb: Maximum reproduction probability (a float between 0-1)        
    clearProb: Maximum clearance probability (a float between 0-1)
    numTrials: number of simulation runs to execute (an integer)
    """
    # Create list of viruses for use in call to Patient
    germList = []
    for i in range(numViruses):
        germList.append(SimpleVirus(maxBirthProb, clearProb))
     
    # Set up a results list containing 300 nested lists, one for each time step
    timeSteps = 300
    masterResults = []
    for i in range(timeSteps):
        masterResults.append([])
    
    # Step through the timeSteps and append population to appropriate sublist
    for trial in range(numTrials):
        testSubject = Patient(germList, maxPop)
        time = 0
        while time < timeSteps:
            population = testSubject.update()
            masterResults[time].append(population)
            time += 1
    
    # Create a list of means at different time steps
    meanList = []
    for i in range(timeSteps):
        mean = sum(masterResults[i]) / numTrials
        meanList.append(mean)
    
    # Create a timestep range list for plotting
    tValues = list(range(timeSteps))
      
    # Start  plotting
    plt.figure("meanVirusPop")
    plt.clf()
    plt.plot(tValues, meanList, 'ro', label = "Simple Virus")
    
    #Don't forget to include axes labels, a legend for the curve, and a title on your plot.
    plt.xlabel("Time Steps")
    plt.ylabel("Mean Virus Population")
    plt.title("Mean Virus Population vs Time")
    plt.legend(loc = 'upper center')
    
# simulationWithoutDrug(numViruses, maxPop, maxBirthProb, clearProb,numTrials):
# simulationWithoutDrug(100, 1000, 0.1, 0.05, 20)      


#
# PROBLEM 3
#
class ResistantVirus(SimpleVirus):
    """
    Representation of a virus which can have drug resistance.
    """   

    def __init__(self, maxBirthProb, clearProb, resistances, mutProb):
        """
        Initialize a ResistantVirus instance, saves all parameters as attributes
        of the instance.

        maxBirthProb: Maximum reproduction probability (a float between 0-1)       

        clearProb: Maximum clearance probability (a float between 0-1).

        resistances: A dictionary of drug names (strings) mapping to the state
        of this virus particle's resistance (either True or False) to each drug.
        e.g. {'guttagonol':False, 'srinol':False}, means that this virus
        particle is resistant to neither guttagonol nor srinol.

        mutProb: Mutation probability for this virus particle (a float). This is
        the probability of the offspring acquiring or losing resistance to a drug.
        """
        SimpleVirus.__init__(self, maxBirthProb, clearProb)
        self.resistances = resistances
        self.mutProb = mutProb


    def getResistances(self):
        """
        Returns the resistances for this virus.
        """
        return self.resistances

    def getMutProb(self):
        """
        Returns the mutation probability for this virus.
        """
        return self.mutProb

    def isResistantTo(self, drug):
        """
        Get the state of this virus particle's resistance to a drug. This method
        is called by getResistPop() in TreatedPatient to determine how many virus
        particles have resistance to a drug.       

        drug: The drug (a string)

        returns: True if this virus instance is resistant to the drug, False
        otherwise.
        """
        return self.resistances.get(drug, False)

    def reproduce(self, popDensity, activeDrugs):
        """
        Stochastically determines whether this virus particle reproduces at a
        time step. Called by the update() method in the TreatedPatient class.

        A virus particle will only reproduce if it is resistant to ALL the drugs
        in the activeDrugs list. For example, if there are 2 drugs in the
        activeDrugs list, and the virus particle is resistant to 1 or no drugs,
        then it will NOT reproduce.

        Hence, if the virus is resistant to all drugs
        in activeDrugs, then the virus reproduces with probability:      

        self.maxBirthProb * (1 - popDensity).                       

        If this virus particle reproduces, then reproduce() creates and returns
        the instance of the offspring ResistantVirus (which has the same
        maxBirthProb and clearProb values as its parent). The offspring virus
        will have the same maxBirthProb, clearProb, and mutProb as the parent.

        For each drug resistance trait of the virus (i.e. each key of
        self.resistances), the offspring has probability 1-mutProb of
        inheriting that resistance trait from the parent, and probability
        mutProb of switching that resistance trait in the offspring.       

        For example, if a virus particle is resistant to guttagonol but not
        srinol, and self.mutProb is 0.1, then there is a 10% chance that
        that the offspring will lose resistance to guttagonol and a 90%
        chance that the offspring will be resistant to guttagonol.
        There is also a 10% chance that the offspring will gain resistance to
        srinol and a 90% chance that the offspring will not be resistant to
        srinol.

        popDensity: the population density (a float), defined as the current
        virus population divided by the maximum population       

        activeDrugs: a list of the drug names acting on this virus particle
        (a list of strings).

        returns: a new instance of the ResistantVirus class representing the
        offspring of this virus particle. The child should have the same
        maxBirthProb and clearProb values as this virus. Raises a
        NoChildException if this virus particle does not reproduce.
        """
        # Prevent virus reproduction if it doesn't have a resistance to an active drug
        for medicine in activeDrugs:
            if self.isResistantTo(medicine) == False:
                raise NoChildException
        
        # Check if production is possible with throw against population density     
        if self.maxBirthProb * (1 - popDensity) >= random.random():
            newResistances = self.getResistances()
            mutationProb = self.getMutProb()
            # Mutate drug resistances
            for drug in newResistances:
                if random.random() <= mutationProb:
                    newResistances[drug] = not newResistances[drug]
            # return a new Resistant Virus
            return ResistantVirus(self.getMaxBirthProb(), self.getClearProb(), newResistances, mutationProb)
        else:
            raise NoChildException
            
class TreatedPatient(Patient):
    """
    Representation of a patient. The patient is able to take drugs and his/her
    virus population can acquire resistance to the drugs he/she takes.
    """

    def __init__(self, viruses, maxPop):
        """
        Initialization function, saves the viruses and maxPop parameters as
        attributes. Also initializes the list of drugs being administered
        (which should initially include no drugs).              

        viruses: The list representing the virus population (a list of
        virus instances)

        maxPop: The  maximum virus population for this patient (an integer)
        """
        Patient.__init__(self, viruses, maxPop)
        self.activeDrugs = []

    def addPrescription(self, newDrug):
        """
        Administer a drug to this patient. After a prescription is added, the
        drug acts on the virus population for all subsequent time steps. If the
        newDrug is already prescribed to this patient, the method has no effect.

        newDrug: The name of the drug to administer to the patient (a string).

        postcondition: The list of drugs being administered to a patient is updated
        """
        if newDrug not in self.getPrescriptions():
            self.activeDrugs.append(newDrug)

    def getPrescriptions(self):
        """
        Returns the drugs that are being administered to this patient.

        returns: The list of drug names (strings) being administered to this
        patient.
        """
        return self.activeDrugs

    def getResistPop(self, drugResist):
        """
        Get the population of virus particles resistant to the drugs listed in
        drugResist.       

        drugResist: Which drug resistances to include in the population (a list
        of strings - e.g. ['guttagonol'] or ['guttagonol', 'srinol'])

        returns: The population of viruses (an integer) with resistances to all
        drugs in the drugResist list.
        """
        resistantCounter = 0
        activeViruses = self.getViruses()
        for pathogen in activeViruses:
            resistsAll = True
            for medicine in drugResist:
                if pathogen.isResistantTo(medicine) == False:
                    resistsAll = False
                    break
            if resistsAll:
                resistantCounter += 1
        return resistantCounter
                    
    def update(self):
        """
        Update the state of the virus population in this patient for a single
        time step. update() should execute these actions in order:

        - Determine whether each virus particle survives and update the list of
          virus particles accordingly

        - The current population density is calculated. This population density
          value is used until the next call to update().

        - Based on this value of population density, determine whether each 
          virus particle should reproduce and add offspring virus particles to 
          the list of viruses in this patient.
          The list of drugs being administered should be accounted for in the
          determination of whether each virus particle reproduces.

        returns: The total virus population at the end of the update (an
        integer)
        """
        # Get updated list after some viruses potentially clear
        workingList = self.getViruses()
        updateList = []
        for pathogen in workingList:
            if pathogen.doesClear() == False:
                updateList.append(pathogen)
        
        # Calculate population density
        popDensity = len(updateList) / self.getMaxPop()
        
        # Populate a list of viruses that are created in this time step
        newGerms = []
        medicines = self.getPrescriptions()
        for pathogen in updateList:
            # Set a variable to check for a drug preventing reproduction
            canReproduce = True
            for drug in medicines:
                if pathogen.isResistantTo(drug) == False:
                    canReproduce = False
                    break
            # If drugs don't prevent reproduction, attempt to reproduce dependent on population density
            if canReproduce:
                try:
                    newGerms.append(pathogen.reproduce(popDensity, medicines))
                except NoChildException:
                    continue
        
        # Add the new viruses to the updated list
        for pathogen in newGerms:
            updateList.append(pathogen)
        
        # Set self.viruses to updated list
        self.viruses = updateList    
        
        # Return total virus population
        return(len(updateList))
#
# PROBLEM 4
#
def simulationWithDrug(numViruses, maxPop, maxBirthProb, clearProb, resistances,
                       mutProb, numTrials):
    """
    Runs simulations and plots graphs for problem 5.

    For each of numTrials trials, instantiates a patient, runs a simulation for
    150 timesteps, adds guttagonol, and runs the simulation for an additional
    150 timesteps.  At the end plots the average virus population size
    (for both the total virus population and the guttagonol-resistant virus
    population) as a function of time.

    numViruses: number of ResistantVirus to create for patient (an integer)
    maxPop: maximum virus population for patient (an integer)
    maxBirthProb: Maximum reproduction probability (a float between 0-1)        
    clearProb: maximum clearance probability (a float between 0-1)
    resistances: a dictionary of drugs that each ResistantVirus is resistant to
                 (e.g., {'guttagonol': False})
    mutProb: mutation probability for each ResistantVirus particle
             (a float between 0-1). 
    numTrials: number of simulation runs to execute (an integer)
    
    """
    # Create list of viruses for use in call to Patient
    germList = []
    for i in range(numViruses):
        germList.append(ResistantVirus(maxBirthProb, clearProb, resistances, mutProb))
        
    # Set up a results list containing 300 nested lists, one for each time step
    timeSteps = 300
    untreatedSteps = timeSteps // 2
    masterResults = []
    resistantResults = []
    for i in range(timeSteps):
        masterResults.append([])
        resistantResults.append([])
    
    # Step through the untreated steps and append population to appropriate sublist
    for trial in range(numTrials):
        testSubject = TreatedPatient(germList, maxPop)
        time = 0
        while time < untreatedSteps:
            population = testSubject.update()
            resistantPopulation = testSubject.getResistPop(['guttagonol'])
            masterResults[time].append(population)
            resistantResults[time].append(resistantPopulation)
            time += 1
        testSubject.addPrescription('guttagonol')
        while time < timeSteps:
            population = testSubject.update()
            resistantPopulation = testSubject.getResistPop(['guttagonol'])
            masterResults[time].append(population)
            resistantResults[time].append(resistantPopulation)
            time += 1
    
    # Create a list of means at different time steps
    meanList = []
    for i in range(timeSteps):
        mean = sum(masterResults[i]) / numTrials
        meanList.append(mean)
    
    resistantMeanList = []
    for i in range(timeSteps):
        mean = sum(resistantResults[i]) / numTrials
        resistantMeanList.append(mean)
    
    # Start  plotting
    plt.clf()
    plt.plot(meanList, 'ro', label = "Total Virus Population")
    plt.plot(resistantMeanList, 'b-', label = "Resistant Virus Population")
    
    #Don't forget to include axes labels, a legend for the curve, and a title on your plot.
    plt.title("ResistantVirus simulation")
    plt.xlabel("time step")
    plt.ylabel("# viruses")
    plt.legend(loc = 'upper center')
    
    '''
    For grader:
    # Start  plotting

    pylab.plot(meanList, 'ro', label = "Total Virus Population")
    pylab.plot(resistantMeanList, 'b-', label = "Resistant Virus Population")
    
    #Don't forget to include axes labels, a legend for the curve, and a title on your plot.
    pylab.title("ResistantVirus simulation")
    pylab.xlabel("time step")
    pylab.ylabel("# viruses")
    pylab.legend(loc = 'upper center')
    pylab.show()
    '''

'''
#Tests - be aware that running multiple tests in on programme causes clf to execute
# Test 1
Test: simulationWithDrug(1, 10, 1.0, 0.0, {}, 1.0, 5)

#Test 2
Test: simulationWithDrug(1, 20, 1.0, 0.0, {"guttagonol": True}, 1.0, 5)

#Test 3
simulationWithDrug(75, 100, .8, 0.1, {"guttagonol": True}, 0.8, 1)
'''
