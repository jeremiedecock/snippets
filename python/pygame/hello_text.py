#!/usr/bin/env python

import pygame

pygame.display.init()
pygame.font.init()

modes_list = pygame.display.list_modes()
#screen = pygame.display.set_mode(modes_list[0], pygame.FULLSCREEN)   # the highest resolution with fullscreen
screen = pygame.display.set_mode(modes_list[-1])                     # the lowest resolution

background_color = (255, 255, 255)
screen.fill(background_color)

font = pygame.font.Font(pygame.font.get_default_font(), 22)
text_surface = font.render("Hello world!", True, (0,0,0))
screen.blit(text_surface, (0,0))         # paste the text at the top left corner of the window

pygame.display.flip()                    # display the image

while True:                              # main loop (event loop)
    event = pygame.event.wait()
    if(event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE)):
        break
