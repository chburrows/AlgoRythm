import pygame
#import pygame_textinput

class Settings:
    def __init__(self, sensitivity = 0, smoothing = 0, multiplier = 100, b_width = 15, b_height = 150, b_gap = 0, b_count = 128, b_color = (255, 0, 0)):
        # All are public
        self.sensitivity = sensitivity
        self.smoothing = smoothing
        self.multiplier = multiplier
        self.b_width = b_width
        self.b_height = b_height
        self.b_gap = b_gap
        self.b_count = b_count
        self.b_color = b_color

    def save(self, file):
        # pickle and save settings to file
        return None
    
    def draw(self, screen, clock, size):
        WHITE = (255, 255, 255)

        # Titles
        font = pygame.font.SysFont(None, 32)
        title_img = font.render('Settings', True, (200, 200, 200))
        vert_prop_img = font.render('Visualizer Properties', True, WHITE)

        # Options
        font_options = pygame.font.SysFont(None, 28)

        opt_imgs = [font_options.render('Sensitivity:', True, WHITE),
            font_options.render('Smoothing Level:', True, WHITE),
            font_options.render('Multiplier:', True, WHITE),
            font_options.render('Bar Width:', True, WHITE),
            font_options.render('Bar Height:', True, WHITE),
            font_options.render('Bar Gap:', True, WHITE),
            font_options.render('Bar Count:', True, WHITE),
            font_options.render('Bar Color:', True, WHITE)]


        x_pos = size[0] // 3 + 20
            
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False, False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_s:
                        return False, True

            screen.fill( (30, 30, 30, 150))

            # Display title text
            screen.blit(title_img, (20, 20))
            screen.blit(vert_prop_img, (x_pos, 20))

            # Display option text images
            y_pos = 50
            for index, img in enumerate(opt_imgs):
                y_pos += 30 + (30 if index == 3 else 0)
                screen.blit(img, (x_pos, y_pos))

            pygame.display.flip()
            clock.tick(30)



