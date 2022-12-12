#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# Copyright (c) 2022 Maksim Perov <coder@frtk.ru>
#

import telebot
import requests
import socket
import json
from time import sleep

TOKEN=''
GROUP_ID=''
TIMEOUT=60*10 # 10 minutes

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(content_types=['text'])
def get(message):
    print(message.text)

def opened(ip, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(1)
    try:
        s.connect((ip, int(port)))
        s.shutdown(socket.SHUT_RDWR)
        return True
    except:
        return False
    finally:
        s.close()

def check_host(ip, port):
    ipup = False
    for i in range(5):
        if opened(ip, port):
            ipup = True
            break
        else:
            sleep(3)
    return ipup

def alert(hostname, _socket):
    bot.send_message(GROUP_ID, "ALERT: " + hostname + "( " + _socket + " ) isn't available!")

if __name__ == "__main__":
    resources = {}
    try:
        with open("resources.json", "r") as file:
            resources = json.load(file)
    except:
        print("Input data error!")
        exit(-1)
    if resources != {}:
        while True:
            for hostname in resources:
                res = resources[hostname]
                _socket = res['host'] + ":" + res['port']
                if res['type'] in ['https', 'http']:
                    try:
                        response = requests.get(res['type'] + "://" + _socket, timeout=30)
                    except:
                        alert(hostname, res['type'] + "://" + _socket)
                else:
                    if not check_host(res['host'], res['port']):
                        alert(hostname, _socket)
            sleep(TIMEOUT)