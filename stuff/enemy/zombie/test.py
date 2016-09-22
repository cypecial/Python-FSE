import glob
from pygame import *

screen=display.set_mode((800,800))
running = True

while running:
    for evt in event.get():
        if evt.type==QUIT:
            running=False
                
    for i in range(12):
        screen.fill((0,0,0))
        pic=image.load("Zombie_Die %s.png" % (i))
        screen.blit(pic,(400,400))
        time.wait(150)
        display.flip()
quit()
