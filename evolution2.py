from deap import base
from deap import creator
from deap import tools
from genetics import *
import pandas as pd
import time
import json
import glob as glob

preset_name = 'default'
preset_path = 'data/presets/' + preset_name
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
toolbox.register("population", initPopulation, list, toolbox.individual, "genepool.csv")

toolbox.register("evaluate", evalOneMax)
toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", tools.mutPolynomialBounded, eta=.5, low=0., up=1., indpb=0.6)
#toolbox.register("mutate", tools.mutGaussian, mu=0.5, sigma=0.1, indpb=0.05)
#toolbox.register("select", tools.selWorst)
toolbox.register("select", tools.selNSGA2)

def main():

    # now load in JSON configuration file
    with open(data_path + 'master_config.json') as f:
        config = json.load(f)
        print(config['mut_rate'])

    time.sleep(config['gen_length'])

    # Init populations
    pops = []
    for csv in glob.glob('*.csv'):
        pops.append(csv)

    print(pops)

    # pop = toolbox.population()

main()