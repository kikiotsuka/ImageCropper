#!/usr/bin/python2
# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals
from time import sleep
import ctypes
import pygame
import sys
import os
import getpass
import Tkinter
import tkFileDialog
from pygame.locals import *
from PIL import Image

"""
If you want to use this program for your own purposes, read here

Things you must install to make this work
	- Python 2.7
		http://www.python.org/getit/
	- Pillow
		http://www.lfd.uci.edu/~gohlke/pythonlibs/#pillow
	- Pygame for Python 2.7
		http://www.lfd.uci.edu/~gohlke/pythonlibs/#pygame
	The above links are for windows users
"""
tutorialtext = """
Using the program
	This program has 2 modes
	Resize-and-crop mode:
		This mode will first resize your image to a size suitable for your
		screen, then go into crop mode, where you can crop a portion of
		the image to use as a wallpaper
	Minimalistic mode:
		This mode is for if you have a small image, such as 500px by 500px,
		and you want it as a wallpaper. The general idea is that the small
		image will be placed in the right bottom corner (by default) and create
		a simple minimalistic wallpaper

	Controls:
		WASD or arrowkeys to move the crop box or image around
		ENTER to confirm region/image location
		ESCAPE to cancel selection
		Q to quit the program without any changes
        SPACE to invert the color ofthe selection box

	Inputs:
        The first time you start this program, it will ask where you wallpapers
        are. Select the folder containing them, and hit ok.

		First you will be asked to give the name of the image to crop
		As long as the wallpaper extensions are {'.jpg', '.jpeg', '.png'}
		you do not need to include the extension. However, if there are multiple
		files with the same name but different extension, you must include the
		extension to select the correct image, otherwise it will attempt to find
		the image with the extensions listed above in that order

		Next, you will be asked to use resize mode
			Type in 'y' for resize mode, and anything else for minimalistic mode

	Note:
		After finishing cropping/exiting the program, there will be a 4 second pause
		Please do not confuse this with a bug or lag, this is a feature if the user
		needs to read error messages on the console
"""

if sys.version_info[0] == 3:
    raw_input = input

def cleanup():
    # deletes temporary images
    if os.path.isfile('tmpcopy.jpg'): os.remove('tmpcopy.jpg')
    if os.path.isfile('tmpresize.jpg'): os.remove('tmpresize.jpg')
    if os.path.isfile('scaleoutput.jpg'): os.remove('scaleoutput.jpg')


def stop():
# exits program, called when user hits q or closes window
    print('Exiting program')
    pygame.quit()
    sleep(4)
    sys.exit()


def getuserinfo():
    global searchloc, f
    confirm = True
    root = Tkinter.Tk()
    root.withdraw()
    dir_opt = options = {}
    options['title'] = 'Select the folder containing your wallpapers'
    f = tkFileDialog.askdirectory(**dir_opt)
    tmp = open('imageresizeruserinfo.txt', 'w')
    tmp.write(str(f) + '\n')
    tmp.write(str(tutorialtext) + '\n')
    tmp.close()

#===variable constants===
# scale size for cropping
scalesize = .75
searchloc = 'C:/Users/' + str(getpass.getuser()) + '/'
user32 = ctypes.windll.user32
userscreenwidth = user32.GetSystemMetrics(0)
userscreenheight = user32.GetSystemMetrics(1)
if os.path.isdir(searchloc):
    os.chdir(searchloc)
    if os.path.isfile('imageresizeruserinfo.txt'):
        try:
            tmp = open('imageresizeruserinfo.txt', 'r')
            f = tmp.readline().rstrip('\n')
            tmp.close()
        except:
            getuserinfo()
    else:
        getuserinfo()
else:
    print('Fatal error: Cannot find path')
    print(searchloc)
    print('Please contact Mitsuru for further assistance')
    cleanup()
    stop()
"""
# user screen's resoltuion
# path to user wallpapers/images
f = 'C:/Users/Mitsuru/Desktop/Wallpapers/'
"""

# ask image name, resize mode or minimalistic mode
if os.path.isdir(f):
    os.chdir(f)
else:
    getuserinfo()
    os.chdir(f)
print('For instructions on using this program, go to')
print('C:\\Users\\' + str(getpass.getuser()) + '\\imageresizeruserinfo.txt\\')
imgname = raw_input('File name:')
resizemode = raw_input('Resize mode (y/n): ') == 'y'
# os.chdir('C:/Users/Mitsuru/Desktop/testpapers/')
pygame.init()
fpsClock = pygame.time.Clock()
#windowSurfaceObj = pygame.display.set_mode((int(userscreenwidth * scalesize), int(userscreenheight * scalesize)))
pygame.display.set_caption('Resize and crop Image Program, By Mitsuru Otsuka')

# attempt to open it, if failed exit program
# backup image elsewhere in case of accidental failure

if os.path.isfile(imgname):
    Image.open(imgname).save('tmpcopy.jpg')
elif os.path.isfile(str(imgname) + '.jpg'):
    imgname += '.jpg'
    Image.open(imgname).save('tmpcopy.jpg')
elif os.path.isfile(str(imgname) + '.jpeg'):
    imgname += '.jpeg'
    Image.open(imgname).save('tmpcopy.jpg')
elif os.path.isfile(str(imgname) + '.png'):
    imgname += '.png'
    Image.open(imgname).save('tmpcopy.jpg')
else:
    print('File not found in')
    print(str(f))
    cleanup()
    stop()
if not os.path.isdir('wallpaperbackup'):
    os.makedirs('wallpaperbackup')
Image.open(imgname).save('wallpaperbackup/1.jpg')
im = Image.open('tmpcopy.jpg')
# resize image for crop mode
if resizemode:
    # size constant is (width, height) tuple
    # Image.ANTIALIAS makes the image look better after resizing
    vertical = True
    if userscreenwidth * 1.0 / im.size[0] * im.size[1] >= userscreenheight * 1.0:
        im2 = im.resize(
            (userscreenwidth, int(userscreenwidth * 1.0 / im.size[0] * im.size[1])), Image.ANTIALIAS)
    else:
        im2 = im.resize(
            (int(userscreenheight * 1.0 / im.size[1] * im.size[0]), userscreenheight), Image.ANTIALIAS)
        vertical = False
    im2.save('tmpresize.jpg')
    print(
        'Computing scaled image size. If image is large, operation may take a while')
    while im2.size[0] * scalesize >= userscreenwidth - 30:  # width too big
        scalesize -= 0.1
        #scalesize = (userscreenwidth * scalesize) / (im2.size[0] * scalesize) * scalesize
    while im2.size[1] * scalesize >= userscreenheight - 30:  # height too big
        scalesize -= 0.1
        #scalesize = (userscreenheight * scalesize) / (im2.size[1] * scalesize) * scalesize
    im2 = im2.resize(
        (int(im2.size[0] * scalesize), int(im2.size[1] * scalesize)), Image.ANTIALIAS)
    im2.save('scaleoutput.jpg')

    os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (
        int((userscreenwidth - im2.size[0]) / 2), int((userscreenheight - im2.size[1]) / 2))
    windowSurfaceObj = pygame.display.set_mode(
        (int(im2.size[0]), int(im2.size[1])))
    resizedimg = pygame.image.load('scaleoutput.jpg')
    if vertical:
        rectangle = Rect(
            (0, int((windowSurfaceObj.get_size()[1] - userscreenheight * scalesize) / 2)),
            (int(userscreenwidth * scalesize), int(userscreenheight * scalesize)))
    else:
        rectangle = Rect(
            (int((windowSurfaceObj.get_size()
             [0] - userscreenwidth * scalesize) / 2), 0),
            (int(userscreenwidth * scalesize), int(userscreenheight * scalesize)))
else:  # simply load image for minimalistic mode
    os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (
        int((userscreenwidth - userscreenwidth * scalesize) / 2), int((userscreenheight - userscreenheight * scalesize) / 2))
    windowSurfaceObj = pygame.display.set_mode(
        (int(userscreenwidth * scalesize), int(userscreenheight * scalesize)))
    moveimg = pygame.image.load('tmpcopy.jpg')
isworking = True

print('Initializing window')
# keylistener variables
up = False
down = False
left = False
right = False
ask = False  # check user confirmation
fontObj = pygame.font.Font('freesansbold.ttf', 14)
msg = 'Press ENTER again to confirm, ESCAPE to cancel'
time = 0  # for picture acceleration
movedist = 1
currentcolor = pygame.Color(0, 0, 0)
if resizemode:  # if picture is black, change item to white so box is viewable
    white = False
else:  # minimalistic picture view mode
    xloc = (userscreenwidth * scalesize) - moveimg.get_size()[0] - 10
    yloc = (userscreenheight * scalesize) - moveimg.get_size()[1] - 10
while isworking:
    windowSurfaceObj.fill(pygame.Color(255, 255, 255))
    if resizemode:
        windowSurfaceObj.blit(resizedimg, (0, 0))
        pygame.draw.rect(windowSurfaceObj, currentcolor, rectangle, 1)
        if ask:
            if vertical:
                pygame.draw.rect(windowSurfaceObj, currentcolor,
                                 (0, 0, rectangle.width, rectangle.top), 0)
                pygame.draw.rect(windowSurfaceObj, currentcolor,
                    (rectangle.left, rectangle.bottom, rectangle.width, windowSurfaceObj.get_size()[1] - rectangle.top), 0)
            else:
                pygame.draw.rect(windowSurfaceObj, currentcolor,
                                 (0, 0, rectangle.left, rectangle.height))
                pygame.draw.rect(windowSurfaceObj, currentcolor,
                    (rectangle.right, rectangle.top, windowSurfaceObj.get_size()[0] - rectangle.right, rectangle.height), 0)
    else:  # not resize mode
        windowSurfaceObj.blit(moveimg, (xloc, yloc))
    if left and not ask:
        if resizemode:
            if rectangle.left > 0:
                rectangle.x -= movedist
        else:
            if xloc + moveimg.get_size()[0] > 0:
                xloc -= movedist
    if right and not ask:
        if resizemode:
            if rectangle.right < windowSurfaceObj.get_size()[0]:
                rectangle.x += movedist
        else:
            if xloc < windowSurfaceObj.get_size()[0]:
                xloc += movedist
    if down and not ask:
        if resizemode:
            if rectangle.bottom < windowSurfaceObj.get_size()[1]:
                rectangle.y += movedist
        else:
            if yloc < windowSurfaceObj.get_size()[1]:
                yloc += movedist
    if up and not ask:
        if resizemode:
            rectangle.y -= movedist
        else:
            if yloc + moveimg.get_size()[1] > 0:
                yloc -= movedist
    if time < 1000:
        movedist = 1
    elif time < 2000:
        movedist = 2
    else:
        movedist = 4
    if resizemode:  # check if it went out of bounds
        if rectangle.left < 0:
            rectangle.left = 0
        if rectangle.top < 0:
            rectangle.top = 0
        if rectangle.bottom > windowSurfaceObj.get_size()[1]:
            rectangle.bottom = windowSurfaceObj.get_size()[1]
        if rectangle.right > windowSurfaceObj.get_size()[0]:
            rectangle.right = windowSurfaceObj.get_size()[0]
    if ask:  # ask image confirmation question
        msgSurfaceObj = fontObj.render(msg, False, pygame.Color(255, 0, 0))
        msgRectobj = msgSurfaceObj.get_rect()
        msgRectobj.topleft = (5, 5)
        pygame.draw.rect(windowSurfaceObj, currentcolor,
            (msgRectobj.left - 2, msgRectobj.top - 2, msgRectobj.width + 2, msgRectobj.height + 2), 0)
        windowSurfaceObj.blit(msgSurfaceObj, msgRectobj)
    for event in pygame.event.get():
        if event.type == QUIT:
            del im
            if resizemode:
                del im2
            cleanup()
            stop()
        elif event.type == KEYDOWN:
            if event.key in (K_LEFT, K_a):
                left = True
            elif event.key in (K_RIGHT, K_d):
                right = True
            elif event.key in (K_DOWN, K_s):
                down = True
            elif event.key in (K_UP, K_w):
                up = True
            elif event.key == K_q:
                del im
                if resizemode:
                    del im2
                cleanup()
                stop()
            elif event.key == K_SPACE:
                if white:
                    currentcolor = pygame.Color(0, 0, 0)
                else:
                    currentcolor = pygame.Color(255, 255, 255)
                white = not white
            elif event.key == K_RETURN:
                if ask:
                    ask = False
                    isworking = False
                else:
                    ask = True
            elif event.key == K_ESCAPE:
                ask = False
        elif event.type == KEYUP:
            if event.key in (K_LEFT, K_a):
                left = False
            elif event.key in (K_RIGHT, K_d):
                right = False
            elif event.key in (K_UP, K_w):
                up = False
            elif event.key in (K_DOWN, K_s):
                down = False
            if not left and not right and not up and not down:
                time = 0
    pygame.display.update()
    time += 30
    fpsClock.tick(30)
    if not ask and not isworking and not resizemode:
        windowSurfaceObj.fill(pygame.Color(255, 255, 255))
        windowSurfaceObj.blit(moveimg, (xloc, yloc))
        pygame.image.save(windowSurfaceObj, imgname)

# crop selected region from picture
if resizemode:
    im = im2.crop(
        (rectangle.left, rectangle.top, rectangle.right, rectangle.bottom))
    #im = im2.crop((rectangle.x, rectangle.y, rectangle.x + rectangle.width, rectangle.y + rectangle.height))
    del im2
else:
    im = Image.open(imgname)
# scale picture back to user resolution and save
im.resize(
    (int(1.0 * im.size[0] / scalesize), int(1.0 * im.size[1] / scalesize)),
    Image.ANTIALIAS).save(imgname)
del im
print('Operation has been completed. The altered image has been saved as "' +
      str(imgname) + '"')
print('A backup of the original image is located in')
#print(str(f[:f[:len(f) - 1].rfind('/') + 1]) + 'wallpaperbackup/')
print(str(f) + 'wallpaperbackup/')
cleanup()
stop()
