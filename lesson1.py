import pygame
import random
pygame.init()
platforms=[]
def randoms():
    global platforms
    x=random.randint(200,800)
    platforms.append([x,0])

def update():
    for i in platforms:
        i[1]+=1
dx=400
dy=450
left=False
right=False
flip=False #false-right, true-left
skrin=pygame.display.set_mode([1000,1000])
clock=pygame.time.Clock()
doodle=pygame.image.load('images/image.png')
platform=pygame.image.load('images\platform.png')
doodle=pygame.transform.scale(doodle,[200,100])
platform=pygame.transform.scale(platform,[200,120])
dl=pygame.transform.flip(doodle,True,False)
time=90
while True:
    clock.tick(60)
    skrin.fill([255,255,255])
    if time==0:
        randoms()
        time=90
    update()
    for i in platforms:
        skrin.blit(platform,(i[0],i[1]))
    if flip==False:
        skrin.blit(doodle,[dx,dy])
    else:
        skrin.blit(dl,[dx,dy])
    if left==True:
        dx=dx-7
    if right==True:
        dx=dx+7
    get=pygame.event.get()
    if dx>1000:
        dx=-200
    if dx<-200:
        dx=1000
    for i in get:
        if i.type==pygame.KEYDOWN:
            if i.key==pygame.K_LEFT:
                left=True
                flip=True
            if i.key==pygame.K_RIGHT:
                right=True
                flip=False
        if i.type==pygame.KEYUP:
            if i.key==pygame.K_LEFT:
                left=False
            if i.key==pygame.K_RIGHT:
                right=False
        if i.type==pygame.QUIT:
            exit()
    time=time-1
    pygame.display.update()
