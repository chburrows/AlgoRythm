import pygame
#pywin32
import win32api 
import win32con
import win32gui

import backend
import settings


class AudioBar:
    def __init__(self, x, max_height, width, color):
        self.x = x
        self.max_height = max_height
        self.width = width
        self.color = color
    def update(self, intensity):
        #calculate y pos of bar based on normalized intensity from 0 to 1
        #could add velocity or some smoothing function here instead of directly translating instensity
        self.draw_y = self.max_height * ( 1 - intensity)
    def draw(self, screen):
        #draw the rectangle to the screen using pygame draw rect
        pygame.draw.rect(screen, self.color, (self.x, self.draw_y , self.width, self.max_height - self.draw_y), 0)


pygame.init()

#scale factor = maybe a non constant scale factor could be better
# it looks like the low end consistently has higher intensity than the high end
SCALE = 300

size = (850, 450)
screen = pygame.display.set_mode(size, pygame.NOFRAME)
pygame.display.set_caption("AlgoRythm")
clock = pygame.time.Clock()

invis = (255, 0, 128)

# Win32 Layered window (From https://stackoverflow.com/questions/550001/fully-transparent-windows-in-pygame)
hwnd = pygame.display.get_wm_info()["window"]
win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE,
                       win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED)
# Set window transparency color
win32gui.SetLayeredWindowAttributes(hwnd, win32api.RGB(*invis), 0, win32con.LWA_COLORKEY)

backend.start_stream()
bars = []
while len(bars) == 0:
    if len(backend.recent_frames) == 0:
        continue
    # creation of the AudioBar objects and add them to the list
    # right now theres as many bars as frequencies, but they could be grouped (averaged?) to create fewer bars here
    bar_width = size[0] / len(backend.last_freqs)
    for i in range(len(backend.last_freqs)):
        bars.append(AudioBar(bar_width * i, size[1], bar_width, (255,0,0)))

run = True
border = False
displaySettings = False
while run:
    for event in pygame.event.get():
        #close program if X button clicked
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            # Press S to open settings
            if event.key == pygame.K_s:
                displaySettings = True
            elif event.key == pygame.K_m:
                # Press M to toggle window border
                border = not border
                if border:
                    screen = pygame.display.set_mode(size)
                else:
                    screen = pygame.display.set_mode(size, pygame.NOFRAME)
        
    if displaySettings:
        displaySettings, run = settings.draw(screen, clock, size)


    #update bars based on levels - have to adjust if fewer bars are used
    for i in range(len(backend.last_levels)):
        bars[i].update(backend.last_levels[i] * SCALE)

    #drawing logic - should be handled mostly in AudioBar draw
    screen.fill( invis )
    for bar in bars:
        bar.draw(screen)

    pygame.display.flip()
    clock.tick(60)
    
backend.stop_stream()
pygame.quit()