import time
import requests
import bs4
import datetime
import json
import pandas as pd
from retrying import retry
from my_token import *
from my_proxy import *
from my_chat_id import *
PROXY = dict(http=PROXY, https=PROXY)
API_URL = "https://api.telegram.org/bot" + TOKEN
def main():
    pass
@retry
def date_initial():
    with open('last_update_id.txt', 'r') as f:
        date_old = f.read()
        
    return date_old
@retry
def sendm(chat_id, textm):
    requests.get(API_URL +"/sendMessage?chat_id=" + str(chat_id) + "&" + "text=" + str(textm), proxies=PROXY)
@retry
def sendme(textm):
    requests.get(API_URL +"/sendMessage?chat_id=" + str(MY_CHAT_ID) + "&" + "text=" + str(textm), proxies=PROXY)

@retry
def get_update():

    s = requests.get(API_URL +"/getupdates", proxies=PROXY).json()
    s = s['result']
    
    return s
if __name__ == "__main__":
    main()
