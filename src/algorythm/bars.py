import pygame
from math import ceil

class AudioBar:
    def __init__(self, settings, i):
        self.index = i
        self.max_height = settings.b_height
        self.update_properties(settings)
    def update_properties(self, settings):
        self.width = settings.b_width
        self.gap = settings.b_gap
        self.color = settings.b_color
        self.x = self.width * self.index + (self.index * self.gap)
        self.draw_y = self.max_height
    def update(self, settings, intensity, text_gap):
        bar_height = intensity * self.max_height
        self.rect = pygame.Rect([self.x+15, 0, self.width, bar_height])
        self.rect.bottom = settings.size[1]-text_gap
        self.color = settings.b_color
    def draw(self, screen):
        #draw the rectangle to the screen using pygame draw rect
        pygame.draw.rect(screen, self.color, self.rect, 0)

class DualBar(AudioBar):
    def update(self, settings, intensity, dt, text_gap, color=None):
        newPos = self.max_height * (1 - intensity * (self.index+1) / 20)
        accel = (newPos - self.draw_y) * settings.smoothing
        self.draw_y += accel * dt
        self.draw_y = max(0, min(self.max_height, self.draw_y))
        bar_height = self.max_height-self.draw_y
        self.rect = pygame.Rect([self.x, 0, self.width, bar_height])
        self.rect.centery = (settings.size[1] - text_gap)/2
        if color is not None:
            self.color = color

class InvertedBar(AudioBar):
    def update(self, settings, intensity, dt, text_gap, color=None):
        newPos = self.max_height * (1 - intensity * (self.index+1) / 20)
        accel = (newPos - self.draw_y) * settings.smoothing
        self.draw_y += accel * dt
        self.draw_y = max(0, min(self.max_height, self.draw_y))
        bar_height = self.max_height-self.draw_y
        self.rect = [self.x, 0, self.width, bar_height]
        if color is not None:
            self.color = color

def build_bars(settings, width, count):
    bars = []
    layout = settings.layout

    # creation of the *Bar objects and add them to the list
    # right now theres as many bars as frequencies, but they could be grouped (averaged?) to create fewer bars here

    if layout == 0:
        for i in range(count):
            bars.append(AudioBar(settings, i))
    elif layout == 1:
        for i in range(count):
            bars.append(InvertedBar(settings, i))
    else:
        for i in range(count):
            bars.append(DualBar(settings, i))
    return bars