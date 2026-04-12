import pygame
import random
pygame.init()
points=[]

def randoms():
    global points
    x=random.randint(0,1500)
    y=random.randint(0,1000)
    col=random.randint(0,255),random.randint(0,255),random.randint(0,255)
    points.append([x,y,col])
def render():
    for i in points:
        pygame.draw.circle(skrin,i[2],[i[0],i[1]],7)

def update():
    mpos=pygame.mouse.get_pos()
    for i in points:
        i[0]+=(mpos[0]-i[0])/20
        i[1]+=(mpos[1]-i[1])/20
        irect=pygame.Rect(i[0]-7,i[1]-7,14,14)
        if irect.collidepoint(mpos):
            points.remove(i)


skrin=pygame.display.set_mode([1500,1000])
clock=pygame.time.Clock()
time=25
while True:
    clock.tick(60)
    skrin.fill([0,0,0])
    render()
    update()
    time=time-1
    if time==0:
        randoms()
        time=25
    get=pygame.event.get()
    for i in get:
        if i.type==pygame.QUIT:
            exit()
    pygame.display.update()

