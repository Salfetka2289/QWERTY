import pygame
import os
import pickle
tilesize=70
camerax=0
cameray=0
tyles=[]
img=pygame.image.load('images/entities/player/idle/21.png')
img=pygame.transform.scale(img,(tilesize,tilesize))

def loadimagess(papka,scale):
    loaded=[]
    for i in os.listdir(papka):
        img=pygame.image.load(papka+'/'+i)
        imgload=pygame.transform.scale(img,[img.get_width()*scale,img.get_height()*scale])
        loaded.append(imgload)
    return(loaded)

decor=loadimagess('graph/resources/decor',tilesize/16)
grass=loadimagess('graph/resources/grass',tilesize/16)
large_decor=loadimagess('graph/resources/large_decor',tilesize/16)
stone=loadimagess('graph/resources/stone',tilesize/16)
spawners=loadimagess('graph/resources/spawners',tilesize/16)
resourses={
    'decor':decor,
    'grass':grass,
    'large_decor':large_decor,
    'stone':stone,
    'spawners':spawners
}
resourstype='grass'
index=0

def get_playercord():
    for i in tyles:
        if i['type']=='spawners' and i['index']==0:
            cordplayerx=i['x']*tilesize
            cordplayery=i['y']*tilesize
            tyles.remove(i)
            return(cordplayerx,cordplayery)
        
def get_enemycord():
    cords=[]
    for i in tyles.copy():
        if i['type']=='spawners' and i['index']==1:
            cordenemyx=i['x']*tilesize
            cordenemyy=i['y']*tilesize
            tyles.remove(i)
            cords.append([cordenemyx,cordenemyy])
    return(cords)

def iscliff(footx,footy):
    for i in tyles:
        bx=i['x']*tilesize
        by=i['y']*tilesize
        bhit=pygame.rect.Rect([bx,by],[70,70])
        if bhit.collidepoint(footx,footy):
            return(False)
    return(True)

            

def render_grid(skrin):
    k=camerax//tilesize
    xstart=k*tilesize
    k1=cameray//tilesize
    ystart=k1*tilesize
    for x in range(xstart,xstart+1500+tilesize,tilesize):
        pygame.draw.line(skrin,(100,100,100),[x-camerax,ystart-cameray],[x-camerax,ystart+1000+tilesize-cameray])
    for y in range(ystart,ystart+1000+tilesize,tilesize):
        pygame.draw.line(skrin,(100,100,100),[xstart-camerax,y-cameray],[xstart+1500+tilesize-camerax,y-cameray])

def load():
    global tyles
    f=open('card','rb')
    tyles=pickle.load(f)
    f.close()

def delate():
    global tyles
    tyles.clear()

def render_tyles(skrin):
    for i in tyles:
        tx=i['x']*tilesize
        ty=i['y']*tilesize
        trt=i['type']
        ti=i['index']
        img=resourses[trt][ti]
        skrin.blit(img,[tx-camerax,ty-cameray])