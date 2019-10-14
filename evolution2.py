'''
New version of evolution.py, which now evolves separate populations rather than one main.

Still to be implemented:
- which genes should be mutated, which shouldn't? (instrument pool, for example, shouldn't be mutated?)
- thorough testing on mutation. Why do some genes not mutate? (working as intended?)
- integration with the updated rest of the code
- Making an up-to-date merge and push this to 'tommy' branch (or master)
- This merge COULD already include updated geometry.py (and whatever else needs to be updated) that can use these genes
- some brainstorming is necessary on how to best use the new population structure, and how (if necessary) to make the
  code iterable for any amount of natures.

Notes:
- I fixed the generation length by moving time.sleep(conf_file['gen_length'] into the loop. Does this still work with
  the 'main file' implementation?
- Mutation rates are now encoded as a list of 4 floats, representing the mutation rate for each
'''


from deap import base
from deap import creator
from deap import tools
from genetics import *
import pandas as pd
import time
import json
import glob as glob

MASTER_CONFIG_PATH = 'data/presets/master_config.json' # probably just pull this from the main file

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

def main(preset_path):

    # load in JSON configuration file
    with open(config_path) as f:
        conf_file = json.load(f)
        print('Mutation rates: ' + str(conf_file['mut_rate']))
        # a list of mut_rates for different pops could be loaded here from config if needed

    # Initializing the populations
    pop_paths = []
    pop_names = []

    for pop_path in glob.glob(preset_path + 'current/*.csv'): # NOTE: I changed it such that .csv files need to be
                                                              # initialized in both 'initial' and 'current'.
        pop_paths.append(pop_path) # for each .csv, retrieve the filename and append a population path

        pop_name = "population_" + pop_path.split('/')[-1].split('.')[0]
        pop_names.append(pop_name) # for each .csv, retrieve the filename and append a population name

    toolbox.register("population", initPopulation, list, toolbox.individual)

    pops = [toolbox.population(pop_path) for pop_path in pop_paths]

    # print(pops)
    # print(pop_names)
    # print(pop_paths)

    MUTPB = conf_file['mut_rate'] # this is now a list with four parameters for the mut_rate of each population
    if not type(MUTPB) == list:
        raise TypeError("Mutation rates must now be given in a list format, with a value for each population")

    g = 0 # generation counter

    for pop in pops: # zip in the initial fitness values for each population
        fitnesses = list(map(toolbox.evaluate, pop))
        for ind, fit in zip(pop, fitnesses):
            ind.fitness.values = fit # not sure how these are formatted, since I can't print them (just produce NaN)

    done = False
    while not done: # no stop condition programmed yet
        g += 1

        print("-- Generation %i --" % g)

        for pop in pops:
            i = pops.index(pop)

            # Select the next generation individuals
            offspring = toolbox.select(pop, len(pop))  # , len(pop))
            # Clone the selected individuals
            offspring = list(map(toolbox.clone, offspring))

            for mutant in offspring:
                if random.random() < MUTPB[i]: # this line still seems to produce a chance of staying constant, even for
                                               # MUTPB = 1. Probably not working as intended. This is the same in the
                                               # original evolution.py, so maybe I'm not understanding it correctly.
                    toolbox.mutate(mutant)
                    del mutant.fitness.values

            # Evaluate the individuals with an invalid fitness
            # invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
            fitnesses = map(toolbox.evaluate, offspring)
            for ind, fit in zip(offspring, fitnesses):
                ind.fitness.values = fit

            pop[:] = offspring

            pop_genes = pd.DataFrame(pop, columns=load_genepool().columns)
            pop_genes.to_csv(pop_paths[i])  # write to new folder (current)

            # code for printing stats (can be commented once no longer needed)
            print(pop)

            '''
            # Gather all the fitnesses in one list and print the stats
            fits = [ind.fitness.values[0] for ind in pop]

            length = len(pop)
            mean = sum(fits) / length
            sum2 = sum(x * x for x in fits)
            std = abs(sum2 / length - mean * 2) * 0.5

            print("  Min %s" % min(fits))
            print("  Max %s" % max(fits))
            print("  Avg %s" % mean)
            print("  Std %s" % std)
            '''

        # now load in JSON configuration file [is this to recheck the mut_rate and other params? might need updating]
        with open(data_path + 'presets/default/config.json') as f:
            conf_file = json.load(f)

        time.sleep(conf_file['gen_length'])


# Testing unit for 'default' preset
preset_name = 'default' # input the preset name here (from GUI)

preset_path = 'data/presets/' + preset_name + '/'
config_path = preset_path + '/' + 'config.json'

main(preset_path) # this could be changed to take the preset_name instead, or some other structure (pull it from another file)

# if __name__ == '__main__':
#     main()