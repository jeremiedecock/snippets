#!/usr/bin/env python

import pygame

pygame.display.init()

modes_list = pygame.display.list_modes()
#screen = pygame.display.set_mode(modes_list[0], pygame.FULLSCREEN)   # the highest resolution with fullscreen
screen = pygame.display.set_mode(modes_list[-1])                     # the lowest resolution

background_color = (255, 255, 255)
screen.fill(background_color)

image = pygame.image.load("./icon.png")  # load an image from a file
screen.blit(image, (0,0))                # paste the image at the top left corner of the window

pygame.display.flip()                    # display the image

while True:                              # main loop (event loop)
    event = pygame.event.wait()
    if(event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE)):
        break
