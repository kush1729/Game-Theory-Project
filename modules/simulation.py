# -*- coding: utf-8 -*-
"""
Created on Sun Mar 13 17:02:13 2022

@author: kushs
"""
import random as rnd
import pygame as pg
import GUI as gui
#import time

TOT_SPECIES = 5
SPECIES_NAME = ["Species %i"%i for i in range(1, TOT_SPECIES+1)]

class Simulation(object):
  #Just carries basic information on predator rates, and carries the method to simulate a (random) game.
  
  def __init__(self, width, height, predRates, numStepsPerUpdate = 5):
    self.predRates = predRates
    self.numStepsPerUpdate = numStepsPerUpdate
    self.run = False
    self.width = width
    self.height= height
    self.A = 0
    self.B = 0
    self.C = 0
    self.calculatePredictors()
  
  def calculatePredictors(self):
    self.A = self.predRates[0][2] * self.predRates[1][4] + self.predRates[1][2]*self.predRates[4][0] - self.predRates[0][1]*self.predRates[2][4] 
    self.B = self.predRates[0][3] * self.predRates[1][4] + self.predRates[1][3]*self.predRates[4][0] - self.predRates[0][1] * self.predRates[3][4] 
    self.C = self.predRates[0][3] * self.predRates[2][4] + self.predRates[2][3] * self.predRates[4][0]-self.predRates[0][2] * self.predRates[3][4]
    
  @staticmethod
  def weightedChoice(weights, totWeights = None, backUp = None):#chooses an index i of the iterable <weights> with probability proportional to <weights>[i]
    if totWeights == None: totWeights = sum(weights)
    if weights == [] or totWeights == 0 and backUp != None:
      weights = backUp
      totWeights = sum(weights)
    x = rnd.randint(1, totWeights)
    i = -1
    while x > 0:
      i += 1
      x -= weights[i]
    return i
  
  def eventHandler(self, event):
    if event.type == pg.KEYDOWN:
      if event.key == pg.K_p:
       self.toggle_pause()
  
  def startSimulation(self, screen, run = False):
    self.run = not run
    self.toggle_pause()
    self.updateScreen(screen)
  
  def updateScreen(self, screen):
    pass
  
  def simulate(self, screen):
    pass
  
  def updateRates(self, newVal, attacker, defender):
    self.predRates[attacker][defender] = newVal
    self.calculatePredictors()
    
  def getPredictionMessage(self, hedge = False):
    if hedge: s = 'are supposed to '
    else: s = ''
    if self.A >0 and self.B > 0:
      return "%s & %s go %sextinct in the long run"%(SPECIES_NAME[2], SPECIES_NAME[3], s)
    elif self.A < 0 and self.C > 0:
      return "%s & %s go %sextinct in the long run"%(SPECIES_NAME[1], SPECIES_NAME[3], s)
    elif self.B < 0 and self.C < 0:
      return "%s & %s go %sextinct in the long run"%(SPECIES_NAME[1], SPECIES_NAME[2], s)
    elif self.A*self.B < 0 and self.A*self.C > 0:
      return "All 5 may stably coexist"
    else:
      return "Unknown"
    
  def toggle_pause(self):
    self.run = not self.run
  
  @staticmethod
  def colorToNumber(hue):
    """
  #  Does what is says. 
  #  This may need to be changed to account for RGBA 
    """
    if isinstance(hue, pg.Color):
      hue = (hue.r, hue.g, hue.b)
    elif isinstance(hue, tuple) and len(hue) == 4:
      hue = hue[:2]
    if hue == gui.BROWN:
      return 5
    elif hue == gui.RED:
      return 4
    elif hue == gui.BLUE:
      return 3
    elif hue == gui.YELLOW:
      return 2
    elif hue == gui.GREEN:
      return 1
    else:
      return -1
    #else:
     # raise Exception("Received Unexpected Colour " + str(hue)) #Might want to raise an exception or do something else this hopefully will just ensure the bad color always loses

  @staticmethod
  def numberToColor(number):
    if number == 5:
      return gui.BROWN
    elif number == 4:
      return gui.RED
    elif number == 3:
      return gui.BLUE
    elif number == 2:
      return gui.YELLOW
    elif number == 1:
      return gui.GREEN
    else:
      return gui.BROWN #This is sort of the default so all errors correct to this


  
  
  
class WellMixedRandom(Simulation):
  #Carries all information for the well-mixed case
  def __init__(self, width, height, predRates, speciesPopulation = [1 for _ in range(TOT_SPECIES)], numStepsPerUpdate = 5, maxKillCount = 150, fontSize = 20, margins = 15, FPS = 60):
    super(WellMixedRandom, self).__init__(width, height, predRates, numStepsPerUpdate)
    self.speciesPop = list(speciesPopulation)
    self.totPop = sum(self.speciesPop)
    self.total = sum(sum(l) for l in predRates)
    self.maxKillCount = maxKillCount
    self.graph = pg.Surface((self.width-5, 3*self.height / 4))
    self.graph.fill(gui.WHITE)
    self.graph_x_pos = 0
    self.graph_width, self.graph_height = self.graph.get_rect().size
    self.updateGraph= 0
    self.graphModulus = 10
    self.numZero = self.speciesPop.count(0) 
    #GUI
    #(self, x, y, width, height, action = RETURN_TRUE, inactivecolour = RED, activecolour = ORANGE, text = None, textcolour = BLACK, size = 25, border = None)
    self.fontSize = fontSize
    self.margins = margins
    self.predictionButton = gui.Button(margins, height - fontSize - 2*margins, int(fontSize * 15 * 0.6), fontSize+margins, inactivecolour = gui.RED, activecolour = gui.ORANGE, text = "Show Prediction", size = fontSize)
    self.showPrediction = False
    #(self, x, y, height, bkg_colour = WHITE, text_colour = BLACK, frozen_colour = GREY, cursorColour = BLACK, default = 0, freeze = False, tot_digits = 6, precision = 3, FPS = 30, rel_origin = (0,0), center_loc = None):
    self.populationInputs = [gui.InputNumberBox(0,0, fontSize, default = self.speciesPop[i], tot_digits = 10, precision = 0, FPS = FPS, center_loc = (int((i+1) * self.margins + (i+0.5) * (width - 6*margins)//5), height - 2 * margins - self.predictionButton.ht - fontSize//2)) for i in range(TOT_SPECIES)]
    
    self.change = False
  
  def updateRates(self, newVal, attacker, defender):
    super(WellMixedRandom, self).updateRates(newVal, attacker, defender)
    self.change = True
  
  def MonteCarloStep(self):  
     if self.numZero >= TOT_SPECIES-1: return
     attacker = Simulation.weightedChoice(self.speciesPop, self.totPop)
     defender = Simulation.weightedChoice(self.speciesPop[:attacker]+self.speciesPop[attacker+1:], self.totPop - self.speciesPop[attacker])
     if defender >= attacker: defender += 1
     if self.predRates[attacker][defender] == 0 and self.predRates[defender][attacker] == 0:
       return
     if self.predRates[attacker][defender] == 0 and self.predRates[defender][attacker] != 0:
       attacker, defender = defender, attacker
     x = self.predRates[attacker][defender] * self.maxKillCount / float(self.total) #* min(self.speciesPop[attacker], self.speciesPop[defender])
     if x>= 1:# or self.speciesPop[attacker] > self.speciesPop[defender]:
       x = int(min(self.speciesPop[defender], x))
       self.speciesPop[defender] -= x
       self.speciesPop[attacker] += x
       if self.speciesPop[defender]<0: 
         self.speciesPop[attacker] -= abs(self.speciesPop[defender])
         self.speciesPop[defender] = 0
     elif rnd.random() < x:
       self.speciesPop[defender] -= 1
       if self.speciesPop[defender]<0: 
         self.speciesPop[defender] = 0
       else:  
         self.speciesPop[attacker] += 1
     self.numZero = self.speciesPop.count(0) 
  
  def toggle_pause(self):
    self.run = not self.run
    for k in range(TOT_SPECIES):
        self.populationInputs[k].set_freeze(self.run)
        
  def eventHandler(self, event):
    super(WellMixedRandom, self).eventHandler(event)
    for k in range(TOT_SPECIES):
      if not self.run and self.populationInputs[k].update(event):
        self.speciesPop[k] = self.populationInputs[k].getValue()
        self.change = True
        self.totPop = sum(self.speciesPop)
  
  def updateScreen(self, screen):
    screen.fill(gui.BLACK)
    self.updateGraph %= self.graphModulus
    if self.run and self.updateGraph == 0:
        #pg.draw.line(self.graph, gui.WHITE, (self.graph_width, 0), (self.graph_width, self.graph_height), 1)
      y_start = 0
      if self.change:
        self.change = False
        pg.draw.line(self.graph, gui.BLACK, (self.graph_x_pos, 0), (self.graph_x_pos, self.graph_height), 1)
        if self.graph_x_pos == self.graph_width-1:
          self.graph.scroll(dx = -1)
        else: self.graph_x_pos += 1
        
      for i in range(TOT_SPECIES):
        line_height = int(round(self.graph_height * (float(self.speciesPop[i]) / float(self.totPop))))
        #if self.speciesPop[i] > 0 and line_height == 0: line_height = 1
        pg.draw.line(self.graph, self.numberToColor(i+1), (self.graph_x_pos, y_start), (self.graph_x_pos, y_start + line_height), 1)
        y_start += line_height
      if self.graph_x_pos == self.graph_width-1:
        self.graph.scroll(dx = -1)
      else: self.graph_x_pos += 1
      
    screen.blit(self.graph, (0,0))
    self.updateGraph+=1
    
    #InputBoxFunctionality
    rect = pg.Rect((0,0), (int((self.width - 6*self.margins)//5), self.fontSize + self.margins))
    for k in range(TOT_SPECIES):
      self.populationInputs[k].blit(screen)
      rect.center = (int((k+1) * self.margins) + int((k+0.5) * (self.width - 6*self.margins)//5), self.graph_height + 2* self.margins + self.fontSize//2)
      pg.draw.rect(screen, Simulation.numberToColor(k+1), rect, self.margins//2)
      gui.message_to_screen(screen, SPECIES_NAME[k], gui.WHITE, rect.center, self.fontSize)
    #Prediction Functionality
    if self.predictionButton.get_click():
      self.showPrediction = not self.showPrediction
      if self.showPrediction:
        self.predictionButton.text = "Hide Prediction"
      else:
        self.predictionButton.text = "Show Prediction"
    self.predictionButton.blit(screen)
    if self.showPrediction:
      gui.message_to_screen(screen, self.getPredictionMessage(), gui.WHITE, ((self.width+self.predictionButton.wd)//2, self.height - self.predictionButton.ht//2 - self.fontSize//2 - int( self.margins * 1.2)), self.fontSize)
      gui.message_to_screen(screen, "(A = %.2f, B = %.2f, C = %.2f)"%(self.A, self.B, self.C), gui.WHITE, ((self.width+self.predictionButton.wd)//2, self.height - self.predictionButton.ht//2 + self.fontSize//2 - int(self.margins*0.8)), self.fontSize)
  
  def simulate(self, window):
    if self.run:
      for _ in range(self.numStepsPerUpdate):
        self.MonteCarloStep()
    for k in range(TOT_SPECIES):
      self.populationInputs[k].setValue(self.speciesPop[k])
    self.updateScreen(window)
  
  
class WellMixedNumerApprox(Simulation):
  #Carries all information for the well-mixed case
  def __init__(self, width, height, predRates, speciesPopulation = [1 for _ in range(TOT_SPECIES)], numStepsPerUpdate = 3, killTimeStep = 0.005, maxKillCount = 250, precision_ord = 4, fontSize = 20, margins = 15, FPS = 60):
    super(WellMixedNumerApprox, self).__init__(width, height, predRates, numStepsPerUpdate)
    totPop = sum(speciesPopulation)
    self.speciesPop = [k / float(totPop) for k in speciesPopulation]
    self.total = sum(sum(l) for l in predRates)
    self.killTimeStep = killTimeStep
    self.maxKillCount = min(maxKillCount, max(10, totPop//1000))
    self.graph = pg.Surface((self.width-5, 3*self.height / 4))
    self.graph.fill(gui.WHITE)
    self.graph_x_pos = 0
    self.graph_width, self.graph_height = self.graph.get_rect().size
    self.updateGraph= 0
    self.graphModulus = 10
    self.precision_ord = precision_ord
    #GUI
    #(self, x, y, width, height, action = RETURN_TRUE, inactivecolour = RED, activecolour = ORANGE, text = None, textcolour = BLACK, size = 25, border = None)
    self.fontSize = fontSize
    self.margins = margins
    self.predictionButton = gui.Button(margins, height - fontSize - 2*margins, int(fontSize * 15 * 0.6), fontSize+margins, inactivecolour = gui.RED, activecolour = gui.ORANGE, text = "Show Prediction", size = fontSize)
    self.showPrediction = False
    #(self, x, y, height, bkg_colour = WHITE, text_colour = BLACK, frozen_colour = GREY, cursorColour = BLACK, default = 0, freeze = False, tot_digits = 6, precision = 3, FPS = 30, rel_origin = (0,0), center_loc = None):
    self.populationInputs = [gui.InputNumberBox(0,0, fontSize, default = self.speciesPop[i], tot_digits = 0, precision = precision_ord+1, FPS = FPS, center_loc = (int((i+1) * self.margins + (i+0.5) * (width - 6*margins)//5), height - 2 * margins - self.predictionButton.ht - fontSize//2)) for i in range(TOT_SPECIES)]
    
    self.change = False
  
  def updateRates(self, newVal, attacker, defender):
    super(WellMixedNumerApprox, self).updateRates(newVal, attacker, defender)
    self.change = True
    
  def eventHandler(self, event):
    super(WellMixedNumerApprox, self).eventHandler(event)
    for k in range(TOT_SPECIES):
      if not self.run and self.populationInputs[k].update(event):
        self.speciesPop[k] = self.populationInputs[k].getValue()
        self.change = True
        #self.fixNumbers()
  
  def toggle_pause(self):
    self.run = not self.run
    for k in range(TOT_SPECIES):
        self.populationInputs[k].set_freeze(self.run)
    
  def MonteCarloStep(self):
    dx = [0] * TOT_SPECIES
    for i in range(TOT_SPECIES):
      for j in range(TOT_SPECIES):
        if j != i:
          dx[i] += (self.predRates[i][j] - self.predRates[j][i]) * self.speciesPop[j] 
      dx[i] *= self.speciesPop[i]  * self.killTimeStep
    for i in range(TOT_SPECIES):
      self.speciesPop[i] = self.speciesPop[i] + dx[i]
    for i in range(TOT_SPECIES):
      if self.speciesPop[i]< 10**(-self.precision_ord):
        for j in range(TOT_SPECIES):
          if j != i:
            self.speciesPop[j] *= 1 / (1.0 + self.speciesPop[i])
        self.speciesPop[i] = 0
      #dx[i] -= int(round(dx[i]))
    #self.speciesPop[rnd.randint(0, TOT_SPECIES-1)] += int(round(sum(dx)))
   # if sum(self.speciesPop) != self.totPop:
   #   raise Exception("Sum of Species population not equal to total population, dx = %s, tot_pop = %d, new_species_pop = %s, sum of pop = %d, sum_dx = %f"%(str(dx), self.totPop, str(self.speciesPop), sum(self.speciesPop), sum(dx)))
#  
  
  def updateScreen(self, screen):
    screen.fill(gui.BLACK)
    self.updateGraph %= self.graphModulus
    if self.run and self.updateGraph == 0:
        #pg.draw.line(self.graph, gui.WHITE, (self.graph_width, 0), (self.graph_width, self.graph_height), 1)
      if self.change:
        self.change = False
        pg.draw.line(self.graph, gui.BLACK, (self.graph_x_pos, 0), (self.graph_x_pos, self.graph_height), 1)
        if self.graph_x_pos == self.graph_width-1:
          self.graph.scroll(dx = -1)
        else: self.graph_x_pos += 1
        
      y_start = 0
      for i in range(TOT_SPECIES):
        line_height = int(round(self.graph_height * self.speciesPop[i]))
        #if self.speciesPop[i] > 0 and line_height == 0: line_height = 1
        pg.draw.line(self.graph, self.numberToColor(i+1), (self.graph_x_pos, y_start), (self.graph_x_pos, y_start + line_height), 1)
        y_start += line_height
      if self.graph_x_pos == self.graph_width-1:
        self.graph.scroll(dx = -1)
      else: self.graph_x_pos += 1
      
    screen.blit(self.graph, (0,0))
    self.updateGraph+=1
    
    #InputBoxFunctionality
    rect = pg.Rect((0,0), (int((self.width - 6*self.margins)//5), self.fontSize + self.margins))
    for k in range(TOT_SPECIES):
      self.populationInputs[k].blit(screen)
      rect.center = (int((k+1) * self.margins) + int((k+0.5) * (self.width - 6*self.margins)//5), self.graph_height + 2* self.margins + self.fontSize//2)
      pg.draw.rect(screen, Simulation.numberToColor(k+1), rect, self.margins//2)
      gui.message_to_screen(screen, SPECIES_NAME[k], gui.WHITE, rect.center, self.fontSize)
      
    #Prediction Functionality
    if self.predictionButton.get_click():
      self.showPrediction = not self.showPrediction
      if self.showPrediction:
        self.predictionButton.text = "Hide Prediction"
      else:
        self.predictionButton.text = "Show Prediction"
    self.predictionButton.blit(screen)
    if self.showPrediction:
      gui.message_to_screen(screen, self.getPredictionMessage(), gui.WHITE, ((self.width+self.predictionButton.wd)//2, self.height - self.predictionButton.ht//2 - self.fontSize//2 - int( self.margins * 1.2)), self.fontSize)
      gui.message_to_screen(screen, "(A = %.2f, B = %.2f, C = %.2f)"%(self.A, self.B, self.C), gui.WHITE, ((self.width+self.predictionButton.wd)//2, self.height - self.predictionButton.ht//2 + self.fontSize//2 - int(self.margins*0.8)), self.fontSize)

  def fixNumbers(self):
    for k in range(TOT_SPECIES):
      if self.speciesPop[k] < 10**(-self.precision_ord):
        self.speciesPop[k] = 0
    s = sum(self.speciesPop)
    for k in range(TOT_SPECIES):
      self.speciesPop[k] /= s
      self.populationInputs[k].setValue(self.speciesPop[k])
  
  def simulate(self, window):
    if self.run:
      self.fixNumbers()
      for _ in range(self.numStepsPerUpdate):
        self.MonteCarloStep()
      self.fixNumbers()
    self.updateScreen(window)
   
    

def checkQuit():
  if pg.event.peek(pg.QUIT):
    pg.display.quit()
    pg.quit()
    quit()

  
class GridGame(Simulation):
  MAX_NUM_ROWS = 400
  MAX_NUM_COLS = 700
  def __init__(self, width, height, predRates, distribution, pullFromImage = False, numRows = None, numCols = None, numStepsPerUpdate = 250, FPS = 50):
      """
      Size is the height and width of field and is a natural number
      PullFromImage is a boolean which denotes if it will pull the field from an image
      the exact method for pulling will be dealt with later.
      Distribution is a list which denotes relative frequency of each species. In order rats to elephants
      """
      super(GridGame, self).__init__(width, height, predRates, numStepsPerUpdate)
      self.margins = 5
      self.fontSize = 15
      self.label_x = self.width //2 + self.margins
      self.label_height = self.margins + self.fontSize
      self.label_width = self.width // 2 - 2*self.margins
      self.label_start_y = self.height - 6*self.margins - 5*self.label_height - int(1.4*self.fontSize)
      self.maxBoardWidth = width - 2 * self.margins
      self.maxBoardHeight = self.label_start_y - 6 * self.margins 
      
      self.maxNumRows = min(self.maxBoardHeight, GridGame.MAX_NUM_ROWS)
      self.maxNumCols = min(self.maxBoardWidth, GridGame.MAX_NUM_COLS)
      self.minNumRows = 40
      self.minNumCols = 70
      if numRows == None: numRows = (self.maxNumRows + self.minNumRows)//2#min(self.maxBoardHeight, GridGame.MAX_NUM_ROWS)
      if numCols == None: numCols = (self.maxNumCols + self.minNumCols)//2#min(self.maxBoardWidth, GridGame.MAX_NUM_COLS)
      self.numRows = numRows
      self.numCols = numCols
      self.pixelSize = max(self.maxBoardWidth//numCols, self.maxBoardHeight//numRows)
      self.boardwidth = self.pixelSize * self.numCols    
      self.boardheight = self.pixelSize * self.numRows 
      self.speciesPop = list(distribution)
      self.Board = pg.Surface((self.boardwidth, self.boardheight))
      self.Board.fill(gui.BLACK)
      self.boardRect = self.Board.get_rect()
      self.boardRect.topleft = ((self.maxBoardWidth - self.boardwidth)//2, (self.maxBoardHeight - self.boardheight)//2 + self.margins//2)
      self.numStepsPerUpdate = int(round((self.numRows * self.numCols )**0.5))
      
      #(self, x, y, height, bkg_colour = WHITE, text_colour = BLACK, frozen_colour = GREY, cursorColour = BLACK, default = 0, freeze = False, tot_digits = 6, precision = 3, FPS = 30, rel_origin = (0,0), center_loc = None):
      self.rowInputLabel = gui.getParagraph("Habitat Height (between %d and %d) ="%(self.minNumRows, self.maxNumRows), gui.WHITE, self.width//2 - 4 * self.fontSize, gui.BLACK, self.fontSize)
      self.colInputLabel = gui.getParagraph("Habitat Width (between %d and %d) ="%(self.minNumCols, self.maxNumCols), gui.WHITE, self.width//2 - 4 * self.fontSize, gui.BLACK, self.fontSize)
      
      self.rowInputBox = gui.InputNumberBox(self.rowInputLabel.get_width() + 2*self.margins, self.height - 4*self.margins - 2*self.fontSize, self.fontSize+self.margins, default = self.numRows, tot_digits = 3, precision = 0, FPS = FPS)
      self.changeRowSize = False
      self.colInputBox = gui.InputNumberBox(self.colInputLabel.get_width() + 2*self.margins, self.height - 5*self.margins - 3*self.fontSize, self.fontSize+self.margins, default = self.numCols, tot_digits = 3, precision = 0, FPS = FPS)
      self.changeColSize = False
      #(self, x, y, width, height, action = RETURN_TRUE, inactivecolour = RED, activecolour = ORANGE, text = None, textcolour = BLACK, size = 25, border = None):
      self.editButton = gui.Button(self.margins, self.label_start_y, self.label_width, self.label_height, text = "EDIT HABITAT", size = self.fontSize)
      self.paintingBoard = False
      self.minBrushPixelSize = 5
      self.maxBrushSize = min(99, self.numRows*2//3, self.numCols * 2 // 3)
      self.curBrushSize = self.maxBrushSize
      self.brushSizeChanged = False
      self.brushSizeInput = gui.InputNumberBox(self.rowInputBox.x, self.editButton.y + self.editButton.ht + self.margins, self.fontSize + self.margins, default = self.curBrushSize, tot_digits = 2, precision = 0, FPS = FPS)
      self.editSpeciesIndex = 0
      editSpeciesButtonWidth = (self.label_width - 4 * self.margins) // 5
      self.editSpeciesButtons = [gui.Button(self.margins + k * (self.margins + editSpeciesButtonWidth), self.brushSizeInput.y + self.brushSizeInput.height + self.margins, editSpeciesButtonWidth, self.label_height, inactivecolour = Simulation.numberToColor(k+1), activecolour = Simulation.numberToColor(k+1), text = '') for k in range(TOT_SPECIES)]
      
      if not pullFromImage:
        self.changeBoardSize(numRows, numCols)
      else: 
        pass ####NO IDEA HOW WE WANT TO IMPLEMENT THIS
   
  def updateScreen(self, window):
    window.fill(gui.BLACK)
    forceChange = False
    if (self.changeRowSize and not self.rowInputBox.active) or (self.changeColSize and not self.colInputBox.active):
      self.brushSizeChanged = True
      forceChange = True
      newRows = int(self.rowInputBox.getValue())
      newCols = int(self.colInputBox.getValue())
      if newRows > self.maxNumRows:
        newRows = self.maxNumRows 
        self.rowInputBox.setValue(newRows)
      if newCols > self.maxNumCols:
        newCols = self.maxNumCols 
        self.colInputBox.setValue(newCols)
      if newRows < self.minNumRows:
        newRows = self.minNumRows 
        self.rowInputBox.setValue(newRows)
      if newCols < self.minNumCols:
        newCols = self.minNumCols 
        self.colInputBox.setValue(newCols)
      self.changeBoardSize(newRows, newCols)
      self.changeRowSize = False
      self.changeColSize = False
    
    minBrushSize = self.minBrushPixelSize // self.pixelSize
    self.maxBrushSize = min(99, self.numRows*2//3, self.numCols * 2 // 3)
    if self.minBrushPixelSize % self.pixelSize != 0: minBrushSize += 1
    
    if (self.brushSizeChanged and (forceChange or not self.brushSizeInput.active)):
        self.brushSizeChanged = False
        forceChange = False
        newInput = self.brushSizeInput.getValue()
        if newInput < minBrushSize: 
          newInput = minBrushSize
          self.brushSizeInput.setValue(minBrushSize)
        elif newInput > self.maxBrushSize:
          newInput = self.maxBrushSize
          self.brushSizeInput.setValue(newInput)
        self.curBrushSize = newInput
    window.blit(self.Board, self.boardRect)
    
    for i in range(TOT_SPECIES):
      pg.draw.rect(window, Simulation.numberToColor(i+1), ((self.label_x, self.label_start_y + i * (self.label_height + self.margins)), (self.label_width, self.label_height)), 2)
      gui.message_to_screen(window, SPECIES_NAME[i] + ": " + str(self.speciesPop[i]), gui.WHITE, (self.label_x + self.label_width // 2, self.label_start_y + i * (self.label_height + self.margins) + self.label_height//2), self.fontSize)
    
    pg.draw.line(window, gui.WHITE, (0, self.maxBoardHeight+self.margins), (self.width, self.maxBoardHeight+self.margins), self.margins//2)
    
    x_start = self.margins 
    for i in range(TOT_SPECIES):
      if i < TOT_SPECIES - 1:
        line_length = int(round((self.width - 2*self.margins) * self.speciesPop[i] / float(sum(self.speciesPop))))
      else:
        line_length = self.width - self.margins - x_start
      #if self.speciesPop[i] > 0 and line_height == 0: line_height = 1
      pg.draw.rect(window, self.numberToColor(i+1), ((x_start, self.maxBoardHeight+2*self.margins), (line_length, self.margins)))
      x_start += line_length
      
    window.blit(self.rowInputLabel, (self.margins, self.rowInputBox.y))
    window.blit(self.colInputLabel, (self.margins, self.colInputBox.y))
    self.rowInputBox.blit(window)
    self.colInputBox.blit(window)
    
    self.editButton.blit(window, freeze = self.run)
    if self.paintingBoard:
      self.brushSizeInput.blit(window)
      
      window.blit(gui.getParagraph("Brush Size (between %d and %d) ="%(minBrushSize, self.maxBrushSize), gui.WHITE, self.brushSizeInput.x - 2 * self.margins, gui.BLACK, size = self.fontSize), (self.margins, self.editButton.y + self.editButton.ht + self.margins))
      for k in range(TOT_SPECIES):
        self.editSpeciesButtons[k].blit(window)
      pg.draw.rect(window, gui.GREY, ((self.editSpeciesButtons[self.editSpeciesIndex].x, self.editSpeciesButtons[self.editSpeciesIndex].y), (self.editSpeciesButtons[self.editSpeciesIndex].wd, self.editSpeciesButtons[self.editSpeciesIndex].ht)), self.margins//2)
      mousex, mousey = pg.mouse.get_pos()
      if self.boardRect.collidepoint(mousex, mousey):
        (toprow, leftcol), (bottomrow, rightcol) = self.getPaintBrushRect(mousex, mousey)
        topleftCoords = (self.boardRect.left + self.pixelSize * leftcol, self.boardRect.top + self.pixelSize * toprow)
        brushheight = self.pixelSize * (bottomrow - toprow)
        brushwidth = self.pixelSize * (rightcol - leftcol)
        pg.draw.rect(window, Simulation.numberToColor(self.editSpeciesIndex+1), (topleftCoords, (brushwidth, brushheight)))
    
    gui.message_to_screen(window, "WELL-MIXED POPULATION PREDICTION: " + self.getPredictionMessage(hedge = True), gui.GOLDENROD, (self.width//2, self.height - self.fontSize-self.margins//2), self.fontSize, italic = True)
   
  def eventHandler(self, event):
    super(GridGame, self).eventHandler(event)
    if self.run:
      self.paintingBoard = False
    if not self.run:
      if self.rowInputBox.update(event):
        self.changeRowSize = True
      if self.colInputBox.update(event):
        self.changeColSize = True
      if self.editButton.get_click():
        self.paintingBoard = not self.paintingBoard
        self.brushSizeInput.set_freeze(not self.paintingBoard)
    if self.paintingBoard:
      if self.brushSizeInput.update(event):
        self.brushSizeChanged = True
      for k in range(TOT_SPECIES):
        if self.editSpeciesButtons[k].get_click():
          self.editSpeciesIndex = k
      if event.type == pg.MOUSEBUTTONDOWN:
        mousex, mousey = pg.mouse.get_pos()
        if self.boardRect.collidepoint(mousex, mousey):
          self.paintOnBoard(mousex, mousey)
  
  def toggle_pause(self):
    self.run = not self.run 
    self.rowInputBox.set_freeze(self.run)
    self.colInputBox.set_freeze(self.run)
    if self.run: 
      self.paintingBoard = False
  
  def getPaintBrushRect(self, mousex, mousey):#returns ((top row number, left col number), (bottom row number, right col number))
    middleRowNum = int((mousey - self.boardRect.y)//self.pixelSize)
    middleColNum = int((mousex - self.boardRect.x) // self.pixelSize)
    topleft = (max(0, middleRowNum - self.curBrushSize//2), max(0, middleColNum - self.curBrushSize//2))
    bottomright = (min(self.numRows, middleRowNum + self.curBrushSize - self.curBrushSize//2), min(self.numCols, middleColNum + self.curBrushSize- self.curBrushSize//2))
    return topleft, bottomright
  
  def paintOnBoard(self, mousex, mousey):
    (toprow, leftcol), (bottomrow, rightcol) = self.getPaintBrushRect(mousex, mousey)
    y = int( toprow * self.pixelSize )
    while y < bottomrow * self.pixelSize:
      x = int(leftcol * self.pixelSize)
      while (x < rightcol * self.pixelSize):
        oldSpecies = Simulation.colorToNumber(self.Board.get_at((x, y)))
        self.speciesPop[oldSpecies-1] -= 1
        self.speciesPop[self.editSpeciesIndex] += 1
        GridGame.editBoard(self.Board, Simulation.numberToColor(self.editSpeciesIndex+1), (x,y), self.pixelSize)
        x += int(self.pixelSize)
      y += int(self.pixelSize)
    
  
  @staticmethod
  def editBoard(surface, color, pos, pixelSize):
    if pixelSize > 1:
        pg.draw.rect(surface, color, (pos, (pixelSize, pixelSize)))
    else:
        surface.set_at(pos, color)
  
  def changeBoardSize(self, newNumRows, newNumCols):
    #Assume boardwidth <= maxBoardWidth and boardheight <= maxBoardHeight
    #Assume speciesPop accurately reflects population on new board
    #Will add new data if necessary
    newNumRows = min(newNumRows, self.maxBoardHeight)
    newNumCols = min(newNumCols, self.maxBoardWidth)
    oldPixelSize = self.pixelSize
    oldWidth = self.boardwidth
    oldHeight = self.boardheight
    newPixelSize = min(self.maxBoardWidth//newNumCols, self.maxBoardHeight//newNumRows)
    newWidth = newNumCols * newPixelSize
    newHeight = newNumRows * newPixelSize
    oldSurf = self.Board 
    newSurf = pg.Surface((newWidth, newHeight))
    newSpeciesPop = [int(round(float(k) * newWidth * newHeight / float(sum(self.speciesPop)))) for k in self.speciesPop]
    distribution = [0 for _ in range(TOT_SPECIES)]
    #Get Old Board Data onto New Board
    x = 0
    oldx= 0
    while (oldx < oldWidth and x < newWidth):
      y = 0
      oldy = 0
      while (oldy < oldHeight and y < newHeight):
        checkQuit()
        curSpecies = Simulation.colorToNumber(oldSurf.get_at((oldx, oldy)))
        if curSpecies == -1:
          curSpecies = 1+Simulation.weightedChoice([newSpeciesPop[i] - distribution[i] for i in range(TOT_SPECIES) if newSpeciesPop[i] != distribution[i]], backUp = newSpeciesPop)
        distribution[curSpecies-1] += 1
        GridGame.editBoard(newSurf, Simulation.numberToColor(curSpecies), (x,y), newPixelSize)
        y += newPixelSize
        oldy += oldPixelSize
      oldx += oldPixelSize 
      x += newPixelSize
    doneWidth = min(newWidth, (oldWidth//oldPixelSize) * newPixelSize)
    doneHeight = min(newHeight, (oldHeight//oldPixelSize) * newPixelSize)
    
    #(if any remaining directly below)
    x = 0
    while doneHeight < newHeight and x < doneWidth:
      y = doneHeight
      while y < newHeight:
        checkQuit()
        curSpecies = 1+Simulation.weightedChoice([newSpeciesPop[i] - distribution[i] for i in range(TOT_SPECIES) if newSpeciesPop[i] != distribution[i]], backUp = newSpeciesPop)
        distribution[curSpecies-1] += 1
        GridGame.editBoard(newSurf, Simulation.numberToColor(curSpecies), (x,y), newPixelSize)
        y += newPixelSize
      x += newPixelSize 
      
    #(if any remaining directly to the right)
    x = doneWidth
    while x < newWidth:
      y = 0
      while y < doneHeight:
        checkQuit()
        curSpecies = 1+Simulation.weightedChoice([max(newSpeciesPop[i] - distribution[i], 0) for i in range(TOT_SPECIES)], backUp = newSpeciesPop)
        distribution[curSpecies-1] += 1
        GridGame.editBoard(newSurf, Simulation.numberToColor(curSpecies), (x,y), newPixelSize)
        y += newPixelSize
      x += newPixelSize 
    
    #(if any remaining to bottom right)
    x = doneWidth
    while x < newWidth:
      y = doneHeight
      while y < newHeight:
        checkQuit()
        curSpecies = 1+Simulation.weightedChoice([max(newSpeciesPop[i] - distribution[i], 0) for i in range(TOT_SPECIES)], backUp = newSpeciesPop)
        distribution[curSpecies-1] += 1
        GridGame.editBoard(newSurf, Simulation.numberToColor(curSpecies), (x,y), newPixelSize)
        y += newPixelSize
      x += newPixelSize 
    
    self.speciesPop = list(distribution)
    self.pixelSize = newPixelSize 
    self.boardwidth = newWidth 
    self.boardheight = newHeight 
    self.Board = newSurf
    self.boardRect = self.Board.get_rect()
    self.numRows = newNumRows
    self.numCols = newNumCols
    self.boardRect.topleft = ((self.maxBoardWidth - self.boardwidth)//2, (self.maxBoardHeight - self.boardheight)//2 + self.margins//2)

  def pairContest(self, aggressor, defender):
    #Returns True if the aggressor wins
    if self.predRates[aggressor][defender] == 0: return False
    x = rnd.random()
    return (x < self.predRates[aggressor][defender])
#    if aggressor == 4 and defender == 0:
#        return True
#    elif defender == 4 and aggressor == 0:
#        return False
#    elif defender > aggressor:
#        return True
#    else:
#        return False 
  
#  def rotateColor(self, x,y):
#      self.Board.set_at((x,y), Simulation.numberToColor(Simulation.colorToNumber((( self.Board.get_at((x,y)))+1) % 5 + 1)))
      
  def runTurn(self):   
    #choose the agressor
    a = rnd.randint(0,self.numCols-1) * self.pixelSize #x_pos
    if a == (self.numCols-1) * self.pixelSize:
      b = rnd.randint(0,self.numRows-2) * self.pixelSize #y_pos
    else:
      b = rnd.randint(0,self.numRows-1) * self.pixelSize #y_pos
    
    species1Pos = (a,b)
    if a == (self.numCols-1) * self.pixelSize:
      species2Pos = (a, b+self.pixelSize)
    elif b == (self.numRows-1) * self.pixelSize:
      species2Pos = (a+self.pixelSize, b)
    elif bool(rnd.getrandbits(1)):
      species2Pos = (a+self.pixelSize, b)
    else:
      species2Pos = (a, b+self.pixelSize)
    species1 = -1+Simulation.colorToNumber(self.Board.get_at(species1Pos))
    species2 = -1+Simulation.colorToNumber(self.Board.get_at(species2Pos))
      
    if self.pairContest(species1, species2): #species1 beats species 2
      GridGame.editBoard(self.Board, Simulation.numberToColor(species1+1), species2Pos, self.pixelSize)
      self.speciesPop[species1] += 1
      self.speciesPop[species2] -= 1
    elif self.pairContest(species2, species1): #species 2 beats species 1
      GridGame.editBoard(self.Board, Simulation.numberToColor(species2+1), species1Pos, self.pixelSize)
      #pg.draw.rect(self.Board, Simulation.numberToColor(species2+1), (species1Pos, (self.pixelSize, self.pixelSize)))
      self.speciesPop[species2] += 1
      self.speciesPop[species1] -= 1
#      
#    if bool(rnd.getrandbits(1)): #Decides the orientation
#        if self.pairContest(Simulation.colorToNumber(self.Board.get_at((a,b))), Simulation.colorToNumber(self.Board.get_at(((a+1, b))))):
#            self.Board.set_at((a+1,b) , self.Board.get_at((a,b)))
#        else:
#            self.Board.set_at((a,b) , self.Board.get_at((a+1,b)))
#    else:
#        if self.pairContest(Simulation.colorToNumber(self.Board.get_at((a,b))), Simulation.colorToNumber(self.Board.get_at(((a, b+1))))):
#            self.Board.set_at((a,b+1) , self.Board.get_at((a,b)) )
#        else:
#            self.Board.set_at((a,b), self.Board.get_at((a,b+1)))

  def simulate(self, window):
    if self.run:
      for i in range(self.numStepsPerUpdate):
        self.runTurn()
    self.updateScreen(window)
