from math import ceil, sqrt, cos, sin
from os.path import isfile

from pygame import color

import algorythm.collect_media_info as media

import pygame
import threading
from PIL import Image

#pywin32
import win32api 
import win32con
import win32gui

import algorythm.backend as backend
from algorythm.settings import Settings, rgb_to_hex, hex_to_rgb

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
    def update(self, settings, intensity, dt, text_gap, color=None):
        newPos = self.max_height * (1 - intensity * (self.index+1) / 20)
        accel = (newPos - self.draw_y) * settings.smoothing
        self.draw_y += accel * dt
        self.draw_y = max(0, min(self.max_height, self.draw_y))
        bar_height = self.max_height-self.draw_y
        self.rect = [self.x, self.draw_y, self.width, bar_height]
        if color is not None:
            self.color = color
    def draw(self, screen):
        #draw the rectangle to the screen using pygame draw rect
        pygame.draw.rect(screen, self.color, self.rect, 0)

class DualBar(AudioBar):
    def update(self, settings, intensity, dt, text_gap, color=None):
        newPos = self.max_height * (1 - intensity * (self.index+1) / 20)
        accel = (newPos - self.draw_y) * settings.smoothing
        self.draw_y += accel * dt
        self.draw_y = max(0, min(self.max_height, self.draw_y))
        bar_height = self.max_height-self.draw_y
        self.rect = [self.x, self.draw_y + bar_height/2 - self.max_height/2, self.width, bar_height]
        if color is not None:
            self.color = color

class InvertedBar(AudioBar):
    def update(self, settings, intensity, dt, text_gap, color=None):
        newPos = self.max_height * (1 - intensity * (self.index+1) / 20)
        accel = (newPos - self.draw_y) * settings.smoothing
        self.draw_y += accel * dt
        self.draw_y = max(0, min(self.max_height, self.draw_y))
        bar_height = self.max_height-self.draw_y
        self.rect = [self.x, 0, self.width, bar_height]
        if color is not None:
            self.color = color

class RadialBar(AudioBar):
    def update(self, settings, intensity, dt, text_gap, color=None):
        newPos = self.max_height * (1 - intensity * self.index / 20)
        accel = (newPos - self.draw_y) * settings.smoothing
        self.draw_y += accel * dt
        self.draw_y = max(0, min(self.max_height, self.draw_y))
        bar_height = self.max_height-self.draw_y
        self.rect = [self.x, 0, self.width, bar_height]
        theta = (360 / (settings.b_count * self.width)) * self.index
        self.x0 = 30 * cos(theta)
        self.y0 = 30 * sin(theta)
        self.x1 = cos(theta) * max(30, 3 * bar_height)
        self.y1 = sin(theta) * max(30, 3 * bar_height)
        if color is not None:
            self.color = color
    def draw(self, screen):
        pygame.draw.line(screen, self.color, (400 + self.x0, 200 + self.y0), (400 + self.x1, 200 + self.y1), ceil(self.width / 2))

def build_bars(settings, width):
    bars = []
    layout = settings.layout

    while len(bars) == 0:
        if len(backend.recent_frames) == 0:
            continue
        # creation of the *Bar objects and add them to the list
        # right now theres as many bars as frequencies, but they could be grouped (averaged?) to create fewer bars here
        settings.b_width = ceil((width - (settings.b_count * settings.b_gap)) / len(backend.last_freqs))
        #TODO - replace if/else ladder with layout dict
        if layout == 1:
            for i in range(len(backend.last_freqs)):
                bars.append(InvertedBar(settings, i))
        elif layout == 2:
            for i in range(len(backend.last_freqs)):
                bars.append(DualBar(settings, i))
        elif layout == 3:
            for i in range(len(backend.last_freqs)):
                bars.append(RadialBar(settings, i))
        else:
            for i in range(len(backend.last_freqs)):
                bars.append(AudioBar(settings, i))
    return bars

def get_song_info():
    global txt_title, txt_artist, cover_obj
    txt_title, txt_artist =  media.collect_title_artist()

def get_cover_obj():
    global cover_obj, song_cover, cover_changed
    cover_obj = media.generate_colors()
    pil_img = cover_obj['album_art']
    if pil_img is not None:
        song_cover = pygame.image.fromstring(pil_img.tobytes(), pil_img.size, pil_img.mode).convert()
        cover_changed = True
    else:
        # Could set song_cover with a template img here when no cover is found
        song_cover = None

def get_song_imgs(settings, fonts):
    global txt_artist, txt_title
    # Render song text
    font_artist, font_title = fonts
    txt_color = settings.text_color

    artist_img = font_artist.render(txt_artist, True, txt_color, INVIS)
    title_img = font_title.render(txt_title, True, txt_color, INVIS)
    return artist_img, title_img

def mix_colors(colors, mix):
    return [int(sqrt((1 - mix) * colors[0][i]**2 + mix * colors[1][i]**2)) for i in range(3)]

# Globals
INVIS = (1,0,1)
WHITE = (255, 255, 255)
size = (850, 450)

txt_title, txt_artist = ("Title", "Artist")

cover_obj = None
song_cover = None
cover_changed = False

def main():
    global song_cover, cover_obj, cover_changed, txt_title, txt_artist
    pygame.init()
    pygame.font.init()
    settings = Settings()
    if isfile("./algorythm_settings"):
        settings = settings.load("algorythm_settings")

    #scale factor = maybe a non constant scale factor could be better
    # it looks like the low end consistently has higher intensity than the high end
    # Scale has been replaced by settings.multiplier

    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("AlgoRythm")
    clock = pygame.time.Clock()

    # Win32 Layered window (From https://stackoverflow.com/questions/550001/fully-transparent-windows-in-pygame)
    hwnd = pygame.display.get_wm_info()["window"]
    win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE,
                        win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED)
    # Set window transparency color
    win32gui.SetLayeredWindowAttributes(hwnd, win32api.RGB(*INVIS), 0, win32con.LWA_COLORKEY)

    # Font for user hints
    font_hint = pygame.font.SysFont(None, 24)
    font_hint2 = pygame.font.SysFont(None, 22, italic=True)

    hint_imgs = [font_hint.render('Key Hints:', True, WHITE, INVIS),
        font_hint2.render('Press S for Settings', True, WHITE, INVIS),
        font_hint2.render('Press M to toggle window border', True, WHITE, INVIS),
        font_hint2.render('Press L to toggle layout', True, WHITE, INVIS)]

    # Song Desciption Text
    # Allow for custom fonts in future

    custom_font = None
    artist_size, title_size = (settings.artist_size, settings.title_size)
    font_artist = pygame.font.SysFont(custom_font, artist_size, bold=True)
    font_title = pygame.font.SysFont(custom_font, title_size, bold=True)
    song_fonts = font_artist, font_title

    # Create thread for getting song info
    t = threading.Thread(target=get_song_info)
    t.start()
    t.join()
    
    # Get cover obj
    # And set song cover
    get_cover_obj()

    # Render default text images
    artist_img, title_img = get_song_imgs(settings, song_fonts)
    info_height = artist_img.get_height() + title_img.get_height()

    if song_cover is not None:
        cover_img = pygame.transform.smoothscale(song_cover, (info_height,info_height))
    else:
        cover_img = None
    
    # Connect to backend and create bars
    backend.start_stream(settings)
    settings.b_height = size[1] - info_height
    bars = build_bars(settings, size[0])

    # Create custom event for retrieving song info
    GET_SONG = pygame.event.custom_type()
    SONG_EVENT = pygame.event.Event(GET_SONG)
    pygame.time.set_timer(SONG_EVENT, 3000) # Time in ms in-between song gathering

    GET_COVER = pygame.event.custom_type()
    COVER_EVENT = pygame.event.Event(GET_COVER)

    # Track ticks
    tick_count = pygame.time.get_ticks()
    getTicksLastFrame = tick_count
    timer = 0
    # Main PyGame render loop
    run = True
    border = True
    displaySettings = False
    last_song_title = txt_title
    color_index = 0
    t = None
    t2 = None

    while run:
        # Track ticks for smoothing
        tick_count = pygame.time.get_ticks()
        deltaTime = (tick_count - getTicksLastFrame) / 1000.0
        getTicksLastFrame = tick_count
        timer += deltaTime
        if timer >= cover_obj['time_per_beat']:
            timer = 0
            color_index += 1

        # Handle pygame events
        for event in pygame.event.get():
            if event.type == GET_SONG:
                # Check for new song info
                if t is not None and t.is_alive():
                    t.join(0)

                last_song_title = txt_title
                t = threading.Thread(target=get_song_info)
                t.start()
            elif event.type == GET_COVER:
                if t2 is not None and t2.is_alive():
                    t2.join(0)
                t2 = threading.Thread(target=get_cover_obj)
                t2.start()
            elif event.type == pygame.QUIT:
                #close program if X button clicked
                run = False
            elif event.type == pygame.KEYDOWN:
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
                elif event.key == pygame.K_l:
                    settings.layout = (settings.layout + 1) % 4
                    bars = build_bars(settings, size[0])
            
        if last_song_title != txt_title:
            # Check to see if the song changed, if so, re-render the text
            artist_img, title_img = get_song_imgs(settings, song_fonts)
            last_song_title = txt_title
            # Check for new cover
            pygame.event.post(COVER_EVENT)

        if displaySettings:
            # run after s key has been pressed
            temp_chunk = settings.b_count
            temp_text = (settings.artist_size, settings.title_size, settings.text_color) 
            # run settings draw function and store resulting bools
            displaySettings, run = settings.draw(screen, clock, size, cover_obj['colors'])
            # Update Text Sizes and color
            if temp_text != (settings.artist_size, settings.title_size, settings.text_color):
                font_artist = pygame.font.SysFont(custom_font, settings.artist_size, bold=True)
                font_title = pygame.font.SysFont(custom_font, settings.title_size, bold=True)
                song_fonts = font_artist, font_title
                artist_img, title_img = get_song_imgs(settings, song_fonts)
                info_height = artist_img.get_height() + title_img.get_height()
                if temp_text[:2] != (settings.artist_size, settings.title_size):
                    settings.b_height = size[1] - info_height
                    cover_img = pygame.transform.smoothscale(song_cover, (info_height,info_height))
            # Update each bar with new settings
            for bar in bars:
                bar.update_properties(settings)

            if temp_chunk != settings.b_count:
                # If chunk was changed, restart stream and rebuld bars
                backend.restart_stream(settings)
                bars = build_bars(settings, size[0])
            settings.save("algorythm_settings")

        #update bars based on levels and multiplier - have to adjust if fewer bars are used
        if cover_obj['colors'] is not None:
            song_colors = cover_obj['colors'][:-1] + cover_obj['colors'][::-1]
            color_index = color_index % (len(song_colors) - 1)
            gradient_colors = [hex_to_rgb(x) for x in song_colors[color_index:color_index+2]]
            color_mix = timer / cover_obj['time_per_beat']
            bar_color = mix_colors(gradient_colors,color_mix)
        else:
            bar_color = settings.b_color

        for i, bar in enumerate(bars):
            bar.update(settings, backend.last_levels[i] * settings.multiplier, deltaTime, info_height, color=bar_color)

        # drawing logic - should be handled mostly in AudioBar draw
        screen.fill( INVIS )

        # Draw each bar
        for bar in bars:
            bar.draw(screen)

        if border:
            # Print each hint text if the border is enabled
            for index, img in enumerate(hint_imgs):
                screen.blit(img, (size[0]*.75-30 ,15+(img.get_height()*index)))

        # Print song text
        screen.blit(artist_img, (info_height+10, size[1]-info_height))
        screen.blit(title_img, (info_height+10, size[1]-title_img.get_height()))

        # Display cover if it exists
        if song_cover is not None:
            if cover_changed or cover_img is None:
                cover_img = pygame.transform.smoothscale(song_cover, (info_height,info_height))
                cover_changed = False
            screen.blit(cover_img, (0,size[1]-info_height))

        pygame.display.flip()
        clock.tick(60)
        
    backend.stop_stream()
    pygame.quit()

if __name__ == "__main__":
    main()
