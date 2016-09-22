from pygame import *

screen = display.set_mode((800,600))
pic = image.load("stuff/pics/submap.png")
running = True
guy=[0,0,True]
VY = 3

picture = image.load("stuff/pics/map.png")

while running:
    for evnt in event.get():               
        if evnt.type == QUIT:
            running = False
    mx, my = mouse.get_pos()
    keys = key.get_pressed()
    
    playerRect = Rect(guy[0],guy[1],30,30)

    if keys[K_a]:
        guy[0] -=5
    if keys[K_d]:
        guy[0] +=5
    if keys[K_SPACE]:
        if guy[2] == True:
            guy[1] -= 80
    if guy[2] == False:
        guy[1] += VY
    screen.fill((0,0,0))
    screen.blit(pic,(0,0))
    if pic.get_at((mx,my))[3] == 0:
        print "True"
    else: print "False"
    if pic.get_at((guy[0]+15,guy[1]+30))[3]==0:
        guy[2] = False
    else: guy[2] = True
    
##    screen.blit(picture,(0,0))
    draw.rect(screen,(0,255,0),playerRect)

    display.flip()
                  
    
quit()
