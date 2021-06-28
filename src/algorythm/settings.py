import pygame
import pygame_textinput as pytxt
import pickle

# Textbox reference https://stackoverflow.com/questions/46390231/how-can-i-create-a-text-input-box-with-pygame

class Settings:
    def __init__(self, 
            sensitivity = 0, smoothing = 7, multiplier = 25, 
            b_width = 15, b_height = 150, b_gap = 2, b_count = 64, b_color = (255, 255, 255), 
            artist_size = 48, title_size = 32, text_color = (255, 255, 255)
        ):
        # All are public
        # Vis Settings
        self.sensitivity = sensitivity
        self.smoothing = smoothing
        self.multiplier = multiplier
        
        # Bar Settings
        self.b_width = b_width
        self.b_height = b_height
        self.b_gap = b_gap
        self.b_count = b_count
        self.b_color = b_color

        # Music Settings
        self.artist_size = artist_size
        self.title_size = title_size
        self.text_color = text_color

    def save(self, filename):
        # pickle and save settings to file
        savefile = open(filename, 'ab')
        pickle.dump(self, savefile)
        savefile.close()
        return None
    
    def draw(self, screen, clock, size):
        WHITE = (255, 255, 255)
        BACK_COLOR = (30, 30, 30)
        GRAY = (200, 200, 200)
        width, height = size

        # Text Input
        text_inputs = [pytxt.TextInput(str(self.sensitivity), max_string_length=4),
            pytxt.TextInput(str(self.smoothing), max_string_length=4),
            pytxt.TextInput(str(self.multiplier), max_string_length=4),
            pytxt.TextInput(str(self.b_width), max_string_length=4),
            pytxt.TextInput(str(self.b_height), max_string_length=4),
            pytxt.TextInput(str(self.b_gap), max_string_length=2),
            pytxt.TextInput(str(self.b_count), max_string_length=4),
            pytxt.TextInput(rgb_to_hex(self.b_color), max_string_length=6)] # Convert rgb to hex

        song_inputs = [pytxt.TextInput(str(self.artist_size), max_string_length=3),
            pytxt.TextInput(str(self.title_size), max_string_length=3),
            pytxt.TextInput(rgb_to_hex(self.text_color), max_string_length=6)]

        # Titles
        font = pygame.font.SysFont(None, 32)
        title_img = font.render('Settings', True, GRAY, BACK_COLOR)
        vert_prop_img = font.render('Visualizer Properties', True, WHITE, BACK_COLOR)
        music_img = font.render('Music Properties', True, WHITE, BACK_COLOR)
        font_hint = pygame.font.SysFont(None, 24, italic=True)
        hint_img = font_hint.render("Press enter to confirm value.", True, GRAY, BACK_COLOR)
        
        # Options
        font_options = pygame.font.SysFont(None, 28)
        
        opt_imgs = [font_options.render('Sensitivity (db):', True, WHITE, BACK_COLOR),
            font_options.render('Smoothing Level:', True, WHITE, BACK_COLOR),
            font_options.render('Multiplier:', True, WHITE, BACK_COLOR),
            font_options.render('Bar Width:', True, WHITE, BACK_COLOR),
            font_options.render('Bar Height:', True, WHITE, BACK_COLOR),
            font_options.render('Bar Gap:', True, WHITE, BACK_COLOR),
            font_options.render('Bar Count:', True, WHITE, BACK_COLOR),
            font_options.render('Bar Color (Hex):', True, WHITE, BACK_COLOR)]

        song_opt_imgs = [font_options.render('Artist Text Size:', True, WHITE, BACK_COLOR),
            font_options.render('Title Text Size:', True, WHITE, BACK_COLOR),
            font_options.render('Text Color:', True, WHITE, BACK_COLOR)]

        x_pos = width // 3
            
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
                if text_inputs[0].update(events):
                    self.sensitivity = int(text_inputs[0].get_text())
                elif text_inputs[1].update(events):
                    self.smoothing = int(text_inputs[1].get_text())
                elif text_inputs[2].update(events):
                    self.multiplier = int(text_inputs[2].get_text())
                elif text_inputs[3].update(events):
                    self.b_width = int(text_inputs[3].get_text())
                elif text_inputs[4].update(events):
                    self.b_height = int(text_inputs[4].get_text())
                elif text_inputs[5].update(events):
                    self.b_gap = int(text_inputs[5].get_text())
                elif text_inputs[6].update(events):
                    self.b_count = int(text_inputs[6].get_text())
                elif text_inputs[7].update(events):
                    self.b_color = hex_to_rgb(text_inputs[7].get_text())
                elif song_inputs[0].update(events):
                    self.artist_size = int(song_inputs[0].get_text())
                elif song_inputs[1].update(events):
                    self.title_size = int(song_inputs[1].get_text())
                elif song_inputs[2].update(events):
                    self.text_color = hex_to_rgb(song_inputs[2].get_text())
            except ValueError:
                print("Error: Invalid input, NaN.")

            screen.fill( BACK_COLOR )

            # Display title text
            screen.blit(title_img, (20, 20))
            screen.blit(vert_prop_img, (x_pos, 20))
            screen.blit(hint_img, (x_pos, 45))
            screen.blit(music_img, (width*2//3, 20))

            # Display visualizer options
            y_pos = 60
            for index, img in enumerate(opt_imgs):
                y_pos += 30 + (30 if index == 3 else 0)
                screen.blit(img, (x_pos, y_pos))
                screen.blit(text_inputs[index].get_surface(), (x_pos + 180, y_pos))
                text_inputs[index].set_pos((x_pos + 180, y_pos))

            # Display Music Options
            y_pos = 60
            for ind, text in enumerate(song_opt_imgs):
                y_pos += 30
                screen.blit(text, (x_pos*2, y_pos))
                screen.blit(song_inputs[ind].get_surface(), (x_pos*2+180, y_pos))
                song_inputs[ind].set_pos((x_pos*2+180, y_pos))

            pygame.display.flip()
            clock.tick(30)


# Conv rgb tuple to hex
def rgb_to_hex(rgb=()):
    if len(rgb) != 3:
        return None

    new_hex = ''
    for c in rgb:
        color_conv = hex(c)[2:]
        new_hex += color_conv
        if len(color_conv) == 1:
            new_hex += '0'
    return new_hex

# Convert hex to rgb tuple
def hex_to_rgb(hex_color):
    if len(hex_color) != 6:
        return None

    return tuple(int(hex_color[i:i+2], 16) for i in (0,2,4))
