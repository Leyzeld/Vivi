import requests
import vk_api
import csv
import json
from transliterate import translit
import difflib
tokken = 'efa09c7b7371a14ba052f13b029e36302d9e572e51af35e1634b46c21ea503ea3de33d04fb591fd5342ad'
session = vk_api.VkApi(token = tokken)
vk = session.get_api()
def  apifriends ():
    v=5.124
    myid = '433191935'
    order ='hints'
    fields ='domain'
    name_case ='nom'#именительный
    response = requests.get('https://api.vk.com/method/friends.get',
        params={
        'user_id' :myid,
        'order' :order,
        'fields' :fields,
        'name_case' :name_case,
        'access_token' :tokken,
        'v' :v
        }
        )
    data = response.json()['response']['items']
    return data

def file_wrirer(ss):
     with open('bdid.csv','w', encoding="utf-8") as file:
         a_pen = csv.writer(file)
         a_pen.writerow(('ferstname','lastname','id'))
         for man in ss:
             a_pen.writerow((man['first_name'],man['last_name'],man['id']))

def send(id, msg):
    vk.messages.send(user_id = id, message = msg, random_id = 0)



def similarity(s1, s2):
  normalized1 = s1.lower()
  normalized2 = s2.lower()
  matcher = difflib.SequenceMatcher(None, normalized1, normalized2)
  return matcher.ratio()

def sendmes(adrest, message):
    ss = apifriends()
   
    f = 0

    for man in ss:
        inlist = man['first_name']+' '+ man['last_name']
        x = len(inlist) - len(adrest)
        file_wrirer(ss)
        k = 0
       
        if(abs(x)<=2 and len(inlist) >= len(adrest)):
            
            k=similarity(inlist, adrest)
            if(k>f):
                f = k 
                idd = man['id']
    
    for man in ss:
        inlist = man['first_name']+' '+ man['last_name']
        tadrest=translit(adrest, language_code='ru', reversed=True)
        x = len(inlist) - len(tadrest)
        file_wrirer(ss)
        k = 0
       
        if(abs(x)<=2 and len(inlist) >= len( tadrest)):
            
            k=similarity(inlist, tadrest)
            if(k>f):
                f = k 
                idd = man['id']

            
       
    send(idd, message)
