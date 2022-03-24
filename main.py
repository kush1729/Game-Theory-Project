# -*- coding: utf-8 -*-
"""
Created on Wed Mar 23 17:31:17 2022

@author: kushs
"""

import sys
import os
folder = os.getcwd()
sys.path.append(folder+"\\modules")
sys.path.append(folder)

import traceback, pygame as pg

import GUI as gui
import simulation as sim
import numpy as np


pg.init()
display_width = 600
display_height = 400
screen = pg.display.set_mode((display_width, display_height))


TOT_SPECIES = 5
sim.TOT_SPECIES = TOT_SPECIES

FPS = 30


predRates = np.zeros((TOT_SPECIES,TOT_SPECIES))

p1 = 0.5
p2 = 0.5
s = 1.2
predRates[4,0] = s
for k in range(TOT_SPECIES-1):
  predRates[k,k+1] = 1
  if k+2 < TOT_SPECIES: predRates[k,k+2] = p1
  if k+3 < TOT_SPECIES: predRates[k,k+3] = p2

def Quit():
    pg.display.quit()
    pg.quit()
    quit()

def runSimulation():
  screen.fill(gui.BLACK)
  simulator = sim.WellMixed(predRates, [500000000 for _ in range(TOT_SPECIES)])
  simulationArea = pg.Surface((display_width-20, display_height-20))
  simulationAreaRect = simulationArea.get_rect()
  simulationAreaRect.center = (display_width//2-10, display_height//2 -10)
  simulator.startSimulation(simulationArea, display_width, display_height)
  clock = pg.time.Clock()
  while True:
    simulator.simulate(simulationArea, display_width, display_height)
    for event in pg.event.get():
      simulator.eventHandler(event)
      if event.type == pg.QUIT:
        Quit()
      elif event.type == pg.KEYDOWN:
        if event.key == pg.K_ESCAPE:
          Quit()

    screen.blit(simulationArea, simulationAreaRect)
    pg.display.update()
    clock.tick(FPS)

try:
  runSimulation()
except Exception as e:
  with open("LOG_FILE.txt", "w") as f:
    f.write(traceback.format_exc())
    pg.quit()
    quit()