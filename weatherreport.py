import requests
import json

def get_weather():
    city = "Нижний Новгород"
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&appid=2eee07cf500fbe8f88d62088090e7e29&units=metric&lang=RU'.format(city)
    res = requests.get(url)
    data = res.json()
    temperature = data['main']['temp']
    realtemp = data['main']['feels_like']
    weatherr = data['weather'][0]['description']
    temperature = int(temperature)
    temperature = str(temperature)
    realtemp = int(realtemp)
    realtemp = str(realtemp)
    alldata = "Погода в городе "+city+". Температура "+ temperature + " градусов цельсия, "+"ощущается как " + realtemp + ". Ожидается "+ weatherr
    return alldata