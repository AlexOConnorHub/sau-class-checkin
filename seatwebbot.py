# #!/usr/bin/env python3
from time import strftime, localtime, sleep
from json import load, dump
from webbot import Browser

def get_class():
    with open('classesbot.json', 'r') as classes_file:
        classes = load(classes_file)
    hour = strftime('%H', localtime())
    if (int(strftime('%M', localtime())) > 55):
        hour = str(int(hour) + 1)
    if(len(hour) < 2):
        hour = '0' + hour
    final = classes[hour].split(":")
    classes[hour] = str(int(final[0])+1)+":"+final[1]+":"+final[2]
    with open('classesbot.json', 'w') as json_file:
        dump(classes, json_file)
    return final
    
secrets = {}
with open('secrets.json', 'r') as secrets_file:
    secrets = load(secrets_file)

# web = Browser(True, "127.0.0.1:8080") #Use for ZAProxy. Can use to get seating ID for bs4 script
# web = Browser(True) #Use to test and see if everything is working with visual feedback
web = Browser(False) #Background script
myClass = get_class()
web.go_to('https://myaccess.southern.edu/mvc/ats/Attendance/Check/' + myClass[0])
web.type(secrets['username'], id="userNameInput")
web.type(secrets['password'], id="passwordInput")
web.click(id='submitButton')
web.click(myClass[1], classname=myClass[2])
web.click(text='yes')