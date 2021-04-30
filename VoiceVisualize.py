import pygame
import sys
import random
from pygame.locals import *
import pyaudio
import numpy as np
import win32api
import win32con
import win32gui

import os
#def initialize():
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (1501,716)
pygame.init()
screen = pygame.display.set_mode((400, 400),pygame.NOFRAME)
fuchsia = (255, 0, 128)
hwnd = pygame.display.get_wm_info()["window"]
win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE,
                       win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED)
win32gui.SetLayeredWindowAttributes(hwnd, win32api.RGB(*fuchsia), 0, win32con.LWA_COLORKEY)
mainClock = pygame.time.Clock()
p = pyaudio.PyAudio()
pygame.init()
pygame.display.set_caption('')
RATE = 44100
CHUNK = 2**10
infoObject = pygame.display.Info()

screen_w = int(infoObject.current_w/2)
screen_h = int(infoObject.current_w/2)
p=pyaudio.PyAudio()
for i in range(0, p.get_device_count()):
    print(i, p.get_device_info_by_index(i)['name'])

device_index = int(input('Device index: '))
stream = p.open(
                format=pyaudio.paInt16,
                channels=1,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK,
                input_device_index=device_index)#loop back is not aviable
p=pyaudio.PyAudio()

#def visualize():
while True:
    data = stream.read(CHUNK)
    data = np.frombuffer(stream.read(CHUNK),dtype=np.int16).astype(np.float64)
    screen.fill(fuchsia) 
    mx = screen_w
    my = screen_h
    cent = mx,my
    pygame.draw.circle(screen, (0, random.randint(128, 255), 255),center=cent, radius=np.average(np.abs(data))/350)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
    pygame.display.update()
    mainClock.tick(30)