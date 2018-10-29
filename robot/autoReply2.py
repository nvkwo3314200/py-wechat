#coding=utf-8
'''
Created on 2018年10月29日

@author: Pan
'''
# -*- coding=utf-8 -*-
import requests
import itchat
import random
KEY = 'd74d5aa877944794b33bd567545842e8'
robots=['']
def get_response(msg):
    apiUrl = 'http://www.tuling123.com/openapi/api'
    data = {
        'key'    : KEY,
        'info'   : msg,
        'userid' : 'wechat-robot',
    }
    try:
        r = requests.post(apiUrl, data=data).json()
        return r.get('text')
    except:
        return
@itchat.msg_register(itchat.content.TEXT)
def tuling_reply(msg):
    defaultReply = 'I received: ' + msg['Text']
    
    reply = get_response(msg['Text'])+random.choice(robots)
    return reply or defaultReply

@itchat.msg_register([itchat.content.TEXT], isGroupChat=True)
#用于接收群里面的对话消息
def print_content(msg):
    return get_response(get_response(msg['Text'])+random.choice(robots))

itchat.auto_login(hotReload=True)
itchat.run()