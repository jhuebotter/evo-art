from deap import base
from deap import creator
from deap import tools
from genetics import *
import pandas as pd
import time
import json
import glob as glob

MASTER_CONFIG_PATH = 'data/presets/master_config.json' # probably just pull this from the main file

preset_name = 'default'
preset_path = 'data/presets/' + preset_name + '/'
config_path = preset_path + '/' + 'config.json'

def evalOneMax(individual):
    x = sum(individual)
    return x,

def initIndividual(icls, content):
    return icls(content)

def initPopulation(pcls, ind_init, filename):
    contents = []
    df = load_genepool(filename)
    for genome in df.values:
        contents.append(list(genome))
    return pcls(ind_init(c) for c in contents)


creator.create("FitnessMax", base.Fitness, weights=(0.00,))
creator.create("Individual", list, fitness=creator.FitnessMax)

toolbox = base.Toolbox()

toolbox.register("individual", initIndividual, creator.Individual)
toolbox.register("population", initPopulation, list, toolbox.individual)

toolbox.register("evaluate", evalOneMax)
toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", tools.mutPolynomialBounded, eta=.5, low=0., up=1., indpb=0.6)
#toolbox.register("mutate", tools.mutGaussian, mu=0.5, sigma=0.1, indpb=0.05)
#toolbox.register("select", tools.selWorst)
toolbox.register("select", tools.selNSGA2)

def main():

    # load in JSON configuration file
    with open(config_path) as f:
        conf_file = json.load(f)
        print(conf_file['mut_rate'])

    time.sleep(conf_file['gen_length'])

    # Initializing the populations
    pop_paths = []
    pop_names = []

    for pop_path in glob.glob(preset_path + '/initial/' '*.csv'):
        pop_paths.append(pop_path) # for each .csv, retrieve the filename and create a population

        pop_name = "population_" + pop_path.split('/')[-1].split('.')[0]
        pop_names.append(pop_name) # for each .csv, retrieve the filename and create a population

    toolbox.register("population", initPopulation, list, toolbox.individual)

    pops = [toolbox.population(pop_path) for pop_path in pop_paths]

    CXPB, MUTPB = 0., conf_file['mut_rate'] # crossover mutation is currently not implemented
    g = 0 # generation counter

    for pop in pops:
        fitnesses = list(map(toolbox.evaluate, pop))
        for ind, fit in zip(pop, fitnesses):
            ind.fitness.values = fit

        # fits = [ind.fitness.values[0] for ind in pop]

    done = False
    while not done: #max(fits) < 100 and g < 1000:
        g += 1

        print("-- Generation %i --" % g)

        # Select the next generation individuals
        offspring = toolbox.select(pop, len(pop))  # , len(pop))
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
        # invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
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

        # print("  Min %s" % min(fits))
        # print("  Max %s" % max(fits))
        # print("  Avg %s" % mean)
        # print("  Std %s" % std)# Select the next generation individuals
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

        # # Gather all the fitnesses in one list and print the stats
        # fits = [ind.fitness.values[0] for ind in pop]

        # length = len(pop)
        # mean = sum(fits) / length
        # sum2 = sum(x * x for x in fits)
        # std = abs(sum2 / length - mean * 2) * 0.5
        #
        # print("  Min %s" % min(fits))
        # print("  Max %s" % max(fits))
        # print("  Avg %s" % mean)
        # print("  Std %s" % std)



    # pop = toolbox.population()

main()