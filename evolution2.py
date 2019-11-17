"""
New version of evolution.py, which now evolves separate populations rather than one main.

Been thinking a bit about what selection etc actually means. In our implementation, there basically is no selection at
all, since we are using a generational model with a comma strategy. There is an equal number of offspring produced
to the amount of parents, which are all replaced (some offspring are left unmutated, but this is still technically
generational). Thus, no parent selection or survivor selection is enforced in the populations. Selection does come
into play for currently playing genes/phenes, but this is not technically evolutionary selection. The structure
could be changed to have survivor selection, for instance by producing a multitude of offspring and cutting a few
based on selection.

There's a bunch of redundancy in cloning offspring etc and the program works exactly the same without doing this (just
mutating the pop directly). I left it in because maybe in the future, it could be more interesting to generate more
offspring.

todo's
- could look a bit more at evolution strategy. Maybe adjust the parameters of .mutPolynomialBounded so a mutrate of
  1 guarantees mutation? This would be a bit more logical and enable more control.
- Update the evolution strategy to actually use survivor selection! The populations now are completely replaced by
  a similar amount of offspring. Over-producing offspring could generate more 'favourable' combinations prior to
  currently playing-selection.

- COULD experiment with 'demes', DEAP's preferred way of implementing multiple populations... but not required.
"""

from deap import base
from deap import creator
from deap import tools
from genetics import *
from presets import *
from fitness import *
import fitness as fit
import pandas as pd
import time
import json
import glob as glob
from itertools import repeat

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

def df_to_phenes(df):
    df = df.apply(make_phenotype, axis=1).tolist()
    return pd.DataFrame(df, columns=load_genepool().columns)


# DEAP stuff
creator.create("FitnessMax", base.Fitness, weights=(0.00,))
creator.create("Individual", list, fitness=creator.FitnessMax)

toolbox = base.Toolbox()

toolbox.register("individual", initIndividual, creator.Individual)
toolbox.register("population", initPopulation, list, toolbox.individual)

toolbox.register("evaluate", distance)
toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", tools.mutPolynomialBounded, eta=.5, low=0., up=1., indpb=0.6)
#toolbox.register("mutate", tools.mutGaussian, mu=0.5, sigma=0.1, indpb=0.05)
toolbox.register("select", tools.selNSGA2)


def main():

    preset_path = read_preset_path()
    preset_config = load_config(preset_path)

    # Initializing the populations
    files = glob.glob(preset_path + 'current/*.csv')
    try:
        files.remove(f'{preset_path}current/playing.csv')
    except:
        pass

    toolbox.register("population", initPopulation, list, toolbox.individual)

    pops = [toolbox.population(file) for file in files]

    MUTPB = preset_config['mut_rate']

    g = 0  # generation counter

    done = False
    while not done:
        g += 1

        next_play = pd.DataFrame(columns=load_genepool().columns)

        print("-- Generation %i --" % g)

        for pop in pops:
            i = pops.index(pop)

            # Select the next generation individuals
            offspring = toolbox.select(pop, len(pop))

            # Clone the selected individuals
            offspring = list(map(toolbox.clone, offspring))

            for mutant in offspring:
                if random.random() < MUTPB[i]:
                    toolbox.mutate(mutant)
                    del mutant.fitness.values

            # fitness assignment for each population // messy, but works...
            offspring_fit = pd.DataFrame(offspring, columns=load_genepool().columns)
            offspring_fit = df_to_phenes(offspring_fit)
            offspring_fit.loc[:, ['pitch', 'nature']] = 0

            # if pop == ...: # using an if statement, different rules can be programmed for different instruments
            optimum = compute_optimum(load_genepool(f'{preset_path}current/playing.csv'))

            fitnesses = map(toolbox.evaluate, offspring, repeat(optimum))

            # for some stupid reason, not printing here will mean the code doesn't work (WTF? python 3 issue i think)
            print(list(zip(offspring, fitnesses)))

            for ind, fit in zip(offspring, list(fitnesses)):
                ind.fitness.values = fit

            pop[:] = offspring

            # save new populations to respective csvs
            pop_genes = pd.DataFrame(pop, columns=load_genepool().columns)
            pop_genes.to_csv(files[i])

            # selection for next_play using NSGA2
            best_genes = toolbox.select(pop, preset_config['instr_counts'][i])
            best_genes = pd.DataFrame(best_genes, columns=load_genepool().columns)
            best_genes['nature'] = files[i].split('/')[-1].replace('.csv', '')

            next_play = pd.concat([next_play, best_genes])

        # not the prettiest code but it works. Maps playing genes back to a pd.df of phenes
        next_play = df_to_phenes(next_play)
        next_play.to_csv(f'{preset_path}current/playing.csv')

        # updating configs
        preset_path = read_preset_path()
        preset_config = load_config(preset_path)

        time.sleep(preset_config['gen_length'])


if __name__ == '__main__':
    main()
