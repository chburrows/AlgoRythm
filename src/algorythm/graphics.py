from math import ceil, sqrt
from os.path import isfile

from pygame.constants import RESIZABLE

import algorythm.collect_media_info as media

import pygame
import threading

#pywin32
import win32api 
import win32con
import win32gui

import algorythm.backend as backend
from algorythm.settings import Settings, rgb_to_hex, hex_to_rgb
from algorythm.menu import draw_menu 
from algorythm.bars import AudioBar, DualBar, InvertedBar, RadialBar


def build_bars(settings, width):
    bars = []
    layout = settings.layout

    while len(bars) == 0:
        if len(backend.recent_frames) == 0:
            continue
        # creation of the *Bar objects and add them to the list
        # right now theres as many bars as frequencies, but they could be grouped (averaged?) to create fewer bars here
        settings.b_width = ceil((width - (settings.b_count * settings.b_gap)) / len(backend.last_freqs))
        settings.b_width = 1 if settings.b_width <= 0 else settings.b_width
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
    global cover_obj, song_cover, cover_changed, default_cover
    cover_obj = media.generate_colors()
    pil_img = cover_obj['album_art']
    if pil_img is not None:
        try:
            song_cover = pygame.image.fromstring(pil_img.tobytes(), pil_img.size, pil_img.mode).convert()
        except ValueError:
            song_cover = default_cover
    else:
        song_cover = default_cover
    cover_changed = True

def get_song_imgs(settings, fonts):
    global txt_artist, txt_title
    # Render song text
    font_artist, font_title = fonts
    txt_color = settings.text_color

    artist_img = font_artist.render(txt_artist, True, txt_color, settings.bkg_color)
    title_img = font_title.render(txt_title, True, txt_color, settings.bkg_color)
    return artist_img, title_img

def mix_colors(colors, mix):
    return [int(sqrt((1 - mix) * colors[0][i]**2 + mix * colors[1][i]**2)) for i in range(3)]

def get_default_cover(font, cover_size):
    #default album art
    default_cover = pygame.Surface((cover_size,cover_size))
    default_cover.fill(WHITE)
    default_cover_text = font.render("?", True, (0,0,0), WHITE)
    r = default_cover.get_rect()
    r.size = default_cover_text.get_size()
    r.center = [cover_size//2]*2
    default_cover.blit(default_cover_text, r)
    return default_cover

# Globals
INVIS = (1,0,1)
WHITE = (255, 255, 255)

txt_title, txt_artist = ("Title", "Artist")

cover_obj = None
song_cover = None
cover_changed = False
default_cover = None

def main():
    global song_cover, cover_obj, cover_changed, txt_title, txt_artist, size, default_cover
    pygame.init()
    pygame.font.init()
    settings = Settings()
    if isfile("./algorythm_settings"):
        settings = settings.load("algorythm_settings")

    #scale factor = maybe a non constant scale factor could be better
    # it looks like the low end consistently has higher intensity than the high end
    # Scale has been replaced by settings.multiplier
    size = settings.size

    screen = pygame.display.set_mode(size, RESIZABLE)
    pygame.display.set_caption("AlgoRythm")
    logo_img = pygame.image.load('logo.png')
    pygame.display.set_icon(logo_img)
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


    hint_imgs = [font_hint.render('Key Hints:', True, WHITE),
        font_hint2.render('Press S for Settings', True, WHITE),
        font_hint2.render('Press M to toggle window border', True, WHITE),
        font_hint2.render('Press L to toggle layout', True, WHITE),
        font_hint2.render('Press H to toggle key hints', True, WHITE)]

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

    # Load song info while menu runs
    # Draw main menu
    selection = draw_menu(screen, clock, size)
    if selection == 1:
        displaySettings = True
    elif selection == 3:
        pygame.quit()
        exit()
    else:
        displaySettings = False

    size = settings.size = screen.get_size()

    t.join()
    

    # Render default text images
    artist_img, title_img = get_song_imgs(settings, song_fonts)
    info_height = artist_img.get_height() + title_img.get_height()

    # Create Default Cover
    default_cover = get_default_cover(font_artist, info_height)

    # Get cover obj and set song cover (default if err)
    get_cover_obj()

    if song_cover is not None:
        cover_img = pygame.transform.smoothscale(song_cover, (info_height,info_height))
    else:
        cover_img = None
    
    # Connect to backend and create bars
    backend.start_stream(settings)
    settings.b_height = size[1] - info_height if settings.b_height == 0 else settings.b_height
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
    last_song_title = txt_title
    color_index = 0
    t = None
    t2 = None
    display_hints = True

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
                        screen = pygame.display.set_mode(size, RESIZABLE)
                    else:
                        screen = pygame.display.set_mode(size, pygame.NOFRAME)
                elif event.key == pygame.K_l:
                    settings.layout = (settings.layout + 1) % 4
                    bars = build_bars(settings, size[0])
                elif event.key == pygame.K_h:
                    display_hints = not display_hints
            elif event.type == pygame.VIDEORESIZE:
                size = settings.size = event.dict['size']
                settings.b_height = size[1] - info_height
                bars = build_bars(settings, size[0])
                settings.save('algorythm_settings')

            
        if last_song_title != txt_title:
            # Check to see if the song changed, if so, re-render the text
            artist_img, title_img = get_song_imgs(settings, song_fonts)
            last_song_title = txt_title
            # Check for new cover
            pygame.event.post(COVER_EVENT)

        if displaySettings:
            # run after s key has been pressed
            temp_chunk = (settings.b_count, settings.b_gap, settings.layout)
            temp_text = (settings.artist_size, settings.title_size, settings.text_color, settings.bkg_color)
            # run settings draw function and store resulting bools
            displaySettings, run = settings.draw(screen, clock, size, cover_obj['colors'])
            # Update Text Sizes and color
            if temp_text != (settings.artist_size, settings.title_size, settings.text_color, settings.bkg_color):
                font_artist = pygame.font.SysFont(custom_font, settings.artist_size, bold=True)
                font_title = pygame.font.SysFont(custom_font, settings.title_size, bold=True)
                song_fonts = font_artist, font_title
                artist_img, title_img = get_song_imgs(settings, song_fonts)
                info_height = artist_img.get_height() + title_img.get_height()
                default_cover = get_default_cover(font_artist, info_height)
                if temp_text[:2] != (settings.artist_size, settings.title_size):
                    settings.b_height = size[1] - info_height
                    cover_img = pygame.transform.smoothscale(song_cover, (info_height,info_height))
            # Update each bar with new settings
            for bar in bars:
                bar.update_properties(settings)
            if temp_chunk != (settings.b_count, settings.b_gap, settings.layout):
                # If chunk was changed, restart stream and rebuld bars
                backend.restart_stream(settings)
                bars = build_bars(settings, size[0])
            if size != settings.size:
                size = settings.size
                settings.b_height = size[1] - info_height
                bars = build_bars(settings, size[0])
            settings.save("algorythm_settings")
             
        #update bars based on levels and multiplier - have to adjust if fewer bars are used
        if settings.dyn_color and cover_obj['colors'] is not None and len(cover_obj['colors']) > 1:
            song_colors = cover_obj['colors'][:-1] + cover_obj['colors'][::-1]
            color_index = color_index % (len(song_colors) - 1) # TODO: Fix modulo by zero crash when only one in song_colors
            gradient_colors = [hex_to_rgb(x) for x in song_colors[color_index:color_index+2]]
            color_mix = timer / cover_obj['time_per_beat']
            bar_color = mix_colors(gradient_colors,color_mix)
        elif cover_obj['colors'] is not None and len(cover_obj['colors']) == 1:
            bar_color = hex_to_rgb(cover_obj['colors'][0])
        else:
            bar_color = settings.b_color

        for i, bar in enumerate(bars):
            bar.update(settings, backend.last_levels[i] * settings.multiplier, deltaTime, info_height, color=bar_color)

        # drawing logic - should be handled mostly in AudioBar draw
        screen.fill(settings.bkg_color)

        if border and display_hints:
            # Print each hint text if the border is enabled
            for index, img in enumerate(hint_imgs):
                screen.blit(img, (size[0]*.75-30 ,15+(img.get_height()*index)))
        
        # Draw each bars
        for bar in bars:
            bar.draw(screen)

        # Print song text
        if settings.enable_artist:
            screen.blit(artist_img, (info_height*settings.enable_cover+10, size[1]-info_height))
        if settings.enable_song:
            screen.blit(title_img, (info_height*settings.enable_cover+10, size[1]-title_img.get_height()))

        # Display cover if it exists
        if song_cover is not None and settings.enable_cover:
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
