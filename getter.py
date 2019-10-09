from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
import datetime

def simple_get(url):
    try:
        with closing(get(url, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                return None

    except RequestException as e:
        log_error('Error during requests to {0} : {1}'.format(url, str(e)))
        return None


def is_good_response(resp):
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200 
            and content_type is not None 
            and content_type.find('html') > -1)


def log_error(e):
    print(e)

def isEmpty(mot):
    if(len(mot) == 0):
        return True
    alph = 'abcdefghijklmnopqrstuvwxyz'
    empty = True
    for lettre in alph:
        if lettre in mot:
            empty = False
    return empty

def convertMenu(menus):
    now = datetime.datetime.now()
    menuTxt = str(now.year)+'-'+str(now.month)+'-'+str(now.day)+'\n'
    for i in range(len(menus)):
        for j in range(len(menus[i])):
            if(j == 0):
                menuTxt = menuTxt + menus[i][j]+'\n'
            else:
                for k in range(len(menus[i][j])):
                    menuTxt = menuTxt +'  - '+menus[i][j][k]+'\n'
    return menuTxt

def runGetter2():
    url = "https://m.univ-angers.fr/menu.php"
    resp = simple_get(url)

    if resp is not None:
        html = BeautifulSoup(resp.decode('utf-8'), 'html.parser')
        plats = []
        menuComplet = []
        lignes = str(html).split('\n')
        for i in range(len(lignes)):
            if ('AfficherMenu' in lignes[i] and 'Resto U Ambroise Croizat - Medecine' in lignes[i]):
                valCompt = i
                menu = lignes[i+2]
                htmlMenu = BeautifulSoup(menu, 'html.parser')
                for h4 in htmlMenu.select('h4'):
                    menuComplet.append([h4.text,[]])
                count = 0
                for ul in htmlMenu.select('ul'):
                    for li in ul.select('li'):
                        if(not(isEmpty(li.text))):
                            menuComplet[count][1].append(li.text)
                    count = count+1
    menuTxt = convertMenu(menuComplet)
    with open('menuDuJour.txt', 'w', encoding='utf-8') as f:
        counter = 0
        for ligne in menuTxt:
            f.write(ligne)
            counter = counter +1
        if(counter < 11):
            f.write('Désolé le système est en train d\'être réparé suite à une fucking mise à jour non prévue')
        f.close()

def runGetter():
    url = "http://www.crous-nantes.fr/restaurant/resto-u-ambroise-croizat/"
    resp = simple_get(url)
    if resp is not None:
        html = BeautifulSoup(resp.decode('utf-8'), 'html.parser')
        plats = []
        menuComplet = []
        lignes = str(html).split('\n')
        for i in range(len(lignes)):
            if ('content-repas' in lignes[i]):
                menu = lignes[i+1]
                htmlMenu = BeautifulSoup(menu, 'html.parser')
                for span in htmlMenu.select('span'):
                    menuComplet.append([span.text,[]])
                count = 0
                for ul in htmlMenu.select('ul'):
                    for li in ul.select('li'):
                        if(not(isEmpty(li.text))):
                            menuComplet[count][1].append(li.text)
                    count = count+1
                break
    menuTxt = convertMenu(menuComplet)
    with open('menuDuJour.txt', 'w', encoding='utf-8') as f:
        counter = 0
        for ligne in menuTxt:
            f.write(ligne)
            counter = counter +1
        if(counter < 11):
            f.write('Désolé le système est en train d\'être réparé suite à une fucking mise à jour non prévue')
        f.close()
    
def getHtmlPage(url):
    resp = simple_get(url)
    return resp

