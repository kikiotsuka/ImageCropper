#!/usr/bin/python2
# -*- coding: utf-8 -*-

from __future__ import print_function
from time import sleep
import ctypes
import pygame
import sys
import os
import getpass
from pygame.locals import *
from PIL import Image
import glob
import pyreadline.rlmain
import readline

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

        If your image has a background color that is not white, hit F to
        fill the background of the entire image with the color of the pixel on the
        mouse

    Controls:
        WASD or arrowkeys to move the crop box or image around
        ENTER to confirm region/image location
        ESCAPE to cancel selection
        Q to quit the program without any changes
        M to toggle message
        Resize Mode only:
            SPACE to invert the color ofthe selection box
        Minimalistic Mode only:
            F to fill background with color at current mouse pixel
            Press and/or hold '+' or '-' to resize the image
                WARNING: Bigger image = more computation = heavy lag

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
def complete(text, state):
    return (glob.glob(text+'*')+[None])[state]


def cleanup():
    # deletes temporary images
    if os.path.isfile('tmpcopy.jpg'): os.remove('tmpcopy.jpg')
    if os.path.isfile('tmpresize.jpg'): os.remove('tmpresize.jpg')
    if os.path.isfile('scaleoutput.jpg'): os.remove('scaleoutput.jpg')
    pygame.quit()


def stop():
# exits program, called when user hits q or closes window
    print('\nNo more images or user requested exit')
    print('Exiting program')
    #pygame.quit()
    sys.exit()


def getuserinfo():
    global searchloc, f
    confirm = True
    while confirm:
        f = raw_input('Enter wallpaper location: ')
        print('Are you sure this is correct?')
        print('Wallpaper location: ' + str(f))
        if raw_input('"yes" or "no": ') == 'yes':
            confirm = False
    tmp = open('imageresizeruserinfo.txt', 'w')
    tmp.write(str(f) + '\n')
    tmp.write(str(tutorialtext) + '\n')
    tmp.close()

#gets all images lower than user's screen res
def getcandidates():
    onlyfiles = [ f2 for f2 in os.listdir(f) if os.path.isfile(os.path.join(f,f2)) ]
    try:
        for f2 in onlyfiles:
            #print(f2)
            if f2 in ('scaleoutput.jpg', 'tmpcopy.jpg', 'tmpresize.jpg'):
                continue
            if os.path.isfile(f2):
                img = Image.open(f2)
                if img.size[0] != userscreenwidth or img.size[1] != userscreenheight:
                    #print(str(f2) + ':' + str(img.size[0]) + ' x ' + str(img.size[1]))
                    todo.append(f2)
    except:
        pass
    del img

#initialize autocomplete
readline.set_completer_delims(' \t\n;')
readline.parse_and_bind("tab: complete")
readline.set_completer(complete)

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
    while not os.path.isdir(f):
        getuserinfo()
    os.chdir(f)
#os.chdir('C:/Users/Mitsuru/Desktop/testpapers') #FIXME========================================================== DEBUG CODE ==================================================
print('\n\nBASIC USAGE AND INSTRUCTIONS\n\n')
print('Arrow keys or WASD to move box or image around')
print('Enter to confirm')
print('M to toggle information message (DISABLED BY DEFAULT)')
print('Q to quit\n')
print('Resize Mode:')
print('    Space to invert box color (for dark pictures)')
print('Minimalistic Mode:')
print('    F then mouse over a pixel to color background the color at mouse location')
print('    Press and/or hold "+" or "-" to resize the image\n')
print('For detailed instructions on using this program, go to')
print('C:\\Users\\' + str(getpass.getuser()) + '\\imageresizeruserinfo.txt\\\n')

#Edits
#print('\n')
todo = []
getcandidates()
#print('\n')
#Edits

#imgname = raw_input('Image name:')
#resizemode = raw_input('Resize mode (y/n): ') == 'y'

# os.chdir('C:/Users/Mitsuru/Desktop/testpapers/')
resizemode = None
changed = False
while len(todo) > 0:
    pygame.init()
    fpsClock = pygame.time.Clock()
    #windowSurfaceObj = pygame.display.set_mode((int(userscreenwidth * scalesize), int(userscreenheight * scalesize)))
    pygame.display.set_caption('Resize and crop Image Program, By Mitsuru Otsuka')

    # attempt to open it, if failed exit program
    # backup image elsewhere in case of accidental failure

    imgname = todo[0]
    tmp = Image.open(imgname)
    scalealgorithm = Image.ANTIALIAS
    if tmp.size[0] < userscreenwidth and tmp.size[1] < userscreenheight:
        scalealgorithm = Image.BICUBIC

    if tmp.size in ((1024, 576), (1280, 720), (1366, 768), (1600, 900), (2048, 1152), (2560, 1440), (2880, 1620), (3840, 2160), (4096, 2304)):
        if userscreenwidth * 1.0 / tmp.size[0] * tmp.size[1] >= userscreenheight * 1.0:
            im2 = tmp.resize((userscreenwidth, int(userscreenwidth * 1.0 / tmp.size[0] * tmp.size[1])), scalealgorithm)
        else:
            im2 = tmp.resize((int(userscreenheight * 1.0 / tmp.size[1] * tmp.size[0]), userscreenheight), scalealgorithm)
        im2.save(imgname, 'JPEG', quality=90)
        del im2, tmp
        continue

    print(str(imgname) + ': ' + str(tmp.size[0]) + ' x ' + str(tmp.size[1]))
    del tmp
    if resizemode == None or not changed:
        resizemode = raw_input('Resize mode (y/n): ') == 'y'
    else:
        changed = False
    if os.path.isfile(imgname):
        if imgname[len(imgname) - 4:] == '.png':
            try:
                imtmp = Image.open(imgname)
                bg = Image.new("RGB", imtmp.size, (255,255,255))
                bg.paste(imtmp,imtmp)
                bg.save(str(imgname[:len(imgname) - 4]) + '.jpg', 'JPEG', quality=90)
                os.remove(imgname)
                imgname = str(imgname[:len(imgname) - 4]) + '.jpg'
                del bg, imtmp
            except:
                os.rename(imgname, str(imgname[:len(imgname) - 4]) + '.jpg')
                imgname = str(imgname[:len(imgname) - 4]) + '.jpg'
        Image.open(imgname).save('tmpcopy.jpg', 'JPEG', quality=90)
    elif os.path.isfile(str(imgname) + '.jpg'):
        imgname += '.jpg'
        Image.open(imgname).save('tmpcopy.jpg', 'JPEG', quality=90)
    elif os.path.isfile(str(imgname) + '.jpeg'):
        imgname += '.jpeg'
        Image.open(imgname).save('tmpcopy.jpg', 'JPEG', quality=90)
    elif os.path.isfile(str(imgname) + '.png'):
        try:
            imtmp = Image.open(str(imgname) + '.png')
            bg = Image.new("RGB", imtmp.size, (255,255,255))
            bg.paste(imtmp,imtmp)
            bg.save(str(imgname) + '.jpg', 'JPEG', quality=90)
            os.remove(imgname)
            imgname += '.jpg'
            del bg, imtmp
        except:
            pass
        os.rename(str(imgname) + '.png', str(imgname) + '.jpg')
        #imgname += '.png'
        Image.open(imgname).save('tmpcopy.jpg', 'JPEG', quality=90)
    else:
        print('File not found in')
        print(str(f))
        print('\n')
        continue
    if not os.path.isdir('wallpaperbackup'):
        os.makedirs('wallpaperbackup')
    Image.open(imgname).save('wallpaperbackup/1.jpg', 'JPEG', quality=90)
    im = Image.open('tmpcopy.jpg')
    # resize image for crop mode
    if resizemode:
        # size constant is (width, height) tuple
        # scalealgorithm makes the image look better after resizing
        vertical = True
        if userscreenwidth * 1.0 / im.size[0] * im.size[1] >= userscreenheight * 1.0:
            im2 = im.resize((userscreenwidth, int(userscreenwidth * 1.0 / im.size[0] * im.size[1])), scalealgorithm)
        else:
            im2 = im.resize((int(userscreenheight * 1.0 / im.size[1] * im.size[0]), userscreenheight), scalealgorithm)
            vertical = False
        im2.save('tmpresize.jpg', 'JPEG', quality=90)
        print(
            'Computing scaled image size. If image is large, operation may take a while')
        while im2.size[0] * scalesize >= userscreenwidth - 30:  # width too big
            scalesize -= 0.1
            #scalesize = (userscreenwidth * scalesize) / (im2.size[0] * scalesize) * scalesize
        while im2.size[1] * scalesize >= userscreenheight - 30:  # height too big
            scalesize -= 0.1
            #scalesize = (userscreenheight * scalesize) / (im2.size[1] * scalesize) * scalesize
        im2 = im2.resize((int(im2.size[0] * scalesize), int(im2.size[1] * scalesize)), scalealgorithm)
        im2.save('scaleoutput.jpg', 'JPEG', quality=90)

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
        #moveimg = pygame.image.load('tmpcopy.jpg')
        im.resize((int(im.size[0] * scalesize), int(im.size[1] * scalesize)), scalealgorithm).save('scaleoutput.jpg', 'JPEG', quality=90)
        moveimg = pygame.image.load('scaleoutput.jpg')
        moveimgdimension = moveimg.get_size()
        aspectratio = 1.0 * moveimgdimension[0] / moveimgdimension[1]

    isworking = True

    print('Initializing window')
    print('Preparing variables 1')
    # keylistener variables
    up = False
    down = False
    left = False
    right = False
    ask = False  # check user confirmation
    time = 0  # for picture acceleration
    movedist = 1
    currentcolor = pygame.Color(0, 0, 0)
    fillcolor = pygame.Color(255, 255, 255)
    fillmode = False
    resizeval = 0
    resizevalincrement = 1
    reallydelete=indeeddelete=False
    changemode=reallychangemode=False
    print('Variable 1 setup complete')
    print('Preparing variables 2')
    if resizemode:  # if picture is black, change item to white so box is viewable
        white = False
    else:  # minimalistic picture view mode
        xloc = (userscreenwidth * scalesize) - moveimg.get_size()[0] - 10
        yloc = (userscreenheight * scalesize) - moveimg.get_size()[1] - 10
        mousex=mousey=0
        plus = False
        minus = False
        sizetime = 0
        keepresizing = False
        k1=k2=k3=k4=k5=k6=k7=k8=k9=False
        leftpos = 0
        toppos = 0
        rightpos = (userscreenwidth * scalesize) - moveimg.get_size()[0]
        midxpos = (userscreenwidth * scalesize) / 2 - moveimg.get_size()[0] / 2
        bottompos = (userscreenheight * scalesize) - moveimg.get_size()[1]
        midypos = (userscreenheight * scalesize) / 2 - moveimg.get_size()[1] / 2
    print('Variables setup')
    print('Starting image manipulation')
    while isworking:
        windowSurfaceObj.fill(fillcolor)
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
        if left and not ask and not reallydelete:
            if resizemode:
                if rectangle.left > 0:
                    rectangle.x -= movedist
            else:
                if xloc + moveimg.get_size()[0] > 0:
                    xloc -= movedist
        if right and not ask and not reallydelete:
            if resizemode:
                if rectangle.right < windowSurfaceObj.get_size()[0]:
                    rectangle.x += movedist
            else:
                if xloc < windowSurfaceObj.get_size()[0]:
                    xloc += movedist
        if down and not ask and not reallydelete:
            if resizemode:
                if rectangle.bottom < windowSurfaceObj.get_size()[1]:
                    rectangle.y += movedist
            else:
                if yloc < windowSurfaceObj.get_size()[1]:
                    yloc += movedist
        if up and not ask and not reallydelete:
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
        if fillmode:
            fillcolor = windowSurfaceObj.get_at((mousex, mousey))
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
                elif event.key == K_f:
                    if fillmode:
                        fillmode = False
                        fillcolor = pygame.Color(255, 255, 255)
                    else:
                        fillmode = True
                        mousex, mousey = pygame.mouse.get_pos()
                elif event.key == K_c:
                    if not changemode:
                        changemode = True
                    else:
                        reallychangemode = True
                elif event.key in (K_EQUALS, K_MINUS):
                    if event.key == K_EQUALS:
                        resizeval += 1
                        plus = True
                    elif event.key == K_MINUS:
                        resizeval -= 1
                        minus = True
                    sizetime = 0
                    tmpim = Image.open('tmpcopy.jpg')
                    tmpx = int((tmpim.size[0] + resizeval) * scalesize)
                    tmpy = int(tmpx / aspectratio)
                    tmpim.resize((tmpx, tmpy), scalealgorithm).save('scaleoutput.jpg', 'JPEG', quality=90)
                    moveimg = pygame.image.load('scaleoutput.jpg')
                    del tmpim, tmpx, tmpy
                elif event.key == K_SPACE:
                    if resizemode:
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
                elif event.key in (K_1, K_KP5):
                    if vertical:
                        rectangle = Rect((0, int((windowSurfaceObj.get_size()[1] - userscreenheight * scalesize) / 2)),
                            (int(userscreenwidth * scalesize), int(userscreenheight * scalesize)))
                    else:
                        rectangle = Rect(
                            (int((windowSurfaceObj.get_size()
                             [0] - userscreenwidth * scalesize) / 2), 0),
                            (int(userscreenwidth * scalesize), int(userscreenheight * scalesize)))
                elif not resizemode and event.key in (K_KP1, K_KP2, K_KP3, K_KP4, K_KP5, K_KP6, K_KP7, K_KP8, K_KP9):
                    if event.key == K_KP1: k1 = True
                    elif event.key == K_KP2: k2 = True
                    elif event.key == K_KP3: k3 = True
                    elif event.key == K_KP4: k4 = True
                    elif event.key == K_KP5: k5 = True
                    elif event.key == K_KP6: k6 = True
                    elif event.key == K_KP7: k7 = True
                    elif event.key == K_KP8: k8 = True
                    elif event.key == K_KP9: k9 = True
                elif event.key == K_KP0:
                    yloc = 0
                    tmpim = Image.open('tmpcopy.jpg')
                    tmpx = int((tmpim.size[0] * scalesize + resizeval * scalesize))
                    tmpy = int(tmpx / aspectratio)
                    if tmpy > scalesize * userscreenheight:
                        while tmpy >= scalesize * userscreenheight:
                            resizeval += -1
                            tmpx = int((tmpim.size[0] * scalesize + resizeval * scalesize))
                            tmpy = int(tmpx / aspectratio)
                    else:
                        while tmpy <= scalesize * userscreenheight:
                            resizeval += 1
                            tmpx = int((tmpim.size[0] * scalesize + resizeval * scalesize))
                            tmpy = int(tmpx / aspectratio)
                    tmpim.resize((tmpx, tmpy), scalealgorithm).save('scaleoutput.jpg', 'JPEG', quality=90)
                    moveimg = pygame.image.load('scaleoutput.jpg')
                    del tmpim, tmpx, tmpy
                elif event.key == K_ESCAPE:
                    ask = False
                    reallydelete = False
                    indeeddelete = False
                    changemode = False
                    reallychangemode = False
                elif event.key == K_DELETE:
                    if reallydelete:
                        indeeddelete = True
                    else:
                        reallydelete = True
            elif event.type == KEYUP:
                if event.key in (K_LEFT, K_a):
                    left = False
                elif event.key in (K_RIGHT, K_d):
                    right = False
                elif event.key in (K_UP, K_w):
                    up = False
                elif event.key in (K_DOWN, K_s):
                    down = False
                elif event.key in (K_EQUALS, K_MINUS):
                    if event.key == K_EQUALS:
                        plus = False
                    elif event.key == K_MINUS:
                        minus = False
                elif event.key in (K_KP1, K_KP2, K_KP3, K_KP4, K_KP5, K_KP6, K_KP7, K_KP8, K_KP9):
                    if event.key == K_KP1: k1 = False
                    elif event.key == K_KP2: k2 = False
                    elif event.key == K_KP3: k3 = False
                    elif event.key == K_KP4: k4 = False
                    elif event.key == K_KP5: k5 = False
                    elif event.key == K_KP6: k6 = False
                    elif event.key == K_KP7: k7 = False
                    elif event.key == K_KP8: k8 = False
                    elif event.key == K_KP9: k9 = False
                if not left and not right and not up and not down:
                    time = 0
            elif event.type == MOUSEMOTION and fillmode:
                mousex, mousey = event.pos
        if not resizemode:
            #print('resizevalincrement:' + str(resizevalincrement) + ', time:' + str(sizetime))
            if plus or minus:
                sizetime += 30
                keepresizing = True
            else:
                keepresizing = False
            if sizetime < 500 and (plus or minus):
                resizevalincrement = 1
            elif sizetime < 750 and (plus or minus):
                resizevalincrement = 2
            elif sizetime < 1000 and (plus or minus):
                resizevalincrement = 3
            elif sizetime < 1500 and (plus or minus):
                resizevalincrement = 5
            if keepresizing:
                if plus:
                    resizeval += resizevalincrement
                elif minus:
                    resizeval -= resizevalincrement
                tmpim = Image.open('tmpcopy.jpg')
                tmpx = int((tmpim.size[0] * scalesize + resizeval * scalesize))
                tmpy = int(tmpx / aspectratio)
                tmpim.resize((tmpx, tmpy), scalealgorithm).save('scaleoutput.jpg', 'JPEG', quality=90)
                moveimg = pygame.image.load('scaleoutput.jpg')
                del tmpim, tmpx, tmpy
        if not resizemode:
            rightpos = (userscreenwidth * scalesize) - moveimg.get_size()[0]
            midxpos = (userscreenwidth * scalesize) / 2 - moveimg.get_size()[0] / 2
            bottompos = (userscreenheight * scalesize) - moveimg.get_size()[1]
            midypos = (userscreenheight * scalesize) / 2 - moveimg.get_size()[1] / 2
            if k1 or k4 or k7: xloc = leftpos
            if k2 or k5 or k8: xloc = midxpos
            if k3 or k6 or k9: xloc = rightpos
            if k1 or k2 or k3: yloc = bottompos
            if k4 or k5 or k6: yloc = midypos
            if k7 or k8 or k9: yloc = toppos
        if indeeddelete:
            break
        if reallydelete:
            box = Rect(0, 0, 50, 50)
            box.center = ((userscreenwidth * scalesize) / 2, (userscreenheight * scalesize) / 2)
            box2 = Rect(0, 0, 25, 25)
            box2.center = box.center
            pygame.draw.rect(windowSurfaceObj, currentcolor, box, 0)
            pygame.draw.rect(windowSurfaceObj, pygame.Color(255, 0, 0), box2, 0)
        if reallychangemode:
            resizemode = not resizemode
            changed = True
            break
        pygame.display.update()
        time += 30
        fpsClock.tick(30)
        """
        if not ask and not isworking and not resizemode:
            windowSurfaceObj.fill(pygame.Color(255, 255, 255))
            windowSurfaceObj.blit(moveimg, (xloc, yloc))
            pygame.image.save(windowSurfaceObj, imgname)
        """
    if reallychangemode:
        cleanup()
        print('\n')
        continue
    if indeeddelete:
        try:
            del im
        except:
            pass
        if resizemode:
            del im2
        print(imgname + ' has been deleted\n')
        cleanup()
        os.remove(imgname)
        continue
    # crop selected region from picture
    if resizemode:
        im = im2.crop((rectangle.left, rectangle.top, rectangle.right, rectangle.bottom))
        #im = im2.crop((rectangle.x, rectangle.y, rectangle.x + rectangle.width, rectangle.y + rectangle.height))
        im.resize((int(1.0 * im.size[0] / scalesize), int(1.0 * im.size[1] / scalesize)),scalealgorithm).save(imgname, 'JPEG', quality=90)
        del im2
    else:
        im = Image.open('tmpcopy.jpg')
        tmpx = int(im.size[0] + resizeval)
        tmpy = int(tmpx / aspectratio)
        if tmpx != im.size[0] or tmpy != im.size[1]:
            print('Image has been resized to ' + str(tmpx) + ' x ' + str(tmpy))
            if resizeval < 0:
                im = im.resize((tmpx, tmpy), Image.ANTIALIAS)
            else:
                im = im.resize((tmpx, tmpy), Image.BICUBIC)
        #im.resize((int((im.size[0] + resizeval)), int(im.size[1] + resizeval)), scalealgorithm)
        imtmpcreate = Image.new("RGB", (userscreenwidth, userscreenheight), (fillcolor[0], fillcolor[1], fillcolor[2]))
        xloc = int(xloc / scalesize)
        yloc = int(yloc / scalesize)
        imtmpcreate.paste(im, (xloc, yloc))
        imtmpcreate.save(imgname, 'JPEG', quality=90)

        #im = Image.open(imgname)
    # scale picture back to user resolution and save
    del im
    print('Operation has been completed. The altered image has been saved as "' +
          str(imgname) + '"')
    print('A backup of the original image is located in')
    #print(str(f[:f[:len(f) - 1].rfind('/') + 1]) + 'wallpaperbackup/')
    print(str(f) + 'wallpaperbackup/')
    cleanup()
    print('\n')
    todo.pop(0)
stop()
