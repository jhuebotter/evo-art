import random
import pandas as pd

size = [1920, 1080]
center = [size[0] / 2, size[1] / 2]

#synths = ['blade', 'sine', 'pretty_bell', 'dull_bell', 'dpulse']
#synths = ['piano', 'mod_synth', 'bass', 'kick']
#samples = ['elec_soft_kick', 'sn_dub', 'tabla_ke3', 'tabla_na_s', 'elec_wood', 'bass_voxy_hit_c', 'drum_cowbell', 'drum_cymbal_pedal']

synths = ['beep', 'dull_bell', 'mod_pulse', 'mod_sine', 'sine']
high_percs = ['drum_cymbal_pedal', 'drum_cymbal_closed', 'drum_tom_hi_soft', 'perc_bell', 'ambi_choir', 'tabla_tun1', 'tabla_tun3', 'tabla_tas3']
low_percs = ['elec_soft_kick', 'tabla_ke2', 'drum_bass_soft', 'drum_tom_mid_soft', 'tabla_re']
snares = ['tabla_na_s', 'elec_wood', 'drum_snare_soft']
bass = ['bass_hard_c', 'bass_hit_c', 'bass_voxy_hit_c', 'mehackit_robot3', 'mehackit_phone1']
vox = ['ambi_choir']

def random_genome():
    # creates a semi random genome
    genes = dict(rootnote=24,#random.randint(24, 35),
                 rootoctave=random.randint(3, 4),
                 order=random.choice([3, 4, 5, 6]),#random.randint(3,12),
                 number=random.randint(1, 6),
                 bpm=random.choice([15, 30, 60]),
                 total_offset=0.,#0.75, #0.125 * random.randint(0, 7),
                 initial_offset=.5,#0.25 * random.randint(1, 4), delta_offset=0.,
                 red=random_color(), green=random_color(), blue=random_color(), line=1, center=center,
                 # this is all relevant for a synth
                 synth=random.randint(0,len(synths)-1),
                 amp=.1 * random.randint(1, 4),
                 pan=random.uniform(-.5, .5),
                 attack=random.uniform(0., .8),
                 attack_level=1.,
                 decay=random.uniform(0., .5),
                 decay_level=0.,
                 sustain=random.uniform(0., 1.),
                 sustain_level=0.,
                 release=random.uniform(0., .5),
                 env_curve=random.choice(['2, 3, 7']),
                 mix=random.uniform(.3, 1.),
                 mod_range=random.choice([5, 7, 12]),
                 # Now the sample related stuff
                 nature=random.randint(0, 100),
                 high_perc=random.randint(0, len(high_percs)-1),
                 low_perc=random.randint(0, len(low_percs)-1),
                 bass=random.randint(0, len(bass)-1),
                 snare=random.randint(0, len(snares)-1),
                 vox=0
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