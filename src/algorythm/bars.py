import pygame
from math import ceil

class AudioBar:
    def __init__(self, settings, i):
        self.index = i
        self.update_properties(settings)
    def update_properties(self, settings):
        self.max_height = settings.b_height
        self.width = settings.b_width
        self.gap = settings.b_gap
        self.color = settings.b_color
        self.x = self.width * self.index + (self.index * self.gap)
        self.draw_y = self.max_height
    def update(self, settings, intensity, dt, text_gap, color=None, height=None):
        newPos = self.max_height * (1 - intensity * (self.index*settings.normalization/100+1) / 10) # Might need some tweaking
        accel = (newPos - self.draw_y) * 100/settings.smoothing # Def needs some tweaking
        self.draw_y += accel * dt
        self.draw_y = max(0, min(self.max_height, self.draw_y))
        bar_height = self.max_height-self.draw_y
        self.rect = pygame.Rect([self.x, (settings.size[1] - self.max_height - text_gap) + self.draw_y, self.width, bar_height])
        if color is not None:
            self.color = color
    def draw(self, screen):
        #draw the rectangle to the screen using pygame draw rect
        pygame.draw.rect(screen, self.color, self.rect, 0)

class DualBar(AudioBar):
    def update(self, settings, intensity, dt, text_gap, color=None, height=None):
        if height is None:
            height=settings.size[1]

        newPos = self.max_height * (1 - intensity * (self.index*settings.normalization/100+1) / 10) # Might need some tweaking
        accel = (newPos - self.draw_y) * 100/settings.smoothing # Def needs some tweaking
        self.draw_y += accel * dt
        self.draw_y = max(0, min(self.max_height, self.draw_y))
        bar_height = self.max_height-self.draw_y
        self.rect = pygame.Rect([self.x, 0, self.width, bar_height])
        if height is None:
            self.rect.centery = (settings.size[1] - text_gap)/2
        else:
            self.rect.centery = settings.size[1] - text_gap - height/2
        if color is not None:
            self.color = color

class InvertedBar(AudioBar):
    def update(self, settings, intensity, dt, text_gap, color=None, height=None):
        newPos = self.max_height * (1 - intensity * (self.index*settings.normalization/100+1) / 10) # Might need some tweaking
        accel = (newPos - self.draw_y) * 100/settings.smoothing # Def needs some tweaking
        self.draw_y += accel * dt
        self.draw_y = max(0, min(self.max_height, self.draw_y))
        bar_height = self.max_height-self.draw_y
        self.rect = pygame.Rect([self.x, 0, self.width, bar_height])
        self.rect.y = 0 if height is None else (settings.size[1] - height - text_gap)
        if color is not None:
            self.color = color

# For preview only
def build_bars(settings, count):
    bars = []
    layout = settings.layout

    # creation of the *Bar objects and add them to the list
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