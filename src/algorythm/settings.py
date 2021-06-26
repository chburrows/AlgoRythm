import pygame
import pygame_textinput as pytxt

# Textbox reference https://stackoverflow.com/questions/46390231/how-can-i-create-a-text-input-box-with-pygame

class Settings:
    def __init__(self, sensitivity = 5, smoothing = 0, multiplier = 15, b_width = 15, b_height = 150, b_gap = 0, b_count = 128, b_color = (255, 0, 0)):
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

        width, height = size

        # Convert rgb to hex
        b_color_hex = ""
        for c in self.b_color:
            color_conv = hex(c)[2:]
            b_color_hex += color_conv
            if len(color_conv) == 1:
                b_color_hex += '0'

        # Text Input
        textInputs = [pytxt.TextInput(str(self.sensitivity), max_string_length=4),
            pytxt.TextInput(str(self.smoothing), max_string_length=4),
            pytxt.TextInput(str(self.multiplier), max_string_length=4),
            pytxt.TextInput(str(self.b_width), max_string_length=4),
            pytxt.TextInput(str(self.b_height), max_string_length=4),
            pytxt.TextInput(str(self.b_gap), max_string_length=2),
            pytxt.TextInput(str(self.b_count), max_string_length=4),
            pytxt.TextInput(b_color_hex, max_string_length=6)]

        # Titles
        font = pygame.font.SysFont(None, 32)
        title_img = font.render('Settings', True, (200, 200, 200))
        vert_prop_img = font.render('Visualizer Properties', True, WHITE)
        
        font_hint = pygame.font.SysFont(None, 24)
        hint_img = font_hint.render("Press enter to confirm value.", True, (200, 200, 200))
        
        # Options
        font_options = pygame.font.SysFont(None, 28)

        opt_imgs = [font_options.render('Sensitivity:', True, WHITE),
            font_options.render('Smoothing Level:', True, WHITE),
            font_options.render('Multiplier:', True, WHITE),
            font_options.render('Bar Width:', True, WHITE),
            font_options.render('Bar Height:', True, WHITE),
            font_options.render('Bar Gap:', True, WHITE),
            font_options.render('Bar Count:', True, WHITE),
            font_options.render('Bar Color (Hex):', True, WHITE)]


        x_pos = width // 3 + 20
            
        while True:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    return False, False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_s:
                        return False, True

            # prob a better way to do this but tired
            try:
                if textInputs[0].update(events):
                    self.sensitivity = int(textInputs[0].get_text())
                elif textInputs[1].update(events):
                    self.smoothing = int(textInputs[1].get_text())
                elif textInputs[2].update(events):
                    self.multiplier = int(textInputs[2].get_text())
                elif textInputs[3].update(events):
                    self.b_width = int(textInputs[3].get_text())
                elif textInputs[4].update(events):
                    self.b_height = int(textInputs[4].get_text())
                elif textInputs[5].update(events):
                    self.b_gap = int(textInputs[5].get_text())
                elif textInputs[6].update(events):
                    self.b_count = int(textInputs[6].get_text())
                elif textInputs[7].update(events):
                    hex_color = textInputs[7].get_text()
                    # Convert hex to rgb tuple
                    self.b_color = tuple(int(hex_color[i:i+2], 16) for i in (0,2,4))
            except ValueError:
                print("Error: Invalid input, NaN.")

            screen.fill( (30, 30, 30, 150))

            # Display title text
            screen.blit(title_img, (20, 20))
            screen.blit(vert_prop_img, (x_pos, 20))
            screen.blit(hint_img, (x_pos, 45))
            # Display option text images
            y_pos = 60
            for index, img in enumerate(opt_imgs):
                y_pos += 30 + (30 if index == 3 else 0)
                screen.blit(img, (x_pos, y_pos))
                screen.blit(textInputs[index].get_surface(), (x_pos + 200, y_pos))
                textInputs[index].set_pos((x_pos + 200, y_pos))

            pygame.display.flip()
            clock.tick(30)



