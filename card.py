import pygame
import os
import pickle
pygame.init()
skrin=pygame.display.set_mode([1500,1000])
clock=pygame.time.Clock()
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
def render_grid():
    k=camerax//tilesize
    xstart=k*tilesize
    k1=cameray//tilesize
    ystart=k1*tilesize
    for x in range(xstart,xstart+1500+tilesize,tilesize):
        pygame.draw.line(skrin,(100,100,100),[x-camerax,ystart-cameray],[x-camerax,ystart+1000+tilesize-cameray])
    for y in range(ystart,ystart+1000+tilesize,tilesize):
        pygame.draw.line(skrin,(100,100,100),[xstart-camerax,y-cameray],[xstart+1500+tilesize-camerax,y-cameray])
    
def transform():
    for tyle in tyles:
        tx=tyle['x']
        ty=tyle['y'] 
        ttype=tyle['type']
        left=False
        right=False
        up=False
        down=False
        if ttype == 'grass' or ttype == 'stone':
            for t in tyles:
                if t['type']==ttype and tx-1==t['x'] and ty==t['y']:
                    left=True
                if t['type']==ttype and tx+1==t['x'] and ty==t['y']:
                    right=True
                if t['type']==ttype and ty-1==t['y'] and tx==t['x']:
                    up=True
                if t['type']==ttype and ty+1==t['y'] and tx==t['x']:
                    down=True
            if  left==False and up==False and right==True:
                tyle['index'] = 0  
            if left==True and up==False and right==True:
                tyle['index'] = 1
            if left==True and up==False and right==False:
                tyle['index'] = 2
            if left==True and up==True and right==False and down==True:
                tyle['index'] = 3
            if left==False and up==True and right==True and down==True:
                tyle['index'] = 7
            if left==True and up==True and right==False and down==False:
                tyle['index'] = 4
            if left==False and up==True and right==True and down==False:
                tyle['index'] = 6
            if left==True and up==True and right==True:
                tyle['index'] = 5

def safe():
    f=open('card','wb')
    pickle.dump(tyles,f)
    f.close()

def load():
    global tyles
    f=open('card','rb')
    tyles=pickle.load(f)
    f.close()

def delate():
    global tyles
    tyles.clear()

while True:
    skrin.fill([0,0,0])
    clock.tick(60)
    mousecord=pygame.mouse.get_pos()
    x=(mousecord[0]+camerax)//tilesize*tilesize-camerax
    y=(mousecord[1]+cameray)//tilesize*tilesize-cameray
    img=resourses[resourstype][index]
    skrin.blit(img,[x,y])
    for i in tyles:
        tx=i['x']*tilesize
        ty=i['y']*tilesize
        trt=i['type']
        ti=i['index']
        img=resourses[trt][ti]
        skrin.blit(img,[tx-camerax,ty-cameray])
    prest=pygame.key.get_pressed()
    render_grid()
    if prest[pygame.K_a]:
        camerax-=5
    if prest[pygame.K_d]:
        camerax+=5
    if prest[pygame.K_w]:
        cameray-=5
    if prest[pygame.K_s]:
        cameray+=5
    ivents=pygame.event.get()
    for i in ivents:
        if i.type==pygame.KEYDOWN:
            if i.key==pygame.K_1:
                resourstype='decor'
                index=0
            if i.key==pygame.K_2:
                resourstype='grass'
                index=0
            if i.key==pygame.K_3:
                resourstype='large_decor'
                index=0
            if i.key==pygame.K_4:
                resourstype='stone'
                index=0
            if i.key==pygame.K_5:
                resourstype='spawners'
                index=0
            if i.key==pygame.K_RIGHT:
                index+=1
                if index>=len(resourses[resourstype]):
                    index=0
            if i.key==pygame.K_t:
                transform()
            if i.key==pygame.K_c and prest[pygame.K_LCTRL]:
                safe()
            if i.key==pygame.K_v and prest[pygame.K_LCTRL]:
                load()
            if i.key==pygame.K_p and prest[pygame.K_LCTRL]:
                delate()
            if i.key==pygame.K_LEFT:
                index-=1
                if index<0:
                    index=len(resourses[resourstype])-1
        if i.type==pygame.MOUSEBUTTONDOWN:
            if i.button==1:
                tyle={
                    'x':(x+camerax)//tilesize,
                    'y':(y+cameray)//tilesize,
                    'type':resourstype,
                    'index':index
                    }
                tyles.append(tyle)
            if i.button==3:
                cx=(x+camerax)//tilesize
                cy=(y+cameray)//tilesize
                for n in tyles:
                    if n['x']==cx and n['y']==cy:
                        tyles.remove(n)
        if i.type==pygame.QUIT:
            safe()
            exit()
    pygame.display.update()