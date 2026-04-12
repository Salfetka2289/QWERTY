import pygame
import os
import random
pygame.init()
skrin=pygame.display.set_mode([1500,1000])
clock=pygame.time.Clock()
x=100
y=100
left=False
right=False
vy=0
enemes=[]
camerax=0
cameray=0
class Eneme:
    def __init__(self):
        self.x=random.randint(-3000,3000)
        self.y=random.randint(0,500)
        self.vy=0 
        self.index=0
        self.timer=7
        self.state='idle'

    def render(self): 
        if self.state=='idle':
            skrin.blit(eidle[self.index],[self.x-camerax,self.y-cameray])
        if self.state=='run':
             skrin.blit(erun[self.index],[self.x-camerax,self.y-cameray])

    def update(self):
        self.vy+=0.2#сила гравитации
        self.y+=self.vy
        if self.y >= 500:
            self.y=500
            self.vy=0
        self.timer-=1
        if self.timer==0:
            self.index+=1
            self.timer=7
            if self.index==len(eidle) and self.state=='idle':
                self.index=0
            if self.index==len(erun) and self.state=='run':
                self.index=0
        if self.state=='run':
            a=random.randint(0,100)
            if a==1:
                self.state='idle'
                self.index=0
        if self.state=='idle':
            a=random.randint(0,100)
            if a==1:
                self.state='run' 
                self.index=0  
def loadimagess(papka,scale):
    loaded=[]
    for i in os.listdir(papka):
        img=pygame.image.load(papka+'/'+i)
        imgload=pygame.transform.scale(img,[img.get_width()*scale,img.get_height()*scale])
        loaded.append(imgload)
    return(loaded)

eidle=loadimagess(papka='images/entities/enemy/idle',scale=5)
erun=loadimagess(papka='images/entities/enemy/run',scale=5)
idle=loadimagess(papka='images/entities/player/idle',scale=5)
run=loadimagess(papka='images/entities/player/run',scale=5)
jump=loadimagess(papka='images/entities/player/jump',scale=5)
side='right'
animations={
    'idle':idle,
    'run':run,
    'jump':jump
}
state='idle'
idx=0
time=7
def render():
    global idx, time
    time=time-1
    if time==0:
        idx=idx+1
        time=7
    if idx>=len(animations[state]):
        idx=0
    if side=='right':
        skrin.blit(animations[state][idx],[x-camerax,y-cameray])
    else:
        runleft=pygame.transform.flip(animations[state][idx],True,False)
        skrin.blit(runleft,[x-camerax,y-cameray])
    pygame.draw.rect(skrin,[53,23,12],[0,650-cameray,1500,350])
    pygame.draw.rect(skrin,[0,158,0],[0,590-cameray,1500,60])



def update():
    global x,state,side,vy,y
    vy+=0.2#сила гравитации
    y+=vy
    if y >= 500:
        y=500
        vy=0
    if left==True:
        x=x-4
        state='run'
        side='left'
    else:
        pass
    if right==True:
        x=x+4
        state='run'
        side='right'
    else:
        pass
    if left==False and right==False:
        state='idle'
    if vy!=0:
        state='jump'
for i in range(50):
    eneme=Eneme()
    enemes.append(eneme)

while True:
    skrin.fill([0,0,0])
    clock.tick(60)
    render()
    update()
    camerax+=(x-750-camerax)/30
    cameray+=(y-500-cameray)/30
    for i in enemes:
        i.render()
        i.update()
    ivents=pygame.event.get()
    for i in ivents:
        if i.type==pygame.KEYDOWN:
            if i.key==pygame.K_a:
                left=True
            if i.key==pygame.K_d:
                right=True
            
            if i.key==pygame.K_SPACE and vy==0:
                vy=-5    
        if i.type==pygame.KEYUP:
            if i.key==pygame.K_a:
                left=False
            if i.key==pygame.K_d:
                right=False 
        if i.type==pygame.QUIT:
            exit()
    pygame.display.update()