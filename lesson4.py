import pygame
import os
pygame.init()
clock=pygame.time.Clock()
skrin=pygame.display.set_mode([1500,1000])

class Player:
    def __init__(self,x,y):
        self.x=x
        self.y=y
        self.vy=-1
        self.mr=False
        self.ml=False
        self.side='right'
        self.animations={
            'idle': Animation(papka='images/entities/player/idle',scale=5),
            'run': Animation(papka='images/entities/player/run',scale=5),
            'jump': Animation(papka='images/entities/player/jump',scale=5),
        }
        self.state='idle'

    def update(self):
        self.vy+=0.15
        self.y+=self.vy
        if self.y >=600:
            self.y=600
            self.vy=0
        if self.ml==True:
            self.x-=5
            self.side='left'
        if self.mr==True:
            self.x+=5
            self.side='right'

    def render(self):
        self.animations[self.state].render(self.x,self.y)
        self.animations[self.state].update()

def loadimagess(papka,scale):
    loaded=[]
    for i in os.listdir(papka):
        img=pygame.image.load(papka+'/'+i)
        imgload=pygame.transform.scale(img,[img.get_width()*scale,img.get_height()*scale])
        loaded.append(imgload)
    return(loaded)

class Animation:
    def __init__(self,papka,scale):
        self.imagess=loadimagess(papka,scale)
        self.index=0
        self.time=20

    def render(self,x,y):
        skrin.blit(self.imagess[self.index],[x,y])
        

    def update(self):
        self.time-=1
        if self.time==0:
            self.index+=1
            self.time=10
        if self.index>len(self.imagess)-1:
            self.index=0

player=Player(0,0)
images=[]
idle=loadimagess(papka='images/entities/player/idle',scale=5)
while True:
    clock.tick(60)
    skrin.fill([0,0,0])
    pygame.draw.rect(skrin,[70,150,70],[0,600+(18*5),1500,400])
    player.render()
    player.update()
    get=pygame.event.get()
    for i in get:
        if i.type==pygame.QUIT:
            exit()
        if i.type==pygame.KEYDOWN:
            if i.key == pygame.K_a:
                player.ml=True
                player.state='run'
            if i.key == pygame.K_d:
                player.mr=True
                player.state='run'
        if i.type==pygame.KEYUP:
            if i.key == pygame.K_a:
                player.ml=False
                player.state='idle'
            if i.key == pygame.K_d:
                player.mr=False
                player.state='idle'
    pygame.display.update()