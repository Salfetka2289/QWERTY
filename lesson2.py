import pygame
import random
pygame.init()
clock=pygame.time.Clock()
left=False
right=False
skrin=pygame.display.set_mode([500,1000])
doodle=pygame.image.load('images\image.png')
platform=pygame.image.load('images\platform.png')
doodle=pygame.transform.scale(doodle,[100,100])
platform=pygame.transform.scale(platform,[140,30])
doodler=doodle
doodlel=pygame.transform.flip(doodle,True,False) 
side='right'
x=100
y=500
vy=-5
yp=0
platforms=[]
def update():
    global x,y,side,doodle,vy, platforms
    if left==True:
        x=x-2.5
        side='left'
    if right==True:
        x=x+2.5
        side='right'
    if side=='left':
        doodle=doodlel
    if side=='right':
        doodle=doodler
    bounddoodle=doodle.get_rect(topleft=[x,y])
    if x > 500:
        x=-100
    if x < -100:
        x=500
    vy+=0.04#сила гравитации
    y+=vy
    for i in platforms:
        i[1]=i[1]+1

def render():
    global platforms
    skrin.blit(doodle,[x,y])
    for i in platforms:
       skrin.blit(platform,[i[0],i[1]])


def prandom():
    global yp
    xp=random.randint(0,360)    
    platforms.append([xp,yp])
time = 150
while True:
    time=time-1
    if time==0:
        prandom() 
        time = 150
    clock.tick(120)
    skrin.fill([255,255,255])
    render()
    update()
    get=pygame.event.get()
    for i in get:
        if i.type == pygame.KEYDOWN:
            if i.key == pygame.K_a:
                left=True
            if i.key == pygame.K_d:
                right=True
        if i.type == pygame.KEYUP:
            if i.key == pygame.K_a:
                left=False
            if i.key == pygame.K_d:
                right=False
        if i.type==pygame.QUIT:
            exit()
    pygame.display.update()

