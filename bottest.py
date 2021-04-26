import requests
import vk_api
import csv
import json
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

# def file_wrirer(ss):
#     with open('bdid.csv','w', encoding="utf-8") as file:
#         a_pen = csv.writer(file)
#         a_pen.writerow(('ferstname','lastname','id'))
#         for man in ss:
#             a_pen.writerow((man['first_name'],man['last_name'],man['id']))

def send(id, msg):
    vk.messages.send(user_id = id, message = msg, random_id = 0)



def sendmes(adrest, message):
    ss = apifriends()
    #print("\n Имя и фамилия получателя")
    #adrest = input()
    f = 0

    for man in ss:
        inlist = man['first_name']+' '+ man['last_name']
        x = len(inlist) - len(adrest)
        if(abs(x)<=2 and len(inlist) >= len(adrest)):
            k = 0
            i = 0
            while i < len(adrest):
                S = inlist
                Sd= adrest
                if(S[i] == Sd[i]):
                    k=k+1            
                i=i+1
            if(k>f):
                f = k 
                idd = man['id']

            
        d = inlist == adrest 
        if(d == True):
             idd = man['id']
             break
    #print(idd)
    #input(firstname, lastname)
    #message = input()
    send(idd, message)
#sendmes('a','a')

    



