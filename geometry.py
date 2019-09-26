import pygame
import math
import time
import pandas as pd
from music import *
from threading import Thread
from genetics import *
from psonic import *


# Define some notes for conversion
C, Cs, D, Ds, E, F, Fs, G, Gs, A, As, B = range(24, 36)

# Initialize the game engine
pygame.init()

# Define the colors we will use in RGB format
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (100, 100, 200)
GREEN = (100, 200, 100)
RED = (200, 100, 100)


# instuments
synths = ['beep', 'dull_bell', 'mod_pulse', 'mod_sine', 'sine']
high_percs = ['drum_cymbal_pedal', 'drum_cymbal_closed', 'drum_tom_hi_soft', 'perc_bell', 'ambi_choir', 'tabla_tun1', 'tabla_tun3', 'tabla_tas3']
low_percs = ['elec_soft_kick', 'tabla_ke2', 'drum_bass_soft', 'drum_tom_mid_soft', 'tabla_re']
snares = ['tabla_na_s', 'elec_wood', 'drum_snare_soft']
bass = ['bass_hard_c', 'bass_hit_c', 'bass_voxy_hit_c', 'mehackit_phone1']
vox = ['ambi_choir']

instruments = [synths, bass, snares, high_percs, low_percs, synths, high_percs, synths, synths, bass]

# Set the height and width of the screen
size = [1200, 800]
center = [size[0] / 2, size[1] / 2]
screen = pygame.display.set_mode(size)
pos_line = [[center[0], 0], center]
linewidth = 1

# Set the scaling factor of the visualization between 0.1 and 0.5
SCALING_FACTOR = 0.3

# Set the maximum iterations per second
fps = 60

pygame.display.set_caption("Evo Art")


def main():

    clock = pygame.time.Clock()

    # ---  Hhere we init the genes -------------------- #
    #for i in range(len(instruments)):
    genes = [dict(instrument=x) for x in range(len(instruments))]
    df = make_genepool(6, genes)
    print(df.head())
    df.to_csv('genepool.csv')

    #genepool = df.to_dict(orient='records')

    # to load the genepool
    df = pd.read_csv('genepool.csv', index_col=0)
    #genepool = df.to_dict(orient='records')  # [genes1]

    #setup_listeners2(df, df['instrument'].values)
    setup_listeners()



    # get some time info
    start = time.time()
    now = time.time()

    # Loop until the user clicks the close button.
    done = False
    while not done:

        # This limits the while loop to a max of 10 times per second.
        # Leave this out and we will use all CPU we can.
        clock.tick(fps)

        # Time each iteration to know how far to move the geometry
        t_minus1 = now - start
        now = time.time()
        t0 = now - start
        delta_t = t0 - t_minus1
        #print(delta_t)

        for event in pygame.event.get():  # User did something
            if event.type == pygame.QUIT:  # If user clicked close
                done = True  # Flag that we are done so we exit this loop

        df = pd.read_csv('genepool.csv', index_col=0)
        genepool = df.to_dict(orient='records')
        # All drawing code happens after the for loop and but
        # inside the main while done==False loop.
        # Clear the screen and set the screen background
        screen.fill(BLACK)
        pygame.draw.polygon(screen, WHITE, pos_line, 1)
        # This is where the magic happens
        for genes in genepool:
            phenotype = make_phenotype(genes)
            make_polygon(phenotype, t0, delta_t)


        # This MUST happen after all the other drawing commands.
        pygame.display.flip()

    # Be IDLE friendly
    pygame.quit()

    # Stop running processes in Sonic Pi
    run("""'/stop-all-jobs'""")
    #run("""use_osc "localhost", 5000
    #        osc '/stop'""")
    print('Stopped program')

    return


def play_sound(genes):
    print()
    print('Note:  ', genes['note'])
    print('Radius:', genes['radius'])
    #process = Thread(target=play_piano, args=[genes])
    #process.start()
    play_synth(genes)
    return


def pol2cart(rho, phi, center=center):
    # get cartesian coordinates from polar
    x = center[1] + rho * math.cos(math.radians(phi + 180))
    y = center[0] - rho * math.sin(math.radians(phi + 180))

    return [y, x]


def rotatePoint(polarcorner, angle, center=center):
    # the name explains this pretty well i think
    newPolarcorner = [polarcorner[0], polarcorner[1] + angle]

    return newPolarcorner


def make_polygon(genes, t, delta_t):
    for i in range(genes['number']):
        factor = round(1. / math.cos(math.radians(180./genes['order'])), 3)
        #print(factor)
        #genes['note'] = genes['rootnote'] + 12 * ((genes['rootoctave'] - 1) + (i * factor / 2.))
        #genes['radius'] = round((genes['rootnote']) * (factor ** ((i + genes['rootoctave'] - 1))), 3)
        #genes['radius'] = round((genes['rootnote'] + (12 * (genes['rootoctave'] - 1))) * ((factor**(i))), 3)
        #genes['note'] = genes['rootnote'] + 12 * ((genes['rootoctave'] - 1) + math.log2(factor) * i)  # + (factor*i))
        #genes['radius'] = 50 + 440 * 10 ** (math.log(2) * (genes['note'] / genes['rootoctave'] * factor))

        genes['note'] = genes['rootnote'] + 12 * ((genes['rootoctave'] - 1) + math.log2(factor) * i)  # + (factor*i))
        genes['radius'] = SCALING_FACTOR * 440 * 10 ** (math.log(2, 10) * (genes['note'] - 69) / 12)


        # get the rotation angles
        prev_angle = round((t-delta_t) * (360. / genes['order']) * (genes['bpm'] / 60.), 3)
        current_angle = round(t * (360. / genes['order']) * (genes['bpm'] / 60.), 3)
        prev_angle += (genes['initial_offset'] * i + genes['total_offset']) * (360. / genes['order'])
        current_angle += (genes['initial_offset'] * i + genes['total_offset']) * (360. / genes['order'])

        pos = []
        for o in range(genes['order']):
            polarcorner = [genes['radius'], o*(360/genes['order'])]
            prev_polarcorner = rotatePoint(polarcorner, prev_angle, center=center)
            polarcorner = rotatePoint(polarcorner, current_angle, center=center)
            prev_polarcorner[1] = round(prev_polarcorner[1] % 360., 3)
            polarcorner[1] = round(polarcorner[1] % 360., 3)
            delta = abs(polarcorner[1] - prev_polarcorner[1])
            if delta > 180.:
                play_synth(genes)
            corner = pol2cart(polarcorner[0], polarcorner[1])
            pos.append(corner)
        print((genes['red'], genes['red'], genes['blue']))
        pygame.draw.polygon(screen, (genes['red'], genes['green'], genes['blue']), pos, linewidth)


    return

if __name__ == "__main__":
    main()