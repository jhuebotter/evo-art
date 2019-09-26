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

exitFlag = 0

class Viz (threading.Thread):
   def __init__(self, threadID, name, counter):
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.name = name
      self.counter = counter
   def run(self):
      print "Starting " + self.name


      print "Exiting " + self.name

def print_time(threadName, counter, delay):
   while counter:
      if exitFlag:
         threadName.exit()
      time.sleep(delay)
      print "%s: %s" % (threadName, time.ctime(time.time()))
      counter -= 1

# Create new threads
thread1 = myThread(1, "VISUALIZATION", 1)
thread2 = myThread(2, "MUSIC", 2)

# Start new Threads
thread1.start()
thread2.start()

print "Exiting Main Thread"