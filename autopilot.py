import pygame
import math
import time
import pandas as pd
import json
from presets import *
from music import *
from genetics import *
from psonic import *

def select_genes():

    # make sure we have the configs
    preset_path = read_preset_path()
    preset_config = load_config(preset_path)
    # init result
    current_genes = pd.DataFrame()




    rand_index = random.randint(0, preset_config['size'] - 1)

    for i in glob.glob(f'{preset_path}initial/*'):
        data = load_genepool(i)#pd.read_csv(i, index_cols=0)
        name = i.split('/')[-1].replace('.csv', '')
        gene = data.iloc[rand_index,]
        gene.loc['nature'] = name
        current_genes = pd.concat([current_genes, gene], axis=1)

    current_genes = current_genes.transpose()
    print(current_genes)
    current_genes.to_csv(f'{preset_path}current/playing.csv')



def main():
    # make sure we have the configs
    preset_path = read_preset_path()
    preset_config = load_config(preset_path)

    # now select some initial playing genes from the instrument genepools
    while True:
        select_genes()
        time.sleep(preset_config['refresh_rate'])


if __name__ == '__main__':
    main()