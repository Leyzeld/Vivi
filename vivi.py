from vosk import Model, KaldiRecognizer
from multiprocessing.dummy import Pool
import sys
import os
import wave
import json
import pyaudio
import pyttsx3
import speech_recognition as sr
import os
import time
import random
from fuzzywuzzy import fuzz
import datetime
import webbrowser
import pyautogui
import urllib.request
from bottest import sendmes

import win32com.client

model = Model("model")
rec = KaldiRecognizer(model, 16000)
p = pyaudio.PyAudio()

stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8000)
stream.start_stream()
speak_engine = pyttsx3.init()
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
        "mus":('найди мне песню','найди мне музыку','песня','музыка','найди песню','найди музыку','включи мне песню','включи мне музыку','включи песню','включи музыку','включи'),
        "sendmes":("Отправь сообщение","сообщение"),
        "coin":("подбрось монетку","кинь монетку")
    }
}

def speak(what):
    print( what )
    speak_engine.say( what )
    speak_engine.runAndWait()
    speak_engine.stop()

def recognize_cmd(cmd):
    RC = {'cmd': '', 'percent': 0}
    for c,v in opts['cmds'].items():
 
        for x in v:
            vrt = fuzz.ratio(cmd, x)
            if vrt > RC['percent']:
                RC['cmd'] = c
                RC['percent'] = vrt
   
    return RC

def execute_cmd(cmd,voice):
    speak("хорошо")
    ch = 0
    if cmd == 'ctime':
    
        now = datetime.datetime.now()
        speak("Сейчас " + str(now.hour) + ":" + str(now.minute))
    elif cmd == 'coin':
        coin = random.randint(1,100)
        print(coin)
        if coin == 50:
            speak("Выпало ребро")
        elif coin > 50:
            speak("Выпал+а решка")
        elif coin < 50:
            speak("Выпал орел")
        

    elif cmd == 'radio':
       
        #os.system("D:\\anison.m3u")
        webbrowser.open_new('https://www.youtube.com/watch?v=5qap5aO4i9A')
   

    elif cmd == 'jokes':
        
        speak("Преподаватель в ВУЗе говорит: — Если я вам проставлю этот зачет, вы в конце концов получите диплом и станете инженерами. Если не поставлю — вы пойдете в армию и будете меня защищать. Даже не знаю, что хуже…")


    elif cmd == 'mus':
        speak("Скажите свой запрос для поиска на YouTube")
        time.sleep(0.1)
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
            print("[log "+str(now.hour) + ":" + str(now.minute)+ ":" + str(now.second)+"] Голос не распознан! YUTUBE")
        except sr.UnknownValueError as e:
            print("[log "+str(now.hour) + ":" + str(now.minute)+ ":" + str(now.second)+"] Неизвестная ошибка YUTUBE")
        webbrowser.open_new('https://www.youtube.com/results?search_query='+ voice)
        
        print('command ')
        print(voice)
        pyautogui.press('tab')
        time.sleep(1.5)
        pyautogui.press('tab')
        time.sleep(1.5) 
        pyautogui.press('enter')

        
    
    elif cmd == 'serch':
        
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
        except sr.UnknownValueError as e:
            print("[log "+str(now.hour) + ":" + str(now.minute)+ ":" + str(now.second)+"] Неизвестная ошибка SEARCH")
        #webbrowser.open_new_tab('https://yandex.ru/search/?lr=10735&text='+ voice)
        webbrowser.open_new_tab('http://www.google.com/search?q='+ voice)

    elif cmd == 'sendmes':
        for i in range(2):
            if i == 0:
                speak("Назовите имя получателя")
            else:
                speak("Скажите текст письма")
            try:
                r = sr.Recognizer()
                m = sr.Microphone(device_index = 1)
                with m as source:
                    r.adjust_for_ambient_noise(source, duration=1)
                    audio1 = r.listen(source)
                    time.sleep(0.1)
                if i == 0:
                    name = r.recognize_google(audio1, language = "ru-RU").lower()
                    print(name)
                else:
                    msg = r.recognize_google(audio1, language = "ru-RU").lower()
                    print(msg)
            except sr.UnknownValueError:
                print("[log "+str(now.hour) + ":" + str(now.minute)+ ":" + str(now.second)+"] Голос не распознан! SEARCH")
            except sr.UnknownValueError as e:
                print("[log "+str(now.hour) + ":" + str(now.minute)+ ":" + str(now.second)+"] Неизвестная ошибка SEARCH")
        sendmes(name,msg)
        
   
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
        #if "виви" in text:
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
            time.sleep(0.1)
            #if voice.startswith(opts["alias"]):
                # обращаются
            cmd = voice

                # for x in opts['alias']:
                #     cmd = cmd.replace(x, "").strip()
            for x in opts['tbr']:
                cmd = cmd.replace(x, "").strip()
                # распознаем и выполняем команду
            cmd = recognize_cmd(cmd)
            ch = execute_cmd(cmd['cmd'],voice)
            #else:
             #   print("Команда не распознана, извините")
# p = Pool(20)
# texts = p.map(recog, open(sys.argv[-1]).readlines())
# print ("\n".join(texts))
def main():
    speak("Добро пожаловать")
    while True:
        text = RecognizedSpeech()
        if "виви" in text:
            callback()
main()