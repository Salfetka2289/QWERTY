import pygame
import os
import lvl
import random
pygame.init()
skrin=pygame.display.set_mode([1500,1000])
Clock=pygame.time.Clock()
scale=5 
def loadimagess(papka,scale):
    loaded=[]
    for i in os.listdir(papka):
        img=pygame.image.load(papka+'/'+i)
        imgload=pygame.transform.scale(img,[img.get_width()*scale,img.get_height()*scale])
        loaded.append(imgload)
    return(loaded)
class Animation:
    def __init__(self,papka):
        self.imagess=loadimagess(papka,scale)
        self.index=0
        self.timer=10
    def render(self,x,y,side):
        if side == 'left':
            sideleft=pygame.transform.flip(self.imagess[self.index], True,False)
            skrin.blit(sideleft,[x-lvl.camerax,y-lvl.cameray])
        else:
            skrin.blit(self.imagess[self.index],[x-lvl.camerax,y-lvl.cameray])
    def update(self):
        self.timer=self.timer-1
        if self.timer==0:
            self.index+=1
            self.timer=10
            if self.index==len(self.imagess):
                self.index=0    

class Player:
    def __init__(self):
        self.x=100
        self.y=100
        self.vy=0
        self.m=0.1
        self.left=False
        self.right=False
        self.speed=False
        self.scale=5
        self.inercia=0
        self.state='idle'
        self.side='right'
        self.callx=False
        self.inr=0  #время нахождения в воздухе (в тактах)
        self.run=Animation(papka='images/entities/player/run')
        self.idle=Animation(papka='images/entities/player/idle')
        self.jump=Animation(papka='images/entities/player/jump')
        self.wall_slide=Animation(papka='images/entities/player/wall_slide')

    def render(self):
        if self.state=='idle':
            self.idle.render(self.x,self.y,self.side)
        if self.state=='run':
            self.run.render(self.x,self.y,self.side)
        if self.state=='jump':
            self.run.render(self.x,self.y,self.side)
        if self.state=='wall_slide':
            self.wall_slide.render(self.x,self.y,self.side)
        playerhit=self.get_hitbox()
        pygame.draw.rect(skrin,[255,0,0],[playerhit.x-lvl.camerax,playerhit.y-lvl.cameray,playerhit.width,playerhit.height],2)

    def update(self):
        self.inr+=1
        self.x+=self.inercia
        if self.inercia>0:
            self.collisionx('right')
        if self.inercia<0:
            self.collisionx('left')
        if abs (self.inercia)<1:
            self.inercia=0
        self.inercia*=0.9
        if self.inr>5:
            self.state='jump'
        if self.inercia==0:
            if self.left == True:
                if self.speed == True:
                    self.x-=10
                    self.collisionx('left')
                else:
                    self.x-=5
                    self.collisionx('left')
                self.state='run'
                self.side='left'
            if self.right == True:
                if self.speed == True:
                    self.x+=10 
                    self.collisionx('right')
                else:
                    self.x+=5
                    self.collisionx('right')
                self.state='run'
                self.side='right'
        self.vy=self.vy+self.m
        self.y+=self.vy
        if self.right == False and self.left == False:
            self.state='idle'
        if self.state=='idle':
            self.idle.update()
        if self.state=='run':
            self.run.update()
        if self.state=='jump':
            self.jump.update()   
        self.vy+=0.2#сила гравитации
        self.y+=self.vy
        if self.inr>5 and self.callx==True:
            self.state='wall_slide'
        self.collisiony()
        

    def collisionx(self,dir):
        self.call_r=False
        self.call_l=False
        self.callx=False
        hitplayer=self.get_hitbox()
        for i in lvl.tyles:
            tx=i['x']*lvl.tilesize
            ty=i['y']*lvl.tilesize
            trt=i['type']
            ti=i['index']
            img=lvl.resourses[trt][ti]
            hittyle=pygame.Rect(tx,ty,img.get_width(),img.get_height())
            if hitplayer.colliderect(hittyle):
                self.callx=True
                if dir=='right':
                    hitplayer.right=hittyle.left
                    self.call_r=True
                if dir=='left':
                    hitplayer.left=hittyle.right
                    self.call_l=True
        self.x=hitplayer.x-12
        
    def collisiony(self):
        hitplayer=self.get_hitbox()
        for i in lvl.tyles:
            tx=i['x']*lvl.tilesize
            ty=i['y']*lvl.tilesize
            trt=i['type']
            ti=i['index']
            img=lvl.resourses[trt][ti]
            hittyle=pygame.Rect(tx,ty,img.get_width(),img.get_height())
            if hitplayer.colliderect(hittyle):
                if self.vy>0:
                    hitplayer.bottom=hittyle.top
                    self.vy=0
                    self.inr=0 #время нахождения в воздухе (в тактах)
                if self.vy<0:
                    hitplayer.top=hittyle.bottom
        self.y=hitplayer.y
    def get_hitbox(self):
        h=pygame.Rect(self.x,self.y,14*5,18*5).inflate(-24,0)
        return(h)
    
class Enemy(Player):
    def __init__(self):
        super().__init__()
        self.time=random.randint(60,180)
        self.run=Animation(papka='images/entities/enemy/run')
        self.idle=Animation(papka='images/entities/enemy/idle')
        self.jump=Animation(papka='images/entities/enemy/idle')
    
    def enemy_control(self):
        self.time-=1
        if self.time<=0:
            if self.right==True or self.left==True:
                self.right=False
                self.left=False
            else:
                r=random.randint(1,2)
                if r==1:
                    self.left=True
                if r==2:
                    self.right=True
            self.time=random.randint(60,180)
        if self.right==True:
            footx=self.x+70
            footy=self.y+70


enemys=[]
player=Player()
lvl.load()  
enemycords=lvl.get_enemycord()
cords=lvl.get_playercord()
for i in enemycords:
    enemy=Enemy()
    enemy.x=i[0]
    enemy.y=i[1]
    enemys.append(enemy)
player.x=cords[0]
player.y=cords[1]
while True:
    skrin.fill([0,0,0])
    Clock.tick(60)
    player.render()
    player.update()
    lvl.render_tyles(skrin)
    lvl.camerax+=(player.x-750-lvl.camerax)/20
    lvl.cameray+=(player.y-500-lvl.cameray)/20
    ivents=pygame.event.get()
    for i in enemys:
        i.render()
        i.update()
        i.enemy_control()
    for i in ivents:
        if i.type==pygame.KEYDOWN:
            if i.key==pygame.K_a:
                player.left=True
            if i.key==pygame.K_d:
                player.right=True
            if i.key==pygame.K_LSHIFT:
                player.speed=True
            if i.key==pygame.K_SPACE and player.state=='wall_slide':
                player.vy=-8
                if player.call_r==True:
                    player.inercia=-30
                    player.side='left'
                else:
                    player.inercia=+30
                    player.side='right'
            if i.key==pygame.K_SPACE and player.inr<5:   #он стоит на земле 
                player.vy=-5                     
        if i.type==pygame.KEYUP:
            if i.key==pygame.K_a:
                player.left=False
            if i.key==pygame.K_d:
                player.right=False
            if i.key==pygame.K_LSHIFT:
                player.speed=False
        if i.type==pygame.QUIT:
            exit()
    pygame.display.update()