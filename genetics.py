import random
import pandas as pd

size = [1920, 1080]
center = [size[0] / 2, size[1] / 2]

#synths = ['blade', 'sine', 'pretty_bell', 'dull_bell', 'dpulse']
#synths = ['piano', 'mod_synth', 'bass', 'kick']
#samples = ['elec_soft_kick', 'sn_dub', 'tabla_ke3', 'tabla_na_s', 'elec_wood', 'bass_voxy_hit_c', 'drum_cowbell', 'drum_cymbal_pedal']

# instuments
synths = ['blade', 'mod_pulse', 'mod_sine', 'pretty_bell']
#synths = ['saw', 'sine', 'pluck']
high_percs = ['drum_cymbal_pedal', 'drum_cymbal_closed', 'drum_tom_hi_soft', 'perc_bell', 'ambi_choir', 'tabla_tun1', 'tabla_tun3', 'tabla_tas3']
low_percs = ['elec_soft_kick', 'tabla_ke2', 'drum_bass_soft', 'drum_tom_mid_soft', 'tabla_re']
#snares = ['tabla_na_s', 'elec_wood', 'drum_snare_soft']
snares = ['drum_snare_soft']
bass = ['bass_hard_c', 'bass_hit_c', 'bass_voxy_hit_c', 'mehackit_phone1']
vox = ['ambi_choir']

instruments = [synths, low_percs, snares, high_percs, synths, synths, high_percs, synths, bass, bass]


def random_genome():
    # creates a semi random genome
    genes = dict(rootnote=random.random(),
                 rootoctave=random.random(),
                 order=random.random(),#
                 number=random.random(),
                 bpm=random.random(),
                 total_offset=random.random(),
                 initial_offset=random.random(),
                 red=random.random(), green=random.random(), blue=random.random(),
                 nature=random.random(),
                 instrument=random.random(),
                 # this is all relevant for a synth
                 amp=random.random(),
                 cutoff=random.random(),
                 pan=random.random(),
                 attack=random.random(),
                 release=random.random(),
                 mod_range=random.random(),
                 mod_phase=random.random(),
                 #effect stuff
                 mix_reverb=random.random(),
                 mix_echo=random.random(),
                 # Now the sample related stuff
                 pitch=random.random()
                 )

    return genes

def make_phenotype(genes):
    # creates a semi random genome
    phenotype = dict(rootnote=int(genes['rootnote'] * 12 + 24),
                 rootoctave=int(genes['rootoctave'] * 3 + 3),
                 order=int(genes['order'] * 9 + 3),
                 number=int(genes['number'] * 4 +1),
                 bpm=int(15*2**int(genes['bpm']*3)),
                 total_offset=(1/16) * int(genes['total_offset'] * 16) * 0.5**int(genes['bpm']*3),
                 initial_offset=(1/16) * int(genes['initial_offset'] * 16) * 0.5**int(genes['bpm']*3),
                 red=int(genes['red'] * 155 + 100), green=int(genes['green'] * 155 + 100),
                 blue=int(genes['blue'] * 155 + 100),
                 nature=int(genes['nature']*4),
                 instrument=int(genes['instrument']*4),
                 # this is all relevant for a synth
                 amp=round(genes['amp'] / 3 + 0.5, 2),
                 cutoff=int(genes['cutoff'] * 70 + 30 ),
                 pan=round(genes['pan'] - 0.5, 2),
                 attack=round(genes['attack'] / 2, 2),
                 release=round(genes['release'], 2),
                 mod_range=int(genes['mod_range'] * 10 + 2),
                 mod_phase=round(genes['mod_phase'] * .7 + .1, 2),
                 #effect stuff
                 mix_reverb=round(genes['mix_reverb'] * .7 + .3, 2),
                 mix_echo=round(genes['mix_echo'] * .7, 2),
                 # Now the sample related stuff
                 pitch=int(genes['pitch'] * 24 - 12)
                 )

    return phenotype


def random_genotype_old():
    # creates a semi random genome
    genes = dict(rootnote=random.randint(24, 35),
                 rootoctave=random.randint(4, 5),
                 order=random.choice([3, 4, 5, 6, 7, 8, 10]),#
                 number=random.randint(3, 4),
                 bpm=random.choice([15, 30, 60]),
                 total_offset=0., #0.125 * random.randint(0, 7),
                 initial_offset= 0.,#* random.randint(0, 16),#0.25 * random.randint(1, 4), delta_offset=0.,
                 red=random_color(), green=random_color(), blue=random_color(), line=2, center=center,
                 nature=random.randint(0, 5),#random.randint(0, len(instruments) - 1),
                 # this is all relevant for a synth
                 synth=random.randint(0,len(synths)-1),
                 amp=.1 * random.randint(1, 8),
                 cutoff=random.randint(30, 100),
                 pan=random.uniform(-.5, .5),
                 attack=random.uniform(0., .0),
                 attack_level=1.,
                 decay=random.uniform(0., .5),
                 decay_level=0.,
                 sustain=random.uniform(0., .5),
                 sustain_level=0.,
                 release=random.uniform(0., 1.),
                 env_curve=random.choice(['2, 3, 7']),
                 mod_range=random.choice([2, 5, 7, 12]),
                 #effect stuff
                 mix=random.uniform(.3, 1.),
                 mix_echo=random.uniform(.1, .8),
                 # Now the sample related stuff
                 high_perc=random.randint(0, len(high_percs)-1),
                 low_perc=random.randint(0, len(low_percs)-1),
                 # bass related (including pitch for the sample
                 bass=random.randint(0, len(bass)-1),
                 pitch=random.randint(-5, 7),
                 #added snare drum
                 snare=random.randint(0, len(snares)-1),
                 vox=0
                 )

    return genes


def map_genes(genes):
    genes['initial_offset'] = 2**genes['bpm']
    genes['bpm'] = 15 * 2 ** genes['bpm']
    return genes

def add_genes(df, genes):
    # adds any genes to a geneome
    df.append(genes, ignore_index=True)

    return df


def make_genepool(size=3, crispr=[dict()]):
    # create a genepool consisting of a number of random genomes
    genepool = []

    for i in range(size):
        gen = random_genome()
        #for k, v in crispr[i].items():
        #    gen[k] = v
        genepool.append(gen)

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

gen = random_genome()

phen = make_phenotype(gen)
print(phen)