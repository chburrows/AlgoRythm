import pygame
from pygame import draw
from algorythm.pygame_objects import Button
import webbrowser
    
def draw_menu(screen, clock, size):
    BACK_COLOR = (30, 30, 30)
    WHITE = (255, 255, 255)  
    GRAY = (200, 200, 200) 

    options = []
    but_size = (size[0]//5, 60)
    x_pos = size[0]//2 - but_size[0]//2
    y_pos = 150

    options = [Button("Start", but_size, (x_pos, y_pos), BACK_COLOR, [130]*3, GRAY, text_size=48, text_color=WHITE),
        Button("Settings", but_size, (x_pos, y_pos+but_size[1]), BACK_COLOR, [130]*3, GRAY, text_size=42, text_color=WHITE),
        Button("Open GitHub", but_size, (x_pos, y_pos+but_size[1]*2), BACK_COLOR, [130]*3, GRAY, text_size=42, text_color=WHITE),
        Button("Quit", but_size, (x_pos, y_pos+but_size[1]*3), BACK_COLOR, [130]*3, GRAY, text_size=42, text_color=WHITE)]

    font_title = pygame.font.SysFont(None, 32)
    title_img = font_title.render('Main Menu', True, GRAY, BACK_COLOR)

    # Run loop
    while True:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                return len(options)-1
            elif event.type == pygame.WINDOWRESIZED:
                size = screen.get_size()
                for i, opt in enumerate(options):
                    opt.pos = (size[0]//2 - but_size[0]//2, y_pos+60*i)
                    opt.rect.topleft = opt.pos


        for i, opt in enumerate(options):
            if opt.update(events):
                if i == 2:
                    webbrowser.open("https://github.com/cburrows1/AlgoRythm", new=0, autoraise=True)
                else:
                    return i

        screen.fill(BACK_COLOR)
        for opt in options: opt.draw(screen)
        screen.blit(title_img, (20, 20))

        pygame.display.update()
        clock.tick(30)
    
def main():
    pygame.init()
    size = (1200, 600)
    screen = pygame.display.set_mode(size, pygame.RESIZABLE)
    clock = pygame.time.Clock()
    draw_menu(screen, clock, size)


if __name__ == "__main__":
    main()
