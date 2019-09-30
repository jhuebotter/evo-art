import threading
import time
import pygame
import math
import time
import pandas as pd
from music import *
from threading import Thread
from genetics import *
from psonic import *
from geometry import *
'''
import other script
threading
start main
gemoetry as thread
music as thread
start config listener as thread
config pops up as a terminal

'''



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

exitFlag = 0



class Viz (threading.Thread):
   def __init__(self, threadID, name, counter):
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.name = name
      self.counter = counter
   def run(self):
      print("Starting ",  self.name)

      # start clock
      clock = pygame.time.Clock()

      # ---  Here we init the genes --- #
      df = make_genepool(4)
      df.to_csv('genepool.csv')
      # genepool = df.to_dict(orient='records')

      # to load the genepool
      df = pd.read_csv('genepool.csv', index_col=0)
      # genepool = df.to_dict(orient='records')  # [genes1]

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
      self.exit()

      # Stop running processes in Sonic Pi
      run("""'/stop-all-jobs'""")

      return

      print("Exiting", self.name)

class Evo(threading.Thread):
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter

    def run(self):
        print("Starting ", self.name)

        # setup listeners in sonic pi
        setup_listeners()


        print("Exiting ", self.name)











# Create new threads
thread1 = Viz(1, "VISUALIZATION", 1)
thread2 = Evo(2, "EVOLUTION", 2)

# Start new Threads
thread1.start()
thread2.start()

print("Exiting Main Thread")