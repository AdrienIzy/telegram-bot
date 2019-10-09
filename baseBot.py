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

from captureVideo import capt, multicapt
from convertAVITOMP4 import convertFile
import ChromeController as ChromeC
from getter import getHtmlPage, runGetter
#from resultBot import getResult
#import minecraftHandler
import requests
import re

#songBot
#captureBot
#restouBot
#mineBot
#dogBot
#tramBot

modules = ["restouBot", "dogBot", "tramBot"]

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
    
    def ping(s, bot, update):
        chatId = int(update.message.chat.id)
        messageSent = s.sendMessage(bot, chatId, "pong")
        sl(2)
        s.sendChatAction(bot, update.message.chat_id, 'typing')
        messageSent.delete()
        
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
            pingMessage_handler = CommandHandler('ping', s.ping)
            s.dispatcher.add_handler(pingMessage_handler)
        if('songBot' in s.modules):
            print("- songBot")
            s.msgInfoRS = None
            if(s.isMac):
                s.driver = webdriver.Chrome('/usr/local/bin/chromedriver')
            else:
                s.driver = webdriver.Chrome()
            requestSongCmd = CommandHandler('rs',s.requestSong)
            s.dispatcher.add_handler(requestSongCmd)

            playerCmd = CommandHandler('cmd', s.commandPlayer)
            s.dispatcher.add_handler(playerCmd)
        if('captureBot' in s.modules):
            print('- captureBot')
            capturer = CommandHandler('capture', s.captureFct)
            s.dispatcher.add_handler(capturer)
        if('restouBot' in s.modules):
            print('- restouBot')
            s.isPollOn = False
            s.botMsg = None
            s.msgPoll = None
            poll_handler = CommandHandler('poll', s.poll)
            s.dispatcher.add_handler(poll_handler)

            restou_handler = CommandHandler('ru', s.getMenu)
            s.dispatcher.add_handler(restou_handler)

            stopPoller = CommandHandler('stopPoll', s.stopPoll)
            s.dispatcher.add_handler(stopPoller)
        if('dogBot' in s.modules):
            print('- dogBot')
            dogHand = CommandHandler('dog', s.getDog)
            s.dispatcher.add_handler(dogHand)
        if('tramBot' in s.modules):
            print('- tramBot')
            tramHand = CommandHandler('t', s.getTram)
            s.dispatcher.add_handler(tramHand)
        '''
        if('resultBot' in s.modules):
            print('- resultBot')
            resultHand = CommandHandler('result', s.getResult)
            s.dispatcher.add_handler(resultHand)
        '''
            
    def sendVideo(s,bot, chatId, fileName):
        bot.send_video(chat_id=chatId, video=open(fileName+'.mp4', 'rb'), supports_streaming=True)

    def captureFct(s,bot, update):
        s.sendMessage(bot, s.ownerId, s.getUserName(update)+": launched "+update.message.text)
        duree=1
        nbCam = 1
        try:
            duree = int(update.message.text.split()[1])
            cam = int(update.message.text.split()[2])
            if(duree<0 or duree>10):
                duree = 1
        except:
            print("Exception :",duree)
            duree=1
            cam = 0
        if(cam == 9):
            (nbCam) = multicapt(duree)
        else:
            (width, height, duration) = capt(duree, cam)
        if(duree>0 and nbCam == 1):
            fileName = 'outpy'
            path = os.getcwd()+s.slash
            convertFile(path,fileName,'.mp4')
            s.sendVideo(bot, update.message.chat_id, fileName)
        elif(duree >0):
            fileName = 'outpy'
            path = os.getcwd()+s.slash
            for i in range(nbCam):
                convertFile(path,fileName+str(i),'.mp4')
                s.sendVideo(bot, update.message.chat_id, fileName+str(i))
        else:
            bot.send_document(chat_id=update.message.chat_id, document = open('capture.jpg','rb'), supports_streaming=True)
            
    def requestSong(s, bot, update):
        s.sendMessage(bot, update.message.chat_id, s.getUserName(update)+': '+update.message.text)
        url = update.message.text.split()[1]
        if("http" in url):
            ChromeC.openChrome(s.driver, url)
            sl(2)
            ChromeC.setVolume(s.driver, 1)
        else:
            msg = update.message.text.split()[1:]
            url = "https://www.youtube.com/results?search_query="
            for i in range(len(msg)):
                url = url +msg[i]
                if(i != len(msg)-1):
                    url = url+'+'
            html = getHtmlPage(url)
            with open('file.html','w') as f:
                for ligne in html:
                    f.write(str(ligne))
                f.close()
            
            ChromeC.openChrome(s.driver, url)
            urlSong = ChromeC.getYtbUrl(s.driver)
            message = urlSong
            bot.sendMessage(chat_id=update.message.chat_id, text=message)
            ChromeC.openChrome(s.driver,urlSong)
            sl(2)
            ChromeC.setVolume(s.driver, 1)
            
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
            
    def handleCmdRs(s, bot,update,cmd):
        cmd = cmd[3:]
        vol = int(ChromeC.getVolume(s.driver))
        if(cmd == "louder"):
            if(vol<100):
                vol = vol+10
            ChromeC.setVolume(s.driver,vol)
        elif(cmd == "quieter"):
            if(vol>0):
                vol = vol-10
            ChromeC.setVolume(s.driver,vol)
        elif(cmd == "play"):
            ChromeC.play(s.driver)
        elif(cmd == "pause"):
            ChromeC.pause(s.driver)
        elif(cmd == "nextVideo"):
            ChromeC.nextVideo(s.driver)
            sl(1)
        elif("fart" in cmd):
            val = int(cmd[5:])
            ChromeC.fart(s.driver, val)
        message = str(vol)+"% :loud_sound:"
        isPlaying = ChromeC.isPlaying(s.driver)
        if(isPlaying == True):
            message = message +' is playing :arrow_forward: '
        else:
            message = message +' is paused :black_medium_square:'
        title = ChromeC.getTitle(s.driver)
        message = message + '\n'+title
        s.deleteInfoRS()
        s.msgInfoRS = s.sendMessage(bot, int(update.callback_query.message.chat.id),message)
        
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

    def getMenu(s, bot, update):
        chatID = str(update.message.chat_id)
        now = datetime.datetime.now()
        if (1 != 1):  # and now.hour>14):
            message = "Trop tard, le RESTOU est ferme maintenant !"
            bot.sendMessage(chat_id = chatID, text=message)
        
        elif (now.weekday() > 4):
            message = "Le RESTOU n'ouvre pas aujourd'hui, profite de ton week-end vindiou"
            if (now.weekday() == 6):
                message = message + " mais pense a revenir demain quand meme"
            s.sendMessage(bot, chatID, message)
        
        else:
            if (rand(0, 8) == 1):
            #if (1==1):
                message = ""
                valRand = rand(0,5)
                url = "https://api.telegram.org/bot"+s.token+"/sendChatAction?chat_id="+chatID+"&action=UPLOAD_VIDEO_NOTE&timeout=10"
                s.simple_get(url)
                #if(1==1):
                if (valRand < 4):
                    sl(3)
                    message = "T'as cru j'etais ton larbin ou quoi ?"
                    s.sendMessage(bot, chatID,message)
                    s.simple_get(url)
                    sl(rand(4,10))
                    message = "Ca me vener les gens comme ça qui pensent que tout est acquis dans la vie..."
                    s.sendMessage(bot, chatID,message)
                    s.simple_get(url)
                    sl(rand(5,10))
                    message = "Qui pensent que juste parce qu'ils ont un privilège ou une capacité de compréhension plus grande que les autres, ils sont forcément supérieurs qu'eux et ils méprisent alors tout ceux qui les entourent"
                    s.sendMessage(bot, chatID,message)
                    s.simple_get(url)
                    sl(rand(10,15))
                    message = "Et le pire n'est pas forcément tout ça, c'est de rester dans l'ignorance fatale la plus incongrue et édifiante que l'on puisse observer jusqu'à ce jour, toute personne de raison saurait se remettre en cause et demander pardon à son prochain, mais la plupart du temps ce n'est pas le cas et rien ne change..."
                    s.sendMessage(bot, chatID,message)
                    s.simple_get(url)
                    sl(rand(15,20))
                    message = "Non monsieur ! Rien ne change car il y a quelque chose de pourri en ce monde, une peste qui ronge cette terre, rien n'est sacré. Même ceux qui ont besoin de prendre leur retraite subissent un stress économique considérable au cours de cette période de l'Histoire. En particulier ceux qui arrangent des arbustes ne sont plus en sécurité au sein de notre gouvernement..."
                    s.sendMessage(bot, chatID,message)
                    s.simple_get(url)
                    sl(rand(15,30))
                    message = "Cette réalité, personne dans cet hémicycle ne la découvre. Et certainement pas moi, sauf à penser que tous ceux qui se sont engagés dans l’action publique et politique locale depuis près de 20 ans y seraient insensibles. Durant ces derniers jours, j’ai beaucoup consulté. Des cuistos. Des chefs réputés. Des commis et leurs associations. Des traiteurs, que je veux remercier de leurs contributions. Les responsables de tous les CROUS et groupes restauratifs représentés au RESTOU et je salue ceux qui, sur ces bancs, ont recherché la voie de l’apaisement."
                    s.sendMessage(bot, chatID,message)
                else:
                    message = "Jsp lol"
                    s.sendMessage(bot, chatID,message)
            else:
                message = "Je vais voir ce qu'il y a dans la cuisine... :runner:"
                s.sendMessage(bot ,chatID, message )
                message = ":star: Voila le menu du jour :star: \n"
                runGetter()
                sl(rand(3, 10) - rand(0, 3))
                with open("menuDuJour.txt", 'r', encoding='utf-8') as f:
                    f.readline()
                    for ligne in f:
                        message = message + ligne
                    message = message + "\n Bon appetit ! :older_man:"
                    s.sendMessage(bot ,chatID, message )
                    
    def simple_get(s, url):
        try:
            with closing(get(url, stream=True)) as resp:
                if is_good_response(resp):
                    return resp.content
                else:
                    return None
    
        except RequestException as e:
            log_error('Error during requests to {0} : {1}'.format(url, str(e)))
            return None
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

    def getDog(s, bot, update):
        allowed_extension = ['jpg','jpeg','png']
        file_extension = ''
        while file_extension not in allowed_extension:
            contents = requests.get('https://random.dog/woof.json').json()    
            url = contents['url']
            file_extension = re.search("([^.]*)$",url).group(1).lower()
        chat_id = update.message.chat_id
        bot.send_photo(chat_id=update.message.chat_id, photo=url)

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

    '''
    def getResult(s, bot, update):
        html = getResult()
        valLenHtmlOrigin = 3424
        #print(len(html))
        soup = BeautifulSoup(html)
        txt = soup.get_text()
        print(datetime.datetime.now())
        print(update.message.chat_id)
        EG = "748461083"
        s.sendMessage(bot, EG, 'Bot launched, every 30 minutes reloads')
        while(len(html) == valLenHtmlOrigin):
            sl(1*60*30)
            print(datetime.datetime.now())
            html = getResult()
            soup = BeautifulSoup(html)
            txt = soup.get_text()
#            s.sendMessage(bot, EG, 'nope')
            #s.sendMessage(bot, update.message.chat_id, ':x: Pas de résultat encore')
#            sl(2)
#            s.sendMessage(bot, update.message.chat_id, txt)
#        else:
        s.sendMessage(bot, s.ownerId, ":white_check_mark: Y'a les dates !!")
        sl(2)
        s.sendMessage(bot, s.ownerId, txt)
        s.sendMessage(bot, EG, ":white_check_mark: Y'a les dates !!")
        sl(2)
        s.sendMessage(bot, EG, txt)
    '''

bot = Bot(modules, dev, owner_chat_id, isMac)


