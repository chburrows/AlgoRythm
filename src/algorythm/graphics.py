import pygame
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
SCALE = 10

size = (700, 500)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("AlgoRythm")
clock = pygame.time.Clock()

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
while run:
    displaySettings = False
    for event in pygame.event.get():
        #close program if X button clicked
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                displaySettings = True
        
    while displaySettings:
        displaySettings, run = settings.draw(screen, clock)


    #update bars based on levels - have to adjust if fewer bars are used
    for i in range(len(backend.last_levels)):
        bars[i].update(backend.last_levels[i] * SCALE)

    #drawing logic - should be handled mostly in AudioBar draw
    screen.fill( (0, 0, 0) )
    for bar in bars:
        bar.draw(screen)

    pygame.display.flip()
    clock.tick(60)
backend.stop_stream()
pygame.quit()