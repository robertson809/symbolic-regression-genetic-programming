import Tree as Tree
import readData as readData
from random import *
from heapq import heappush, heappop
import copy
import math

#next implement mutate and debug


##main driver program
##population, and list of lists for train data
def evolution(data, gen_size, details, tol):
    """
    :param data: the training data set, a list of input output touples
    :param gen_size: the size of each generation, could vary
    :param details: a touble specifying the type of selection (1 for tournament),
    and for tournament, the number of tournaments
    :param tol: the error below which we consider ourselves to have found the solution
    """
    #error tolerance
    kings = []
    converged = False
    #create a population
    print ('making original generation')
    original = new_gen(gen_size)
    print ('finished making original generation')

    heappush(kings, original[1])


    old_gen = original
    #simulate generations of natural selection
    converg_count = 0
    gen_count = 0
    while not converged:
        if kings[0].fitness < tol:
            converged = True
            print("Error below tolerance, sucess! Printing king")
            king.root.display()
            print("Broke tolerance after ", gen_count, " generations")
            break


        gen_count += 1
        print ('generation', gen_count, ' completed, creating', ' generation...', gen_count + 1)
        next_gen = run_generation(old_gen, details, data)
        king = next_gen[1]
        print ('most fit individual from generation ', gen_count, ' has fitness', king.fitness)

        try:
            heappush(kings, king)
        except:
            print (' tie break error')
            continue

        #aging the population
        old_gen = next_gen

        #if we have reached tolerance

        print(" the most fit king so far has fitness ", kings[0].fitness)
        kings[0].root.display()
        print(" the most fit king from this generation has fitness ", king.fitness)
        king.root.display()
        #if we don't improve five times in a row, consider us converged
        #kings[0] gets the smallest element in the heap
        if king.fitness > kings[0].fitness:
            converg_count += 1
            if converg_count == 7:
                print('fitness has not improved in 7 generations, ending')
                converged = True
        else:
            converg_count = 0





    #after debugging, actually run evolution
    #count = 0
    #keep going until a new king's error is within tolerance
    # while (next_gen[1].fitness < tol and count < 10,000):
    #     next_gen = run_generation(next_gen, details, data)
    #     count += 1
    #


def roulette(old_gen, num_, data):
    return



def run_generation(old_gen, details, data):
    """

    :param old_gen: the generation to produce children from in index zero, the king in index 1
    :param details: a touple, the first integer specifying the type of
    parent selection (1 for tournament), the second entry specifying the
    number of tournaments (for tournament)
    :param data: the test data set
    :return: tuple: the first entry is the new population, of size equal to the
    old_gen, the second is the best overall tree from the new generation
    """
    next_gen = []
    best_fitness = float('inf')
    king = None
    #get the tournament size if we are having a tournament
    if details[0] == 1:
        #add the old king
        next_gen.append(old_gen[1])
        num_tourns = details[1]
        count = 0
        while(len(next_gen) < len(old_gen[0])):
            count += 1
            print ("running tournament ", count)
            champs = tournament(old_gen[0], num_tourns, data)
            #get n kids from a tournament that splits the population into n groups
            for i in range(num_tourns):
                # randomly select two parents
                index1 = randint(0, len(champs) - 1)
                index2 = randint(0, len(champs) - 1)
                # no asexual reproduction
                while index1 == index2:
                    index2 = randint(0, len(champs) - 1)
                # reproduction
                child = champs[index1].crossover(champs[index2])
                #mutate 5% of the time
                child.mutate(child.root)
                child.calcFitness(data)
                if child.fitness < best_fitness:
                    best_fitness = child.fitness
                    king = copy.deepcopy(child)
                next_gen.append(child)

                #5% of the time, add a new tree
                if randint(0,100) < 5:
                    next_gen.append(Tree.Tree(10))
                #print ('child ', i, 'of tournament ', count, ' has fitness', child.fitness)


    if details[0] == 2:
        champs = roulette(old_gen[0], details[1], data)


    print("size of the old generation is", len(old_gen[0]))
    print("size of new gen is", len(next_gen))
    return next_gen, king


def new_gen(size):
    """
    :type size: size of the generation
    :return tuple: the new generation in the first entry,
    the very best individual in the second entry
    """
    forest = []
    best_fitness = float('inf')
    king = None
    ##create population and rank them by fitness
    for i in range(size):
        forest.append(Tree.Tree(15))
        # calculate fitness
        forest[i].calcFitness(data)
        if forest[i].fitness < best_fitness:
            best_fitness = forest[i].fitness
            king = copy.deepcopy(forest[i])
    return forest, king


def tournament(pop, num_torns, data):
    """
    split the population into num_torn groups, plus one for the leftovers,
    then return the best of those groupsas the mating pool

    Requires that the list of trees, pop, is randomized


    For added complexity, we can change from just giving the best,
    to giving the best with probability p (probably around .8), the
    second best with probability p*(1-p), and the third best with probability
    p((1-p)^2), giving the remainder to the first best

    :param pop: the population to select a mate pool from
    :param num_torns: the number of tornaments to hold
    :param data: the data to test each individual's fitness on
    :return champions: a list of num_torns different champions, who
    are the most fit
    """
    champions = []
    # the size of each tournament
    torn_size = int(len(pop) / num_torns)
    # torns = []

    # create num_torn tournaments from which to choose a winner
    for i in range(num_torns):
        # 2nd place implementation
        # torns.append([])
        # run tournaments
        best = float('inf')
        best_tree = None
        for j in range(torn_size):
            fitness = pop[(i * torn_size) + j].calcFitness(data)
            # see if its the best
            if fitness < best:
                best = fitness
                best_tree = copy.deepcopy(pop[(i * torn_size) + j])
            # Use this if you want to keep track and give second place a chance
            # torns[i].append(pop[(i * torn_size) + j])
        # final best
        if best_tree is not None:
            champions.append(best_tree)
        else:
            print("No tree had a fitness better than infinity")
        print ("The tournament of size ", torn_size, "produced a champion of fitness: ", best)

    if len(pop) % num_torns != 0:
        # add the stragglers leftover from integer division to the last one
        # definitely check this
        best = float('inf')
        best_tree = None
        for j in range(len(pop) % num_torns):
            fitness = pop[((num_torns - 1) * torn_size) + torn_size + j].calcFitness(data)
            if fitness < best:
                best = fitness
                best_tree = copy.deepcopy(pop[((num_torns - 1) * torn_size) + torn_size + j])
        if best_tree is not None:
            champions.append(best_tree)
        # torns.append([])
        # Use for 2nd place chance
        # torns[num_torns].append(pop[((num_torns - 1) * torn_size) + torn_size + i])
    return champions


##testing
# Tree1 = Tree.Tree(5)
# Tree1.display_tree()

print ('reading data')
data = readData.readData('test1.csv')
print ('done reading data')



#evolution with the data set, 100 people in a generation, (tournament selction with fifteen tournaments),
#and mse error tolerance of 1
gen_size = 100
evolution(data, gen_size, (1, int(math.sqrt(gen_size))), .1)
evo