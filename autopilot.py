import time
import pandas as pd
from presets import *
from genetics import *
import glob


def initialize_current(preset_path):

    create_folder(f'{preset_path}current')

    for file in glob.glob(f'{preset_path}initial/*'):
        data = load_genepool(file)
        name = file.split('/')[-1]
        save_genepool(data, f'{preset_path}current/{name}')


def select_genes(index, preset_path):

    phenotypes = []

    files = glob.glob(f'{preset_path}current/*.csv')
    try:
        files.remove(f'{preset_path}current/playing.csv')
    except:
        print()

    for file in files:
        data = load_genepool(file)
        name = file.split('/')[-1].replace('.csv', '')
        gene = data.iloc[index,]
        gene.loc['nature'] = name
        phenotype = make_phenotype(gene)
        phenotypes.append(phenotype)

    current_phenotypes = pd.DataFrame(phenotypes)
    current_phenotypes.to_csv(f'{preset_path}current/playing.csv')


def main():

    # make sure we have the configs
    preset_path = read_preset_path()
    preset_config = load_config(preset_path)

    initialize_current(preset_path)

    # now select some initial playing genes from the instrument genepools
    i = 0

    while True:

        # make sure we have the configs
        preset_path = read_preset_path()
        preset_config = load_config(preset_path)

        if i % 10 == 0:
            index = random.randint(0, preset_config['size']-1)
            print("changing index")
        select_genes(index, preset_path)
        i += 1
        time.sleep(preset_config['refresh_rate'])


if __name__ == '__main__':
    main()