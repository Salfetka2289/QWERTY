import pygame
import random
pygame.init()
skrin=pygame.display.set_mode([1500,1000])
radius=[]

def random():
    global radius
    from random import randint
    rand = randint(5,20)
    radius.append(rand)
    

def render():
    global radius,mousecord
    for i in radius:
        pygame.draw.circle(skrin,[255,79,0],[mousecord],i)
        
while True:
    skrin.fill([0,0,0])
    render()
    get=pygame.event.get()

    for i in get:
        if i.type==pygame.QUIT:
            exit()
    pygame.display.update()

