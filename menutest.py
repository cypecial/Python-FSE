from pygame import *
import glob
from random import *
from math import *

init()

#############################loading components of game#########################

#myCmp compares every sprite frame and sorts them in the right order(1,2,...,10)
def myCmp(f1,f2):
    n1 = int(f1[11:-4].split(" ")[-1])
    n2 = int(f2[11:-4].split(" ")[-1])
    return cmp(n1,n2)
##===========================loading sprites==================================##
all_natsu = []
natsu_sprites = glob.glob("stuff/natsu/*.png")
natsu_sprites.sort(myCmp)
for each in natsu_sprites:
    name = each.strip(".png").split("\\")[-1] #the sprite frame number
    pic = image.load(each)  #the corresponding picture
    all_natsu.append([name,pic])
##all_frames = [each.split() for each in open("frames.txt").readlines()]
natsu_sprite_right = {}
natsu_sprite_left = {}

houkou_data = {}
houkou_data["Houkou"] = [0,1,2,3]
houkou_data["FlameStart"] = [0,1,2]
houkou_data["Flame"] = [3,4,5]
houkou_data["FlameEnd"] = [6,7]


#~~~~~~~~~~~~~~~~~~~~~~~~for all natsu sprites facing right~~~~~~~~~~~~~~~~~~~~#

for name, pic in all_natsu:
    name = name.split(" ")[0]   #splits the name and frame number so we can use
                                # the name as a key in our dictionary
    if name not in natsu_sprite_right:
        natsu_sprite_right[name] = [pic] #if not found make new list
    else:
        natsu_sprite_right[name].append(pic)   #if found then append the pic

#~~~~~~~~~~~~~~~~~~~~~~~for all natsu sprites facing left~~~~~~~~~~~~~~~~~~~~~~#

for name,pic in all_natsu:
    name = name.split(" ")[0]
    pic=transform.flip(pic,True,False)
    if name not in natsu_sprite_left:
        natsu_sprite_left[name] = [pic] 
    else:
        natsu_sprite_left[name].append(pic)

##---------------------------enemies------------------------------------------##
                            ####zombie####
all_zombie = []
zombie_sprites = glob.glob("stuff/enemy/zombie/*.png")
zombie_sprite_data ={}
for each in zombie_sprites:
    name = each.strip(".png").split("\\")[-1] #the sprite frame number
    pic = image.load(each)  #the corresponding picture
    all_zombie.append([name,pic])
for name, pic in all_zombie:
    name = name.split(" ")[0]   
    if name not in zombie_sprite_data:
        zombie_sprite_data[name] = [pic]
    else:
        zombie_sprite_data[name].append(pic)

##=============================loading music==================================##

##mixer.music.load("stuff/sound/Fiesta(FairyTail - OP6).mp3")
##mixer.music.play(-1)
        
##==================================pictures==================================##

bkgd = image.load("stuff/pics/map.png")
submap = image.load("stuff/pics/submap.png")

cursorpic = image.load("stuff/pics/cursor.png")
bhealth = image.load("stuff/pics/base health.png")
health = image.load("stuff/pics/health.png")
mana = image.load("stuff/pics/mana.png")
htemp = image.load("stuff/pics/health template.png")

health_pics = [bhealth,health,mana,htemp]

                        ####beginning of the game####

survival_3 = image.load("stuff/pics/3.png")
survival_2 = image.load("stuff/pics/2.png")
survival_1 = image.load("stuff/pics/1.png")
survival_survival = image.load("stuff/pics/survival.png")
survival_data = [survival_3,survival_2,survival_1,survival_survival]
game_begin = False
countdown = True
survival_frame = 0
survival_picture = survival_data[survival_frame]
count = 20
countSurvival = 0


##############################loading done######################################

################################Enemy Programming###############################

##-------------------------enemy information----------------------------------##

spawnLocation = [0,400,600,800,1000,1500,1700,1900]
timewait=0
enemies=[]
action_pick_delay = 0
enemynumber = 20

##################################Enemy functions###############################

def spawnEnemies():
    global timewait
    global enemynumber
    if timewait == 50:
        if len(enemies) < 10:
            if enemynumber != 0:
                location = choice(spawnLocation)
    #same info as guy       [x-cord,y-cord,health,mana,delay,move,orientation,onground,enemy_dmg,die]
                enemies.append([location,497,10,None,0,"Walk_Right",0,"Right",True,None,False])
                timewait=0
                enemynumber -= 1
    else: timewait+=1
    
def enemyMove():
    global action_pick_delay
    global game_begin
    zombie_action = ["Walk_Left","Walk_Right"]
    if game_begin:
        if guy[ORIENTATION] == "Right":        
            pic_width,pic_height = natsu_sprite_right[guy[MOVE]][guy[FRAMENUMBER]].get_size()
        elif guy[ORIENTATION] == "Left":        
            pic_width,pic_height = natsu_sprite_left[guy[MOVE]][guy[FRAMENUMBER]].get_size()

        for each in enemies:
            if each[DIE] == True:
                if each[MOVE] != "Die":
                    each[FRAMENUMBER] = 0
                    each[MOVE] = "Die"
            else:       
                if abs(each[X]-guy[X]) >= 200:
                    action_pick_delay += 1
                    if action_pick_delay == 10:
                        action_pick_delay = 0
                        move = zombie_action[randint(0,1)]
                        if each[MOVE] != move:
                            each[MOVE] = move
                            each[FRAMENUMBER] = 0

                else:
                    if guy[X] > each[X]:
                        if each[MOVE] != "Walk_Right":
                            each[MOVE] = "Walk_Right"
                            each[FRAMENUMBER] = 0

                    elif guy[X] < each[X]:
                        if each[MOVE] != "Walk_Right":
                            each[MOVE] = "Walk_Left"
                            each[FRAMENUMBER] = 0
                        
                if each[MOVE] == "Walk_Left":
                    each[ORIENTATION] = "Left"
                    if each[X] >= 0:
                        each[X] -= 1
                    else: each[X] = 0
                elif each[MOVE] == "Walk_Right":
                    if each[X] <= 2400:
                        each[X] += 1
                    else: each[X] = 0
                    each[ORIENTATION] = "Right"

                if guy[X] >= 500 and guy[X] < 1900:
                    if guy[ORIENTATION] == "Right":
                        playerRect = Rect(500-pic_width/2,guy[Y],pic_width,-pic_height)
                        playerRect.normalize()
                    
                    elif guy[ORIENTATION] == "Left":           
                        playerRect = Rect(500+pic_width/2,guy[Y],-pic_width,-pic_height)
                        playerRect.normalize()

                    offset = 500 - (guy[X]-each[X])
                    enemy_width,enemy_height = zombie_sprite_data[each[MOVE]][each[FRAMENUMBER]].get_size()
                    enemyRect = Rect(offset,each[Y],enemy_width,-enemy_height)
                    enemyRect.normalize()
                    
                    if enemyRect.colliderect(playerRect):
                        if each[ORIENTATION] == "Right":
                            if each[MOVE] != "Attack_Right":
                                each[MOVE] = "Attack_Right"
                                each[FRAMENUMBER] = 0
                        elif each[ORIENTATION] == "Left":
                            if each[MOVE] != "Attack_Left":
                                each[MOVE] = "Attack_Left"
                                each[FRAMENUMBER] = 0
                else:
                    if guy[X] < 500:
                        if guy[ORIENTATION] == "Right":
                            playerRect = Rect(guy[X]-pic_width/2,guy[Y],pic_width,-pic_height)
                            playerRect.normalize()
                            
                        elif guy[ORIENTATION] == "Left":           
                            playerRect = Rect(guy[X]+pic_width/2,guy[Y],-pic_width,-pic_height)
                            playerRect.normalize()

                        enemy_width,enemy_height = zombie_sprite_data[each[MOVE]][each[FRAMENUMBER]].get_size()
                        enemyRect = Rect(each[X],each[Y],enemy_width,-enemy_height)
                        enemyRect.normalize()

                        if enemyRect.colliderect(playerRect):
                            if each[ORIENTATION] == "Right":
                                if each[MOVE] != "Attack_Right":
                                    each[MOVE] = "Attack_Right"
                                    each[FRAMENUMBER] = 0
                            elif each[ORIENTATION] == "Left":
                                if each[MOVE] != "Attack_Left":
                                    each[MOVE] = "Attack_Left"
                                    each[FRAMENUMBER] = 0

                    elif guy[X] >= 1900:
                        if guy[ORIENTATION] == "Right":
                            playerRect = Rect(guy[X]-1400-pic_width/2,guy[Y],pic_width,-pic_height)
                            playerRect.normalize()
                            
                        elif guy[ORIENTATION] == "Left":           
                            playerRect = Rect(guy[X]-1400+pic_width/2,guy[Y],-pic_width,-pic_height)
                            playerRect.normalize()


                        enemy_width,enemy_height = zombie_sprite_data[each[MOVE]][each[FRAMENUMBER]].get_size()
                        enemyRect = Rect(each[X]-1400,each[Y],enemy_width,-enemy_height)
                        enemyRect.normalize()
                            
                        if enemyRect.colliderect(playerRect):
                            if each[ORIENTATION] == "Right":
                                if each[MOVE] != "Attack_Right":
                                    each[MOVE] = "Attack_Right"
                                    each[FRAMENUMBER] = 0
                            elif each[ORIENTATION] == "Left":
                                if each[MOVE] != "Attack_Left":
                                    each[MOVE] = "Attack_Left"
                                    each[FRAMENUMBER] = 0

def drawEnemy():
    global game_begin
    if game_begin:
        for each in enemies:
            if each[FRAMENUMBER] == len(zombie_sprite_data[each[MOVE]]):
                if each[MOVE] == "Die":
                    each[DIE] == False
                    enemies.remove(each)
                else:
                    each[FRAMENUMBER] = 0

            else:
                enemy_width,enemy_height = zombie_sprite_data[each[MOVE]][each[FRAMENUMBER]].get_size()
                if each[ORIENTATION] == "Right":
                    if guy[0] >= 500 and guy[0] < 1900:
                        offset = 500 - (guy[0]-each[0])
                        pos = (offset,each[Y]-enemy_height)
                        screen.blit(zombie_sprite_data[each[MOVE]][each[FRAMENUMBER]],(pos))

                    else:
                        if guy[0] < 500:
                            pos = (each[X],each[Y]-enemy_height)
                        elif guy[0] >= 1900:
                            pos = (each[X]-1400,each[Y]-enemy_height)
                        screen.blit(zombie_sprite_data[each[MOVE]][each[FRAMENUMBER]],(pos))
                    
                elif each[ORIENTATION] == "Left":
                    if guy[0] >= 500 and guy[0] < 1900:
                        offset = 500 - (guy[0]-each[0])
                        pos = (offset,each[Y]-enemy_height)
                        screen.blit(zombie_sprite_data[each[MOVE]][each[FRAMENUMBER]],(pos))

                    else:
                        if guy[0] < 500:
                            pos = (each[X],each[Y]-enemy_height)
                        elif guy[0] >= 1900:
                            pos = (each[X]-1400,each[Y]-enemy_height)
                        screen.blit(zombie_sprite_data[each[MOVE]][each[FRAMENUMBER]],(pos))
################################Draw Map########################################

def drawMap():
    #if the player is is in the middle of the map
    offset = 500 - guy[0]
    if guy[0] >= 500 and guy[0] < 1900:
        screen.blit(submap, (offset,0))
        screen.blit(bkgd, (offset,0))
        drawGuy(500,guy[1])
    #if the player is at the sides of the map
    else:
        if guy[0] < 500:
            screen.blit(submap, (0,0))
            screen.blit(bkgd,(0,0))
            drawGuy(guy[0],guy[1])
        elif guy[0] >= 1900:
            screen.blit(submap, (-1400,0))
            screen.blit(bkgd,(-1400,0))
            drawGuy(guy[0]-1400,guy[1])
            
    if countdown == True:
        survival_picture = survival_data[survival_frame]
        screen.blit(survival_picture,(0,0))


##---------------------------Player Information-------------------------------##
    
#[x-cord,y-cord,health,mana,delay,move,orientation,onground,heal_hp,heal_mp,hurt]
guy = [1200,497,200,400,0,"Intro",0,"Right",True,False,False,False]
##Intro = True
X = 0
Y = 1
HEALTH = 2
MANA = 3
DELAY = 4
MOVE = 5
FRAMENUMBER = 6
ORIENTATION = 7
ONGROUND = 8
heal_hp=9
heal_mp=10
HURT = 11
ENEMYDMG = 9
DIE = 10
                        ########jump data#########
gravity = 4
jumprate = 10
countJ = 0
jump = True
                        #######stun and hurt rate#######
hurtrate = 10
hurtcount = 0
stunrate = 30
countH = 0
countS = 0

attack_moves = ["Combo","Houkou","Kenkaku","Gakizume"]
###########################Houkou data#########################################
houkou_frame = 0
houkou_sprite = 0
houkou_move = ""
flag_houkou = True
##############################Intro Data########################################
Intro = True
############################Player Functions####################################

def checkAction():
    global attack_moves
    global houkou_move
    global houkou_frame
    global flag_houkou

    global Intro
    
    global gravity
    global jumprate
    global jump
    uninterruptable = ["Jump","Gakizume","Combo","Kenkaku","Houkou","Charge"]
#------------------------------basic actions--------------------------------
    keys=key.get_pressed()
    if guy[ONGROUND] == True:
        if keys[K_h]:
            if guy[MOVE] != "Houkou":
                guy[MOVE] = "Houkou"
                guy[FRAMENUMBER] = 0
                houkou_move = ""
                houkou_frame = 0
                flag_houkou = True

        if Intro == True:
            if guy[MOVE]!= "Intro":
                guy[MOVE] = "Intro"
                guy[FRAMENUMBER] = 0
                
        elif keys[K_a]:
            if guy[MOVE] not in uninterruptable:
                pic = natsu_sprite_left[guy[MOVE]][guy[FRAMENUMBER]]
                pic_width = pic.get_width()
                if guy[MOVE] != "Walk":
                    guy[FRAMENUMBER] = 0
                if guy[ORIENTATION] != "Left":
                    guy[ORIENTATION] = "Left"
                guy[MOVE] = "Walk"
                if guy[X] > pic_width/2:
                    guy[X] -= 10
                else: guy[X] = pic_width/2
    #walk right    
        elif keys[K_d]:
            if guy[MOVE] not in uninterruptable:
                pic = natsu_sprite_right[guy[MOVE]][guy[FRAMENUMBER]]
                pic_width = pic.get_width()
                if guy[MOVE] != "Walk":
                    guy[FRAMENUMBER] = 0
                if guy[ORIENTATION] != "Right":
                    guy[ORIENTATION] = "Right"
                guy[MOVE] = "Walk"
                if guy[X] < 2400 - pic_width/2:
                    guy[X] += 10
                else: guy[X] = 2400 - pic_width/2
        #heal    
        elif keys[K_LCTRL]:
            if guy[MOVE] != "Charge":
                guy[MOVE] = "Charge"
                guy[FRAMENUMBER] = 0
        #jump    
        elif keys[K_w]:
            if guy[ONGROUND]:
                if guy[MOVE] != "Jump":
                    guy[MOVE]  = "Jump"
                    guy[FRAMENUMBER] = 0
                if guy[ONGROUND] == True:
                    if jump:
                        guy[MOVE]  = "Jump"
                        guy[FRAMENUMBER] = 0
                        jump = False
        #gakizume
        elif keys[K_g]:
            if guy[MOVE] != "Gakizume":
                guy[FRAMENUMBER] = 0   
                guy[MOVE] = "Gakizume"   

        #combo att    
        elif keys[K_j]: 
            if guy[MOVE] != "Combo":
                guy[FRAMENUMBER] = 0   
                guy[MOVE] = "Combo"

        #kenkaku     
        elif keys[K_k]:
            if guy[MOVE] != "Kenkaku":
                guy[FRAMENUMBER] = 0
                guy[MOVE] = "Kenkaku"

        elif guy[MOVE] not in uninterruptable: #combo/ attack moves are uninteruptable6
            if guy[MOVE] != "Stance":
                guy[FRAMENUMBER] = 0
                guy[MOVE] = "Stance"
    else:
        if keys[K_a]:
            guy[ORIENTATION] = "Left"
            guy[X] -= 10
        elif keys[K_d]:
            guy[ORIENTATION] = "Right"
            guy[X] +=10

#-----------------------------combinations-----------------------------
        
def drawGuy(xpos,ypos):
    global houkou_frame
    global houkou_sprite

    global Intro
    
    global gravity
    global jumprate
    global jump
    keys=key.get_pressed()
    #-------health/mana management-----
    #while moving
    if guy[HEALTH]<200: guy[heal_hp]=True
    if guy[MANA]<400: guy[heal_mp]=True
    if guy[HEALTH]>=200: guy[heal_hp]=False
    if guy[MANA]>=400: guy[heal_mp]=False
    if guy[MOVE] == "Houkou":
        guy[MANA]-=1
    if guy[MOVE] == "Charge" and guy[heal_hp] == True: guy[HEALTH]+=1
    if guy[MOVE] == "Charge" and guy[heal_mp] == True: guy[MANA]+=1
        
    #after move
    if guy[FRAMENUMBER] == len(natsu_sprite_right[guy[MOVE]]):
        if guy[MOVE] == "Combo":
            guy[MANA] -= 5
        elif guy[MOVE] == "Kenkaku":
            guy[MANA] -= 20
        elif guy[MOVE] == "Gakizume":
            guy[MANA] -= 7
    #----------------------------------  
        
    if guy[MOVE] == "Houkou":
        if guy[ORIENTATION] == "Right":
            pic_houkou = natsu_sprite_right[guy[MOVE]][guy[FRAMENUMBER]]
            pic_flame = natsu_sprite_right["H_flame"][houkou_frame]
            pic_width , pic_height = pic_houkou.get_size()
            flame_width , flame_height = pic_flame.get_size()
            center = pic_width/2
            flameRect = Rect(xpos -center + pic_width,ypos-pic_height-50,flame_width,flame_height)
            if houkou_frame != 0:
                screen.blit(pic_flame,(xpos -center + pic_width,ypos-pic_height-50))
                flameRect.normalize()
                draw.rect(screen,(255,0,0),flameRect,2)
            screen.blit(pic_houkou,(xpos-center,ypos-pic_height))

        elif guy[ORIENTATION] == "Left":
            pic_houkou = natsu_sprite_left[guy[MOVE]][guy[FRAMENUMBER]]
            pic_flame = natsu_sprite_left["H_flame"][houkou_frame]
            pic_width , pic_height = pic_houkou.get_size()
            flame_width , flame_height = pic_flame.get_size()
            center = pic_width/2
            flameRect = Rect(xpos -center + pic_width,ypos-pic_height-50,-flame_width,flame_height)
            if houkou_frame !=0:
                draw.rect(screen,(255,0,0),flameRect,2)
                screen.blit(pic_flame,(xpos - center - flame_width,ypos-pic_height-50))

            screen.blit(pic_houkou,(xpos + center - pic_width,ypos-pic_height))
            
    else:        
        if guy[ORIENTATION] == "Right":
            if guy[FRAMENUMBER] == len(natsu_sprite_right[guy[MOVE]]):
                guy[FRAMENUMBER] = 0
                if guy[MOVE] == "Intro":
                    Intro = False
                guy[MOVE] = "Stance"
            pic = natsu_sprite_right[guy[MOVE]][guy[FRAMENUMBER]]
            pic_width , pic_height = pic.get_size()
            center = pic_width/2
            if submap.get_at((guy[X]+center,guy[Y]))[3] == 0:
                guy[ONGROUND] = False
            else: guy[ONGROUND] = True
            screen.blit(pic,(xpos-center,ypos-pic_height))
        elif guy[ORIENTATION] == "Left":
            if guy[FRAMENUMBER] == len(natsu_sprite_left[guy[MOVE]]):
                guy[FRAMENUMBER] = 0
                if guy[MOVE] == "Intro":
                    Intro = False
                guy[MOVE] = "Stance"
            pic = natsu_sprite_left[guy[MOVE]][guy[FRAMENUMBER]]
            pic_width , pic_height = pic.get_size()
            center = pic_width/2
            if submap.get_at((guy[X]+center,guy[Y]))[3] == 0:
                guy[ONGROUND] = False
            else: guy[ONGROUND] = True
            screen.blit(pic,(xpos + center - pic_width,ypos-pic_height))

    if guy[MOVE] == "Walk":
        if keys[K_w]:
            if guy[ONGROUND]:
                guy[Y] -= 20
    if guy[MOVE] == "Jump":
        if guy[FRAMENUMBER] < 3 and guy[FRAMENUMBER] > 0:
            guy[Y] -= 5
        elif guy[FRAMENUMBER] >= 3 and guy[FRAMENUMBER] < 4:
            guy[Y] += gravity
        if keys[K_a]:    
            if guy[X] > pic_width/2:
                guy[X] -= 10
            else: guy[X] = pic_width/2
        
        elif keys[K_d]:
            if guy[X] < 2400 - pic_width/2:
                guy[X] += 10
            else: guy[X] = 2400 - pic_width/2
def advanceFrame():
    global houkou_frame
    global houkou_move
    global houkou_sprite
    global flag_houkou

    global jumprate
    global jump
    global countJ
    
    global hurtrate
    global countH

    global game_begin
    global countdown
    global count 
    global countSurvival
    global survival_frame
    
    if guy[ONGROUND] == False:
        guy[1] += gravity
    
    if countJ >= jumprate:
        jump = True
        countJ = 0
    else:
        countJ += 1
        
    if guy[HURT] == True:
        if countH >= hurtrate:
            guy[HURT] = False
            countH = 0
        else:
            countH += 1
            
    if countdown == True:
        if countSurvival == count:
            countSurvival = 0
            survival_frame += 1
        else:
            countSurvival += 1
                
        if survival_frame == 4:
            countdown = False
            game_begin = True
            
    if game_begin:
        if guy[MOVE] == "Houkou":
            guy[DELAY] += 1
            if guy[DELAY] % 3 == 0:
                guy[DELAY] = 0
                guy[FRAMENUMBER] += 1
                houkou_sprite += 1
            
            if guy[FRAMENUMBER] >= len(houkou_data["Houkou"]):
                guy[FRAMENUMBER] = houkou_data["Houkou"][-1]
                if flag_houkou:
                    houkou_move = "FlameStart"
                    houkou_sprite = 0
                flag_houkou = False
            if houkou_move == "FlameStart":
                if houkou_sprite >= len(houkou_data["FlameStart"]):
                    houkou_sprite = 0
                    houkou_move = "Flame"
                houkou_frame = houkou_data["FlameStart"][houkou_sprite]
            elif houkou_move == "FlameEnd":
                if houkou_sprite >= len(houkou_data["FlameEnd"]):
                    houkou_sprite = 0
                    guy[MOVE] = "Stance"
                    guy[FRAMENUMBER] = 0
                houkou_frame = houkou_data["FlameEnd"][houkou_sprite]
            elif houkou_move == "Flame":
                reverse = houkou_data["Flame"][:-1]
                if houkou_sprite >= len(houkou_data["Flame"]):
                    houkou_sprite = 0
                elif houkou_sprite >= len(reverse):
                    houkou_sprite = 0
                houkou_frame = houkou_data["Flame"][houkou_sprite]
        else:
            guy[DELAY] += 1
            if guy[DELAY] % 3 == 0:
                guy[DELAY] = 0
                guy[FRAMENUMBER] += 1
                    
        for each in enemies:
            each[DELAY] += 1
            if each[DELAY] % 3 == 0:
                each[DELAY] = 0
                each[FRAMENUMBER] += 1
                
    else:
        guy[FRAMENUMBER] = 0
        for each in enemies:
            each[FRAMENUMBER] = 0
    #(ENEMIES AS WELL OR ELSE THEY WONT MOVE ...)
            
def damageCalculation():
    global houkou_move
    global houkou_frame
    global flameRect
    if game_begin:
        #I am trying to find the closest enemy to the player becasuse some moves only damgae one enemy
##        if guy[MOVE] in attack_moves:
        closest = 2400
        enemy_index = 0
        for i in range(len(enemies)):
            if guy[ORIENTATION] == "Right":
                if enemies[i][X]-guy[X] < closest:
                    closest = enemies[i][X]-guy[X]
                    enemy_index = i
            elif guy[ORIENTATION] == "Left":
                if guy[X] - enemies[i][X] < closest:
                    closest = guy[X] - enemies[i][X]
                    enemy_index = i
                            
        if guy[X] >= 500 and guy[X] < 1900:
            if guy[ORIENTATION] == "Right":
                pic = natsu_sprite_right[guy[MOVE]][guy[FRAMENUMBER]]
                pic_width , pic_height = pic.get_size()
                playerRect = Rect(500-pic_width/2,guy[Y],pic_width,-pic_height)
                playerRect.normalize()
                
            elif guy[ORIENTATION] == "Left":
                pic = natsu_sprite_left[guy[MOVE]][guy[FRAMENUMBER]]
                pic_width , pic_height = pic.get_size()            
                playerRect = Rect(500+pic_width/2,guy[Y],-pic_width,-pic_height)
                playerRect.normalize()
            for each in enemies:
                each[ENEMYDMG] = True
                offset = 500 - (guy[X]-each[X])
                enemy_width,enemy_height = zombie_sprite_data[each[MOVE]][each[FRAMENUMBER]].get_size()
                enemyRect = Rect(offset,each[Y],enemy_width,-enemy_height)
                enemyRect.normalize()
                if each[MOVE] == "Attack_Right" or each[MOVE] == "Attack_Left":
                    if guy[HURT] == False:
                        guy[HEALTH]-= 1
                        guy[HURT] = True
                if guy[ORIENTATION] == "Right":
                    if each[X] < guy[X]:
                        each[ENEMYDMG] = False
                elif guy[ORIENTATION] == "Left":
                    if each[X] > guy[X]:
                        each[ENEMYDMG] = False
                if guy[MOVE] in attack_moves:
                    if playerRect.colliderect(enemyRect) and guy[MOVE] != "Houkou":
                        if each[ENEMYDMG] == True:
                            if guy[MOVE] == "Combo":
                                enemies[enemy_index][HEALTH] -= 5
                            elif guy[MOVE] == "Kenkaku":
                                enemies[enemy_index][HEALTH] -= 10
                            elif guy[MOVE] == "Gakizumi":
                                enemies[enemy_index][HEALTH] -= 10
                elif guy[MOVE] == "Houkou":
                    if houkou_move == "Flame":
                        if guy[ORIENTATION] == "Left":
##                            flameRect = Rect(xpos -center + pic_width,ypos-pic_height-50,flame_width,flame_height)
##                            flameRect.normalize()
                            if flameRect.colliderect(enemyRect):
                                each[HEALTH] -= 5
                if each[HEALTH] <= 0:
                    each[HEALTH] = 0
                draw.rect(screen,(0,0,0),enemyRect,2)
                draw.rect(screen,(0,255,0),playerRect,2)
                    
                        
        else:
            if guy[X] < 500:
                if guy[ORIENTATION] == "Right":
                    pic = natsu_sprite_right[guy[MOVE]][guy[FRAMENUMBER]]
                    pic_width , pic_height = pic.get_size()
                    playerRect = Rect(guy[X]-pic_width/2,guy[Y],pic_width,-pic_height)
                    playerRect.normalize()
                    
                elif guy[ORIENTATION] == "Left":
                    pic = natsu_sprite_left[guy[MOVE]][guy[FRAMENUMBER]]
                    pic_width , pic_height = pic.get_size()            
                    playerRect = Rect(guy[X]+pic_width/2,guy[Y],-pic_width,-pic_height)
                    playerRect.normalize()

                for each in enemies:
                    each[ENEMYDMG] = True
                    enemy_width,enemy_height = zombie_sprite_data[each[MOVE]][each[FRAMENUMBER]].get_size()
                    enemyRect = Rect(each[X],each[Y],enemy_width,-enemy_height)
                    enemyRect.normalize()
                    if each[MOVE] == "Attack_Right" or each[MOVE] == "Attack_Left":
                        if guy[HURT] == False:
                            guy[HEALTH]-= 1
                            guy[HURT] = True
                    if guy[ORIENTATION] == "Right":
                        if each[X] < guy[X]:
                            each[ENEMYDMG] = False
                    elif guy[ORIENTATION] == "Left":
                        if each[X] > guy[X]:
                            each[ENEMYDMG] = False
                    if guy[MOVE] in attack_moves:
                        if playerRect.colliderect(enemyRect) and guy[MOVE] != "Houkou":
                            if each[ENEMYDMG] == True:
                                if guy[MOVE] == "Combo":
                                    enemies[enemy_index][HEALTH] -= 5
                                elif guy[MOVE] == "Kenkaku":
                                    enemies[enemy_index][HEALTH] -= 10
                                elif guy[MOVE] == "Gakizumi":
                                    enemies[enemy_index][HEALTH] -= 10
                        elif guy[MOVE] == "Houkou":
                            if houkou_move == "Flame":
                                if guy[ORIENTATION] == "Left":
                                    sdfsdf=0
##                                    flame_width , flame_height = pic_flame.get_size()
##                                    flameRect = Rect(xpos -center + pic_width,ypos-pic_height-50,flame_width,flame_height)
##                                    flameRect.normalize()
##                                    if flameRect.colliderect(enemyRect):
##                                        each[HEALTH] -= 5
                    if each[HEALTH] <= 0:
                        each[HEALTH] = 0
                    draw.rect(screen,(0,0,0),enemyRect,2)
                    draw.rect(screen,(0,255,0),playerRect,2)

            elif guy[X] >= 1900:
                if guy[ORIENTATION] == "Right":
                    pic = natsu_sprite_right[guy[MOVE]][guy[FRAMENUMBER]]
                    pic_width , pic_height = pic.get_size()
                    playerRect = Rect(guy[X]-1400-pic_width/2,guy[Y],pic_width,-pic_height)
                    playerRect.normalize()
                    
                elif guy[ORIENTATION] == "Left":
                    pic = natsu_sprite_left[guy[MOVE]][guy[FRAMENUMBER]]
                    pic_width , pic_height = pic.get_size()            
                    playerRect = Rect(guy[X]-1400+pic_width/2,guy[Y],-pic_width,-pic_height)
                    playerRect.normalize()

                for each in enemies:
                    each[ENEMYDMG] = True
                    enemy_width,enemy_height = zombie_sprite_data[each[MOVE]][each[FRAMENUMBER]].get_size()
                    enemyRect = Rect(each[X]-1400,each[Y],enemy_width,-enemy_height)
                    enemyRect.normalize()
                    if each[MOVE] == "Attack_Right" or each[MOVE] == "Attack_Left":
                        if guy[HURT] == False:
                            guy[HEALTH]-= 1
                            guy[HURT] = True
                    if guy[ORIENTATION] == "Right":
                        if each[X] < guy[X]:
                            each[ENEMYDMG] = False
                    elif guy[ORIENTATION] == "Left":
                        if each[X] > guy[X]:
                            each[ENEMYDMG] = False
                    if playerRect.colliderect(enemyRect) and guy[MOVE] != "Houkou":
                        if each[ENEMYDMG] == True:
                            if guy[MOVE] == "Combo":
                                enemies[enemy_index][HEALTH] -= 5 
                            elif guy[MOVE] == "Kenkaku":
                                enemies[enemy_index][HEALTH] -= 10
                            elif guy[MOVE] == "Gakizumi":
                                enemies[enemy_index][HEALTH] -= 10
                    elif guy[MOVE] == "Houkou":
                        if houkou_move == "Flame":
                            if guy[ORIENTATION] == "Left":
##                                flameRect = Rect(xpos -center + pic_width,ypos-pic_height-50,flame_width,flame_height)
##                                flameRect.normalize()
                                if flameRect.colliderect(enemyRect):
                                    each[HEALTH] -= 5
                    if each[HEALTH] <= 0:
                        each[HEALTH] = 0
                    draw.rect(screen,(0,0,0),enemyRect,2)
                    draw.rect(screen,(0,255,0),playerRect,2)

def drawHealth():
    global running
    
    hp = -4*(200-guy[HEALTH])
    mp = -2*(400-guy[MANA])
    screen.blit(health_pics[0],(0,600))
    screen.blit(health_pics[1],(hp,600))
    screen.blit(health_pics[2],(mp,600))
    screen.blit(health_pics[3],(0,600))
    
    for each in enemies:
        enemy_width,enemy_height = zombie_sprite_data[each[MOVE]][each[FRAMENUMBER]].get_size()
        if guy[X] >= 500 and guy[X] < 1900:
            offset = 500 - (guy[X]-each[X])
            pos = (offset,each[Y])
        else:
            if guy[0] < 500:
                pos = (each[X],each[Y])
            elif guy[0] >= 1900:
                pos = (each[X]-1400,each[Y])
        enemy_hp = enemy_width*each[HEALTH]/10
        draw.rect(screen,(255,0,0),(pos[X],each[Y]-10,enemy_width,10))
        draw.rect(screen,(0,255,0),(pos[X],each[Y]-10,enemy_hp,10))
        if each[HEALTH] <= 0:
            each[DIE] = True
            
    if guy[HEALTH]<=0: guy[HEALTH]=0
    if guy[MANA]<=0: guy[MANA]=0
    if guy[HEALTH]>=200: guy[HEALTH]=200
    if guy[MANA]>=400: guy[MANA]=400
        
#-------------------------------------menu------------------------------------#
def instructions(page):
    running = True
    mouse.set_visible(False)
    inst = image.load("stuff/pics/instructions.png")
    inst = transform.smoothscale(inst, screen.get_size())
    screen.blit(inst,(0,0))
    bac=screen.copy()
    while running:
        keys=key.get_pressed()
        for evnt in event.get():          
            if keys[K_ESCAPE]:
                running = False
        mx,my = mouse.get_pos()
        screen.blit(bac,(0,0))
        screen.blit(cursorpic,(mx-25,my-25))
        display.flip()
    return "menu"
        
def credit(page):
    running = True
    mouse.set_visible(False)
    cred = image.load("stuff/Pics/credits.png")
    cred = transform.smoothscale(cred, screen.get_size())
    screen.blit(cred,(0,0))
    bac=screen.copy()
    while running:
        keys=key.get_pressed()
        for evnt in event.get():          
            if keys[K_ESCAPE]:
                running = False
        mx,my = mouse.get_pos()
        screen.blit(bac,(0,0))
        screen.blit(cursorpic,(mx-25,my-25))
        display.flip()
    return "menu"

def quitgame(page):
    running = True
    mouse.set_visible(False)
    note = image.load("stuff/pics/quit.png")
    back = screen.copy()
    note = transform.smoothscale(note, screen.get_size())
    buttons = [Rect(391,y*88+332,205,65) for y in range(2)]
    vals = ["menu","game"]
    while running:
        for evnt in event.get():          
            if evnt.type == QUIT:
                return "exit"

        mx,my = mouse.get_pos()
        mb = mouse.get_pressed()
        screen.blit(back,(0,0))
        screen.blit(note,(0,0))
        for r,v in zip(buttons,vals):
            if r.collidepoint(mx,my):
                draw.rect(screen,(255,25,0),r,4)
                if mb[0]==1:
                    return v
        screen.blit(cursorpic,(mx-25,my-25))
        display.flip()

def game(page):
    mixer.music.load("stuff/sound/Fiesta(FairyTail - OP6).wav")
    mixer.music.play(-1)
    screen = display.set_mode((1000,723))#,FULLSCREEN)
    running = True
    mouse.set_visible(False)
    myclock = time.Clock()
    global houkou_move
    global houkou_frame
    global flag_houkou
    global enemynumber
    while running:
        for evt in event.get():
            if evt.type == KEYDOWN:
                if evt.key == K_ESCAPE:
                    running = False
            if evt.type == KEYUP:
                if evt.key == K_h:
                    houkou_move = "FlameEnd"
        if enemynumber <= 9:
            mixer.music.stop()
            win_music.play(-1)
            
        mx,my = mouse.get_pos()
        keys=key.get_pressed()
        screen.set_clip(Rect(0,0,1000,723))
            
        spawnEnemies()
        enemyMove()
        
        checkAction()
        advanceFrame()
        
        drawMap()
        drawEnemy()

        damageCalculation()
        drawHealth()
        
        myclock.tick(150)

        display.flip()

    return "quitgame"
def menu(page):
    mixer.music.load("stuff/sound/fairy tail intro.wav")
    win_music.stop()
    mixer.music.play(-1)
    running = True
    mouse.set_visible(False)
    back = image.load("stuff/pics/menu.png")
    buttons = [Rect(663,y*122+346,305,100) for y in range(3)]
    vals = ["game","instructions","credits"]
    while running:
        for evnt in event.get():
            if evnt.type == QUIT:
                return "exit"
            if evnt.type == KEYDOWN:
                if evnt.key == K_ESCAPE:
                    return "exit"

        mx,my = mouse.get_pos()
        mb = mouse.get_pressed()
        
        screen.blit(back,(0,0))
        for r,v in zip(buttons,vals):
            if r.collidepoint(mx,my):
                draw.rect(screen,(255,25,0),r,4)
                if mb[0]==1:
                    return v
        screen.blit(cursorpic,(mx-25,my-25))
                
        display.flip()
        
win_music = mixer.Sound("stuff/sound/Natsu theme.wav")

screen = display.set_mode((1000, 723))#,FULLSCREEN)
running = True
x,y = 0,0
OUTLINE = (150,50,30)
page = "menu"
while page != "exit":
    if page == "menu":
        page = menu(page)
    if page == "game":
        page = game(page)
    if page == "quitgame":
        page = quitgame(page)
    if page == "instructions":
        page = instructions(page)       
    if page == "credits":
        page = credit(page)    
    
quit()
