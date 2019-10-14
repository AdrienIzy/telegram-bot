#pip3.6 install selenium
from selenium import webdriver
import time
import urllib
import urllib3
from time import sleep as sl

#x=input("Enter the URL")
#refreshrate=int(input("Enter the number of seconds"))
#x = "https://selenium-python.readthedocs.io/getting-started.html"
refreshrate = 5
#driver = webdriver.Firefox()
global volumeLevel

counter = 0
'''
while counter != 1:
    time.sleep(refreshrate)
    #driver.close()
    newUrl = "https://web.telegram.org/#/im?p=g378274679"
    driver.get(newUrl)
    #driver.refresh()
    counter = counter + 1
    '''

pauser = True

def mute(driver):
    player_status = driver.execute_script("ytb = document.getElementById('movie_player') ; ytb.mute()")    
    
def pause(driver):
    player_status = driver.execute_script("ytb = document.getElementById('movie_player') ; ytb.pauseVideo()")
    
def play(driver):
    player_status = driver.execute_script("ytb = document.getElementById('movie_player') ; ytb.playVideo()")    

def isAdOn(driver):
    player_status = driver.execute_script("ytb = document.getElementById('movie_player') ; ytb.getAdState()")

def setVolume(driver,value):
    player_status = driver.execute_script("ytb = document.getElementById('movie_player') ; ytb.setVolume("+str(value)+")")

def getVolume(driver):
    volumeLevel = driver.execute_script("ytb = document.getElementById('movie_player') ; return ytb.getVolume()")
    return volumeLevel

def nextVideo(driver):
    driver.execute_script("ytb = document.getElementById('movie_player') ;ytb.nextVideo()")

def getTitle(driver):
    return driver.execute_script("return document.getElementsByClassName('title')[0].innerText")

def getUrl():
    print("impl the get url")

def fart(driver, nb):
    if(nb == 0):
        driver.execute_script("ytb = document.getElementById('movie_player') ; ytb.seekTo(12)")
    elif(nb == 1):
        driver.execute_script("ytb = document.getElementById('movie_player') ; ytb.seekTo(16.5)")
    elif(nb == 2):
        driver.execute_script("ytb = document.getElementById('movie_player') ; ytb.seekTo(20.8)")
    elif(nb == 3):
        driver.execute_script("ytb = document.getElementById('movie_player') ; ytb.seekTo(24.8)")
    elif(nb == 4):
        driver.execute_script("ytb = document.getElementById('movie_player') ; ytb.seekTo(24.8)")
    elif(nb == 5):
        driver.execute_script("ytb = document.getElementById('movie_player') ; ytb.seekTo(29)")
    elif(nb == 6):
        driver.execute_script("ytb = document.getElementById('movie_player') ; ytb.seekTo(34)")
    elif(nb == 7):
        driver.execute_script("ytb = document.getElementById('movie_player') ; ytb.seekTo(42.9)")  

def openChrome(driver,newUrl):
    driver.get(newUrl)
    '''
    while True:
        sl(5)
        #print(driver.text)
        print(driver.find_element_by_class_name("ytp-time-current").text)
        print(driver.find_element_by_class_name('ytp-time-duration').text)
        print(driver.find_element_by_class_name('ytp-bound-time-right').text)
        print(driver.find_element_by_class_name('ytp-progress-bar').text)
        #player_status = driver.execute_script("return document.getElementById('movie_player').getPlayerState()")
        player_status = driver.execute_script("ytb = document.getElementById('movie_player') ; return ytb.getPlayerState()")
        print(player_status)
        if(pauser):
            pause()
    '''

	
def getYtbUrl(driver):
    url2 = driver.execute_script("d = document.getElementById('contents').childNodes;ddd = d[0];dddd = ddd.childNodes;ddddd = dddd[5].childNodes;count = 0;obj = ddddd[count];while(obj.is != 'ytd-video-renderer'){count = count+1;obj = ddddd[count]};vid = obj.childNodes;vidElem2 = vid[1].childNodes;vidElem4 = vidElem2[3].childNodes;vidElem6 = vidElem4[1].childNodes;vidElem7 = vidElem6[1].childNodes;vidElem8 = vidElem7[1].childNodes;vidElem9 = vidElem8[3];return vidElem9.href")
    return url2

def isPlaying(driver):
    isPaused = driver.execute_script("return document.getElementsByClassName('paused-mode').length")
    if(isPaused != 0 ):
        return False
    else:
        return True

'''
d = document.getElementById('contents').childNodes;
ddd = d[0];
dddd = ddd.childNodes;
ddddd = dddd[5].childNodes;
count = 0;
obj = ddddd[count];
while(obj.is == "ytd-video-renderer"){count = count+1;obj = ddddd[count]};
vid = obj.childNodes;
vidElem2 = vid[1].childNodes;
vidElem4 = vidElem2[3].childNodes;
vidElem6 = vidElem4[1].childNodes;
vidElem7 = vidElem6[1].childNodes;
vidElem8 = vidElem7[1].childNodes;
vidElem9 = vidElem8[3];
return vidElem9.href

'''
