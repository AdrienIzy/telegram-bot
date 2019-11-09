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

modules = ["tramBot"]

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

    def getTram(s, bot, update):
        arret = ""
        sens = ""
        arretMessage = "Jean Moulin"
        sensMessage = "Angers Roseraie"
        custom = False
        if(len(update.message.text)>3):
            custom = True
            try:
                commande = update.message.text[3:].split(" - ")
                sens = commande[0].upper().replace(" ", "+")
                sensMessage = commande[0]
                arret = commande[1].upper().replace(" ", "+")
                arretMessage = commande[1]
            except:
                print("Exception :", "1")
                sens = "ANGERS+ROSERAIE"
                arret = "JEAN+MOULIN"
        else :
            arret="JEAN+MOULIN"
            sens = "ANGERS+ROSERAIE"

        print(sens)
        print(arret)

        url = 'https://data.angers.fr/api/records/1.0/search/?dataset=bus-tram-circulation-passages&rows=300&sort=-arrivee&facet=mnemoligne&facet=nomligne&facet=dest&facet=mnemoarret&facet=nomarret&facet=numarret'
        url += '&refine.mnemoligne=A'
        url += '&refine.dest=' + sens
        url += '&refine.nomarret=' + arret

        print(url)
        
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

            if custom:
                message = ":tram_car: Prochain tram vers "+sensMessage+" depuis "+arretMessage+" : "
                message += time
            else:
                message = ":tram_car: Prochain tram depuis Jean Moulin : "
                message += time
            s.sendMessage(bot, chat_id, message)
        except: 
            chat_id = update.message.chat_id
            s.sendMessage(bot, chat_id, 'Jsp, j\'ai 4 projets en même temps frère :neutral_face:')
            print("Exception :", "2")

bot = Bot(modules, dev, owner_chat_id, isMac)
