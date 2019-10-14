#for the telegram bot
#pip3 install python-telegram-bot

#for request song
#pip3 install selenium

#for convert image and fetching from camera
#pip3 install imageio-ffmpeg
#pip3 install opencv-python
#pip3 install imageio

#To request http pages
#pip3 install requests
#pip3 install BeautifulSoup4

import os
from telegram.ext import CommandHandler, Updater, MessageHandler, Filters, CallbackQueryHandler
from telegram import InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton, ReplyKeyboardMarkup, Video, PhotoSize
from time import sleep as sl
from emoji import emojize
from selenium import webdriver
import datetime
from random import randint as rand
from bs4 import BeautifulSoup

#from resultBot import getResult
#import minecraftHandler
import requests
import re

#songBot
#restouBot
#dogBot
#tramBot

modules = ["poll", "tramBot"]

dev = True
owner_chat_id = '274609775'
isMac = True

class Bot:
    def __init__(s, modules, dev, owner_chat_id, isMac):
        print("-- Initializing the bot --")
        s.isMac = isMac
        s.slash = s.getSlash()
        s.ownerId = owner_chat_id
        s.dev = dev
        s.modules = modules
        s.token = '862576529:AAHmqHWqMqqm70Cw1plDVmFXCD-GxcTixRg'
        #s.sendMessage(s.ownerId, "Bot was started")
        s.startBot()
        
    def getSlash(s):
        if(s.isMac):
            return '/'
        else:
            return '\\'

    def sendMessage(s, bot, chatId, message):
        mess = bot.send_message(chat_id=chatId, text=emojize(str(message), use_aliases=True))
        return mess

    def sendMessage2(s, bot, chatId, message, markup):
        mess = bot.send_message(chat_id=chatId, text=message, reply_markup=markup)
        return mess

    def sendChatAction(s, bot, chatId, action):
        bot.send_chat_action(chatId, action, 4)
        
    def start(s, bot, update):
        s.sendMessage(bot, update.message.chat_id, ":star: Salut :star:")

    def getUserName(s, update):
        userName = ""
        try:
            if(update.message != None and update.message.chat.username != None):
                userName = update.message.chat.username
            elif(update.message != None and update.message.chat.first_name != None):
                userName = update.message.chat.first_name
        except:
            print("error on getUserName")
            userName = "Bob"
        return userName
        
    def startBot(s):
        updater = Updater(token = s.token)
        s.dispatcher = updater.dispatcher
        s.add_handlers()
        updater.start_polling()
    
    def add_handlers(s):
        start_handler = CommandHandler('start', s.start)
        s.dispatcher.add_handler(start_handler)
        s.dispatcher.add_handler(CallbackQueryHandler(s.callbackHandler))
        if(s.dev == True):
            print("- devFct")
        if('tramBot' in s.modules):
            print('- tramBot')
            tramHand = CommandHandler('t', s.getTram)
            s.dispatcher.add_handler(tramHand)
        if('poll' in s.modules):
            print('- poll')
            s.isPollOn = False
            s.botMsg = None
            s.msgPoll = None
            poll_handler = CommandHandler('poll', s.poll)
            s.dispatcher.add_handler(poll_handler)
            stopPoller = CommandHandler('stopPoll', s.stopPoll)
            s.dispatcher.add_handler(stopPoller)
            
    def build_menu(s, buttons, n_cols, header_buttons=None, footer_buttons=None):
        menu =[buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
        if header_buttons:
            menu.insert(0, header_buttons)
        if footer_buttons:
            menu.append(footer_buttons)
        return menu

    def callbackHandler(s, bot, update):
        data = update.callback_query.data
        if('rs' in data):
            s.handleCmdRs(bot,update,data)
        else:
            s.handleCmdRestou(bot, update)
        
    def deleteInfoRS(s):
        try:
            if(s.msgInfoRS != None):
                s.msgInfoRS.delete()
                s.msgInfoRS = None
        except:
            print("Error on deleteInfoRs")
    
    def commandPlayer(s,bot, update):
        button_list = [
                InlineKeyboardButton(emojize(":sound:", use_aliases=True), callback_data='rs_quieter'),
                InlineKeyboardButton(emojize(":loud_sound:", use_aliases=True), callback_data='rs_louder'),
                InlineKeyboardButton(emojize(":arrow_forward:", use_aliases=True), callback_data='rs_play'),
                InlineKeyboardButton(emojize(":black_medium_square:", use_aliases=True), callback_data='rs_pause'),
                InlineKeyboardButton(emojize(":fast_forward:", use_aliases=True), callback_data='rs_nextVideo'),
                InlineKeyboardButton(emojize("fart1", use_aliases=True), callback_data='rs_fart_1'),
                InlineKeyboardButton(emojize("fart2", use_aliases=True), callback_data='rs_fart_2'),
                InlineKeyboardButton(emojize("fart3", use_aliases=True), callback_data='rs_fart_3'),
                InlineKeyboardButton(emojize("fart4", use_aliases=True), callback_data='rs_fart_4'),
                InlineKeyboardButton(emojize("fart5", use_aliases=True), callback_data='rs_fart_5'),
                InlineKeyboardButton(emojize("fart6", use_aliases=True), callback_data='rs_fart_6'),
                InlineKeyboardButton(emojize("fart7", use_aliases=True), callback_data='rs_fart_7'),
                InlineKeyboardButton(emojize(":round_pushpin:", use_aliases=True), callback_data='rs_getInfo'),
            ]
        reply_markup = InlineKeyboardMarkup(s.build_menu(button_list, n_cols=2))
        botMsgCmd = bot.send_message(chat_id=update.message.chat_id,text="Send command for the player", reply_markup=reply_markup)
                    
    def poll(s, bot, update):
        s.isPollOn = True
        s.clearFile()
        button_list = [
            InlineKeyboardButton(emojize("Moi :hand:", use_aliases=True), callback_data='choixOk'),
            InlineKeyboardButton(emojize("Nope :x:", use_aliases=True), callback_data='choixNope')
        ]
        reply_markup = InlineKeyboardMarkup(s.build_menu(button_list, n_cols=2))
        s.botMsg = s.sendMessage2(bot, update.message.chat_id, "Qui vient au RU ?", reply_markup)
        
    def clearFile(s):
        with open('listUsers.txt','w') as f:
            f.write('\n\n')
            f.close()
    def handleCmdRestou(s, bot, update):
        if (s.isPollOn):
            s.deletePollMessages()
            userId = int(update.callback_query.from_user.id)
            userName = update.callback_query.from_user.first_name
            chatId = int(update.callback_query.message.chat.id)
            userIdentification = str(userId)+':'+str(userName)
            listOk = s.getUserList(True)
            listNotOk = s.getUserList(False)
            if (update.callback_query.data == "choixOk"):
                if(userIdentification not in listOk):
                    s.addUser(userId,userName, True)
                    if(userIdentification in listNotOk):
                        s.removeUser(userId,userName,False)
            else:
                if(userIdentification not in listNotOk):
                    s.addUser(userId,userName, False)
                    if(userIdentification in listOk):
                        s.removeUser(userId,userName,True)
            namesOk = s.getNameList(True)
            namesNotOk = s.getNameList(False)        
            message = ':hand: Venant :'
            for i in range(len(namesOk)):
                message += ' ' + str(namesOk[i])
            message += '\n:x: Venant pas :'
            for i in range(len(namesNotOk)):
                message += ' ' + str(namesNotOk[i])
            button_list = [
                InlineKeyboardButton(emojize("Moi :hand:", use_aliases=True), callback_data='choixOk'),
                InlineKeyboardButton(emojize("Nope :x:", use_aliases=True), callback_data='choixNope')
            ]
            reply_markup = InlineKeyboardMarkup(s.build_menu(button_list, n_cols=2))
            s.botMsg = s.sendMessage2(bot, chatId, "Qui vient au RU ?", reply_markup)
            s.msgPoll = s.sendMessage(bot, chatId, message)

    def deletePollMessages(s):
        if (s.msgPoll != None):
            s.msgPoll.delete()
            s.msgPoll = None
        if (s.botMsg != None):
            s.botMsg.delete()
            s.botMsg = None
            
    def getUserList(s, isOk):
        liste = []
        with open('listUsers.txt','r') as f:
            count = 0
            for ligne in f:
                if(count == 0 and isOk):
                    liste = ligne.strip('\n').split('_')[1:]
                elif(count == 1 and isOk == False):
                    liste = ligne.strip('\n').split('_')[1:]
                count = count+1
        return liste

    def addUser(s, userId, userName,isOk):
        listOk = ""
        listNotOk = ""
        with open('listUsers.txt', 'r') as fr:
            count = 0
            for ligne in fr:
                if(count == 0):
                    listOk = ligne
                elif(count == 1):
                    listNotOk = ligne
                count = count+1
            fr.close()
        with open('listUsers.txt','w') as fw:
            if(isOk):
                fw.write(listOk.strip()+'_'+str(userId)+':'+str(userName)+'\n')
                fw.write(listNotOk)
            else:
                fw.write(listOk)
                fw.write(listNotOk.strip()+'_'+str(userId)+':'+str(userName)+'\n')
            fw.close()
    
    def removeUser(s, userId, userName,isOk):
        listOk = ""
        listNotOk = ""
        with open('listUsers.txt', 'r') as fr:
            count = 0
            for ligne in fr:
                if(count == 0):
                    listOk = ligne
                elif(count == 1):
                    listNotOk = ligne
                count = count+1
            fr.close()
        listeYeah =  listOk.strip('\n').split('_')[1:]
        listeNotYeah = listNotOk.strip('\n').split('_')[1:]
        if(isOk):
            for i in range(len(listeYeah)):
                if(listeYeah[i] == str(userId)+':'+str(userName)):
                    listeYeah.remove(str(userId)+':'+str(userName))
                    break
        else:
            for i in range(len(listeNotYeah)):
                if(listeNotYeah[i] == str(userId)+':'+str(userName)):
                    listeNotYeah.remove(str(userId)+':'+str(userName))
                    break
        listOkOut = listeYeah[:]
        listNotOkOut = listeNotYeah[:]
        s.writeFile(listOkOut, listNotOkOut)

    def writeFile(s, listOk, listNotOk):
        with open('listUsers.txt', 'w') as f:
            for i in range(len(listOk)):
                if(listOk[i] != ''):
                    f.write('_'+str(listOk[i]))
            f.write('\n')
            for i in range(len(listNotOk)):
                if(listNotOk[i] != ''):
                    f.write('_'+str(listNotOk[i]))
            f.write('\n')
            f.close()

    def getNameList(s, isOk):
        listeName = ""
        with open('listUsers.txt','r') as f:
            count = 0
            for ligne in f:
                if(count == 0 and isOk):
                    listeName = ligne.strip('\n')
                elif(count == 1 and isOk == False):
                    listeName = ligne.strip('\n')
                count = count+1
        listeName = s.removeNumbersFrom(listeName)
        listeNameAft = listeName.split('_:')[1:]
        return listeNameAft
    
    def removeNumbersFrom(s, listeName):
        liste = ""
        for i in range(len(listeName)):
            if(listeName[i] not in '1234567890'):
                liste = liste+listeName[i]
        return liste
    
    def stopPoll(s, bot, update):
        s.isPollOn = False
        s.clearFile()
        s.deletePollMessages()

    def getTram(s, bot, update):
        arret="JEAN+MOULIN"
        sens = "ANGERS+ROSERAIE"
        '''
        try:
            commande = update.message.text.split('-')
            sens = commande[0].split(' ',1)[1]
            sensFormat = sens.upper().split()[0]+"+"+sens.upper().split()[1]
            arret = commande[1]
            arretFormat = arret.upper().split()
            if (len(arretFormat)>1):
                arretFormat = arretFormat[0]+"+"+arretFormat[1]
            else:
                arretFormat = arretFormat[0]

        except:
            print("Exception :", "1")
            sensFormat = "ANGERS+ROSERAIE"
            arretFormat = "JEAN+MOULIN"
            '''

        url = 'https://data.angers.fr/api/records/1.0/search/?dataset=bus-tram-circulation-passages&rows=300&sort=-arrivee&facet=mnemoligne&facet=nomligne&facet=dest&facet=mnemoarret&facet=nomarret&facet=numarret'
        url += '&refine.mnemoligne=A'
        url += '&refine.dest=' + sens
        url += '&refine.nomarret=' + arret
        
        contents = requests.get(url).json()
        try:
            trams = contents['records']
            now = datetime.datetime.now()
            nextTram = []

            for tram in trams:
                arriveeJson = tram['fields']['arrivee']
                arriveeJson = arriveeJson.split('+',1)[0]
                arriveeDatetime = datetime.datetime.strptime(arriveeJson, '%Y-%m-%dT%H:%M:%S')
                if (arriveeDatetime > now):
                    nextTram.append(arriveeDatetime)
            time = nextTram[0].strftime("%H:%M:%S")
            chat_id = update.message.chat_id
            message = ":tram_car: Prochain tram depuis Jean Moulin : "
            message += time
            s.sendMessage(bot, chat_id, message)
        except: 
            chat_id = update.message.chat_id
            s.sendMessage(bot, chat_id, 'Jsp, j\'ai 4 projets en même temps frère :neutral_face:')
            print("Exception :", "2")

bot = Bot(modules, dev, owner_chat_id, isMac)
