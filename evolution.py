from deap import base, creator, tools
from genetics import *
import pandas as pd
import time
import json

MASTER_CONFIG_PATH = 'data/presets/master_config.json' # probably just pull this from the main file

preset_name = 'default'
preset_path = 'data/presets/' + preset_name + '/'
config_path = preset_path + '/' + 'config.json'

def evalOneMax(individual):

    # This is the fitness function

    x = sum(individual)

    return x,

def initIndividual(icls, content):

    # How to make an individual

    return icls(content)

def initPopulation(pcls, ind_init, filename):

    # How to make a population

    df = load_genepool(filename)

    return pcls(ind_init(c) for c in df.values)


creator.create("FitnessMax", base.Fitness, weights=(0.00,))
creator.create("Individual", list, fitness=creator.FitnessMax)

toolbox = base.Toolbox()

toolbox.register("individual", initIndividual, creator.Individual)
toolbox.register("population", initPopulation, list, toolbox.individual, "genepool.csv")

toolbox.register("evaluate", evalOneMax)
toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", tools.mutPolynomialBounded, eta=.5, low=0., up=1., indpb=0.6)
#toolbox.register("mutate", tools.mutGaussian, mu=0.5, sigma=0.1, indpb=0.05)
#toolbox.register("select", tools.selWorst)
toolbox.register("select", tools.selNSGA2)


def main():

    # now load in JSON configuration file
    with open(data_path + 'config.json') as f:
        config = json.load(f)
        print(config['mut_rate'])

    time.sleep(config['gen_length'])

    # Init population
    pop = toolbox.population()



    # Evaluate the entire population
    fitnesses = list(map(toolbox.evaluate, pop))
    for ind, fit in zip(pop, fitnesses):
        ind.fitness.values = fit

    # CXPB  is the probability with which two individuals
    #       are crossed
    # MUTPB is the probability for mutating an individual
    CXPB, MUTPB = 0., config['mut_rate']

    # Extracting all the fitnesses of
    fits = [ind.fitness.values[0] for ind in pop]

    # Variable keeping track of the number of generations
    g = 0

    # Begin the evolution
    done = False
    while not done: #max(fits) < 100 and g < 1000:
        # A new generation
        g = g + 1

        #CXPB = 0.5
        #if g % 20 == 0:
        #    CXPB = 0.5

        print("-- Generation %i --" % g)

        # Select the next generation individuals
        offspring = toolbox.select(pop, len(pop))#, len(pop))
        # Clone the selected individuals
        offspring = list(map(toolbox.clone, offspring))

        # Apply crossover and mutation on the offspring
        for child1, child2 in zip(offspring[::2], offspring[1::2]):
            if random.random() < CXPB:
                print('crossing')
                toolbox.mate(child1, child2)
                del child1.fitness.values
                del child2.fitness.values

        for mutant in offspring:
            if random.random() < MUTPB:
                toolbox.mutate(mutant)
                del mutant.fitness.values

        # Evaluate the individuals with an invalid fitness
        #invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = map(toolbox.evaluate, offspring)
        for ind, fit in zip(offspring, fitnesses):
            ind.fitness.values = fit

        pop[:] = offspring

        pop_genes = pd.DataFrame(pop, columns=load_genepool().columns)
        pop_genes.to_csv('genepool.csv')

        # Gather all the fitnesses in one list and print the stats
        fits = [ind.fitness.values[0] for ind in pop]

        length = len(pop)
        mean = sum(fits) / length
        sum2 = sum(x * x for x in fits)
        std = abs(sum2 / length - mean * 2) * 0.5

        #print("  Min %s" % min(fits))
        #print("  Max %s" % max(fits))
        #print("  Avg %s" % mean)
        #print("  Std %s" % std)


        # now load in JSON configuration file
        with open(data_path + 'config.json') as f:
            config = json.load(f)
        time.sleep(config['gen_length'])

    return


if __name__ == '__main__':
    main()