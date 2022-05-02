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
import math


pg.init()
display_width = 1200
display_height = 600
screen = pg.display.set_mode((display_width, display_height))
MAIN_CAPTION = "A Five-Species Jungle Game"
pg.display.set_caption(MAIN_CAPTION)
#pg.display.set_icon(<pg.surface picture>)

TOT_SPECIES = 5
sim.TOT_SPECIES = TOT_SPECIES
SPECIES_NAME = ["Big Tree", "Small Tree", "Shrub", "Grass", "Dirt"]
sim.SPECIES_NAME = SPECIES_NAME
FPS = 100
PRED_PREY_PAIRS = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (1, 4), (2, 3), (2, 4), (3, 4), (4, 0)]
preSetRates = [
    {(4,0):0.1 , (0,2):0.5, (1,3):0.5, (2,4):0.5},#1,4,5
    {(4,0):0.8, (0,2):0.5, (1,3):0.5, (2,4):0.5},#all
    {(4,0):1.5, (0,2):0.8, (1,3):0.8, (2,4):0.8},#1,2,5
    {(4,0):1, (0,2):0.8, (1,3):0.8, (2,4):0.8,(0,3): 0.3,(1,4): 0.3},#all 
    {(4,0):0.5, (0,2):0.8, (1,3):0.8, (2,4):0.8,(0,3): 0.3,(1,4): 0.3},#1,4,5
    {(4,0):1.35, (0,2):0.8, (1,3):0.8, (2,4):0.8,(0,3): 0.3,(1,4): 0.3},#1,2,5
    {(4,0):0.8, (0,2):1.2, (1,3):1.2, (2,4):1.2,(0,3): 0.25,(1,4): 0.25},#all
    {(4,0):0.6, (0,2):1.2, (1,3):1.2, (2,4):1.2,(0,3): 0.25,(1,4): 0.25},#1,4,5
    {(4,0):1.2, (0,2):1.2, (1,3):1.2, (2,4):1.2,(0,3): 0.25,(1,4): 0.25},#1,2,5
    {(4,0):0.3, (0,2):1.6, (1,3):1.6, (2,4):1.6,(0,3): 0.5,(1,4): 0.5},#1,4,5
    {(4,0):0.65, (0,2):1.6, (1,3):1.6, (2,4):1.6,(0,3): 0.5,(1,4): 0.5},#all
    {(4,0):1.1, (0,2):1.6, (1,3):1.6, (2,4):1.6,(0,3): 0.5,(1,4): 0.5}#1,2,5
    ]

for i in range(len(preSetRates)):
  for k in range(TOT_SPECIES-1):
    preSetRates[i][(k,k+1)] = 1.0

for i in range(len(preSetRates)):
  for t in PRED_PREY_PAIRS:
    if not preSetRates[i].has_key(t):
      preSetRates[i][t] = 0.0

distribution = [3000]+[4000]*3 + [10000]
totalPopulation = sum(distribution)

defaultIndex = 4
def setPredRates(index = defaultIndex):
  if index < 0 or index >= len(preSetRates):
    index = defaultIndex
  l = [[0.0 for _ in range(TOT_SPECIES)] for _ in range(TOT_SPECIES)]
  for (i,j) in PRED_PREY_PAIRS:
    l[i][j] = preSetRates[index][(i,j)]
  return l

predRates = setPredRates()

def Quit():
    pg.display.quit()
    pg.quit()
    quit()

def drawArrow(surface, tail_loc, head_loc, colour = gui.BLACK, head_height = 15, head_semi_width = 5, line_width = 2):
  diff = tuple(head_loc[i] - tail_loc[i] for i in (0,1))
  length = float(math.hypot(diff[0], diff[1]))
  cross_ratio = float(head_height) / length
  cross_pt = tuple(cross_ratio * tail_loc[i] + (1 - cross_ratio) * head_loc[i] for i in (0,1))
  tail_tip = tuple(tuple(int(cross_pt[i] + ((s * ((-1)**i) * diff[1-i] * head_semi_width) / length)) for i in (0,1)) for s in (-1, 1))
  pg.draw.line(surface, colour, tail_loc, head_loc, line_width)
  pg.draw.polygon(surface, colour, (head_loc, tail_tip[0], tail_tip[1]))
  
  
MIXED_RANDOM = 0
MIXED_APPROX = 1
STRUCTURED = 2
MENU_SCREEN = 3
HELP_SCREEN = 4


def runSimulation(simType = MIXED_APPROX):
  global distribution
  global totalPopulation 
  global predRates
  totalPopulation = sum(distribution)
  
  screen.fill(gui.WHITE)
  #initialize simulation
  simulationArea = pg.Surface((int(display_width * 0.65), display_height))
  simulationAreaRect = simulationArea.get_rect()
  simulationAreaRect.topleft = (0,0)
  caption = MAIN_CAPTION + ' - '
  
  if simType == MIXED_RANDOM:
    simulator = sim.WellMixedRandom(simulationAreaRect.width, simulationAreaRect.height, predRates, distribution, FPS = FPS)
    caption += "Random Simulation, Well-Mixed Population"
  elif simType == MIXED_APPROX:
    simulator = sim.WellMixedNumerApprox(simulationAreaRect.width, simulationAreaRect.height, predRates, distribution, FPS = FPS)
    caption += "Numerical Solution to PDE, Well-Mixed Population"
  elif simType == STRUCTURED:
    caption += "Structured Population"
    simulator = sim.GridGame(simulationAreaRect.width, simulationAreaRect.height, predRates, distribution, FPS = FPS)
    
  pg.display.set_caption(caption)  
  simulator.startSimulation(simulationArea)
  
  #Initialize Key + pred_rate input boxes
  margins = 10
  menu_width = display_width - simulationAreaRect.width - 2*margins
  button_font_size = 23
  menu_button_width = (menu_width - margins) // 2
  
  key_margin = 8
  keyfontsize = 20
  inputBoxSize = 17
  label_width = menu_button_width // 2 + keyfontsize//2 + key_margin*2
  label_height = keyfontsize + key_margin
  line_width = 2
  key = pg.Surface((menu_width, int(5 * label_height + button_font_size + 7* key_margin + 4 * (3 * key_margin + inputBoxSize))))
  key_rect = key.get_rect()
  key_rect.left = simulationAreaRect.width + margins
  presetsRect = pg.Rect((0,0), (key_rect.width, 2*button_font_size+2*margins))
  presetsRect.left = key_rect.left
  presetsRect.bottom = display_height - margins
  key_rect.bottom = presetsRect.top - margins
  
  #(self, x, y, width, height, action = RETURN_TRUE, inactivecolour = RED, activecolour = ORANGE, text = None, textcolour = BLACK, size = 25, border = None):
  preset_margins = 2*margins//3
  numpresets = len(preSetRates)
  preset_widths = (presetsRect.width - (numpresets+1)*preset_margins)//numpresets
  presetBtns = [gui.Button(presetsRect.centerx + (k - numpresets/2)* (preset_widths + preset_margins), presetsRect.centery + preset_margins, preset_widths, button_font_size, inactivecolour = gui.GOLDENROD, activecolour = gui.GOLD, text = str(k+1), size = button_font_size - preset_margins) for k in range(numpresets)]
  gui.message_to_screen(screen, "Preset Predation Rates", gui.BLACK, (presetsRect.centerx, presetsRect.top + preset_margins//2+button_font_size//2), button_font_size)
  
  key.fill(gui.WHITE)
  gui.message_to_screen(key, "How Different Species Interact", gui.BLACK, (menu_width//2, margins + button_font_size//2), button_font_size)
  #draw arrows
  label_centers = [(key_rect.width // 2, key_margin*6 + button_font_size + i * (label_height + 3 * key_margin + inputBoxSize)) for i in range(5)]
  for i in range(TOT_SPECIES-1):
    drawArrow(key, label_centers[i], (label_centers[i+1][0], label_centers[i+1][1] - label_height//2) , head_height = key_margin, head_semi_width = key_margin//2, line_width = line_width)
  
  rightGap = (key_rect.width//2 - label_width//2)//4
  leftGap = (label_centers[0][0] - label_width//2)//3
  pg.draw.lines(key, gui.BLACK, False, (
      (label_centers[0][0], label_centers[0][1]-2*key_margin-label_height//2),
      (key_rect.width - rightGap, label_centers[0][1]-2*key_margin-label_height//2),
      (key_rect.width - rightGap, label_centers[4][1]+key_margin+label_height//2),
      (label_centers[4][0], label_centers[4][1]+key_margin+label_height//2), 
      (label_centers[4][0], label_centers[4][1]+label_height//2)), 
  line_width)
  drawArrow(key, (label_centers[0][0], label_centers[0][1]-2*key_margin-label_height//2), (label_centers[0][0], label_centers[0][1]-label_height//2), head_height = key_margin, head_semi_width = key_margin//2, line_width = line_width)
  
  for i in (0, 1, 2):
    tail_fix_y = 0
    head_fix_y = 0
    if i == 0:
      head_fix_y = -label_height//6
    if i== 2:
      tail_fix_y = label_height // 6
    pg.draw.lines(key, gui.BLACK, False, (
      (label_centers[i][0], label_centers[i][1]+tail_fix_y),
      (label_centers[i][0] - label_width//2 - (i%2+1)*leftGap, label_centers[i][1]+tail_fix_y),
      (label_centers[i+2][0] - label_width//2 - (i%2+1)*leftGap, label_centers[i+2][1]+head_fix_y)),
  line_width)
    drawArrow(key, (label_centers[i+2][0] - label_width//2 - (i%2+1)*leftGap, label_centers[i+2][1]+head_fix_y), (label_centers[i+2][0] - label_width//2, label_centers[i+2][1]+head_fix_y), head_height = key_margin, head_semi_width = key_margin//2, line_width = line_width)
  
  for i in (0, 1):
    pg.draw.lines(key, gui.BLACK, False, (
      label_centers[i],
      (label_centers[i][0] + label_width//2 + (i+1)*rightGap, label_centers[i][1]),
      (label_centers[i+3][0] + label_width//2 + (i+1)*rightGap, label_centers[i+3][1])),
  line_width)
    drawArrow(key, (label_centers[i+3][0] + label_width//2 + (i+1)*rightGap, label_centers[i+3][1]), (label_centers[i+3][0] + label_width//2, label_centers[i+3][1]), head_height = key_margin, head_semi_width = key_margin//2, line_width = line_width)
    
  label_rect = pg.Rect(0, key_margin*4 + button_font_size , label_width, label_height)
  #label_rect.centerx = key_rect.width // 2
  for i in range(TOT_SPECIES):
    label_rect.center = label_centers[i]
    pg.draw.rect(key, gui.WHITE, label_rect)
    pg.draw.rect(key, sim.Simulation.numberToColor(i+1), label_rect, 3)
    pg.draw.rect(key, sim.Simulation.numberToColor(i+1), pg.Rect(label_rect.topleft, (label_height, label_height)))
    gui.text_to_button(key, SPECIES_NAME[i], gui.BLACK, label_rect.left + label_height, label_rect.top, label_width - label_height, label_height, keyfontsize)
  
  #Initialize Buttons
  
  menu_button_width = (menu_width - 3*margins) // 2
  menu_button_height = button_font_size + margins*2
  mainmenu_btn = gui.Button(simulationAreaRect.width + margins, margins, menu_button_width, menu_button_height, inactivecolour = gui.LIGHTBLUE, activecolour = gui.SKYBLUE, text = "MENU", size = button_font_size)
  helpmenu_btn = gui.Button(simulationAreaRect.width + 2*margins + menu_button_width, margins, menu_button_width, menu_button_height, inactivecolour = gui.LIGHTGREEN, activecolour = gui.GREEN, text = "HELP", size = button_font_size)
  pause_btn = gui.Button(simulationAreaRect.width + margins, 2*margins + menu_button_height, menu_button_width, menu_button_height, inactivecolour = gui.PINK, activecolour = gui.PEACH, text = "PAUSE", size = button_font_size)
  quit_btn = gui.Button(simulationAreaRect.width + 2*margins + menu_button_width, 2*margins + menu_button_height, menu_button_width, menu_button_height, inactivecolour = gui.RED, activecolour = gui.ORANGE, text = "QUIT", size = button_font_size)
  pg.draw.rect(key, gui.BLACK, ((0,0), key_rect.size), margins//2)
  screen.blit(key, key_rect)
  
  #initialize text_boxes
  #(x, y, height, bkg_colour = WHITE, text_colour = BLACK, frozen_colour = GREY, cursorColour = BLACK, default = 0, freeze = False, tot_digits = 6, precision = 3, FPS = 30, rel_origin = (0,0)):
  tot_digits = 1
  precision = 3
  predRateInputs = [[None for _ in range(TOT_SPECIES)] for _ in range(TOT_SPECIES)]
  for i in range(TOT_SPECIES-1):
    predRateInputs[i][i+1] = gui.InputNumberBox(0,0, inputBoxSize, default = predRates[i][i+1], tot_digits = tot_digits, precision = precision, FPS = FPS, center_loc = (label_centers[i][0] + key_rect.left, label_centers[i][1] + key_rect.top + label_height//2 + key_margin + inputBoxSize//2))
     
  for i in (0,1,2):
    fix_y = (i - 1) * 4 * key_margin
    predRateInputs[i][i+2] = gui.InputNumberBox(0,0, inputBoxSize, default = predRates[i][i+2], tot_digits = tot_digits, precision = precision, FPS = FPS, center_loc = (label_centers[i][0] - label_width//2 - (i%2+1)*leftGap + key_rect.left, key_rect.top + (label_centers[i][1] + label_centers[i+2][1] + fix_y)//2))
    
  for i in (0,1):
    predRateInputs[i][i+3] = gui.InputNumberBox(0,0, inputBoxSize, default = predRates[i][i+3], tot_digits = tot_digits, precision = precision, FPS = FPS, center_loc = (label_centers[i][0] + label_width//2 + (i+1)*rightGap + key_rect.left, key_rect.top + (label_centers[i][1] + label_centers[i+3][1])//2))
    
  predRateInputs[4][0] = gui.InputNumberBox(0,0, inputBoxSize, default = predRates[4][0], tot_digits = tot_digits, precision = precision, FPS = FPS, center_loc = (key_rect.left+key_rect.width - 4*key_margin, key_rect.centery))
  #(key_rect.width - 4*key_margin, label_centers[0][1]-2*key_margin-label_height//2)
  
  clock = pg.time.Clock()
  pauseMessageRect = pg.Rect((0,0), (simulationAreaRect.width - 6*margins, 2*margins + 2*button_font_size))
  pauseMessageRect.centerx = simulationAreaRect.width//2
  pauseMessageRect.top = button_font_size//2
  pauseMessageRectAtTop = True
  #(msg, colour, width, backcolour, size = 25, bold = False, italic = False, linespacing = 0, paraspacing = 15, hyphenated = False)
  #helpMessage = gui.getParagraph("CLICK 'PLAY' OR PRESS 'P' TO START.\nYou may tweak the various parameters by clicking on the textboxes.", gui.BLACK, simulationAreaRect.width, gui.PEACH, int(button_font_size * 0.75), italic = True, linespacing = 1, paraspacing = 5)
  #helpRect = helpMessage.get_rect()
  #helpRect.topleft = (0,0)
  
  while True:
    simulator.simulate(simulationArea)
    
    if not simulator.run:
      for n in range(numpresets):
        if presetBtns[n].get_click():
          for (i,j) in PRED_PREY_PAIRS:
            simulator.updateRates(preSetRates[n][(i,j)], i, j)
            predRateInputs[i][j].setValue(preSetRates[n][(i,j)])
      
    if mainmenu_btn.get_click():
      distribution = simulator.speciesPop
      if simType == MIXED_APPROX:
        distribution = [int(k * totalPopulation) for k in distribution]
      return MENU_SCREEN
    helpmenu_btn.get_click()
    if pause_btn.get_click():
      simulator.toggle_pause()
    if quit_btn.get_click():
      distribution = simulator.speciesPop
      if simType == MIXED_APPROX:
        distribution = [int(k * totalPopulation) for k in distribution]
      Quit()
    for event in pg.event.get():
      if event.type == pg.QUIT:
        distribution = simulator.speciesPop
        if simType == MIXED_APPROX:
          distribution = [int(k * totalPopulation) for k in distribution]
        Quit()
      elif event.type == pg.KEYDOWN:
        if event.key == pg.K_ESCAPE:
          distribution = simulator.speciesPop
          if simType == MIXED_APPROX:
            distribution = [int(k * totalPopulation) for k in distribution]
          Quit()
          
      simulator.eventHandler(event)
      if not simulator.run:
        for (i,j) in PRED_PREY_PAIRS:
          if predRateInputs[i][j] != None:
              if predRateInputs[i][j].update(event):
                simulator.updateRates(predRateInputs[i][j].getValue(), i, j)
        
    screen.blit(simulationArea, simulationAreaRect)
    mainmenu_btn.blit(screen)
    helpmenu_btn.blit(screen)
    quit_btn.blit(screen)
    for n in range(numpresets):
      presetBtns[n].blit(screen, freeze = simulator.run)
    if simulator.run: 
      pause_btn.text = "PAUSE"
    else: pause_btn.text = "PLAY"
    pause_btn.blit(screen)
    for (i,j) in PRED_PREY_PAIRS:
      if predRateInputs[i][j] != None:
        if simulator.run: predRateInputs[i][j].set_freeze(True)
        elif predRateInputs[i][j].freeze: predRateInputs[i][j].set_freeze(False)
        predRateInputs[i][j].blit(screen)
    if not simulator.run:
      #(screen, msg, color, center_loc, size, italic = False, bold = False):
      mousex, mousey =  pg.mouse.get_pos( )
      if simType == STRUCTURED and simulator.paintingBoard and simulator.boardRect.collidepoint((mousex, mousey)):
          pauseMessageRectAtTop = False
      elif pauseMessageRectAtTop and pauseMessageRect.collidepoint((mousex, mousey)):
          pauseMessageRectAtTop = False
      elif mousey > display_height // 2 or mousex > simulationAreaRect.right:
          pauseMessageRectAtTop = True
      if pauseMessageRectAtTop:  
        pauseMessageRect.top = button_font_size//2
      else:
        pauseMessageRect.bottom = display_height - button_font_size//2
      pg.draw.rect(screen, gui.PEACH, pauseMessageRect)
      gui.message_to_screen(screen, "CLICK 'PLAY' OR PRESS 'P' TO START THE SIMULATION.", gui.BLACK, (pauseMessageRect.centerx, pauseMessageRect.top + button_font_size), int(button_font_size * 0.85))
      gui.message_to_screen(screen, "You may tweak various parameters by clicking on the grey textboxes.", gui.BLACK, (pauseMessageRect.centerx, pauseMessageRect.bottom - button_font_size), int(button_font_size * 0.75))
    pg.display.update()
    
    clock.tick(FPS)


def menuScreen():
  pg.display.set_caption(MAIN_CAPTION)
  screen.fill(gui.BLACK)
  fontSize = 25
  titleSize =47
  title_y = display_height/4 - 2*fontSize
  margins = 20
  gui.message_to_screen(screen, "WELCOME TO A FIVE SPECIES JUNGLE GAME", gui.CYAN, (display_width//2, title_y), titleSize, bold = True, italic = True)
  
  introString = """We simulate the interactions between five different species, in the framework of evolutionary game theory. Here, all species play against 'the field'. We thus explore how inter-species collaboration naturally arises in nature."""
  introMsg = gui.getParagraph(introString, gui.WHITE, display_width - 2*margins, gui.BLACK, size = fontSize, linespacing =1, hyphenated = False, italic = True)
  introRect = introMsg.get_rect()
  introRect.centerx = display_width//2
  introRect.top = title_y + fontSize + 2* margins
  screen.blit(introMsg, introRect)
  
  #buttons 
  button_y = introRect.bottom + 2*margins
  button_height = (display_height - button_y - 2* margins)
  button_width = (display_width - 7 * margins) // 4
  left_button_x = 2*margins
  #(self, x, y, width, height, action = RETURN_TRUE, inactivecolour = RED, activecolour = ORANGE, text = None, textcolour = BLACK, size = 25, border = None)
  well_mixed_random = gui.Button(left_button_x, button_y, button_width, button_height, text = "MIXED RANDOM")
  well_mixed_approx = gui.Button(left_button_x + margins + button_width, button_y, button_width, button_height, text = "NUMERIC SOLVE")
  structured = gui.Button(left_button_x+ 2*(margins + button_width), button_y, button_width, button_height, text = "STRUCTURED")
  help_btn = gui.Button(left_button_x + 3*(margins + button_width), button_y, button_width, button_height, text = "HELP")
  
  clock = pg.time.Clock()
  while True:
    if well_mixed_random.get_click():
      return MIXED_RANDOM
    if well_mixed_approx.get_click():
      return MIXED_APPROX
    if structured.get_click():
      rect = pg.Rect((0,0), (display_width -button_width, int(1.25*titleSize)))
      rect.center = screen.get_rect().center
      pg.draw.rect(screen, gui.PEACH, rect)
      gui.message_to_screen(screen, "INITIALIZING BOARD... PLEASE WAIT", gui.BLACK, rect.center, titleSize)
      pg.display.update()
      return STRUCTURED
    if help_btn.get_click():
      pass
    for event in pg.event.get():
      if event.type == pg.QUIT:
        Quit()
      elif event.type == pg.KEYDOWN:
        if event.key == pg.K_ESCAPE:
          Quit()
    
    well_mixed_random.blit(screen)
    well_mixed_approx.blit(screen)
    structured.blit(screen)
    help_btn.blit(screen)
    pg.display.update()
    clock.tick(max(FPS//4, 25))

currentScreen = MENU_SCREEN
try:
  while True:
    if currentScreen == MENU_SCREEN:
      currentScreen = menuScreen()
    elif currentScreen in (MIXED_RANDOM, MIXED_APPROX, STRUCTURED):
      currentScreen = runSimulation(currentScreen)
    else:
      Quit()
      
except Exception as e:
  with open("LOG_FILE.txt", "w") as f:
    f.write(traceback.format_exc())
    pg.quit()
    quit()