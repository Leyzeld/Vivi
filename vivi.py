from vosk import Model, KaldiRecognizer
import sys
import os
import scipy.io.wavfile as siw
import json
import pyaudio
import pyttsx3
import speech_recognition as sr
import time
import random
from fuzzywuzzy import fuzz
import datetime
import webbrowser
import pyautogui
import urllib.request
import win32com.client
from vksendmessage import sendmes
import pygame
from pygame.locals import *
import win32api
import win32con
import win32gui
from threading import Thread
import numpy as np
import wave
from wifi import is_internet_available, get_download_speed
from weatherreport import get_weather

model = Model("model")
rec = KaldiRecognizer(model, 16000)
p = pyaudio.PyAudio()

stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8000)
stream.start_stream()
speak_engine = pyttsx3.init()
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (1501,716)
pygame.init()
screen = pygame.display.set_mode((400, 400),pygame.NOFRAME)
fuchsia = (255, 0, 128)
hwnd = pygame.display.get_wm_info()["window"]
win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE,
                       win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED)
win32gui.SetLayeredWindowAttributes(hwnd, win32api.RGB(*fuchsia), 0, win32con.LWA_COLORKEY)
win32gui.SetWindowPos(pygame.display.get_wm_info()['window'], -1, 1501, 716, 0, 0, 0x0001)
mainClock = pygame.time.Clock()
pygame.display.set_caption('')
infoObject = pygame.display.Info()
screen_w = int(infoObject.current_w/2)
screen_h = int(infoObject.current_w/2)
screen.fill(fuchsia) 
mx = screen_w
my = screen_h
cent = mx,my
speak_engine.setProperty('voice', 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_RU-RU_IRINA_11.0')

opts = {
    "alias": ('Вика','Викусик','Виктория','виви','киви'),
    "tbr": ('скажи','расскажи','покажи','сколько','произнеси'),
    "tbr_youtub_m": ('найди мне песню','найди мне музыку','песня','музыка','найди песню','найди музыку','включи мне песню','включи мне музыку','включи песню','включи музыку','найди мне','песни', 'песню','мелодию','музыку','включи'),

    "cmds": {
        "ctime": ('текущее время','время','который час'),
        "radio": ('включи радио','радио'),
        "jokes": ('анекдот','рассмеши меня','ты знаешь анекдоты'),
        "serch":('поисковый запрос','поиск'),   
        "mus":('найди мне песню','найди мне музыку','песня','музыка','найди песню','найди музыку','включи мне песню','включи мне музыку','включи песню','включи музыку'),
        "sendmes":('отправь сообщение','сообщение'),
        "coin":('подбрось монетку','кинь монетку'),
        "speed":('скорость интернета','проверь интернет'),
        "about":('расскажи о себе','что ты умеешь','какие у тебя функции'),
        "weather":('погода','скажи погоду','прогноз погоды'),
        "abort":('ничего','не надо','отмена','не слушай'),
        "pause":('пауза', 'поставь на паузу','продолжи воспроизведение'),
        "meta":('скажи цель нашего проекта','цель проекта')
    }
}


def circlevis(data):
    i = 0
    while i < len(data):
        pygame.event.pump() #для работы визуализации в фоне. Запоминает последнее состояние визуализации
        mx = screen_w
        my = screen_h
        cent = mx,my
        if i + 700 < len(data):
            i += 700
        elif i + 700 > len(data):
            pygame.display.update()
            mainClock.tick(30)
            break
        screen.fill(fuchsia) 
       
        circ = pygame.draw.circle(screen, (0, 255, 255),center=cent, radius=5+np.average(np.abs(data[i]))/150)
        circ = pygame.draw.circle(screen, (0, 200, 255),center=cent, radius=6+np.average(np.abs(data[i]))/200)
        circ = pygame.draw.circle(screen, (0, 180, 255),center=cent, radius=7+np.average(np.abs(data[i]))/250)
        circ = pygame.draw.circle(screen, (0, 150, 255),center=cent, radius=8+np.average(np.abs(data[i]))/300)
        circ = pygame.draw.circle(screen, (0, 128, 255),center=cent, radius=9+np.average(np.abs(data[i]))/350)

        pygame.display.update()
        mainClock.tick(30)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
    circ = pygame.draw.circle(screen, (0, 220, 255),center=cent, radius=9)
    circ = pygame.draw.circle(screen, (0, 100, 255),center=cent, radius=5)
    pygame.display.update()
    mainClock.tick(30)

def speak(what):

    print( what )
    speak_engine.save_to_file(what, "what.wav")
    speak_engine.runAndWait()
    pygame.mixer.music.load("what.wav")
    pygame.mixer.music.set_volume(100)
    spf = wave.open("what.wav", "rb")
    signal = spf.readframes(-1)
    signal = np.frombuffer(signal, np.int16)
    thread1 = Thread(target = pygame.mixer.music.play(0))
    thread2 = Thread(target = circlevis(signal)) #отрисовка кружочка
    thread1.start()
    thread2.start()
    spf.close()
    while True:
        if pygame.mixer.music.get_busy() == False:
            pygame.mixer.music.unload()
            os.remove("what.wav")
            break


def recognize_cmd(cmd):
    RC = {'cmd': '', 'percent': 0}
    for c,v in opts['cmds'].items():
 
        for x in v:
            vrt = fuzz.ratio(cmd, x)
            if vrt > RC['percent']:
                RC['cmd'] = c
                RC['percent'] = vrt
   
    return RC

def execute_cmd(cmd):
    now = datetime.datetime.now()   
    ch = 0
    if cmd == 'about':
        speak("Меня зовут Виви. Я голосовой помошник")
        speak("Я могу сказать текущее время, рассказать анекдот, подкинуть монетку. Так же могу поставить видео на паузу или продолжить воспроизведение")
        if is_internet_available():
            speak("Проверить скорость соединения интернета, сказать прогноз погоды. Отправить сообщение пользователю ВКонтакте, включить радио и найти то, что вы хотите при помощи Google или YouTube")
        else:
            speak("Мои полные возможности будут доступны после соединения с интернетом")
    elif cmd == 'pause':
        pyautogui.press('stop')
    elif cmd == "meta":
        speak("Цель нашего проекта - облегчение использования современных технологий для пользователя путем использования нашего голосового помощника.")
    elif cmd == 'abort':
        return 0
    elif cmd == 'weather':
        w = get_weather()
        speak(w)
    elif cmd == 'speed':
        speak("Устанавливаю соединение с сервером")
        now = datetime.datetime.now()   
        speed = get_download_speed()
        now2 = datetime.datetime.now()   

        if speed == 0:
            speak("Соединение с интернетом отсутствует")
        else:
            speak("Скорость соединения составляет "+ str(speed) +" мегабит в секунду")
        print(now)
        print(now2)


    elif cmd == 'ctime':
        speak("Сейчас " + str(now.hour) + ":" + str(now.minute))
    elif cmd == 'coin':
        coin = random.randint(1,100)
        print(coin)
        if coin == 50:
            speak("Выпало ребро")
        elif coin > 50:
            speak("Выпала решка")
        elif coin < 50:
            speak("Выпал орел")
        

    elif cmd == 'radio':
        if is_internet_available():
            webbrowser.open_new('https://www.youtube.com/watch?v=5qap5aO4i9A')
        else:
            speak("В связи с отсутствием интернета эта функция не доступна")
   

    elif cmd == 'jokes':
        
        speak("Преподаватель в ВУЗе говорит: — Если я вам проставлю этот зачет, вы в конце концов получите диплом и станете инженерами. Если не поставлю — вы пойдете в армию и будете меня защищать. Даже не знаю, что хуже…")


    elif cmd == 'mus':
        if is_internet_available():
            speak("Скажите свой запрос для поиска на YouTube")
            tr = 1
            while tr == 1:
                try:
                    print("Start")

                    r = sr.Recognizer()
                    m = sr.Microphone(device_index = 1)
                    with m as source:
                        r.adjust_for_ambient_noise(source, duration=1)
                        audio1 = r.listen(source)
                    voice = r.recognize_google(audio1, language = "ru-RU").lower()
                    print(voice)
                except sr.UnknownValueError:
                    speak('Я вас не поняла, повторите')
                    print("[log "+str(now.hour) + ":" + str(now.minute)+ ":" + str(now.second)+"] Голос не распознан! YUTUBE")
                    continue    
                except sr.UnknownValueError as e:
                    print("[log "+str(now.hour) + ":" + str(now.minute)+ ":" + str(now.second)+"] Неизвестная ошибка YUTUBE")
                    speak('Я вас не поняла, повторите') 
                tr = 0    
            webbrowser.open_new('https://www.youtube.com/results?search_query='+ voice)

            print('command ')
            print(voice)
            pyautogui.press('tab')
            time.sleep(1.5)
            pyautogui.press('tab')
            time.sleep(1.5) 
            pyautogui.press('enter')
            time.sleep(1.5) 
            pyautogui.press('f')    
        else:
            speak("В связи с отсутствием интернета эта функция не доступна")

        
    
    elif cmd == 'serch':
        if is_internet_available():
            tr = 1

            while tr == 1:
                speak("Скажите свой запрос")
                try:
                    r = sr.Recognizer()
                    m = sr.Microphone(device_index = 1)
                    with m as source:
                        r.adjust_for_ambient_noise(source, duration=1)
                        audio1 = r.listen(source)
                        time.sleep(0.1)
                    voice = r.recognize_google(audio1, language = "ru-RU").lower()
                    print(voice)
                except sr.UnknownValueError:
                    print("[log "+str(now.hour) + ":" + str(now.minute)+ ":" + str(now.second)+"] Голос не распознан! SEARCH")
                    speak('Я вас не поняла, повторите')

                except sr.UnknownValueError as e:
                    print("[log "+str(now.hour) + ":" + str(now.minute)+ ":" + str(now.second)+"] Неизвестная ошибка SEARCH")
                tr = 0
            webbrowser.open_new_tab('http://www.google.com/search?q='+ voice)
            speak("Вот что мне удалось найти по запросу" + voice)
        else:
            speak("В связи с отсутствием интернета эта функция не доступна")

    elif cmd == 'sendmes':
        if is_internet_available():
            tr = 1
            while tr == 1:

                speak("Назовите имя получателя")
                try:
                    print("start")
                    r = sr.Recognizer()
                    m = sr.Microphone(device_index = 1)
                    with m as source:
                        r.adjust_for_ambient_noise(source, duration=1)
                        audio1 = r.listen(source)
                        name = r.recognize_google(audio1, language = "ru-RU").lower()
                        print(name)
                        i = 1
                except sr.UnknownValueError:
                    print("[log "+str(now.hour) + ":" + str(now.minute)+ ":" + str(now.second)+"] Голос не распознан! SENDMES")
                    speak('Я вас не поняла, повторите')
                    i = 0
                except sr.UnknownValueError as e:
                    print("[log "+str(now.hour) + ":" + str(now.minute)+ ":" + str(now.second)+"] Неизвестная ошибка SENDMES")
                    speak('Я вас не поняла, повторите')
                    i = 0
                if i != 0:    
                    speak("Скажите текст письма")
                    try:
                        print("start")
                        r = sr.Recognizer()
                        m = sr.Microphone(device_index = 1)
                        with m as source:
                            r.adjust_for_ambient_noise(source, duration=1)
                            audio1 = r.listen(source)
                            msg = r.recognize_google(audio1, language = "ru-RU").lower()
                            print(msg)
                            tr = 0
                    except sr.UnknownValueError:
                        print("[log "+str(now.hour) + ":" + str(now.minute)+ ":" + str(now.second)+"] Голос не распознан! SENDMES")
                        speak('Я вас не поняла, повторите')
                    except sr.UnknownValueError as e:
                        print("[log "+str(now.hour) + ":" + str(now.minute)+ ":" + str(now.second)+"] Неизвестная ошибка SENDMES")
                        speak('Я вас не поняла, повторите')

            sendmes(name,msg)
        else:
            speak("В связи с отсутствием интернета эта функция не доступна")
        
   
    else:
        speak('Я вас не поняла, повторите')
        ch = 1
    return ch


def RecognizedSpeech():
    print("initialized")
    text = ""
    while True:
        data = stream.read(100,exception_on_overflow=False)
        if len(data) == 0:
            break

        if rec.AcceptWaveform(data):
            jres = json.loads(rec.Result())
            text = text + " " + jres['text']
            print("Accep...     "+text)
        if text != "":
            jres = json.loads(rec.FinalResult())
            text = text + " " + jres['text']
            print("end      "+text)
            return (text)        
    jres = json.loads(rec.FinalResult())
    text = text + " " + jres['text']
    print("end      "+text)
    return (text)

def callback():
    ch = 1
    while ch == 1:

            speak("Я слушаю")
            voice = RecognizedSpeech()
            cmd = voice
            for x in opts['tbr']:
                cmd = cmd.replace(x, "").strip()
            cmd = recognize_cmd(cmd)
            ch = execute_cmd(cmd['cmd'],)
def main():

    speak("Добро пожаловать. Я голосовой помошник Виви")
    if is_internet_available():
        speak("Обнаружено соединение с интернетом. Доступны все функции")
    else:
        speak("Соединение с интернетом не доступно. Перехожу в оффлайн режим")

    while True:
        s = "start"
        circlevis(s)
        text = RecognizedSpeech()
        if "виви" in text:
            callback()
main()