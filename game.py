import pygame
import os
import lvl
pygame.init()
skrin=pygame.display.set_mode([1500,1000])
Clock=pygame.time.Clock()
left=False
right=False
speed=False
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
        self.scale=5
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
        if self.inr>5:
            self.state='jump'
        if left == True:
            if speed == True:
                self.x-=10
                self.collisionx('left')
            else:
                self.x-=5
                self.collisionx('left')
            self.state='run'
            self.side='left'
        if right == True:
            if speed == True:
                self.x+=10 
                self.collisionx('right')
            else:
                self.x+=5
                self.collisionx('right')
            self.state='run'
            self.side='right'
        self.vy=self.vy+self.m
        self.y+=self.vy
        if right == False and left == False:
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
                if dir=='left':
                    hitplayer.left=hittyle.right
        self.x=hitplayer.x
        
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
        h=pygame.Rect(self.x,self.y,14*5,18*5)
        return(h)
    
class Enemy(Player):
    def __init__(self):
        super().__init__()
        self.run=Animation(papka='images/entities/enemy/run')
        self.idle=Animation(papka='images/entities/enemy/idle')
        self.jump=Animation(papka='images/entities/enemy/idle')
enemy=Enemy()
player=Player()
lvl.load()  
cords=lvl.get_playercord()
player.x=cords[0]
player.y=cords[1]
while True:
    skrin.fill([0,0,0])
    Clock.tick(60)
    player.render()
    player.update()
    enemy.render()
    enemy.update() 
    lvl.render_tyles(skrin)
    lvl.camerax+=(player.x-750-lvl.camerax)/20
    lvl.cameray+=(player.y-500-lvl.cameray)/20
    ivents=pygame.event.get()
    for i in ivents:
        if i.type==pygame.KEYDOWN:
            if i.key==pygame.K_a:
                left=True
            if i.key==pygame.K_d:
                right=True
            if i.key==pygame.K_LSHIFT:
                speed=True
        if i.type==pygame.KEYUP:
            if i.key==pygame.K_a:
                left=False
            if i.key==pygame.K_d:
                right=False
            if i.key==pygame.K_LSHIFT:
                speed=False
            if i.key==pygame.K_SPACE and player.inr<5:   #он стоит на земле 
                player.vy=-5                     
        if i.type==pygame.QUIT:
            exit()
    pygame.display.update()