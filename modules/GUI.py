# -*- coding: utf-8 -*-
"""
Created on Wed Mar 23 17:23:44 2022

@author: kushs
"""
"""Module for buttons, list boxes etc, as well as the module that will contain any generic function for GUI stuff
Each of the interface elements must be a python class
This module will heavily use the following things in python:
1. functions can be assigned to variables, be values in dictionaries, be passed as arguments in function definitions
and generally act like class objects
eg:
x = int
x(4.90) return 4 etc.
2. functions have 2 special kind of arguments:
*parameter and **keywordparameter
what *parameter does is take multiple letf over arguments passed in function definition and combine them in a tuple.
eg:
def test(a, *numbers):
    for i in numbers:
        print i+a, ",", 
test(4, 1, 2, 3, 4, 5) #outputs:  '5, 6, 7, 8, 9,'
what **keywords does is take multiple left over keyword arguments and combine them as a dictionary.
eg:
def test(**stuff):
    for key in stuff:
        print key, stuff[key]
test(a = 2, b = 3.0, lol = '100', d = [5, 6])
output:
a 2
b 3.0
lol 100
d [5, 6]
"""
import pygame as pg
import time


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
LIGHTGREEN = (0, 255, 191)
DARKGREEN = (34, 139, 34)
YELLOW = (255, 255, 0)
GOLD = (255, 215, 0)
GOLDENROD = (218, 165, 32)
BLUE = (0, 0, 255)
LIGHTBLUE = (0, 191, 255)
DARKBLUE = (0, 0, 175)
SKYBLUE = (135, 206, 235)
LIGHTGREY = (218, 218, 218)
GREY = (126, 126, 126)
DARKGREY = (80, 80, 80)
TOMATO = (255, 99, 71)
SIENNA = (160, 82, 45)
DARKORANGE = (255, 120, 0)
PURPLE = (255, 0, 255)
CYAN = (0, 255, 255)
ORANGE = (255, 165, 0)
PEACH = (255, 218, 185)
GREENYELLOW = (173, 255, 47)
PINK = (255, 181, 197)
BROWN = (139, 69, 19)

#---------------------------------------------------------------------------------------
RAW_TEXT_FONT_SIZE = 100

def text_objects(text, colour, size, bold = False, italic = False, numreturn = 2, surface_only = False):
    """returns a text surface.
text must be a single line.
Size is the height of rectangle of the pygame.Surface object for the line of text"""
    textSurface = pg.font.SysFont("comicsansms", size, bold = bold, italic = italic).render(text, True, colour)
    #w, h = textSurface.get_size()
    #scalar = float(size) / float(h)
    #textSurface = pg.transform.scale(textSurface, (int(w * scalar), size))
    if surface_only: return textSurface
    if numreturn == 2: return textSurface, textSurface.get_rect()
    else: return textSurface.get_rect()
  
#def text_objects(text, colour, size, ):
###    font_dict = {'small':smallfont, 'medium':medfont, 'large':largefont, 'smallmed':smallmedfont, 'mediumlarge':mediumlargefont}
#    #size is font size as an integer
#    
#    textSurface = pg.font.SysFont("comicsansms", size).render(text, True, colour)

def text_to_button(screen, msg, color, btnx, btny, btnwidth, btnheight, size = 25, bold = False, italic = False):
    textSurf , textRect = text_objects(msg, color, size, bold = bold, italic = italic)
    textRect.center = ((btnx + (btnwidth / 2)), (btny + (btnheight / 2)))
    screen.blit(textSurf, textRect)

def message_to_screen(screen, msg, color, center_loc, size, italic = False, bold = False):
    textSurf , textRect = text_objects(msg, color, size, bold = bold, italic = italic)
    textRect.center = center_loc
    screen.blit(textSurf, textRect)
    return textRect

#-------------------------------------------------------------------------------

def getParagraph(msg, colour, width, backcolour, size = 25, bold = False, italic = False, linespacing = 0, paraspacing = 15, hyphenated = False):
    """Get a pygame.Surface text object to use for blitting, by left aligning the msg.
Used for blitting large paragraphs, constrained by width.
size is the pixel height for the text, and backcolour is the background colour.
linespacing is the pixel gap between consecutive lines, whereas paraspacing is the pixel gap between consecutive paragraphs
If hyphenated is True, then if word overflows the width it will append a '-' and carry over rest of word to next line
If False, the entire word will get carried over.
As this method may be memory and time inefficient [O(len(msg))] for large messages, should be called once before the while True loop.
Blit the surface directly onto the screen."""
    if msg == None or msg == '':
        msg = 'MESSAGE'
    def getSurf(c):
        return text_objects(c, colour, size, bold, italic, surface_only = True)
    
    character_height = getSurf('|').get_height()
    tempSurf = pg.Surface((width, character_height*len(msg)))
    tempSurf.fill(backcolour)
    x = 0
    y = 0
    if hyphenated:
        hypSurf = getSurf('-') 
        hypwidth = hypSurf.get_width()
        n = len(msg)
        i = 0
        while i < n and hyphenated:
            if msg[i] == '\n':
                x = 0
                y += (character_height + paraspacing)
            else:
                t = getSurf(msg[i])
                dx = t.get_width() 
                if msg[i] in (" ", "") and x != 0: #change back
                    tempSurf.blit(t, (x, y))
                    x += dx
                else:
                    if (i < n-1 and not msg[i+1].isalnum()) or i == n-1:
                        #x + dx > width should not occur, due to hyphenating...
                        tempSurf.blit(t, (x, y))
                        x += dx
                    else: #i < n-1 and msg[i+1].isalnum() always True, if above is False
                        dx1 = max(hypwidth, getSurf(msg[i+1]).get_width())
                        if (x + dx + dx1) <= width:
                            tempSurf.blit(t, (x, y))
                            x += dx
                        elif (x + dx + dx1) > width and (x + dx) <= width: #space for only 1 character left
                            tempSurf.blit(hypSurf, (x, y))
                            x = width + 1
                            i -= 1
                        else: #x + dx > width
                            i -= 1
                            x += dx
            if x >= width:
                x = 0
                y += (character_height+linespacing)
            i += 1

    #if not hyphenated::
    if not hyphenated:
        #msg = msg.replace('\n', ' \n')
        wordSep = ".,/?\\-=!&;:"
        word = ""
        for c in msg:
            if c in wordSep or c.isspace() or c == '\n':
                if c == '\n':
                    tc = ''
                else:
                    tc = c
                t = getSurf((word+tc))
                dx = t.get_width()
                if x + dx > width:
                    x = 0
                    y += (character_height+linespacing)
                tempSurf.blit(t, (x, y))
                x += dx
                word = ""
            else:
                word += c
            if c == '\n':
                x = 0
                y += (character_height+paraspacing)
                c = ''
    if x == 0: height = y
    else: height = y + character_height+linespacing
    surface = pg.Surface((width, height))
    surface.fill(backcolour)
    surface.blit(tempSurf, (0, 0))
    return surface

#-------------------------------------------------------------------------------
class Clickable(object):
    """parent class for any GUI element that takes a mouse click"""
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.ht = height
        self.wd = width
    def get_click(self, left = True):
        #left is a parameter for choosing which mouse key gets clicked.
        #left = True for left click and left = False for right click
        i = 0 if left == True else 1
        cur = pg.mouse.get_pos()
        clicked = pg.mouse.get_pressed()[i]
        if clicked and (self.x < cur[0] < self.x + self.wd) and (self.y < cur[1] < self.y + self.ht):
            return True
        return False

#---------------------------------------------------------------------------

class Button(Clickable):
    RETURN_TRUE = 1
    RETURN_FALSE = 2
    RETURN_NONE = 0
    def __init__(self, x, y, width, height, action = RETURN_TRUE, inactivecolour = RED, activecolour = ORANGE, text = None, textcolour = BLACK, size = 25, border = None):
        """'action' parameter will take either a function object, or a constant value defined in the class attributes of Button.
if action is a function, then the function should not take any parameters (this class will not pass any parameters)
when the action function is called, this class will return whatever the action() function returns.
if action is a constant defined in the class attributes of Button, then action will be assigned a particular null function
as defined by the name of the constant."""
        super(Button, self).__init__(x, y, width, height)
        def tempTrue(): return True
        def tempFalse(): return False
        def tempNone(): return None
        self.string = False
        if action == Button.RETURN_TRUE:
            action = tempTrue
        elif action == Button.RETURN_FALSE:
            action = tempFalse
        elif action == Button.RETURN_NONE:
            action = tempNone
        elif isinstance(action, str):
            self.string = True
        self.action = action
        self.inactive = inactivecolour
        self.active = activecolour
        self.border = border 
        if text == None:
            text = action.__name__.upper()
            if self.string:
                text = self.action
        self.text = text
        self.textcolour = textcolour
        self.size = size
    def blit(self, surface, update = False, freeze = False):
        cur = pg.mouse.get_pos()
        if not freeze and (self.x < cur[0] < self.x+self.wd) and (self.y < cur[1] < self.y + self.ht):
            c = self.active
        else:
            c = self.inactive
        pg.draw.rect(surface, c, (self.x, self.y, self.wd, self.ht))
        if self.border != None:
            pg.draw.rect(surface, self.border, (self.x, self.y, self.wd, self.ht), 1)
        text_to_button(surface, self.text, self.textcolour, self.x, self.y, self.wd, self.ht, self.size)
        if update:
            pg.display.update()
    def get_click(self, delay = True):
        flag = super(Button, self).get_click(True)
        if flag:
            if delay:
                time.sleep(0.1)
            if self.string:
                return self.action
            return self.action()

#--------------------------------------------------------------------------------------

class Dragable(object):
    '''Object that can be dragged by the mouse.
Mouse has to be held while shifting.
'''
    def __init__(self, x, y, width, height, colour = BLACK, restrict = None, xinterval = (-50, 100000),
                 yinterval = (-50, 100000), steps = 1):
        ''''restrict' restricts the movement of the object along a particular axis
restrict can only be 'y', 'x' to lock the y axis and x axis respectively
anything else does not lock any axis.
xinterval/yinterval is a 2-tuple of integers that gives a lower and upper bound
if they are None, then no limits shall be taken.
steps gives the size of the jump that the object will make'''
        self.x = x
        self.y = y
        self.movex = not(restrict == 'x')
        self.movey = not(restrict == 'y')
        self.wd = width
        self.ht = height
        self.drag = False
        self.colour = colour
        self.dx = 0
        self.dy = 0
        self.xlim = xinterval
        if not self.movex:
            self.xlim = (self.x, self.x)
        self.ylim = yinterval 
        if not self.movey:
            self.ylim = (self.y, self.y)
        self.steps = steps
        self.active = tuple(min(25+c, 200) for c in colour)
        self.dragcolour = tuple(min(int(1.5*c), 240) for c in colour)
#
#        if self.steps == 1:
#            self.xbuckets = None
#            self.ybuckets = None
#            self.xind = None
#            self.yind = None
#        else:
#            self.xbuckets = tuple(range(self.xlim[0], self.xlim[1]+1, self.steps))
#            self.ybuckets = tuple(range(self.ylim[0], self.ylim[1]+1, self.steps))
#            self.xind = (self.x - self.xlim[0])/self.steps
#            self.yind = (self.y - self.ylim[0])/self.steps
#            if self.xind >= len(self.xbuckets) or self.xind < 0:
#                self.xind = 0
#                self.x = self.xbuckets[self.xind]
#            if self.yind >= len(self.ybuckets) or self.yind < 0:
#                self.yind = 0
#                self.y = self.ybuckets[self.yind]
                
    def xbuckets(self, index):
      if not self.movex: return self.x
      if index < 0: index = 0
      if index > (self.xlim[1] - self.xlim[0]) / self.steps: index = (self.xlim[1] - self.xlim[0]) / self.steps
      return self.xlim[0] + index * self.steps 
    
    def ybuckets(self, index):
      upper = (self.ylim[1] - self.ylim[0]) / self.steps
      if not self.movey: return self.y
      if index < 0: index = 0
      if index > upper: index = upper
      return self.ylim[0] + index * self.steps 
    
    def __is_inside(self, (mx, my)):
        return (self.x < mx < self.x + self.wd) and (self.y < my < self.y + self.ht)
      
    def get_dragged(self):
        cur = pg.mouse.get_pos()
        clicked = pg.mouse.get_pressed()[0]
        if not self.drag and self.__is_inside(cur) and clicked:
            self.drag = True
            self.dx = self.steps*((cur[0] - self.x)//self.steps)
            self.dy = self.steps*((cur[1] - self.y)//self.steps)
        if self.drag and clicked:
            oldx = self.x
            oldy = self.y
            self.xind = abs(cur[0] - self.dx - self.xlim[0])/self.steps
            self.yind = abs(cur[1] - self.dy - self.ylim[0])/self.steps
            self.x = self.xbuckets(self.xind)
            self.y = self.ybuckets(self.yind)
            
            if not(self.xlim[0] <= self.x <= self.xlim[1]) or not self.movex:
                self.x = oldx
            if not(self.ylim[0] <= self.y <= self.ylim[1]) or not self.movey:
                self.y = oldy
        elif self.drag and not clicked:
            self.drag = False
            self.dx = 0
            self.dy = 0
        
        return self.drag
    
    def blit(self, surface, update = False):
        if self.drag:
            c = self.dragcolour
        elif self.__is_inside(pg.mouse.get_pos()):
            c = self.active
        else:
            c = self.colour
        pg.draw.rect(surface, c, (self.x, self.y, self.wd, self.ht))
        if update: pg.display.update()
#----------------------------------------------------------------------------
 
class InputNumberBox(object):
  def __init__(self, x, y, height, bkg_colour = WHITE, text_colour = BLACK, frozen_colour = GREY, cursorColour = BLACK, default = 0, freeze = False, tot_digits = 6, precision = 3, FPS = 30, rel_origin = (0,0), center_loc = None):
    #tot_digits = number of digits to the left of decimal point
    #precision = number of digits to the right of decimal point
    self.x = x
    self.y = y
    self.rel_origin = rel_origin
    #self.width = width
    self.height = height
    self.margin = min(max(1, int (height * 0.1)), 5)
    self.bkg_colour = bkg_colour
    self.text_colour = text_colour
    self.cursor_colour = cursorColour
    self.frozen_colour = frozen_colour
    self.freeze = freeze
    self.active = False
    self.precision = precision
    self.tot_digits = tot_digits
    self.freezeFirstDigit = False
    if tot_digits == 0:
      self.tot_digits = 1
      self.freezeFirstDigit = True
      tot_digits=1
    self.curDisplay = [None]*(tot_digits) + [0] * precision
    self.cursorIndex = 0#precision-1
    if self.freezeFirstDigit:
      self.cursorIndex += 1
    self.numberImages = [text_objects(str(i), text_colour, self.height - 2*self.margin)[0] for i in range(10)]
    self.number_width = max(img.get_rect().width for img in self.numberImages)
    self.decimalImg = text_objects('.', text_colour, self.height - 2*self.margin)[0]
    self.decimalImgWidth = self.decimalImg.get_rect().width
    self.width = (precision + tot_digits) * self.number_width + cmp(precision, 0) * self.decimalImgWidth
    self.cursorBlinkModulus = FPS/5
    self.cursorBlinkIndex = 0#self.cursorBlinkModulus
    self.showCursor = True
    if center_loc != None:
      self.x = center_loc[0] - (self.width//2)
      self.y = center_loc[1] - (self.height//2)
    self.setValue(default)
  
  def getValue(self):
    magnitude = 10.0 ** (self.tot_digits - 1)
    v = 0
    for d in self.curDisplay:
      if d != None:
        v += (magnitude * d)
      magnitude /= 10.0
    return v
  
  def setValue(self, v):
    if isinstance(v, int): v = float(v)
    str_v = ("%." + str(self.precision) + "f")%v#str(round(v, self.precision))
    if v < 10.0**(-self.precision):
      str_v = "0."+('0'*self.precision)
    if '.' in str_v:
      dot_index = str_v.index('.')
    elif self.precision == 0:
      dot_index = len(str_v)
      str_v += '.'
    else:
      print v, "string = ", str_v
      str_v = "0.0"
      dot_index = 1
    
    i = dot_index-1
    j = self.tot_digits-1
    while i >= 0 and j >= 0:
      self.curDisplay[j] = int(str_v[i])
      i -= 1
      j -= 1
    while j >= 0:
      self.curDisplay[j] = None
      j -= 1
    if self.curDisplay[self.tot_digits-1] == None:
      self.curDisplay = 0
    i = dot_index+1
    j = self.tot_digits
    while i < len(str_v) and j <self.tot_digits + self.precision:
      self.curDisplay[j] = int(str_v[i])
      i += 1
      j += 1
    while j<self.tot_digits + self.precision:
      self.curDisplay[j] = 0
      j += 1
  
  def set_freeze(self, boo):
    self.freeze = boo
    self.active = False
  
  def __blink(self):
    if self.active: self.cursorBlinkIndex += 1
    if self.cursorBlinkIndex == self.cursorBlinkModulus:
      self.showCursor = not self.showCursor
      self.cursorBlinkIndex = 0
  
  def update(self, event):
    if self.freeze: return False
    changeState = False
    if self.active and event.type == pg.KEYDOWN:
      if event.key == pg.K_RETURN or event.key == pg.K_KP_ENTER:
        self.active = False
      shift_left = False
      shift_right = False
      if event.key == pg.K_BACKSPACE:
        if self.cursorIndex < self.tot_digits: #deleting a digit to left of decimal
          del self.curDisplay[self.cursorIndex]
          self.curDisplay = [None] + self.curDisplay
          changeState = True
        else: #deleting a digit to right of decimal
          del self.curDisplay[self.cursorIndex]
          self.curDisplay.append(0)
          changeState = True
          shift_left = True
        self.getValue()
      if event.key == pg.K_LEFT: 
        shift_left = True
      if event.key == pg.K_RIGHT: 
        shift_right = True
      numberKeys = (pg.K_0, pg.K_1, pg.K_2, pg.K_3, pg.K_4, pg.K_5, pg.K_6, pg.K_7, pg.K_8, pg.K_9)
      if event.key in numberKeys:
        for i in range(10):
          if event.key == numberKeys[i]:
            changeState = True
            if self.cursorIndex < self.tot_digits:
              #for j in range(self.cursorIndex):
              #  self.curDisplay[j] = self.curDisplay[j+1]
              self.curDisplay[self.cursorIndex] = i
              #shift_left = True
            else:
              self.curDisplay[self.cursorIndex] = i
              shift_right = True
            self.setValue(self.getValue())
      
        
      if shift_right:
        self.cursorIndex += 1
        self.cursorIndex = min(self.cursorIndex, self.precision + self.tot_digits - 1)
      if shift_left:
        self.cursorIndex -= 1
        self.cursorIndex = max(self.cursorIndex, 0)
        if self.freezeFirstDigit and self.cursorIndex == 0:
          self.cursorIndex = 1
        
    if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
      mousex, mousey = pg.mouse.get_pos()
      mousex -= self.rel_origin[0]
      mousey -= self.rel_origin[1]
      if mousey < self.y or mousey > self.y + self.height or mousex < self.x or mousex > self.x+self.width:
        self.active = False
      else:
        self.active = True
        changeState = True
        rel_x = mousex - self.x
        if rel_x < self.tot_digits * self.number_width and (not self.freezeFirstDigit or rel_x >= self.number_width):
          self.cursorIndex = int(rel_x // self.number_width)
          changeState = True  
        elif rel_x > self.tot_digits * self.number_width + self.decimalImgWidth:
          self.cursorIndex = self.tot_digits + int((rel_x - self.tot_digits * self.number_width - self.decimalImgWidth)// self.number_width)
          changeState = True
    return changeState
  
  def blit(self, screen):
    self.__blink()
    bkg_colour = (self.bkg_colour if self.active else self.frozen_colour)
    pg.draw.rect(screen, bkg_colour, pg.Rect(self.x, self.y, self.width, self.height))
    curx = self.x
    for i in range(len(self.curDisplay)):
      if self.curDisplay[i] != None:
        digit_img = self.numberImages[self.curDisplay[i]]
        rect = digit_img.get_rect()
        rect.center = (curx + self.number_width // 2, self.y + self.height//2)
        screen.blit(digit_img, rect)
      if self.showCursor and self.active and self.cursorIndex == i:
        pg.draw.rect(screen, self.cursor_colour, (curx, self.y, self.number_width, self.height), self.margin)
      curx += self.number_width
      if i == self.tot_digits - 1 and self.precision != 0:
        rect = self.decimalImg.get_rect()
        rect.center = (curx + self.decimalImgWidth//2, self.y + self.height//2)
        screen.blit(self.decimalImg, rect)
        curx += self.decimalImgWidth
        

#----------------------------------------------------------------------------  
#class Slider(object):
#  def __init__(self, min_pos, max_pos, min_value, max_value, default_value = None, square_size = 10, text_center_rel_pos = (0,0), colour = GREY, step_incr = None, label = ''):
#    #all positions are considered to be center positions
#    self.min_pos = min_pos
#    self.max_pos = max_pos
#    self.min_value = min_value
#    self.max_value = max_value
#    if default_value == None: default_value = self.min_value
#    self.cur_value = default_value
#    self.colour = colour
#    if step_incr == None:
#      step_incr = max(1, min((max_value - min_value) / (max_pos[t] - min_pos[t]) for t in (0,1) if max_pos[t] != min_pos[t]))
#    self.step_incr = step_incr
#    self.text_center_rel_pos = text_center_rel_pos
#    self.label = label
#    self.increase_dir = tuple(cmp(max_pos[t], min_pos[t]) for t in (0,1))
#    self.step_size = tuple(int(float(max_pos[t] - min_pos[t]) * float(self.step_incr)/ float(max_value - min_value)) for t in (0,1))
#    self.square_size = square_size
#    self.scroller = Dragable(min_pos[0] + self.increase_dir[0] * self.square_size)
#    
#  def __getIndex(self):
#    return int(float(self.cur_value - self.min_value) / self.step_incr)
#  
#  def __getPos(self, t):
#    if self.step_size[t] == 0: return self.min_pos[t]
#    return self.min_pos[t] + (self.increase_dir[t] * self.square_size // 2) + self.step_size[t] * self.__getIndex()
#----------------------------------------------------------------------------
            
class ListBox(object):
    def __init__(self, x, y, width, height, items, ind_ht, bkgcolour = WHITE):
        #ind_ht is the individual height of each box in the ListBox
        #the height will auto adjust to ensure that ind_ht divides height
        self.x = x
        self.y = y
        self.wd = width
        self.arrowsize = 20
        if height % ind_ht != 0:
            dyup = height % ind_ht
            dydown = ind_ht - (height%ind_ht)
            if dyup > dydown:
                dht = dydown
            else:
                dht = -dyup
        else:
            dht = 0
        self.ht = height + dht
        self.numvisible = (self.ht/ind_ht)
        if len(items) < self.numvisible:
            items += ('',)*(self.numvisible-len(items))
        self.items = items
        self.ind_ht = ind_ht
        if items[-1] != '':
            self.hidden = len(items) - self.numvisible
        else:
            self.hidden = 0
##(x, y, width, height, action = RETURN_TRUE, inactivecolour = red, activecolour = orange,
##                 text = None, textcolour = black, size = 25)
        self.uparrow = Button(self.x+self.wd, self.y, self.arrowsize, self.arrowsize, Button.RETURN_TRUE,
                              GREY, LIGHTGREY, text = '/\\', size = self.arrowsize/5, border = BLACK)
        self.downarrow = Button(self.x+self.wd, self.y+self.ht-self.arrowsize, self.arrowsize, self.arrowsize,
                                Button.RETURN_TRUE, GREY, LIGHTGREY, text = '\\/', size = self.arrowsize/5,
                                border = BLACK)
        self.bkgcolour = bkgcolour
        self.scroll = self.__get_scroller()
        self.pos = 0

    def __get_scroller(self):
        ht = ((self.ht - 2*self.arrowsize)*self.numvisible)/len(self.items)
        remitems = self.hidden
        remspace = ((self.ht - 2*self.arrowsize)*self.hidden)/len(self.items)
        try:
            step = remspace/remitems
        except ZeroDivisionError:
            return None
        topmost = self.y + self.uparrow.ht 
        bottom = topmost + step*self.hidden
        return Dragable(self.x+self.wd, self.y+self.uparrow.wd, self.uparrow.wd, ht, colour = GREY, restrict = 'x',
                        yinterval = (topmost, bottom), steps = step)
    
    def __iter__(self):
        for i in self.items:
            yield i

    def __drag_scroller(self):
        if self.hidden == 0 or self.scroll == None: return
        topmost = self.y+self.uparrow.ht
        #buckets = [topmost+self.scroll.steps*i for i in xrange(self.hidden+1)]
        if self.scroll.get_dragged():
            self.pos = abs(topmost - self.scroll.y)/self.scroll.steps
    
    def shift(self):
        self.__drag_scroller()
        if self.downarrow.get_click(delay = False):
            if self.pos < len(self.items) - self.numvisible:
                self.pos += 1
                if self.scroll != None:
                    self.scroll.y += self.scroll.steps
        elif self.uparrow.get_click(delay = False):
            if self.pos > 0:
                self.pos -= 1
                if self.scroll != None:
                    self.scroll.y -= self.scroll.steps
    
    def blit(self, screen, update = False):
        pg.draw.rect(screen, self.bkgcolour, (self.x+self.wd, self.y, self.uparrow.wd, self.ht))
        self.uparrow.blit(screen, update = False)
        self.downarrow.blit(screen, update = False)
        if self.scroll == None:
            pg.draw.rect(screen, GREY, (self.x+self.wd, self.y+self.uparrow.ht, self.uparrow.wd, self.ht - 2*self.arrowsize))
        else:
            self.scroll.blit(screen, update = False)
        pg.draw.rect(screen, BLACK, (self.x-1, self.y-1, self.wd+self.uparrow.wd+2, self.ht+2), 1)
        pg.draw.line(screen, BLACK, (self.x+self.wd, self.y), (self.x+self.wd, self.y+self.ht))
        pg.draw.rect(screen, self.bkgcolour, (self.x, self.y, self.wd, self.ht))
        for i in xrange(self.pos, self.pos + self.numvisible):
            j = i - self.pos
            text_to_button(screen, str(self.items[i]), BLACK, self.x, self.y + j*self.ind_ht, self.wd,
                           self.ind_ht, int(self.ind_ht//(2.5)))
            if i != self.pos + self.numvisible - 1:
                pg.draw.rect(screen, BLACK, (self.x, self.y+(j+1)*self.ind_ht-1, self.wd, 2))
        if update: pg.display.update()

#---------------------------------------------------------------------------------------------------

class ClickListBox(ListBox, Clickable):
    RETURN_NAME = 1
    def __init__(self, x, y, width, height, actionkeys, actionvalues, ind_ht, bkgcolour = WHITE, activecolour = RED, repeat_action = False):
        self.keys = actionkeys
        self.actions = actionvalues
        self.repeat = repeat_action
        super(ClickListBox, self).__init__(x, y, width, height, self.keys, ind_ht, bkgcolour)
        self.activeselectcolour = activecolour
        self.activated = None
        
    def __is_inside(self, (mx, my)):
        return (self.x < mx < self.x + self.wd) and (self.y < my < self.y + self.ht)
    
    def get_click(self):
        self.shift()   
        if super(ClickListBox, self).get_click():
            cury = pg.mouse.get_pos()[1]
            self.activated = self.pos + (cury - self.y)//self.ind_ht
        elif pg.mouse.get_pressed()[0] and not self.__is_inside(pg.mouse.get_pos()):
            self.activated = None
        if self.activated != None:
            i = self.activated
            if not self.repeat:
                self.activated = None
            if self.actions[i] == ClickListBox.RETURN_NAME:
                return self.keys[i]
            else:
                return self.actions[i] 
            
            
    def blit(self, surface, update = False):
        super(ClickListBox, self).blit(surface, False)
        cur = pg.mouse.get_pos()
        if self.activated != None:
            i = self.activated
            j = i - self.pos
            pg.draw.rect(surface, self.activeselectcolour, (self.x, self.y + j*self.ind_ht, self.wd, self.ind_ht), 2)
            text_to_button(surface, self.keys[i], BLACK, self.x, self.y + j*self.ind_ht, self.wd,
                           self.ind_ht, 1+int(self.ind_ht//2.5))
        elif self.__is_inside(cur):
            cury = cur[1]
            k = self.pos + (cury - self.y)//self.ind_ht
            j = k - self.pos
            pg.draw.rect(surface, self.activeselectcolour, (self.x, self.y + j*self.ind_ht, self.wd, self.ind_ht), 2)
