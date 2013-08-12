#!/usr/bin/env python

import pygame

pygame.display.init()

pygame.time.set_timer(pygame.USEREVENT+1, 1000)
pygame.time.set_timer(pygame.USEREVENT+2, 2000)

while True:
    #pygame.time.wait(500)                # wait 500ms
    event = pygame.event.wait()
    
    if event.type == pygame.USEREVENT+1:
        print pygame.time.get_ticks(), "hello"
    elif event.type == pygame.USEREVENT+2:
        print pygame.time.get_ticks(), "hi"

