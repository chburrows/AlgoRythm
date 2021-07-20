from math import ceil
from os.path import isfile

import algorythm.collect_media_info as media

import pygame
import threading

#pywin32
import win32api 
import win32con
import win32gui

import algorythm.backend as backend
from algorythm.settings import Settings

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
    def update(self, settings, intensity, dt, text_gap):
        newPos = self.max_height * (1 - intensity * self.index / 20)
        accel = (newPos - self.draw_y) * settings.smoothing
        self.draw_y += accel * dt
        self.draw_y = max(0, min(self.max_height, self.draw_y))
        bar_height = self.max_height-self.draw_y
        self.rect = [self.x, (size[1]-self.max_height-text_gap) + self.draw_y, self.width, bar_height]
    def draw(self, screen):
        #draw the rectangle to the screen using pygame draw rect
        pygame.draw.rect(screen, self.color, self.rect, 0)

class DualBar(AudioBar):
    def update(self, settings, intensity, dt, text_gap):
        newPos = self.max_height * (1 - intensity * self.index / 20)
        accel = (newPos - self.draw_y) * settings.smoothing
        self.draw_y += accel * dt
        self.draw_y = max(0, min(self.max_height, self.draw_y))
        bar_height = self.max_height-self.draw_y
        self.rect = [self.x, (size[1]-self.max_height-text_gap) + self.draw_y - 180 + bar_height/2, self.width, bar_height]

class InvertedBar(AudioBar):
    def update(self, settings, intensity, dt, text_gap):
        newPos = self.max_height * (1 - intensity * self.index / 20)
        accel = (newPos - self.draw_y) * settings.smoothing
        self.draw_y += accel * dt
        self.draw_y = max(0, min(self.max_height, self.draw_y))
        bar_height = self.max_height-self.draw_y
        self.rect = [self.x, 0, self.width, bar_height]

def build_bars(settings, width):
    bars = []
    layout = settings.layout

    while len(bars) == 0:
        if len(backend.recent_frames) == 0:
            continue
        # creation of the *Bar objects and add them to the list
        # right now theres as many bars as frequencies, but they could be grouped (averaged?) to create fewer bars here
        settings.b_width = ceil((width - (settings.b_count * settings.b_gap)) / len(backend.last_freqs))
        if layout == 0:
            for i in range(len(backend.last_freqs)):
                bars.append(AudioBar(settings, i))
        elif layout == 1:
            for i in range(len(backend.last_freqs)):
                bars.append(InvertedBar(settings, i))
        else:
            for i in range(len(backend.last_freqs)):
                bars.append(DualBar(settings, i))
    return bars

def get_song_info():
    global txt_title, txt_artist
    txt_title, txt_artist = media.collect_title_artist()

def get_song_imgs(settings, fonts):
    global txt_artist, txt_title
    # Render song text
    font_artist, font_title = fonts
    txt_color = settings.text_color

    artist_img = font_artist.render(txt_artist, True, txt_color, INVIS)
    title_img = font_title.render(txt_title, True, txt_color, INVIS)
    return artist_img, title_img


# Globals
INVIS = (1,0,1)
WHITE = (255, 255, 255)
size = (850, 450)


txt_title, txt_artist = ("Title", "Artist")

def main():
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

    # Render default text images
    artist_img, title_img = get_song_imgs(settings, song_fonts)

    # Connect to backend and create bars
    backend.start_stream(settings)
    settings.b_height = size[1] - (artist_img.get_height() + title_img.get_height())
    bars = build_bars(settings, size[0])

    # Create custom event for retrieving song info
    GET_SONG = pygame.event.custom_type()
    SONG_EVENT = pygame.event.Event(GET_SONG)
    pygame.time.set_timer(SONG_EVENT, 3000) # Time in ms in-between song gathering

    # Track ticks
    t = pygame.time.get_ticks()
    getTicksLastFrame = t

    # Main PyGame render loop
    run = True
    border = True
    displaySettings = False
    last_song_title = txt_title
    while run:
        # Track ticks for smoothing
        t = pygame.time.get_ticks()
        deltaTime = (t - getTicksLastFrame) / 1000.0
        getTicksLastFrame = t

        for event in pygame.event.get():
            if event.type == GET_SONG:
                # Check for new song info
                last_song_title = txt_title
                t = threading.Thread(target=get_song_info)
                t.start()
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
                    settings.layout = (settings.layout + 1) % 3
                    bars = build_bars(settings, size[0])

        if last_song_title != txt_title:
            # Check to see if the song changed, if so, re-render the text
            artist_img, title_img = get_song_imgs(settings, song_fonts)
            
        if displaySettings:
            # run after s key has been pressed
            temp_chunk = settings.b_count
            temp_text = (settings.artist_size, settings.title_size, settings.text_color) 
            # run settings draw function and store resulting bools
            displaySettings, run = settings.draw(screen, clock, size)
            # Update Text Sizes and color
            if temp_text != (settings.artist_size, settings.title_size, settings.text_color):
                font_artist = pygame.font.SysFont(custom_font, settings.artist_size, bold=True)
                font_title = pygame.font.SysFont(custom_font, settings.title_size, bold=True)
                song_fonts = font_artist, font_title
                artist_img, title_img = get_song_imgs(settings, song_fonts)
                if temp_text[:2] != (settings.artist_size, settings.title_size):
                    settings.b_height = size[1] - (artist_img.get_height() + title_img.get_height())
            # Update each bar with new settings
            for bar in bars:
                bar.update_properties(settings)
            if temp_chunk != settings.b_count:
                # If chunk was changed, restart stream and rebuld bars
                backend.restart_stream(settings)
                bars = build_bars(settings, size[0])
            settings.save("algorythm_settings")

        #update bars based on levels and multiplier - have to adjust if fewer bars are used
        for i, bar in enumerate(bars):
            bar.update(settings, backend.last_levels[i] * settings.multiplier, deltaTime, artist_img.get_height() + title_img.get_height())

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
        screen.blit(artist_img, (0, size[1]-(artist_img.get_height()+title_img.get_height())))
        screen.blit(title_img, (0, size[1]-title_img.get_height()))

        pygame.display.flip()
        clock.tick(60)
        
    backend.stop_stream()
    pygame.quit()

if __name__ == "__main__":
    main()
