import pygame
from pygame.locals import *

class Button():
    # Track The State Of Button
    STATE_IDLE = 'idle' # button up,mouse not over the button
    STATE_ARMED = 'armed' # button is down, mouse over the button
    STATE_DISARMED = 'disarmed'
    def __init__(self, window, loc, up, down):
        self.window = window
        self.loc = loc
        self.surfaceUp = pygame.image.load(up)
        self.surfaceDown = down
        self.rect = self.surfaceUp.get_rect()
        self.rect[0] = loc[0]
        self.rect[1] = loc[1]
        self.state = Button.STATE_IDLE
    
    def handleEvent(self, eventObj):
        if eventObj.type not in (MOUSEMOTION, MOUSEBUTTONUP, MOUSEBUTTONDOWN):
            return False
        
        eventPointInButtonRect = self.rect.collidepoint(eventObj.pos)

        if self.state == Button.STATE_IDLE:
            if (eventObj.type == MOUSEBUTTONDOWN) and eventPointInButtonRect:
                self.state = Button.STATE_ARMED
        elif self.state == Button.STATE_ARMED:
            if (eventObj.type == MOUSEBUTTONUP) and eventPointInButtonRect:
                self.state = Button.STATE_IDLE
                return True # Button Clicked
            if (eventObj.type == MOUSEMOTION) and (not eventPointInButtonRect):
                self.state = Button.STATE_DISARMED
        elif self.state == Button.STATE_DISARMED:
            if eventPointInButtonRect:
                self.state = Button.STATE_ARMED
            elif eventObj.type == MOUSEBUTTONUP:
                self.state = Button.STATE_IDLE
        return False
    
    def draw(self):
        if self.state == Button.STATE_ARMED:
            self.window.blit(self.surfaceDown, self.loc)
        else:
            self.window.blit(self.surfaceUp, self.loc)