import pygame
import math
from music import *

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
    i = 0.

    genes1 = dict(size=40, order=3, color=GREEN, number=3, factor=2., line=1, speed=3., delta_offset=-0.,
                  initial_offset=0, center=center, cutoff=70, amp=1., decay=0.05, decay_level=0.0,
                  sustain=0.3, sustain_level=0.5, release=5, detune=0.4, env_curve=7, mod_pulse_width=0.5)
    genes2 = dict(size=80, order=4, color=RED, number=3, factor=2., line=1, speed=8., delta_offset=-0.,
                  initial_offset=22.5, center=center, cutoff=70, amp=1., decay=0.05, decay_level=0.0,
                  sustain=0.3, sustain_level=0.5, release=5, detune=0.4, env_curve=7, mod_pulse_width=0.5)
    '''
    genes3 = dict(size=10, order=3, color=GREEN, number=5, factor=2., line=1, speed=3., delta_offset=1.,
                  initial_offset=0., center=center, cutoff=70, amp=1., decay=0.05, decay_level=0.0,
                  sustain=0.3, sustain_level=0.5, release=5, detune=0.4, env_curve=7, mod_pulse_width=0.5)
    genes4 = dict(size=10, order=3, color=GREEN, number=5, factor=2., line=1, speed=-3., delta_offset=-1.,
                  initial_offset=0., center=center, cutoff=70, amp=1., decay=0.05, decay_level=0.0,
                  sustain=0.3, sustain_level=0.5, release=5, detune=0.4, env_curve=7, mod_pulse_width=0.5)
    '''
    genepool = [genes1] #, genes2] #, genes3, genes4] #, genes5]

    # Loop until the user clicks the close button.
    done = False
    while not done:

        # This limits the while loop to a max of 10 times per second.
        # Leave this out and we will use all CPU we can.
        clock.tick(100)

        for event in pygame.event.get():  # User did something
            if event.type == pygame.QUIT:  # If user clicked close
                done = True  # Flag that we are done so we exit this loop

        # All drawing code happens after the for loop and but
        # inside the main while done==False loop.

        # Clear the screen and set the screen background
        screen.fill(BLACK)

        i += stepsize
        #if i > 360.:
        #    i = 0.

        for genes in genepool:
            #genes['current_offset'] = i * genes['speed']
            make_polygon(genes, i)

        # This MUST happen after all the other drawing commands.
        pygame.display.flip()
        # wait 60 ms until loop restart
        #pygame.time.wait(10)


    # Be IDLE friendly
    pygame.quit()

    return


def play_sound(genes):
    genes['note'] = math.log(genes['radius'], 2) * 12
    print(genes['note'])
    play_piano(genes)
    pass


def pol2cart(rho, phi, center=center):
    x = center[1] + rho * math.cos(math.radians(phi))
    y = center[0] - rho * math.sin(math.radians(phi))
    return [y, x]


def rotatePoint(polarcorner, angle, center=center):

    newPolarcorner = [polarcorner[0], polarcorner[1] + angle]

    return newPolarcorner


def make_polygon(genes, c):
    for i in range(genes['number']):
        genes['radius'] = genes['size'] * (genes['factor']**(i))
        prev_angle = round((genes['delta_offset'] * (c-stepsize) + genes['initial_offset']) * i + genes['speed'] * (c-stepsize), 3)
        current_angle = round((genes['delta_offset'] * c + genes['initial_offset']) * i + genes['speed'] * c, 3)
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