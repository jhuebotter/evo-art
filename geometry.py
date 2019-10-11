import pygame
import math
import time
import pandas as pd
from music import *
from genetics import *
from psonic import *
from presets import *
from autopilot import *
import json

# Set the height and width of the screen
size = [1400, 700]
center = [size[0] / 2, size[1] / 2]
pos_line = [[center[0], 0], center]

# Set the scaling factor of the visualization between 0.1 and 0.5
SCALING_FACTOR = 0.5

# How thick are the lines on the screen
LINEWIDTH = 2

# Set the maximum iterations per second
FPS = 60

# Define some colors for the screen
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Initialize the game engine
pygame.init()
pygame.display.set_caption("Evo Art")
screen = pygame.display.set_mode(size)

def main():

    print("Starting geometry main function.")
    time.sleep(1)
    clock = pygame.time.Clock()

    # ---  Here we init the genes -------------------- #
    '''
    #for i in range(len(instruments)):
    genes = [dict(instrument=x) for x in range(len(instruments))]
    df = make_genepool(1, genes)
    #print(df.head())
    df.to_csv('genepool.csv')

    #genepool = df.to_dict(orient='records')

    # to load the genepool
    #df = pd.read_csv('genepool.csv', index_col=0)
    #genepool = df.to_dict(orient='records')  # [genes1]
    '''
    # make sure we have our config files
    preset_path = read_preset_path()
    preset_config = load_config(preset_path)

    # set csv of currently playing instrument
    playing = preset_path + 'current/playing.txt'

    #setup_listeners2(df, df['instrument'].values)
    setup_listeners2()

    # get some time info
    start = time.time()
    now = time.time()

    # Loop until the user clicks the close button.
    done = False
    i = 0
    while not done:

        # This limits the while loop to a max of 10 times per second.
        # Leave this out and we will use all CPU we can.
        clock.tick(FPS)

        # Time each iteration to know how far to move the geometry
        t_minus1 = now - start
        now = time.time()
        t0 = now - start
        delta_t = t0 - t_minus1
        #print(delta_t)

        if i % FPS == 0:

            print(i)

            # make sure we have our config files
            preset_path = read_preset_path()
            preset_config = load_config(preset_path)

            # set csv of currently playing instrument
            playing = preset_path + 'current/playing.csv'

            for event in pygame.event.get():  # User did something
                if event.type == pygame.QUIT:  # If user clicked close
                    done = True  # Flag that we are done so we exit this loop

            try:
                df = load_genepool(playing)
            except:
                print('error loading genepool')
                pass

            phenotypes = df.to_dict(orient='records')

        i += 1

        # All drawing code happens after the for loop and but
        # inside the main while done==False loop.
        # Clear the screen and set the screen background
        screen.fill(BLACK)
        pygame.draw.polygon(screen, WHITE, pos_line, 1)

        # This is where the magic happens
        for phenotype in phenotypes:
            #phenotype = make_phenotype(genes)
            make_polygon(phenotype, t0, delta_t)

        # This MUST happen after all the other drawing commands.
        pygame.display.flip()

    # Be IDLE friendly
    pygame.quit()

    stop_all_listeners()

    #run("""use_osc "localhost", 5000
    #        osc '/stop'""")
    print('Stopped program')

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

    # Now this is where the magic happens...

    for i in range(genes['number']):
        factor = round(1. / math.cos(math.radians(180./genes['order'])), 3)

        genes['note'] = genes['rootnote'] + 12 * ((genes['rootoctave'] - 1) + math.log2(factor) * i)  # + (factor*i))
        genes['radius'] = SCALING_FACTOR * 440 * 10 ** (math.log(2, 10) * (genes['note'] - 69) / 12)

        shape_base_note = genes['note'] if i == 0 else shape_base_note
        genes['pitch'] = ((genes['note'] - shape_base_note) / 24 * 12) * 2


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
        pygame.draw.polygon(screen, (genes['red'], genes['green'], genes['blue']), pos, LINEWIDTH)

    return