import pyttsx3
import speech_recognition as sr
import os
import time
from fuzzywuzzy import fuzz
import datetime
import webbrowser
import pyautogui
import urllib.request
from bottest import sendmes

import win32com.client
import time

# настройки
opts = {
    "alias": ('Вика','Викусик','Виктория','виви'),
    "tbr": ('скажи','расскажи','покажи','сколько','произнеси'),
    "tbr_youtub_m": ('найди мне песню','найди мне музыку','песня','музыка','найди песню','найди музыку','включи мне песню','включи мне музыку','включи песню','включи музыку','найди мне','песни', 'песню','мелодию','музыку','включи'),

    "cmds": {
        "ctime": ('текущее время','время','который час'),
        "radio": ('включи радио','радио'),
        "jokes": ('анекдот','рассмеши меня','ты знаешь анекдоты'),
        "serch":('поисковый запрос','поиск'),   
        "mus":('найди мне песню','найди мне музыку','песня','музыка','найди песню','найди музыку','включи мне песню','включи мне музыку','включи песню','включи музыку','включи'),
        "sendmes":("Отправь сообщение","сообщение")
    }
}




# функции
def speak(what):
    print( what )
    speak_engine.say( what )
    speak_engine.runAndWait()
    speak_engine.stop()

def callback(recognizer, audio):
    ch = 1
    while ch == 1:
        try:
            speak("Я слушаю, хозяин")
            m = sr.Microphone(device_index = 1)
            with m as source:
                recognizer.adjust_for_ambient_noise(source, duration=1)
                audio1 = recognizer.listen(source)
                time.sleep(0.1)
            voice = recognizer.recognize_google(audio1, language = "ru-RU").lower()
            print("[log "+str(now.hour) + ":" + str(now.minute)+"] Распознано: " + voice)
            #if voice.startswith(opts["alias"]):
                # обращаются
            cmd = voice

                # for x in opts['alias']:
                #     cmd = cmd.replace(x, "").strip()
            for x in opts['tbr']:
                cmd = cmd.replace(x, "").strip()
                # распознаем и выполняем команду
            cmd = recognize_cmd(cmd)
            ch = execute_cmd(cmd['cmd'],recognizer,voice)
            #else:
             #   print("Команда не распознана, извините")

        except sr.UnknownValueError:
            print("[log "+ str(now.hour) + ":" + str(now.minute) + ":" + str(now.second)+"] Голос не распознан")
            speak('Я вас не поняла, повторите')

        except sr.UnknownValueError as e:
             print("[log "+ str(now.hour) + ":" + str(now.minute) + ":" + str(now.second)+"] Неизвестная ошибка")

 
def recognize_cmd(cmd):
    RC = {'cmd': '', 'percent': 0}
    for c,v in opts['cmds'].items():
 
        for x in v:
            vrt = fuzz.ratio(cmd, x)
            if vrt > RC['percent']:
                RC['cmd'] = c
                RC['percent'] = vrt
   
    return RC


 
def     execute_cmd(cmd,recognizer,voice):
    speak("yes sir")
    ch = 0
    if cmd == 'ctime':
    
        now = datetime.datetime.now()
        speak("Сейчас " + str(now.hour) + ":" + str(now.minute))
   
    elif cmd == 'radio':
       
        #os.system("D:\\anison.m3u")
        webbrowser.open_new('https://www.youtube.com/watch?v=5qap5aO4i9A')
   

    elif cmd == 'jokes':
        
        speak("Археологи нашли ножницы возрастом около четырех тысяч лет. Так вот, они оказались менее тупыми, чем фанаты Милого во Франксе.")


    elif cmd == 'mus':
        for x in opts['tbr_youtub_m']:
                 voice = voice.replace(x, "").strip()
        webbrowser.open_new('https://www.youtube.com/results?search_query='+ voice)
        
        print('command ')
        print(voice)
        pyautogui.press('tab')
        time.sleep(1.5)
        pyautogui.press('tab')
        time.sleep(1.5) 
        pyautogui.press('enter')

        
    
    elif cmd == 'serch':
        
        speak("Скажите свой запрос, хозяин")
        try:
            r = sr.Recognizer()
            m = sr.Microphone(device_index = 1)
            with m as source:
                r.adjust_for_ambient_noise(source, duration=1)
                audio1 = r.listen(source)
                time.sleep(0.1)
            voice1 = r.recognize_google(audio1, language = "ru-RU").lower()
            print(voice1)
        except sr.UnknownValueError:
            print("[log "+str(now.hour) + ":" + str(now.minute)+ ":" + str(now.second)+"] Голос не распознан! SEARCH")
        except sr.UnknownValueError as e:
            print("[log "+str(now.hour) + ":" + str(now.minute)+ ":" + str(now.second)+"] Неизвестная ошибка SEARCH")
        #webbrowser.open_new_tab('https://yandex.ru/search/?lr=10735&text='+ voice)
        webbrowser.open_new_tab('http://www.google.com/search?q='+ voice1)

    elif cmd == 'sendmes':
        speak("Назовите имя получателя, хозяин")
        try:
            r = sr.Recognizer()
            m = sr.Microphone(device_index = 1)
            with m as source:
                r.adjust_for_ambient_noise(source, duration=1)
                audio1 = r.listen(source)
                time.sleep(0.1)
            name = r.recognize_google(audio1, language = "ru-RU").lower()
            print(name)
        except sr.UnknownValueError:
            print("[log "+str(now.hour) + ":" + str(now.minute)+ ":" + str(now.second)+"] Голос не распознан! SEARCH")
        except sr.UnknownValueError as e:
            print("[log "+str(now.hour) + ":" + str(now.minute)+ ":" + str(now.second)+"] Неизвестная ошибка SEARCH")
        speak("Скажите текст письма, хозяин")
        try:
            r = sr.Recognizer()
            m = sr.Microphone(device_index = 1)
            with m as source:
                r.adjust_for_ambient_noise(source)
                audio1 = r.listen(source)
                time.sleep(0.1)
            msg = r.recognize_google(audio1, language = "ru-RU")
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
 
# запуск

speak_engine = pyttsx3.init()
speak_engine.setProperty('voice', 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_RU-RU_IRINA_11.0')

speak("Добро пожаловать, хозяин")
#speak("г-ры-ры-ры-ры-ры-ры-рыр")



# webbrowser.open_new('https://www.youtube.com/results?search_query='+ 'qween')

# time.sleep(1.5)
# pyautogui.press('tab')
# #pyautogui.press('tab')
# pyautogui.press('enter')



while True:             
    
    r = sr.Recognizer()
    m = sr.Microphone(device_index = 1)
    now = datetime.datetime.now()
    with m as source:
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
        #time.sleep(0.5)

    try:

        voice = r.recognize_google(audio, language = "ru-RU")
        print(voice)
        if voice.startswith(opts["alias"]):
            callback(r, audio)
    except sr.UnknownValueError:
        print("[log "+str(now.hour) + ":" + str(now.minute)+ ":" + str(now.second)+"] Голос не распознан! NAME")
    except sr.UnknownValueError as e:
        print("[log "+str(now.hour) + ":" + str(now.minute)+ ":" + str(now.second)+"] Неизвестная ошибка NAME")

        #time.sleep(0.1)

    # forced cmd test


#stop_listening = r.listen_in_background(m, callback)
#while True: time.sleep(0.1) # infinity loop