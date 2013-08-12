#!/usr/bin/env python

import pygame
import datetime
import sys

pygame.init()

modes_list = pygame.display.list_modes()
#screen = pygame.display.set_mode(modes_list[0], pygame.FULLSCREEN)   # the highest resolution with fullscreen
screen = pygame.display.set_mode(modes_list[-1])                     # the lowest resolution

background_color = (255, 255, 255)

font_name = pygame.font.get_default_font()
font_size = 26
text_font = pygame.font.Font(font_name, font_size)

while True:                              # main loop (event loop)
    # WAIT
    pygame.time.wait(100)                # wait 100ms

    # EVENTS
    for event in pygame.event.get():     # check events
        if(event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE)):
            sys.exit(0)

    # DATE
    dt = datetime.datetime.now()
    dt_str = dt.strftime("%A, %d %B %Y - %H:%M:%S")

    # DISPLAY
    screen.fill(background_color)            # clear the screen

    text_surface = text_font.render(dt_str, True, (0,0,0))
    screen.blit(text_surface, (0,0))         # paste the text at the top left corner of the window

    pygame.display.flip()                    # display the image

