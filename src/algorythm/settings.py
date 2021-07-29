import pygame
from algorythm.collect_media_info import generate_colors
from algorythm.bars import *
from algorythm.pygame_objects import TextInput, Button
import pickle
import random
import copy

# Textbox reference https://stackoverflow.com/questions/46390231/how-can-i-create-a-text-input-box-with-pygame

class Settings:
    def __init__(self, 
            normalization = 50, smoothing = 15, multiplier = 25, 
            b_width = 15, b_height = 0, b_gap = 2, b_count = 150, b_color = (255, 255, 255), 
            artist_size = 68, title_size = 54, text_color = (255, 255, 255),
            layout = 0, size = (1300, 800), bkg_color = (0,0,0),
            dyn_color = True, en_artist=True, en_song=True, en_cover=True
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

        self.bkg_color = bkg_color

        # Music Settings
        self.artist_size = artist_size
        self.title_size = title_size
        self.text_color = text_color

        # Layout setting
        # Layout is an int that corresponds to type. 0 = Normal, 1 = Inverted, 2 = Dual, 3 = Radial
        self.layout = layout
        self.size = size

        # Button Settings
        self.dyn_color = dyn_color
        self.enable_artist = en_artist
        self.enable_song = en_song
        self.enable_cover = en_cover

    def Settings(self, settings_):
        return copy.deepcopy(settings_)

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

        DARK_RED = (153, 0, 0)
        RED = (255, 0, 0)
        LIGHT_RED = (255, 102, 102)
        ORANGE = (255,128,0)
        YELLOW = (255, 255, 0)
        LIME_GREEN = (128, 255, 0)
        DARK_GREEN = (0, 153, 0)
        GREEN = (0, 255, 0)
        LIGHT_GREEN = (102, 255, 102)
        AQUA = (0, 255, 255)
        PALE_BLUE = (0, 128, 255)
        BLUE = (0, 0, 255)
        PURPLE = (127, 0, 255)
        PINK = (255, 0, 255)
        BLACK = (0, 0, 0)
        GRAY = (128,128,128)
        WHITE = (255, 255, 255)

        width, height = size

        sample_rgb_colors = [DARK_RED, RED, LIGHT_RED, ORANGE, YELLOW, LIME_GREEN, DARK_GREEN, GREEN, LIGHT_GREEN, AQUA, PALE_BLUE, BLUE, PURPLE, PINK, BLACK, GRAY, WHITE]
        colors = None

        # Call color scheme function, catch exceptions, and create rectangles for palette
        x_color = (width // 3) + 10
        y_color = 420

        # Ensure colors were found
        if colors_hex is not None:
            colors = []
            color_palette = []
            for i in range(len(colors_hex)):
                colors.append(hex_to_rgb(colors_hex[i]))
                color_palette.append(pygame.Rect(x_color + (20*i), y_color, 20, 20))

        sample_colors = []
        cutoff = width//60 - 1
        for i in range(ceil(len(sample_rgb_colors)/cutoff)):
            for j in range(cutoff):
                if i*cutoff + j >= len(sample_rgb_colors):
                    break
                sample_colors.append(pygame.Rect(x_color + (20*j), y_color+(20*i)+20, 20, 20))


        # Text Input
        text_inputs = [TextInput(str(self.normalization), max_string_length=3),
            TextInput(str(self.smoothing), max_string_length=3),
            TextInput(str(self.multiplier), max_string_length=4),
            TextInput(str(self.b_width), max_string_length=4),
            TextInput(str(self.b_height), max_string_length=4),
            TextInput(str(self.b_gap), max_string_length=3),
            TextInput(str(self.b_count), max_string_length=4),
            TextInput(rgb_to_hex(self.b_color), max_string_length=6),
            TextInput(rgb_to_hex(self.bkg_color), max_string_length=6)] # Convert rgb to hex

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
        hint2_img = font_hint.render("Try setting a color to \"INV\".", True, GRAY, BACK_COLOR)
        preview_img = font.render('Visualizer Preview', True, WHITE, BACK_COLOR)
        
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
            font_options.render('Background Color (Hex):', True, WHITE, BACK_COLOR),
            font_options.render('Dynamic Bar Color:', True, WHITE, BACK_COLOR)]

        song_opt_imgs = [font_options.render('Artist Text Size:', True, WHITE, BACK_COLOR),
            font_options.render('Title Text Size:', True, WHITE, BACK_COLOR),
            font_options.render('Text Color (Hex):', True, WHITE, BACK_COLOR),
            font_options.render('Display Artist:', True, WHITE, BACK_COLOR),
            font_options.render("Display Title:", True, WHITE, BACK_COLOR),
            font_options.render('Display Cover Art:', True, WHITE, BACK_COLOR)]

        # Choose layout
        layout_opt_imgs = [font.render('Layout Selection', True, WHITE, BACK_COLOR),
            font_options.render('Normal Bars:', True, WHITE, BACK_COLOR),
            font_options.render('Inverted Bars:', True, WHITE, BACK_COLOR),
            font_options.render('Dual Bars:', True, WHITE, BACK_COLOR),
            font_options.render('Radial Bars:', True, WHITE, BACK_COLOR)]

        # Button Objects
        save_bttn = Button("Save", (150, 60), (width-180, height-90), (0,230,38), (0,179,30), (0,255,42), text_size=32, set_border=True)
        dynamic_checkbox = Button("", (20,20), (width*7//12, 90+30*len(opt_imgs)), [97]*3, [158]*3, WHITE, True, toggle=True)
        dynamic_checkbox.active = self.dyn_color

        close_bttn = Button("x", (40,40), (width-60, 20), DARK_RED, RED, LIGHT_RED, True, text_size=48)

        song_boxes = []
        for i in range(3):
            song_boxes.append(Button("", (20,20), (width*11//12, 90+30*(i+3)), [97]*3, [158]*3, WHITE, True, toggle=True))
        song_boxes[0].active = self.enable_artist
        song_boxes[1].active = self.enable_song
        song_boxes[2].active = self.enable_cover

        layout_boxes = []
        for i in range(4):
            layout_boxes.append(Button("", (20,20), (width//4, 130+30*(i)), [97]*3, [158]*3, WHITE, True, toggle=True))
            layout_boxes[i].active = True if i == self.layout else False

        # Preview
        def build_preview_bars():
            p_width = width//3 - 40
            count = p_width//(self.b_gap+self.b_width) if self.layout != 3 else self.b_count
            preview_bars = build_bars(self, count)
            for bar in preview_bars:
                bar.max_height = bar.draw_y = height//3
                bar.x += 20
                bar.update(self, random.gauss(.5, 0.15)*2/(bar.index +1) * self.multiplier, 0.015, 30, color=self.b_color, height=height//3, width=p_width)
            return preview_bars

        p_bars = build_preview_bars()

        width_diff = 0
        while True:
            # Starting x_pos for text options
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
                            text_inputs[7].input_string = rgb_to_hex(self.b_color)
                            p_bars = build_preview_bars()
                    if colors is not None:
                        for index, c_rect in enumerate(color_palette):
                            if c_rect.collidepoint(pos):
                                self.b_color = colors[index]
                                text_inputs[7].input_string = rgb_to_hex(self.b_color)
                                p_bars = build_preview_bars()
                elif event.type == pygame.VIDEORESIZE:
                    size = self.size = screen.get_size()
                    width_diff = size[0] - width
                    width, height = size
                    # Reposition buttons/checkboxes
                    save_bttn.pos = (width-180, height-90)
                    save_bttn.rect.topleft = save_bttn.pos
                    dynamic_checkbox.pos = (width*7//12, 90+30*len(opt_imgs))
                    dynamic_checkbox.rect.topleft = dynamic_checkbox.pos
                    close_bttn.pos = (width-60, 20)
                    close_bttn.rect.topleft = close_bttn.pos
                    for ind, b in enumerate(song_boxes):
                        b.pos = (width*11//12, 90+30*(ind+3))
                        b.rect.topleft = b.pos
                    for i, lb in enumerate(layout_boxes):
                        lb.pos = (width//4, 130+30*(i))
                        lb.rect.topleft = lb.pos
                    p_bars = build_preview_bars() # Reset preview

            # If save button was pressed, update setting values 
            if save_bttn.update(events):
                try:
                    norm = int(text_inputs[0].get_text())
                    self.normalization = norm if norm >= 0 and norm <= 100 else 100 if norm > 100 else 0
                    text_inputs[0].input_string = str(self.normalization)

                    smooth = int(text_inputs[1].get_text())
                    self.smoothing = smooth if smooth > 0 and smooth <= 100 else 100 if smooth > 100 else 1
                    text_inputs[1].input_string = str(self.smoothing)

                    mult = int(text_inputs[2].get_text())
                    self.multiplier = mult if mult > 0 else 1
                    text_inputs[2].input_string = str(self.multiplier)

                    wid = int(text_inputs[3].get_text())
                    self.b_width = wid if wid > 0 else 1
                    text_inputs[3].input_string = str(self.b_width)
                    
                    ht = int(text_inputs[4].get_text())
                    self.b_height = ht if ht > 0 else 1
                    text_inputs[4].input_string = str(self.b_height)

                    gap = int(text_inputs[5].get_text())
                    self.b_gap = gap if gap >= 0 else 0
                    text_inputs[5].input_string = str(self.b_gap)
                    
                    self.b_count = min(int(text_inputs[6].get_text()), width//(self.b_gap+1))
                    self.b_count = 1 if self.b_count < 1 else self.b_count
                    text_inputs[6].input_string = str(self.b_count)

                    # Bar Color Option
                    b_c = text_inputs[7].get_text()
                    if b_c.upper() == 'INV':
                        self.b_color = (1,0,1)
                    elif len(b_c) != 6:
                        text_inputs[7].input_string = rgb_to_hex(self.b_color)
                        raise ValueError("Invalid Hex")
                    else:
                        self.b_color = hex_to_rgb(b_c)

                    # Background Color Option
                    bkg_c = text_inputs[8].get_text()
                    if bkg_c.upper() == 'INV':
                        self.bkg_color = (1,0,1)
                    elif len(bkg_c) != 6:
                        text_inputs[8].input_string = rgb_to_hex(self.bkg_color)
                        raise ValueError("Invalid Hex")
                    else:
                        self.bkg_color = hex_to_rgb(bkg_c)

                    # Song Options
                    a_size = int(song_inputs[0].get_text())
                    self.artist_size = a_size if a_size > 0 else self.artist_size
                    song_inputs[0].input_string = str(self.artist_size)

                    t_size = int(song_inputs[1].get_text())
                    self.title_size = t_size if t_size > 0 else self.title_size
                    song_inputs[1].input_string = str(self.title_size)

                    t_c = song_inputs[2].get_text()
                    if t_c.upper() == 'INV':
                        self.text_color = (1,0,1)
                    elif len(t_c) != 6:
                        song_inputs[2].input_string = rgb_to_hex(self.text_color)
                        raise ValueError("Invalid Hex")
                    else:
                        self.text_color = hex_to_rgb(t_c)
                except ValueError:
                    # Validate input, show err in button
                    save_bttn.temp_change((200, 10, 0), "Invalid Input", 3000)

                p_bars = build_preview_bars()

            if close_bttn.update(events):
                # Exit settings
                return False, True

            # If collecting input from a text box, check if there was an update to value, then assign it to settings attribute
            for ti in text_inputs:
                ti.update(events)
            for si in song_inputs:
                si.update(events)

            # Checkbox for dynamic color checked
            if dynamic_checkbox.update(events):
                self.dyn_color = not self.dyn_color

            if song_boxes[0].update(events):
                self.enable_artist = not self.enable_artist
            if song_boxes[1].update(events):
                self.enable_song = not self.enable_song
            if song_boxes[2].update(events):
                self.enable_cover = not self.enable_cover

            screen.fill(BACK_COLOR)
            
            for i, lb in enumerate(layout_boxes):
                if lb.update(events):
                    self.layout = i
                    p_bars = build_preview_bars()
                lb.active = True if i == self.layout else False

            # NOTE: Text has to be blit to screen using the img rendered above. Just use screen.blit(img, (xpos, ypos))
            # Display title text
            screen.blit(title_img, (20, 20))
            screen.blit(vert_prop_img, (x_pos, 20))
            screen.blit(hint_img, (x_pos, 45))
            screen.blit(hint2_img, (x_pos*2, 45))
            screen.blit(music_img, (x_pos*2, 20))

            # Display visualizer options
            y_pos = 60
            for index, img in enumerate(opt_imgs):
                y_pos += 30 + (30 if index == 3 else 0)
                screen.blit(img, (x_pos, y_pos))
                if index != 9:
                    screen.blit(text_inputs[index].get_surface(), (x_pos*2-x_pos/4, y_pos))
                    text_inputs[index].set_pos((x_pos*2-x_pos/4, y_pos))

            # Display sample color rectangles, update pos if necessary
            if width_diff != 0:
                cutoff = width//60 - 1
                for i in range(ceil(len(sample_rgb_colors)/cutoff)):
                    for j in range(cutoff):
                        if i*cutoff + j >= len(sample_rgb_colors):
                            break
                        sample_colors[i*cutoff+j].topleft=(width//3 + 10 + (20*j), 420+(20*i)+20)

            for i in range(len(sample_colors)):
                pygame.draw.rect(screen, sample_rgb_colors[i], sample_colors[i])

            # Display color palette for gradient
            if colors is not None:
                for ind, col in enumerate(colors):
                    if width_diff != 0:
                        color_palette[ind].x = width//3 + 10 + (20*ind)
                    pygame.draw.rect(screen, col, color_palette[ind])

            # Display Music Options
            y_pos = 60
            for ind, text in enumerate(song_opt_imgs):
                y_pos += 30
                screen.blit(text, (x_pos*2, y_pos))
                if ind <=2:
                    screen.blit(song_inputs[ind].get_surface(), (x_pos*3-x_pos/4, y_pos))
                    song_inputs[ind].set_pos((x_pos*3-x_pos/4, y_pos))

            # Display layout opts
            y_pos = 70
            for i, lo_img in enumerate(layout_opt_imgs):
                screen.blit(lo_img, (30, y_pos))
                y_pos += 30 + (30 if i == 0 else 0)

            # NOTE: For anything else that needs to be displayed, create an object with pygame (such as Rect), and draw it here with pygame.draw
            save_bttn.draw(screen)
            close_bttn.draw(screen)
            dynamic_checkbox.draw(screen)
            for cb in song_boxes: cb.draw(screen) 
            for lb in layout_boxes: lb.draw(screen)

            # Display preview
            for i,bar in enumerate(p_bars):
                if i == len(p_bars) - 1 and self.layout == 3:
                    #Check if current bar is last bar in radial layout to display overlapping circle
                    bar.draw(screen, True)
                else:
                    bar.draw(screen)

            pr = preview_img.get_rect()
            pr.centerx = x_pos//2
            pr.bottom = height*2//3 - 50
            screen.blit(preview_img, pr)

            width_diff = 0
            pygame.display.flip()
            clock.tick(30)


# Conv rgb tuple to hex
def rgb_to_hex(rgb=()):
    if len(rgb) != 3:
        return None

    new_hex = ''
    for c in rgb:
        color_conv = hex(c)[2:]
        if len(color_conv) == 1:
            new_hex += '0'
        new_hex += color_conv
    return new_hex

# Convert hex to rgb tuple
def hex_to_rgb(hex_color):
    if len(hex_color) == 7 and hex_color[0] == '#':
        hex_color = hex_color[1:]

    if len(hex_color) != 6:
        return None

    return tuple(int(hex_color[i:i+2], 16) for i in (0,2,4))
