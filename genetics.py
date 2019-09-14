import random
import pandas as pd

size = [1920, 1080]
center = [size[0] / 2, size[1] / 2]

synths = ['piano', 'sine', 'pretty_bell']
#synths = ['piano', 'mod_synth', 'bass', 'kick']

samples = ['elec_soft_kick', 'sn_dub', 'tabla_ke3', 'tabla_na_s', 'elec_wood', 'bass_voxy_hit_c', 'drum_cowbell', 'drum_cymbal_pedal']


def random_genome():
    # creates a semi random genome
    genes = dict(rootnote=random.randint(24, 35),
                 rootoctave=4, #random.randint(3, 6),
                 order=random.randint(3, 3),
                 number=2, #random.randint(1,4),
                 bpm=12.5*random.randint(1,4),
                 total_offset=0.75, #0.125 * random.randint(0, 7),
                 initial_offset=0.5,#0.125 * random.randint(1, 8), delta_offset=0.,
                 red=random_color(), green=random_color(), blue=random_color(), line=1, center=center,
                 # this is all relevant for a synth
                 synth=random.randint(0,len(synths)-1),
                 amp=0.1 + 0.1 * random.randint(1, 3),
                 pan=0.,
                 attack=random.uniform(0., 1.),
                 attack_level=1.,
                 decay=random.uniform(0., 1.),
                 decay_level=0.,
                 sustain=random.uniform(0., 1.),
                 sustain_level=0.,
                 release=random.uniform(0., 1.),
                 env_curve=random.randint(1, 7),
                 mix=0.0,
                 # Now the sample related stuff
                 nature=random.randint(0, 4),
                 sample=random.randint(0, len(samples)-1)
                 )




    return genes


def add_genes(df, genes):
    # adds any genes to a geneome
    df.append(genes, ignore_index=True)

    return df


def make_genepool(size=3):
    # create a genepool consisting of a number of random genomes
    genepool = []
    for i in range(size):
        genepool.append(random_genome())
    df = pd.DataFrame(genepool)

    return df


def load_genepool(filename='genepool.csv'):
    # loads a genepool from a given file
    df = pd.read_csv(filename, index_col=0)

    return df


def save_genepool(df, filename='genepool.csv'):
    # saves a genepool to a given file
    df.to_csv(filename)

    return


def set_colors(genes, rgb=[0.8, 0.5, 0.2], random_colors=True):
    # change a genes color values
    if random_colors:
        genes['red'] = random_color()
        genes['green'] = random_color()
        genes['blue'] = random_color()
    else:
        genes['red'] = 100 + int(rgb[0] * 155)
        genes['green'] = 100 + int(rgb[1] * 155)
        genes['blue'] = 100 + int(rgb[2] * 155)
    return genes


def random_color():
    # get a random color value
    return 100 + int(random.uniform(0, 155))