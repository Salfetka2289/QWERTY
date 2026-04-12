import pygame
pygame.init()
clock=pygame.time.Clock()
skrin=pygame.display.set_mode([1500,1000])

while True:
    clock.tick(60)
    skrin.fill([0,0,0])
    get=pygame.event.get()
    for i in get:
        if i.type==pygame.QUIT:
            exit()
    pygame.display.update()

