import pygame

    
def draw_menu(self, screen, size):
    BACK_COLOR = (30, 30, 30)
    WHITE = (255, 255, 255)  
    GRAY = (200, 200, 200) 

    options = []
    x_pos = 380
    y_pos = 210

    options.append(pygame.Rect(x_pos, y_pos, 30, 50)) # option to go straight to visualizer
    options.append(pygame.Rect(x_pos + (60), y_pos, 30, 50)) # option to display settings

    font_title = pygame.font.SysFont(None, 32)
    font_options = pygame.font.SysFont(None, 20)

    start_img = font_options.render('Start', True, WHITE, BACK_COLOR)
    screen.blit(start_img, (x_pos + (10), y_pos))

    settings_img = font_options.render('Settings', True, WHITE, BACK_COLOR)
    screen.blit(settings_img, (x_pos + (70), y_pos))

    title_img = font_title.render('Main Menu', True, GRAY, BACK_COLOR)
    screen.blit(settings_img, (20, 20))

    pygame.display.update()

    while True:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                return False, False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # If left mouse button was clicked, get mouse position
                pos = pygame.mouse.get_pos()
                # Check if obj is clicked on using something such as:
                # if RectObj.collidepoint(pos)
                if options[0].collidepoint(pos):
                    pass


        screen.fill(BACK_COLOR)
        for opt in options: pygame.draw.rect(screen, opt)
    
