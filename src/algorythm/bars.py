import pygame
from math import ceil, sqrt, cos, sin, pi


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
    def update(self, settings, intensity, dt, text_gap, color=None, height=None, width=None):
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
    def update(self, settings, intensity, dt, text_gap, color=None, height=None, width=None):
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
    def update(self, settings, intensity, dt, text_gap, color=None, height=None, width=None):
        newPos = self.max_height * (1 - intensity * (self.index*settings.normalization/100+1) / 10) # Might need some tweaking
        accel = (newPos - self.draw_y) * 100/settings.smoothing # Def needs some tweaking
        self.draw_y += accel * dt
        self.draw_y = max(0, min(self.max_height, self.draw_y))
        bar_height = self.max_height-self.draw_y
        self.rect = pygame.Rect([self.x, 0, self.width, bar_height])
        self.rect.y = 0 if height is None else (settings.size[1] - height - text_gap)
        if color is not None:
            self.color = color

class RadialBar(AudioBar):
    def update(self, settings, intensity, dt, text_gap, color=None, height=None, width=None):
        newPos = self.max_height * (1 - intensity * (self.index*settings.normalization/100+1) / 10) # Might need some tweaking
        accel = (newPos - self.draw_y) * 100/settings.smoothing # Def needs some tweaking
        self.draw_y += accel * dt
        self.draw_y = max(0, min(self.max_height, self.draw_y))
        bar_height = self.max_height - self.draw_y

        #Make radius relative to screen size?
        r = ceil(min(settings.size[0], settings.size[1]) / 15)
        #r = 30
        theta = (2 * pi * self.index / settings.b_count) - (pi / 4)
        #Use window center or account for info gap?
        if height is None:
            self.c = (settings.size[0] // 2, settings.size[1] // 2)
        else:
            self.c = (width//2, (settings.size[1] - text_gap) - height // 2)

        #self.c = (ceil(settings.size[0] / 2), ceil(settings.size[1] / 2))
        self.inner = (r * cos(theta), r * sin(theta))
        self.outer = (max(r, 2 * bar_height) * cos(theta), max(r, 2 * bar_height) * sin(theta))
        if color is not None:
            self.color = color
        self.radius = r
        self.bg_color = settings.bkg_color
    def draw(self, screen, last=False):
        #width adjustment?
        pygame.draw.line(screen, self.color, (self.c[0] + self.inner[0], self.c[1] + self.inner[1]), (self.c[0] + self.outer[0], self.c[1] + self.outer[1]), ceil(self.width / 3))
        if last:
            pygame.draw.circle(screen, self.bg_color, self.c, self.radius * 1.1)
# For preview only
def build_bars(settings, count):
    bars = []
    layout = settings.layout

    # creation of the *Bar objects and add them to the list
    if layout == 1:
        for i in range(count):
            bars.append(InvertedBar(settings, i))
    elif layout == 2:
        for i in range(count):
            bars.append(DualBar(settings, i))    
    elif layout == 3:
        for i in range(count):
            bars.append(RadialBar(settings, i))
    else:
        for i in range(count):
            bars.append(AudioBar(settings, i))
    return bars