# -*- coding: utf-8 -*-
"""
Created on Sun Mar 13 17:02:13 2022

@author: kushs
"""
import numpy as np
import random as rnd
import pygame as pg
import GUI as gui

TOT_SPECIES = 5

class Simulation(object):
  #Just carries basic information on predator rates, and carries the method to simulate a (random) game.
  
  def __init__(self, predRates = np.zeros((TOT_SPECIES, TOT_SPECIES), float)):
    self.predRates = predRates
    self.total = np.sum(predRates)
    self.run = False
    
  def playOff(self, attacker, defender):#carries out a simulation of species <attacker> attacking species <defender>. Returns True if defender loses, else False.
    if attacker == defender or self.predRates[attacker, defender] == 0: return False
    prob = rnd.random() * self.total 
    return (prob < self.predRates[attacker, defender])
  
  @staticmethod
  def weightedChoice(weights, totWeights = None):#chooses an index i of the iterable <weights> with probability proportional to <weights>[i]
    if totWeights == None: totWeights = sum(weights)
    x = rnd.randint(1, totWeights)
    i = -1
    while x > 0:
      i += 1
      x -= weights[i]
    return i
  
  def eventHandler(self, event):
    if event.type == pg.KEYDOWN:
      if event.key == pg.K_p:
       self.run = not self.run
  
  def startSimulation(self, screen, width, height):
    self.run = True
    self.updateScreen(screen, width, height)
  
  def updateScreen(self, screen, width, height):
    pass
  
  def simulate(self, screen, width, height):
    pass
    
  
  
  
class WellMixed(Simulation):
  #Carries all information for the well-mixed case
  def __init__(self, predRates = np.zeros((TOT_SPECIES, TOT_SPECIES), float), speciesPopulation = [1 for _ in range(TOT_SPECIES)], numStepsPerUpdate = 100):
    super(Simulation, self).__init__(predRates)
    self.speciesPop = speciesPopulation
    self.totPop = sum(self.speciesPop)
    self.numStepsPerUpdate = numStepsPerUpdate
    self.A = self.predRates[0,2] * self.predRates[1,4] + self.predRates[1,2]*self.predRates[4,0] - self.predRates[0,1]*self.predRates[2,4] 
    self.B = self.predRates[0,3] * self.predRates[1,4] + self.predRates[1,3]*self.predRates[4,0] - self.predRates[0,1] * self.predRates[3,4] 
    self.C = self.predRates[0,3] * self.predRates[2,4] + self.predRates[2,3] * self.predRates[4,0]-self.predRates[0,2] * self.predRates[3,4]
    
    
  def MonteCarloStep(self):
     attacker = Simulation.weightedChoice(self.speciesPop, self.totPop)
     defender = Simulation.weightedChoice(self.speciesPop[:attacker]+self.speciesPop[attacker+1:], self.totPop - self.speciesPop[attacker])
     if defender >= attacker: defender += 1
     success = self.playOff(attacker, defender)
     if success:
       self.speciesPop[defender] -= 1
       self.speciesPop[attacker] += 1
  
  def updateScreen(self, screen, width, height):
    screen.fill(gui.BLACK)
    gui.message_to_screen(screen, "Total Population = %d"%self.totPop, gui.WHITE, (width//2, 30), 25)
    for k in range(TOT_SPECIES):
      gui.message_to_screen(screen, "Species %d = %d"%(k+1, self.speciesPop[k]), gui.WHITE, (width//2, 30*(k+2)), 25)
    gui.message_to_screen(screen, "A = %.2f, B = %.2f, C = %.2f"%(self.A, self.B, self.C), gui.WHITE, (width//2, 30*(TOT_SPECIES+2)), 25)
    if self.A >0 and self.B > 0:
      prediction = "exactly one or all three of 1, 2, 5 survive; 3, 4 eventually will die"
    elif self.A < 0 and self.C > 0:
      prediction = "exactly one or all three of 1, 3, 5 survive; 2, 4 eventually will die"
    elif self.B < 0 and self.C < 0:
      prediction = "exactly one or all three of 1, 4, 5 survive; 2, 3 eventually will die"
    elif self.A*self.B < 0 and self.A*self.C > 0:
      prediction = "All 5 can coexist"
    else:
      prediction = "unknown"
    gui.message_to_screen(screen, "Prediction: %s"%prediction, gui.WHITE, (width//2, 30*(TOT_SPECIES+3)), 25)
  
  def simulate(self, screen, width, height):
    if self.run:
      for _ in range(self.numStepsPerUpdate):
        self.MonteCarloStep()
    self.updateScreen(screen, width, height)
  