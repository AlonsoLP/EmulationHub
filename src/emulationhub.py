#!/usr/bin/python

import pygame, math, sys, subprocess
from pygame.locals import *
from pygame import Surface, draw, transform
from subprocess import check_output

pygame.init()
myfont = pygame.font.Font('Roboto-Regular.ttf', 42)

listado = subprocess.check_output('xrandr').split()
resolucion = [int(s) for s in listado[listado.index('primary') + 1].replace('+','x').split('x') if s.isdigit()]
screen = pygame.display.set_mode((resolucion[0],resolucion[1]),pygame.NOFRAME)

#
#
#########################################################################


def grayscale_image(surf): 
    width, height = surf.get_size() 
    for x in range(width): 
	for y in range(height): 
    	    red, green, blue, alpha = surf.get_at((x, y)) 
    	    L = 0.3 * red + 0.59 * green + 0.11 * blue 
    	    gs_color = (L, L, L, alpha) 
    	    surf.set_at((x, y), gs_color) 
    return surf 


class Emulator:

    def __init__(self, name, image, command = ''):
	self.name = str(name)
	self.x = self.y = 0
        self.image = pygame.image.load(str(image))
	self.width = self.image.get_width()
	self.height = self.image.get_height()
	self.scale = 0.6
	self.image_smoothscale = pygame.transform.scale(grayscale_image(self.image), (int(self.width*self.scale),int(self.height*self.scale)))
	self.visible = 1
	self.command = str(command)
	self.games = 0


    def set_name(self, name):
	self.name = str(name)
    def get_name(self):
	return(self.name)

    def set_command(self, command):
	self.command = str(command)
    def get_command(self):
	return(self.command)

    def set_games(self, games):
	self.games = int(games)
    def get_games(self):
	return(self.games)

    def set_position(self, (x,y)):
        self.x = int(x)
        self.y = int(y)
    def get_position(self):
        return(self.x, self.y)

    def get_height(self, scale = 0):
	if (scale == 0): factor = 1
	else: factor = self.scale
        return(int(self.height*factor))
    def get_width(self, scale = 0):
	if (scale == 0): factor = 1
	else: factor = self.scale
        return(int(self.width*factor))

    def set_scale(self, scale):
	if (self.scale != scale):
    	    self.scale = float(scale)
	    self.image_smoothscale = pygame.transform.scale(grayscale_image(self.image), (int(self.image.get_width()*scale),int(self.image.get_height()*scale)))
    def get_scale(self):
        return(self.scale)

    def set_visible(self, visible):
        self.visible = int(visible)
    def get_visible(self):
        return(self.visible)

    def draw(self, screen, scale = 0):
        if ((self.x<=resolucion[0]) & (self.x>=-self.get_width(scale))):
	    if (scale == 0):
		screen.blit(self.image, (self.x, self.y))
	    elif (scale == 1):
		screen.blit(self.image_smoothscale, (self.x, self.y))

# self.oranges = []
# for x in range(10):
#     self.oranges.append(SpriteOrange('orange.png'))
# for o in self.oranges:
#     o.update()
# for o in self.oranges:
#     o.draw(self.screen)


def AAfilledRoundedRect(surface,rect,color,radius=0.4):

    """
    AAfilledRoundedRect(surface,rect,color,radius=0.4)

    surface : destination
    rect    : rectangle
    color   : rgb or rgba
    radius  : 0 <= radius <= 1
    """

    rect         = Rect(rect)
    color        = Color(*color)
    alpha        = color.a
    color.a      = 0
    pos          = rect.topleft
    rect.topleft = 0,0
    rectangle    = Surface(rect.size,SRCALPHA)

    circle       = Surface([min(rect.size)*3]*2,SRCALPHA)
    draw.ellipse(circle,(0,0,0),circle.get_rect(),0)
    circle       = transform.smoothscale(circle,[int(min(rect.size)*radius)]*2)

    radius              = rectangle.blit(circle,(0,0))
    radius.bottomright  = rect.bottomright
    rectangle.blit(circle,radius)
    radius.topright     = rect.topright
    rectangle.blit(circle,radius)
    radius.bottomleft   = rect.bottomleft
    rectangle.blit(circle,radius)

    rectangle.fill((0,0,0),rect.inflate(-radius.w,0))
    rectangle.fill((0,0,0),rect.inflate(0,-radius.h))

    rectangle.fill(color,special_flags=BLEND_RGBA_MAX)
    rectangle.fill((255,255,255,alpha),special_flags=BLEND_RGBA_MIN)

    return surface.blit(rectangle,pos)



#
#
#########################################################################

background = pygame.image.load('wallpaper-3.jpg')
background = pygame.transform.scale(background, (resolucion[0],resolucion[1]))
pygame.draw.rect(background,(255,255,255),(0,(resolucion[1]/2)-130,resolucion[0],260))
pygame.draw.rect(background,(63,63,63),(0,(resolucion[1]/2)-135,resolucion[0],5))
pygame.draw.rect(background,(63,63,63),(0,(resolucion[1]/2)+130,resolucion[0],5))

amiga = Emulator('Amiga','amiga.png','/opt/bin/amiga-emulator')
atari2600 = Emulator('Atari 2600','atari2600.png','/opt/bin/atari2600-emulator')
gb = Emulator('GameBoy','gb.png','/opt/bin/gameboy-emulator')

clock = pygame.time.Clock()
direccion = 0
BLACK = (0,0,0)
x = 0
distancia = 2
aceleracion = 64
factor = 1.8

while 1:
    # USER INPUT
    clock.tick(30)
    for event in pygame.event.get():
        if not hasattr(event, 'key'): continue
        down = event.type == KEYDOWN     # key down or up?
        if event.key == K_RIGHT: direccion = 1
        elif event.key == K_LEFT: direccion = 2
        elif event.key == K_ESCAPE: sys.exit(0)     # quit the game
    screen.fill(BLACK)

    if (direccion == 1) : # DER
	if ((x > 5*(resolucion[0]/6)) & (aceleracion>16/factor)): aceleracion /= factor
	x += distancia*aceleracion
    elif (direccion == 2) : # IZQ
	if ((x <= resolucion[0]/6) & (aceleracion>16/factor)) : aceleracion /= factor
	x -= distancia*aceleracion

    if ((x <= 0) | (x >= resolucion[0])) :
	direccion = 0
	distancia = 2
	aceleracion = 64

    screen.blit(background, (0,0))

    label1 = myfont.render("X: "+str(amiga.get_position()), 1, (255,63,63))
    label2 = myfont.render("A: "+str(aceleracion), 1, (255,63,63))
    label3 = myfont.render("Res: "+str((resolucion[0],resolucion[1])), 1, (255,63,63))
    screen.blit(label3, (100, 50))
    screen.blit(label1, (100, 100))
    screen.blit(label2, (100, 150))

#    AAfilledRoundedRect(screen,((resolucion[0]/2)-150,800,300,60),(63,63,63),1)

    help_middle = pygame.Surface((resolucion[0],55), pygame.SRCALPHA)
    help_middle.fill((255,255,255,128))
    screen.blit(help_middle, (0,(resolucion[1]/2)+135))

    label4 = myfont.render("34589 GAMES AVAILABLE", 1, (63,63,63))
    label4pos = label4.get_rect()
    label4pos.centerx = background.get_rect().centerx
    label4pos.centery = (resolucion[1]/2)+163
    screen.blit(label4, label4pos)

#    help_down = pygame.Surface((resolucion[0],100), pygame.SRCALPHA)
#    help_down.fill((255,255,255,128))                         # notice the alpha value in the color
#    screen.blit(help_down, (0,resolucion[1]-100))

    # IZQ
    amiga.set_position((x,(resolucion[1]/2)-(amiga.get_height(1)/2)))
    amiga.draw(screen,1)
    # CENTRO
    gb.set_position((x+(resolucion[0]/2)-(gb.get_width(0)/2),(resolucion[1]/2)-(gb.get_height()/2)))
    gb.draw(screen,0)
    # DER
    atari2600.set_position((x+resolucion[0]-atari2600.get_width(1),(resolucion[1]/2)-(atari2600.get_height(1)/2)))
    atari2600.draw(screen,1)
    # NUEVO

    pygame.display.flip()




