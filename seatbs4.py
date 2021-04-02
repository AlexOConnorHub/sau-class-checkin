#!/usr/bin/env python3
from requests import Session
from bs4 import BeautifulSoup
from json import load, dump
from time import localtime, strftime
def get_class():
    with open('Seating/classes.json', 'r') as classes_file:
        classes = load(classes_file)
    hour = strftime('%H', localtime())
    if (int(strftime('%M', localtime())) > 55):
        hour = str(int(hour) + 1)
    if(len(hour) < 2):
        hour = '0' + hour
    final = classes[hour].split(":")
    classes[hour] = str(int(final[0])+1)+":"+final[1]
    with open('Seating/classes.json', 'w') as json_file:
        dump(classes, json_file)
    return final
secrets = {}
with open('Seating/secrets.json', 'r') as secrets_file:
    secrets = load(secrets_file)
myClass = get_class()
session = Session()
SEATING_CHECK_URL = 'https://myaccess.southern.edu/mvc/ats/Attendance/Check/' + myClass[0]
headers = {
    "Accept": "text/html,application/xhtml xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Upgrade-Insecure-Requests": "1",
    "Connection": "keep-alive",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4202.0 Safari/537.36",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-User": "?1",
    "Accept-Language": "en-US,en;q=0.9",
    "Sec-Fetch-Mode": "navigate"
}
response_myaccess = session.get("https://myaccess.southern.edu", headers=headers)
soup = BeautifulSoup(response_myaccess.content, features='lxml')
form_element = soup.find('form')
adfs_url = form_element.get('action')
saml_element = soup.find('input', attrs={'name':'SAMLRequest'})
relaystate_element = soup.find('input', attrs={'name':'RelayState'})
post_params = {
    'SAMLRequest': saml_element.get('value'),
    'RelayState': relaystate_element.get('value')
}
response_auth_post1 = session.post(url=adfs_url, data=post_params)
soup = BeautifulSoup(response_auth_post1.content, features='lxml')
login_url = soup.find('form', id='options').get('action')
login_post_params = {
    'UserName':   secrets['username'],
    'Password':   secrets['password'],
    'as_sfid':    soup.find('input', attrs={'name':'as_sfid'}).get('value'),
    'as_fid':     soup.find('input', attrs={'name':'as_fid'}).get('value'),
    'AuthMethod': 'FormsAuthentication'
}
response_login_post = session.post(url=login_url, data=login_post_params)
soup = BeautifulSoup(response_login_post.content, features='lxml')
saml_url = soup.find('form').get('action')
saml_post_params = {
    'as_sfid':      soup.find('input', attrs={'name':'as_sfid'}).get('value'),
    'as_fid':       soup.find('input', attrs={'name':'as_fid'}).get('value'),
    'RelayState':   soup.find('input', attrs={'name':'RelayState'}).get('value'),
    'SAMLResponse': soup.find('input', attrs={'name':'SAMLResponse'}).get('value')
}
response_saml_post = session.post(url=saml_url, data=saml_post_params)
soup = BeautifulSoup(response_saml_post.content, features='lxml')
last_auth_url = soup.find('form').get('action')
last_auth_params = {
    'wresult': soup.find('input', attrs={'name':'wresult'}).get('value'),
    'wa':      soup.find('input', attrs={'name':'wa'}).get('value'),
    'wctx':    soup.find('input', attrs={'name':'wctx'}).get('value'),
    'as_sfid': soup.find('input', attrs={'name':'as_sfid'}).get('value'),
    'as_fid':  soup.find('input', attrs={'name':'as_fid'}).get('value'),
}
response_last_auth_post = session.post(url=last_auth_url, data=last_auth_params)
response = session.get(SEATING_CHECK_URL)
soup = BeautifulSoup(response.content, features='lxml')
seat_number = "online=No&seatId=" + myClass[1]
print(seat_number)
seating_response = session.post(url=SEATING_CHECK_URL, data=seat_number)
