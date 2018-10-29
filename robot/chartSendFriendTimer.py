#coding=utf-8
'''
Created on 2018年10月29日

@author: Pan
'''
from datetime import datetime
import itchat
import xlrd
from apscheduler.schedulers.background import BlockingScheduler
import os

def loginCallback():
    print("***登录成功***")


def exitCallback():
    print("***已退出***")
    
def SentChatMsg(name, context, scheduler):
    itchat.get_friends(update=True)
    iFriends = itchat.search_friends(name)
    for friend in iFriends:
        if friend['NickName'] == name:
            userName = friend['UserName']
            break
    itchat.send_msg(context, userName)
    print("发送时间：" + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "\n"
                                                                   "发送到：" + name + "\n"
                                                                                   "发送内容：" + context + "\n")
    print("*********************************************************************************")
    scheduler.print_jobs()

def getJob(fileName='AutoSentChatroom.xlsx', sheetName='Chatfriends'):
    scheduler = BlockingScheduler()
    workbook = xlrd.open_workbook(
    os.path.join(os.path.dirname(os.path.realpath(__file__)), fileName))
    sheet = workbook.sheet_by_name(sheetName)
    iRows = sheet.nrows
    index = 1
    for i in range(1, iRows):
        textList = sheet.row_values(i)
        name = textList[0]
        context = textList[2]
        float_dateTime = textList[1]
        date_value = xlrd.xldate_as_tuple(float_dateTime, workbook.datemode)
        date_value = datetime(*date_value[:5])
        if datetime.now() > date_value:
            continue
        date_value = date_value.strftime('%Y-%m-%d %H:%M:%S')
        textList[1] = date_value
        scheduler.add_job(SentChatMsg, 'date', run_date=date_value,
                          kwargs={"name": name, "context": context, 'scheduler':scheduler})
        print("任务" + str(index) + ":\n"
                                  "待发送时间：" + date_value + "\n"
                                                          "待发送到：" + name + "\n"
                                                                           "待发送内容：" + context + "\n"
                                                                                                "******************************************************************************\n")
        index = index + 1
        if index == 1:
            print("***没有任务需要执行***")      
    return scheduler

if __name__ == '__main__':
    itchat.auto_login(hotReload=True, loginCallback=loginCallback, exitCallback=exitCallback)
    getJob().start()