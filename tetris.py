import pygame
pygame.init()
skrin=pygame.display.set_mode([1500,1000])
Clock=pygame.time.Clock()
tilesize=50
figures=[]
def create_figure():
    global figures
    figure=['simple',[tilesize,tilesize],[tilesize,2*tilesize],[2*tilesize,2*tilesize],[2*tilesize,3*tilesize],'up']
    figures.append(figure)
def render():
    for i in (figures):
        for n in i[1:]:       
            pygame.draw.rect(skrin,[167,231,251],[n[0],n[1],tilesize,tilesize])
def move():
    for i in figures:
        for m in i[1:]:
            m[1]=m[1]+tilesize
create_figure()
time=10
while True:
    Clock.tick(30)
    skrin.fill([0,0,0])
    time=time-1
    if time==0:
        move()
        time=10
    render()
    ivents=pygame.event.get()
    for i in ivents:
        if i.type==pygame.QUIT:
            exit()
    pygame.display.update()