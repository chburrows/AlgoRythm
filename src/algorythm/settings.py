import pygame
from algorythm.collect_media_info import generate_colors
from algorythm.pygame_objects import TextInput, Button
import pickle

# Textbox reference https://stackoverflow.com/questions/46390231/how-can-i-create-a-text-input-box-with-pygame

class Settings:
    def __init__(self, 
            normalization = 100, smoothing = 100, multiplier = 25, 
            b_width = 15, b_height = 150, b_gap = 2, b_count = 64, b_color = (255, 255, 255), 
            artist_size = 48, title_size = 32, text_color = (255, 255, 255),
            layout = 0, size = (1200, 600)
        ):
        # All are public
        # Vis Settings
        self.normalization = normalization
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

        # Layout setting
        # Layout is an int that corresponds to type. 0 = Normal, 1 = Inverted, 2 = Dual
        self.layout = layout
        self.size = size

    def save(self, filename):
        # pickle and save settings to file
        savefile = open(filename, 'wb')
        pickle.dump(self, savefile)
        savefile.close()
        return None

    def load(self, filename):
        savefile = open(filename, 'rb')
        temp = pickle.load(savefile)
        savefile.close()
        return temp

    def draw(self, screen, clock, size, colors_hex):
        BACK_COLOR = (30, 30, 30)

        WHITE = (255, 255, 255)
        GRAY = (200, 200, 200)
        BLACK = (0, 0, 0)
        RED = (255, 0, 0)
        BLUE = (0, 0, 255)
        GREEN = (0, 255, 0)

        width, height = size

        sample_rgb_colors = [RED, GREEN, BLUE, WHITE, GRAY, BLACK]
        colors = None

        # Call color scheme function, catch exceptions, and create rectangles for palette
        x_color = (width // 3) + 10
        y_color = 385

        # Ensure colors were found
        if colors_hex is not None:
            colors = []
            color_palette = []
            for i in range(len(colors_hex)):
                colors.append(hex_to_rgb(colors_hex[i]))
                color_palette.append(pygame.Rect(x_color + (20*i), y_color, 20, 20))

        sample_colors = []
        for i in range(len(sample_rgb_colors)):
            sample_colors.append(pygame.Rect(x_color + (20*i), y_color+20, 20, 20))


        # Text Input
        text_inputs = [TextInput(str(self.normalization), max_string_length=3),
            TextInput(str(self.smoothing), max_string_length=4),
            TextInput(str(self.multiplier), max_string_length=4),
            TextInput(str(self.b_width), max_string_length=4),
            TextInput(str(self.b_height), max_string_length=4),
            TextInput(str(self.b_gap), max_string_length=2),
            TextInput(str(self.b_count), max_string_length=4),
            TextInput(rgb_to_hex(self.b_color), max_string_length=6)] # Convert rgb to hex

        song_inputs = [TextInput(str(self.artist_size), max_string_length=3),
            TextInput(str(self.title_size), max_string_length=3),
            TextInput(rgb_to_hex(self.text_color), max_string_length=6)]

        # Setting Titles
        # Create font with a set size
        font = pygame.font.SysFont(None, 32)
        # Render an image with a text phrase using font
        title_img = font.render('Settings', True, GRAY, BACK_COLOR)
        vert_prop_img = font.render('Visualizer Properties', True, WHITE, BACK_COLOR)
        music_img = font.render('Music Properties', True, WHITE, BACK_COLOR)
        font_hint = pygame.font.SysFont(None, 24, italic=True)
        hint_img = font_hint.render("Press save to confirm values.", True, GRAY, BACK_COLOR)
        
        # Option text
        # NOTE: To add a new font size for text follow the format below, changing the number to the desired font size
        font_options = pygame.font.SysFont(None, 28)
        
        # NOTE: Then render the image using above font with ("Text", True, (R,G,B), BACK_COLOR)
        # If displaying multiple text elements in a row, it is easier to store them in an array
        opt_imgs = [font_options.render('Normalization:', True, WHITE, BACK_COLOR),
            font_options.render('Smoothing Level:', True, WHITE, BACK_COLOR),
            font_options.render('Multiplier:', True, WHITE, BACK_COLOR),
            font_options.render('Bar Width:', True, WHITE, BACK_COLOR),
            font_options.render('Bar Height:', True, WHITE, BACK_COLOR),
            font_options.render('Bar Gap:', True, WHITE, BACK_COLOR),
            font_options.render('Bar Count:', True, WHITE, BACK_COLOR),
            font_options.render('Bar Color (Hex):', True, WHITE, BACK_COLOR),
            font_options.render('Bar Color (Gradient):', True, WHITE, BACK_COLOR)]

        song_opt_imgs = [font_options.render('Artist Text Size:', True, WHITE, BACK_COLOR),
            font_options.render('Title Text Size:', True, WHITE, BACK_COLOR),
            font_options.render('Text Color:', True, WHITE, BACK_COLOR)]

        # Starting x_pos for text options

        save_bttn = Button("Save", (150, 60), (width-180, height-90), (0,230,38), (0,179,30), (0,255,42), text_size=32)
            
        while True:
            x_pos = width // 3
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    return False, False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_s:
                        return False, True
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    # If left mouse button was clicked, get mouse position
                    pos = pygame.mouse.get_pos()
                    # Check if obj is clicked on using something such as:
                    # if RectObj.collidepoint(pos)
                    for i, s_rect in enumerate(sample_colors):
                        if s_rect.collidepoint(pos):
                            self.b_color = sample_rgb_colors[i]
                    if colors is not None:
                        for index, c_rect in enumerate(color_palette):
                            if c_rect.collidepoint(pos):
                                self.b_color = colors[index]
                elif event.type == pygame.VIDEORESIZE:
                    width,height = size = self.size = screen.get_size()
                    save_bttn.pos = (width-180, height-90)
                    save_bttn.rect.topleft = save_bttn.pos

            # If collecting input from a text box, check if there was an update to value, then assign it to settings attribute
            for ti in text_inputs:
                ti.update(events)
            for si in song_inputs:
                si.update(events)

            # If save button was pressed, update setting values 
            if save_bttn.update(events):
                try:
                    norm = int(text_inputs[0].get_text())
                    self.normalization = norm if norm >= 0 else 100 if norm > 100 else 0
                    text_inputs[0].input_string = str(self.normalization)

                    smooth = int(text_inputs[1].get_text())
                    self.smoothing = smooth if smooth > 0 else 100 if smooth > 100 else 1
                    text_inputs[1].input_string = str(self.smoothing)

                    mult = int(text_inputs[2].get_text())
                    self.multiplier = mult if mult > 0 else 1
                    text_inputs[2].input_string = str(self.multiplier)

                    self.b_width = int(text_inputs[3].get_text())
                    self.b_height = int(text_inputs[4].get_text())
                    self.b_gap = int(text_inputs[5].get_text())
                    self.b_count = min(int(text_inputs[6].get_text()), width//(self.b_gap+1))
                    self.b_color = hex_to_rgb(text_inputs[7].get_text())
                    self.artist_size = int(song_inputs[0].get_text())
                    self.title_size = int(song_inputs[1].get_text())
                    self.text_color = hex_to_rgb(song_inputs[2].get_text())
                except ValueError:
                    # Validate input, show err in button
                    save_bttn.temp_change((200, 10, 0), "Invalid Input", 3000)

            screen.fill( BACK_COLOR )

            # NOTE: Text has to be blit to screen using the img rendered above. Just use screen.blit(img, (xpos, ypos))
            # Display title text
            screen.blit(title_img, (20, 20))
            screen.blit(vert_prop_img, (x_pos, 20))
            screen.blit(hint_img, (x_pos, 45))
            screen.blit(music_img, (x_pos*2, 20))

            # Display visualizer options
            y_pos = 60
            for index, img in enumerate(opt_imgs):
                y_pos += 30 + (30 if index == 3 else 0)
                screen.blit(img, (x_pos, y_pos))
                if index < len(text_inputs):
                    screen.blit(text_inputs[index].get_surface(), (x_pos*2-x_pos/4, y_pos))
                    text_inputs[index].set_pos((x_pos*2-x_pos/4, y_pos))

            # Display sample color rectangles
            for i in range(len(sample_colors)):
                sample_colors[i].left = x_pos + 10 + 20*i
                pygame.draw.rect(screen, sample_rgb_colors[i], sample_colors[i])

            # Display color palette for gradient
            if colors is not None:
                for ind, col in enumerate(colors):
                    color_palette[ind].left = x_pos + 10 + 20*ind
                    pygame.draw.rect(screen, col, color_palette[ind])

            # Display Music Options
            y_pos = 60
            for ind, text in enumerate(song_opt_imgs):
                y_pos += 30
                screen.blit(text, (x_pos*2, y_pos))
                screen.blit(song_inputs[ind].get_surface(), (x_pos*3-x_pos/4, y_pos))
                song_inputs[ind].set_pos((x_pos*3-x_pos/4, y_pos))


            # NOTE: For anything else that needs to be displayed, create an object with pygame (such as Rect), and draw it here with pygame.draw
            save_bttn.draw(screen)

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
    if hex_color[0] == '#':
        hex_color = hex_color[1:]

    if len(hex_color) != 6:
        return None

    return tuple(int(hex_color[i:i+2], 16) for i in (0,2,4))
