import pygame
import os
pygame.init()
clock=pygame.time.Clock()
skrin=pygame.display.set_mode([1500,1000])


def loadimagess(papka,scale):
    loaded=[]
    for i in os.listdir(papka):
        img=pygame.image.load(papka+'/'+i)
        imgload=pygame.transform.scale(img,[img.get_width()*scale,img.get_height()*scale])
        loaded.append(imgload)
    return(loaded)
idle=loadimagess(papka='images/exploseons',scale=3)
idx=0
time=7
def render():
    global idx, time
    time=time-1
    if time==0:
        idx=idx+1
        time=7
    if idx>=len(idle):
        idx=0
    skrin.blit(idle[idx],[300,300])

while True:
    skrin.fill([0,0,0])
    clock.tick(60)
    render()
    get=pygame.event.get()
    for i in get:
        if i.type==pygame.QUIT:
            exit()
    pygame.display.update()

    sky=loadimagess(papka='images/entities/player/sky',scale=5)