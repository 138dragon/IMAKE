import sys
import pygame
import TM as detect
import cv2 as cv
import random
from pygame.locals import *

cap = cv.VideoCapture(0)
cap.set(3,640)
cap.set(4,480)

#initialization
pygame.init()
pygame.mixer.init()
pygame.mixer.pre_init(44100,-16,2,512)
screen = pygame.display.set_mode((640, 480), DOUBLEBUF)

clock = pygame.time.Clock()

#blit with opacity
def blit_alpha(target, source, location, opacity):
    x = location[0]
    y = location[1]
    temp = pygame.Surface((source.get_width(), source.get_height())).convert()
    temp.blit(target, (-x, -y))
    temp.blit(source, (0, 0))
    temp.set_alpha(opacity)        
    target.blit(temp, location)
    
def check_collision(pos,pos_now,distance):
    if -distance<pos_now[0]-pos[0]<distance and -distance<pos_now[1]-pos[1]<distance:
        return True
    else:
        return False

# not used
def check_spill(bucket_1,bucket_2,paints,spill,bucket,size,color):
    if spill==0:
        screen.blit(bucket_1,(bucket[0]-int(size/2),bucket[1]-int(size/2)))
    else:
        screen.blit(paints,(color[0]-int(size/2),color[1]-int(size/2)))
        screen.blit(bucket_2,(bucket[0]-int(size/2),bucket[1]-int(size/2)))
        spill+=1
        if spill==20:
            spill=0

def imgLoad(name):
    return pygame.image.load('sprites/'+name+'.png')

def drawObject(animal, XY, opacity):
    blit_alpha(screen,animal, XY,opacity)

#user image
#flower=pygame.image.load('flower.png')
#flower_size=50
#flower = pygame.transform.scale(flower, (flower_size, flower_size))
#blink=pygame.image.load('blink.png')
#blink_opacity=100
flag=1
broom_flag=0

# PAINT IMG
guide1=pygame.transform.scale(imgLoad('guide_1'),(500,120))
guide2=pygame.transform.scale(imgLoad('guide_2'),(500,120))

paints_size=80
paints_y=pygame.transform.scale(imgLoad('paints_y'),(paints_size,paints_size))
paints_g=pygame.transform.scale(imgLoad('paints_g'),(paints_size,paints_size))
paints_s=pygame.transform.scale(imgLoad('paints_s'),(paints_size,paints_size))
paints_p=pygame.transform.scale(imgLoad('paints_p'),(paints_size,paints_size))
broom_1=pygame.transform.scale(imgLoad('broom1'),(67,116))
broom_2=pygame.transform.scale(imgLoad('broom2'),(89,143))

bucket_y_img=pygame.transform.scale(imgLoad('bucket_y'),(paints_size,paints_size))
bucket_g_img=pygame.transform.scale(imgLoad('bucket_g'),(paints_size,paints_size))
bucket_p_img=pygame.transform.scale(imgLoad('bucket_p'),(paints_size,paints_size))
bucket_s_img=pygame.transform.scale(imgLoad('bucket_s'),(paints_size,paints_size))
bucket_y_3=pygame.transform.scale(imgLoad('bucket_y_3'),(147,paints_size))
bucket_g_3=pygame.transform.scale(imgLoad('bucket_g_3'),(147,paints_size))
bucket_p_3=pygame.transform.scale(imgLoad('bucket_p_3'),(147,paints_size))
bucket_s_3=pygame.transform.scale(imgLoad('bucket_s_3'),(147,paints_size))

bucket_y_2=pygame.transform.scale(imgLoad('bucket_y_2'),(paints_size,paints_size))
bucket_g_2=pygame.transform.scale(imgLoad('bucket_g_2'),(paints_size,paints_size))
bucket_p_2=pygame.transform.scale(imgLoad('bucket_p_2'),(paints_size,paints_size))
bucket_s_2=pygame.transform.scale(imgLoad('bucket_s_2'),(paints_size,paints_size))

animal_init = ['horse','bird', 'cat']
animal_flag = 0

mousepos=[]
animals=[]
colors=[]
opacity=[]
done=False #done game

color_now=None
animal_now='cat'
opacity_now=300
highest_len = 0

#spill time
spill_y=0
spill_g=0
spill_s=0
spill_p=0

#paint time
time=0

#guide window
guide_count=0
guide2_count=0

#color
YELLOW=(255,255,0)
GREEN=(0,255,0)
SKYBLUE=(23,219,255)
PINK=(255,0,255)


#coordinate
bucket_y=(150,100)
yellow=(220,100)
bucket_g=(100,200)
green=(170,200)
bucket_s=(380,300)
skyblue=(450,300)
pink=(650,300)
bucket_p=(580,300)
broom=(550,100)

distance=40

#camera
pos_prev = (60, 60)
pos_now = (60, 60)

X=0
Y=0
X2=0
Y2=0

while not done:
    clock.tick(10)

    for event in pygame.event.get(): 
        if event.type == pygame.QUIT:  
            done = True
            
        #마우스 클릭시 동물이 바뀜
        elif event.type== pygame.MOUSEBUTTONDOWN:
            if animal_now=='horse':
                animal_now='cat'
            elif animal_now=='cat':
                animal_now='bird'
            elif animal_now=='bird':
                animal_now='horse'
    
    screen.fill((0,0,0))
    screen.blit(pygame.image.load('sprites/background.jpg'),(0,0))
    
    pos_prev = pos_now
    # get hand point from video
    ret,img = cap.read()
      
    if ret == False:
        continue

    img = cv.resize(img, (640,480))
    points = pygame.mouse.get_pos()
    
    #cv.imshow('result', img)
    # if person head is found
    if type(points) is tuple:
        pos_now = points

    # if user goes out of the screen, change animal
    if not(0 < pos_now[0] < 640 and 0 < pos_now[1] < 480): 
        animal_flag += 1
        animal_now = animal_init[flag%3]
    


        # check if user collided to buckets
    if check_collision(bucket_y,pos_now,distance):
        spill_y+=1
        if spill_y!=0:
            color_now='_y'
            time=1
            opacity_now=300
    elif check_collision(bucket_g,pos_now,distance):
        spill_g+=1
        if spill_g!=0:
            color_now='_g'
            time=1
            opacity_now=300
    elif check_collision(bucket_s,pos_now,distance):
        spill_s+=1
        if spill_s!=0:
            color_now='_s'
            time=1
            opacity_now=300
    elif check_collision(bucket_p,pos_now,distance):
        spill_p+=1
        if spill_p!=0:
            color_now='_p'
            time=1
            opacity_now=300

##        # check if user collided to spilled paint
##    if check_collision(yellow,pos_now,distance):
##        if spill_y!=0:
##            color_now='_y'
##            time=1
##            opacity_now=300
##    elif check_collision(green,pos_now,distance):
##        if spill_g!=0:
##            color_now='_g'
##            time=1
##            opacity_now=300
##    elif check_collision(skyblue,pos_now,distance):
##        if spill_s!=0:
##            color_now='_s'
##            time=1
##            opacity_now=300
##    elif check_collision(pink,pos_now,distance):
##        if spill_p!=0:
##            color_now='_p'
##            time=1
##            opacity_now=300
    
    if time>0:
        time+=1
        opacity_now-=10
        if time==30:
            color_now='time_over'
            time=0
            
    # broom img
    if broom_flag==0:
        screen.blit(broom_1,(broom[0]-int(67/2),broom[1]-int(116/2)))

    # draw stand up/spilled paint bucket depending on 'spill_' bool
    if spill_y==0:#YELLO
        screen.blit(bucket_y_img,(bucket_y[0]-int(paints_size/2),bucket_y[1]-int(paints_size/2)))
    elif spill_y>0 and spill_y<3:
        screen.blit(bucket_y_2,(bucket_y[0]-int(paints_size/2),bucket_y[1]-int(paints_size/2)))
        spill_y+=1
    else :
        screen.blit(bucket_y_3,(bucket_y[0]-int(paints_size/2),bucket_y[1]-int(paints_size/2)))
        spill_y+=1
        if spill_y>20:
            spill_y=0
            X=random.randint(50,600)
            Y=random.randint(50,430)
            yellow=(X,Y)
            bucket_y=(yellow[0]-70,yellow[1])
    
    if spill_g==0:#GREEN
        screen.blit(bucket_g_img,(bucket_g[0]-int(paints_size/2),bucket_g[1]-int(paints_size/2)))
    elif spill_g>0 and spill_g<3:
        screen.blit(bucket_g_2,(bucket_g[0]-int(paints_size/2),bucket_g[1]-int(paints_size/2)))  
        spill_g+=1
    else :
        screen.blit(bucket_g_3,(bucket_g[0]-int(paints_size/2),bucket_g[1]-int(paints_size/2)))
        spill_g+=1
        if spill_g>20:
            spill_g=0
            X=random.randint(50,600)
            Y=random.randint(50,430)
            green=(X,Y)
            bucket_g=(green[0]-70,green[1])
    
    if spill_s==0:#SKYBLUE
        screen.blit(bucket_s_img,(bucket_s[0]-int(paints_size/2),bucket_s[1]-int(paints_size/2)))
    elif spill_s>0 and spill_s<3:
        screen.blit(bucket_s_2,(bucket_s[0]-int(paints_size/2),bucket_s[1]-int(paints_size/2)))
        spill_s+=1
    else :
        screen.blit(bucket_s_3,(bucket_s[0]-int(paints_size/2),bucket_s[1]-int(paints_size/2)))
        spill_s+=1
        if spill_s>20:
            spill_s=0
            X=random.randint(50,600)
            Y=random.randint(50,430)
            skyblue=(X,Y)
            bucket_s=(skyblue[0]-70,skyblue[1])
    
    if spill_p==0:#PINK
        screen.blit(bucket_p_img,(bucket_p[0]-int(paints_size/2),bucket_p[1]-int(paints_size/2)))
    elif spill_p>0 and spill_p<3:
        screen.blit(bucket_p_2,(bucket_p[0]-int(paints_size/2),bucket_p[1]-int(paints_size/2)))
        spill_p+=1
    else :
        screen.blit(bucket_p_3,(bucket_p[0]-int(paints_size/2),bucket_p[1]-int(paints_size/2)))
        spill_p+=1
        if spill_p>20:
            spill_p=0
            X=random.randint(50,600)
            Y=random.randint(50,430)
            pink=(X,Y)
            bucket_p=(pink[0]-70,pink[1])

    # ERASE
    if check_collision(broom,pos_now,distance):
        mousepos.clear()
        animals.clear()
        opacity.clear()
        screen.blit(broom_2,(broom[0]-int(89/2),broom[1]-int(143/2)))
        sfx1 = pygame.mixer.Sound('sound/erase.ogg')
        sfx1.set_volume(0.5)
        sfx1.play()
        broom_flag=1
    else:
        broom_flag=0
        
        

    # user img
    
    #screen.blit(flower,(pos_now[0]-int(flower_size/2),pos_now[1]-int(flower_size/2)))
    if flag==1:
        X=random.randint(0,40)
        Y=random.randint(0,40)

    screen.blit(imgLoad('blink'+str(flag)),(pos_now[0]-X,pos_now[1]-Y))

    if flag==4:
        X2=random.randint(0,40)
        Y2=random.randint(0,40)
    screen.blit(imgLoad('blink'+str(flag-3 if flag>3 else flag+5)),(pos_now[0]-X2,pos_now[1]-Y2))

    if flag==8:
        flag=0

    flag+=1

    if opacity_now <= 10:
        guide_count += 1
    else:
        guide_count = 0
        
    # if user did not touch any bucket yet, no footstep printing
    if color_now is None:
        #guide window blit
        if guide_count>=20:
            screen.blit(guide1,(100,100))
            if (spill_y>0 and spill_y<20) or (spill_s>0 and spill_s<20) or (spill_g>0 and spill_g<20) or (spill_p>0 and spill_p<20):
                screen.blit(guide2,(100,100))
                guide2_count += 1
        if guide2_count > 0:
            screen.blit(guide2,(100,100))
            guide2_count += 1
            if guide2_count >= 15:
                guide2_count = 0
                guide_count = 0
        pygame.display.update()
        continue

    elif color_now is not 'time_over':
        mousepos.append(pos_now)
        mousepos_count = len(mousepos)
        animals.append((detect.rotate_img(animal_now+color_now,mousepos[mousepos_count-2],mousepos[mousepos_count-1])))
        opacity.append(opacity_now)
        '''
        sfx1 = pygame.mixer.Sound('sound/step.ogg')
        sfx1.set_volume(0.5)
        sfx1.play()
        '''
        
    # draw footsteps on screen
    for i in range(len(mousepos)):
        drawObject(animals[i],mousepos[i],opacity[i])

    if len(mousepos) > highest_len:
        highest_len = len(mousepos)
        cv.imwrite('output/popimage.jpg', img)
        pygame.image.save(screen,"output/screenshot.jpg")
        

    #guide window blit
    if guide_count>=20:
        screen.blit(guide1,(100,100))
        if (spill_y>0 and spill_y<20) or (spill_s>0 and spill_s<20) or (spill_g>0 and spill_g<20) or (spill_p>0 and spill_p<20):
            screen.blit(guide2,(100,100))
            guide2_count += 1
    if guide2_count > 0:
        screen.blit(guide2,(100,100))
        guide2_count += 1
        if guide2_count >= 15:
            guide2_count = 0
            guide_count = 0
    
    
    pygame.display.update()
    
pygame.quit()
cv.destroyAllWindows()
cap.release()
