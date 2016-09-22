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

mixer.music.load("stuff/sound/Fiesta(FairyTail - OP6).mp3")
##mixer.music.play(-1)
        
##==================================pictures==================================##

bkgd = image.load("stuff/pics/map.png")
cursorpic = image.load("stuff/pics/cursor.png")
bhealth = image.load("stuff/pics/base health.png")
health = image.load("stuff/pics/health.png")
mana = image.load("stuff/pics/mana.png")
htemp = image.load("stuff/pics/health template.png")

health_pics = [bhealth,health,mana,htemp]

##############################loading done######################################

################################Enemy Programming###############################

##-------------------------enemy information----------------------------------##

spawnLocation = [0,400,600,800,1000,1400,1700,1900]
timewait=0
enemies=[[choice(spawnLocation),497,10,None,0,"Walk_Right",0,"Right",True]]
action_pick_delay = 0
        
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
##    win_music = mixer.Sound("stuff/sound/Natsu theme.wav")
    screen = display.set_mode((1000,723))#,FULLSCREEN)
    running = True
    mouse.set_visible(False)
    myclock = time.Clock()
    global comboAction
    global houkou_move
    global houkou_frame
    global flag_houkou 
    while running:
        for evt in event.get():
            if evt.type == KEYDOWN:
                if evt.key == K_ESCAPE:
                    running = False
            if evt.type == KEYUP:
                if evt.key == K_h:
                    houkou_move = "FlameEnd"
                    
        mx,my = mouse.get_pos()
        keys=key.get_pressed()
        screen.set_clip(Rect(0,0,1000,723))
        if keys[K_SPACE]:
            mixer.music.stop()
            win_music.play(-1)

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
 
screen = display.set_mode((1000, 723))
running = True
x,y = 0,0
OUTLINE = (150,50,30)
page = "menu"

win_music = mixer.Sound("stuff/sound/Natsu theme.wav")

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
