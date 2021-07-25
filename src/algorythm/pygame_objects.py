"""
Copyright 2017, Silas Gyger, silasgyger@gmail.com, All rights reserved.

Borrowed from https://github.com/Nearoo/pygame-text-input under the MIT license.
"""

import os.path

import pygame
import pygame.locals as pl

pygame.font.init()


class TextInput:
    """
    This class lets the user input a piece of text, e.g. a name or a message.
    This class let's the user input a short, one-lines piece of text at a blinking cursor
    that can be moved using the arrow-keys. Delete, home and end work as well.
    """
    def __init__(
            self,
            initial_string="",
            font_family="",
            font_size=28,
            antialias=True,
            text_color=(255, 255, 255),
            cursor_color=(240, 240, 240),
            repeat_keys_initial_ms=400,
            repeat_keys_interval_ms=35,
            max_string_length=-1,
            password=False):
        """
        :param initial_string: Initial text to be displayed
        :param font_family: name or list of names for font (see pygame.font.match_font for precise format)
        :param font_size:  Size of font in pixels
        :param antialias: Determines if antialias is applied to font (uses more processing power)
        :param text_color: Color of text (duh)
        :param cursor_color: Color of cursor
        :param repeat_keys_initial_ms: Time in ms before keys are repeated when held
        :param repeat_keys_interval_ms: Interval between key press repetition when held
        :param max_string_length: Allowed length of text
        """

        # Text related vars:
        self.antialias = antialias
        self.text_color = text_color
        self.font_size = font_size
        self.max_string_length = max_string_length
        self.password = password
        self.input_string = initial_string  # Inputted text

        if not os.path.isfile(font_family):
            font_family = pygame.font.match_font(font_family)

        self.font_object = pygame.font.Font(font_family, font_size)

        # Text-surface will be created during the first update call:
        self.surface = pygame.Surface((1, 1))
        self.surface.set_alpha(0)

        # Vars to make keydowns repeat after user pressed a key for some time:
        self.keyrepeat_counters = {}  # {event.key: (counter_int, event.unicode)} (look for "***")
        self.keyrepeat_intial_interval_ms = repeat_keys_initial_ms
        self.keyrepeat_interval_ms = repeat_keys_interval_ms

        # Things cursor:
        self.cursor_surface = pygame.Surface((int(self.font_size / 20 + 1), self.font_size))
        self.cursor_surface.fill(cursor_color)
        self.cursor_position = len(initial_string)  # Inside text
        self.cursor_visible = False  # Switches every self.cursor_switch_ms ms
        self.cursor_switch_ms = 500  # /|\
        self.cursor_ms_counter = 0

        self.pos = (0, 0)

        self.active = False

        self.clock = pygame.time.Clock()

    def update(self, events):
        for event in events:
            if event.type == pl.MOUSEBUTTONDOWN:
                if self.check_collide(event.pos):
                    self.active = True
                else:
                    self.active = False
            if event.type == pl.KEYDOWN and self.active:
                self.cursor_visible = True  # So the user sees where he writes

                # If none exist, create counter for that key:
                if event.key not in self.keyrepeat_counters:
                    if not event.key == pl.K_RETURN: # Filters out return key, others can be added as necessary
                        self.keyrepeat_counters[event.key] = [0, event.unicode]

                if event.key == pl.K_BACKSPACE:
                    self.input_string = (
                        self.input_string[:max(self.cursor_position - 1, 0)]
                        + self.input_string[self.cursor_position:]
                    )

                    # Subtract one from cursor_pos, but do not go below zero:
                    self.cursor_position = max(self.cursor_position - 1, 0)
                elif event.key == pl.K_DELETE:
                    self.input_string = (
                        self.input_string[:self.cursor_position]
                        + self.input_string[self.cursor_position + 1:]
                    )

                elif event.key == pl.K_RETURN:
                    return True

                elif event.key == pl.K_RIGHT:
                    # Add one to cursor_pos, but do not exceed len(input_string)
                    self.cursor_position = min(self.cursor_position + 1, len(self.input_string))

                elif event.key == pl.K_LEFT:
                    # Subtract one from cursor_pos, but do not go below zero:
                    self.cursor_position = max(self.cursor_position - 1, 0)

                elif event.key == pl.K_END:
                    self.cursor_position = len(self.input_string)

                elif event.key == pl.K_HOME:
                    self.cursor_position = 0

                elif len(self.input_string) < self.max_string_length or self.max_string_length == -1:
                    # If no special key is pressed, add unicode of key to input_string
                    self.input_string = (
                        self.input_string[:self.cursor_position]
                        + event.unicode
                        + self.input_string[self.cursor_position:]
                    )
                    self.cursor_position += len(event.unicode)  # Some are empty, e.g. K_UP

            elif event.type == pl.KEYUP:
                # *** Because KEYUP doesn't include event.unicode, this dict is stored in such a weird way
                if event.key in self.keyrepeat_counters:
                    del self.keyrepeat_counters[event.key]

        # Update key counters:
        for key in self.keyrepeat_counters:
            self.keyrepeat_counters[key][0] += self.clock.get_time()  # Update clock

            # Generate new key events if enough time has passed:
            if self.keyrepeat_counters[key][0] >= self.keyrepeat_intial_interval_ms:
                self.keyrepeat_counters[key][0] = (
                    self.keyrepeat_intial_interval_ms
                    - self.keyrepeat_interval_ms
                )

                event_key, event_unicode = key, self.keyrepeat_counters[key][1]
                pygame.event.post(pygame.event.Event(pl.KEYDOWN, key=event_key, unicode=event_unicode))

        # Re-render text surface:
        string = self.input_string
        if self.password:
            string = "*" * len(self.input_string)
        self.surface = self.font_object.render(string, self.antialias, self.text_color)
        self.rect = self.surface.get_rect()

        # Update self.cursor_visible
        if self.active:
            self.cursor_ms_counter += self.clock.get_time()
            if self.cursor_ms_counter >= self.cursor_switch_ms:
                self.cursor_ms_counter %= self.cursor_switch_ms
                self.cursor_visible = not self.cursor_visible

            if self.cursor_visible:
                cursor_y_pos = self.font_object.size(self.input_string[:self.cursor_position])[0]
                # Without this, the cursor is invisible when self.cursor_position > 0:
                if self.cursor_position > 0:
                    cursor_y_pos -= self.cursor_surface.get_width()
                self.surface.blit(self.cursor_surface, (cursor_y_pos, 0))

        self.clock.tick()
        return False

    def get_surface(self):
        return self.surface

    def get_text(self):
        return self.input_string

    def get_cursor_position(self):
        return self.cursor_position

    def set_text_color(self, color):
        self.text_color = color

    def set_cursor_color(self, color):
        self.cursor_surface.fill(color)

    def clear_text(self):
        self.input_string = ""
        self.cursor_position = 0

    def set_pos(self, pos_):
        self.pos = pos_

    def check_collide(self, pos_):
        # Added by Laurence to check that a textbox is being clicked on
        size = self.surface.get_size()
        bounds = (size[0] + self.pos[0], size[1] + self.pos[1])

        if pos_[0] >= self.pos[0] and pos_[0] <= bounds[0] and pos_[1] >= self.pos[1] and pos_[1] <= bounds[1]:
            return True
        return False


class Button:
    def __init__(self, text, size, pos,
    inactive_color, hover_color, clicked_color, border_color=(0,0,0),
    text_size=24, text_color=(0,0,0)):
        self.text = text
        self.size = size
        self.inactive_color = inactive_color
        self.hover_color = hover_color
        self.clicked_color = clicked_color
        self.border_color = border_color
        self.text_size = text_size
        self.text_color = text_color

        self.active_color = inactive_color
        self.pos = pos
        self.rect = pygame.Rect(pos, size)

        self.font = pygame.font.SysFont(None, self.text_size)
        self.text_img = self.font.render(self.text, True, self.text_color)

        self.temp_set = False
        self.temp_count_ms = 0
        self.clock = pygame.time.Clock()

    def update(self, events):
        if self.temp_set and self.temp_count_ms <= 0:
            self.active_color = self.inactive_color
            self.text_img = self.font.render(self.text, True, self.text_color)
            self.temp_set = False
        elif self.temp_count_ms > 0:
            self.temp_count_ms -= self.clock.get_time()
        elif not self.temp_set:
            for ev in events:
                m_pos = pygame.mouse.get_pos()
                if self.check_collide(m_pos):
                    if ev.type == pl.MOUSEBUTTONDOWN:
                        self.active_color = self.clicked_color
                        return True
                    else:
                        self.active_color = self.hover_color
                else:
                    self.active_color = self.inactive_color

        self.clock.tick()
        return False
        
    def draw(self, screen):
        pygame.draw.rect(screen, self.active_color, self.rect)
        t_size = self.text_img.get_size()
        screen.blit(self.text_img, (self.pos[0] + self.size[0]/2 - t_size[0]/2, self.pos[1] + self.size[1]/2 - t_size[1]/2))

    def get_rect(self):
        return self.rect

    def temp_change(self, color, text, time):
        self.active_color = color
        self.temp_count_ms = time
        self.temp_set = True
        self.text_img = self.font.render(text, True, self.text_color)

    def check_collide(self, pos_):
        bounds = (self.size[0] + self.pos[0], self.size[1] + self.pos[1])

        if pos_[0] >= self.pos[0] and pos_[0] <= bounds[0] and pos_[1] >= self.pos[1] and pos_[1] <= bounds[1]:
            return True
        return False

if __name__ == "__main__":
    pygame.init()

    button = Button("Hello World", (120, 60), (100,50), (50,50,50), (100,100,100), (150,150,150), text_size=24, text_color=(255,255,255))
    screen = pygame.display.set_mode((1000, 200))
    clock = pygame.time.Clock()

    screen.fill((225, 225, 225))
    while True:

        events = pygame.event.get()
        if button.update(events):
            button.temp_change((255,0,0), "ERROR", 3000)
        for event in events:
            if event.type == pygame.QUIT:
                exit()

        # Feed it with events every frame
        
        button.draw(screen)
        pygame.display.update()
        clock.tick(30)