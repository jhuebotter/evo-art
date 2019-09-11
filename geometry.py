import pygame
import math
import time
from music import *

# Define some notes for conversion
C, Cs, D, Ds, E, F, Fs, G, Gs, A, As, B = range(24, 36)

# Initialize the game engine
from typing import Any
pygame.init()

# Define the colors we will use in RGB format
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (100, 100, 200)
GREEN = (100, 200, 100)
RED = (200, 100, 100)


# Set the height and width of the screen
size = [1440, 900]
center = [size[0] / 2, size[1] / 2]
screen = pygame.display.set_mode(size)

# Set the maximum iterations per second
fps = 100
stepsize = 0.2

pygame.display.set_caption("Evo Art")

'''
polar2z = lambda r,θ: r * exp( 1j * θ )
polar2xy = lambda r,θ: (np.real(r * exp( 1j * θ )) + center[0], np.imag(r * exp( 1j * θ )) + center[1])
z2polar = lambda z: ( abs(z), angle(z) )
xy2polar = lambda x,y: (np.sqrt(x**2 + y**2), np.arctan2(y, x))
'''

def main():

    clock = pygame.time.Clock()

    genes1 = dict(rootnote=C, rootoctave=4, size=40, order=6, color=GREEN, number=3, line=1,
                  delta_offset=0., bpm=60, total_offset=0.,
                  initial_offset=0.5, center=center, cutoff=50, amp=0.5, decay=0.05, decay_level=0.0,
                  sustain=0.3, sustain_level=0.5, release=5, detune=0.4, env_curve=7, mod_pulse_width=0.5)
    genes2 = dict(rootnote=A, rootoctave=3, size=40, order=8, color=GREEN, number=2, line=1,
                  delta_offset=0., bpm=60, total_offset=0.,
                  initial_offset=0.5, center=center, cutoff=70, amp=0.5, decay=0.05, decay_level=0.0,
                  sustain=0.3, sustain_level=0.5, release=5, detune=0.4, env_curve=7, mod_pulse_width=0.5)

    genepool = [genes1]

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
        # print(delta_t)

        for event in pygame.event.get():  # User did something
            if event.type == pygame.QUIT:  # If user clicked close
                done = True  # Flag that we are done so we exit this loop

        # All drawing code happens after the for loop and but
        # inside the main while done==False loop.
        # Clear the screen and set the screen background
        screen.fill(BLACK)

        # This is where the magic happens
        for genes in genepool:
            make_polygon(genes, t0, delta_t)

        # This MUST happen after all the other drawing commands.
        pygame.display.flip()



    # Be IDLE friendly
    pygame.quit()

    return


def play_sound(genes):
    print()
    print('Note:  ', genes['note'])
    print('Radius:', genes['radius'])
    play_piano(genes)
    return


def pol2cart(rho, phi, center=center):
    # get cartesian coordinates from polar
    x = center[1] + rho * math.cos(math.radians(phi))
    y = center[0] - rho * math.sin(math.radians(phi))

    return [y, x]


def rotatePoint(polarcorner, angle, center=center):
    # the name explains this pretty well i think
    newPolarcorner = [polarcorner[0], polarcorner[1] + angle]

    return newPolarcorner


def make_polygon(genes, t, delta_t):
    for i in range(genes['number']):
        factor = round(1. / math.cos(math.radians(180./genes['order'])), 3)
        #print(factor)
        genes['note'] = genes['rootnote'] + (12 * (i + genes['rootoctave'] - 1) * factor / 2.)
        genes['radius'] = ((genes['rootnote']) * (factor**((i + genes['rootoctave'] - 1))))

        # get the rotation angles
        prev_angle = round((t-delta_t) * (360. / genes['order']) * (genes['bpm'] / 60.), 3)
        current_angle = round(t * (360. / genes['order']) * (genes['bpm'] / 60.), 3)
        prev_angle += (genes['initial_offset'] * i + genes['total_offset']) * (360. / genes['order'])
        current_angle += (genes['initial_offset'] * i + genes['total_offset']) * (360. / genes['order'])

        pos = []
        for o in range(genes['order']):
            polarcorner = [genes['radius'], o*(360/genes['order'])]
            prev_polarcorner = rotatePoint(polarcorner, prev_angle, center=genes['center'])
            polarcorner = rotatePoint(polarcorner, current_angle, center=genes['center'])
            prev_polarcorner[1] = round(prev_polarcorner[1] % 360., 3)
            polarcorner[1] = round(polarcorner[1] % 360., 3)
            delta = abs(polarcorner[1] - prev_polarcorner[1])
            if delta > 180.:
                play_sound(genes)
            corner = pol2cart(polarcorner[0], polarcorner[1])
            pos.append(corner)
        pygame.draw.polygon(screen, genes['color'], pos, genes['line'])

    return

if __name__ == "__main__":
    main()