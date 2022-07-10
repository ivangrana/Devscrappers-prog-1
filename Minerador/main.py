from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import ui
from selenium.webdriver import ActionChains
import requests
from bs4 import BeautifulSoup
import random
import time

# def raspador(filename):
#     filename = 'exemplo.png'

#     img1 = np.array(Image.open(filename))

#     texto_raspado = pytesseract.image_to_string(img1)

#     print(texto_raspado)

#palavras_chaves = ["crypto"]

links_raspados = []
new_list = []
urls = ['https://www.nbcnews.com/business','https://markets.businessinsider.com/','https://www.reuters.com/business/finance']

def raspador_palavras_chave2(key,url):
  #urls que serão mineradas
    reqs = requests.get(url) #request do link
    soup = BeautifulSoup(reqs.text, 'html.parser')  #criação do objeto beautifulSoup
    for k in key:
     for link in soup.find_all('a'):
       try:
           if (k not in link.get('href') or (len(link) < 2)):
             pass
           elif (k in link.get('href')): #inserção das palavras chaves
            links_raspados.append(link.get('href'))
       except:
        pass

def raspador_palavras_chave(key,url):
  #urls que serão mineradas
    reqs = requests.get(url) #request do link
    soup = BeautifulSoup(reqs.text, 'html.parser')  #criação do objeto beautifulSoup
    for k in key:
     for link in soup.find_all('a'):
       try:
           if ('/' not in link.get('href') or (len(link) < 2)):
             pass
           elif (k in link.get('href')): #inserçsão das palavras chaves
            links_raspados.append(url + link.get('href'))
       except:
        pass


def captura_tela(item):
    driver = webdriver.Firefox()

    driver.get(item)

    action = ActionChains(driver)
    
    name_news = str(random.randint(10,10000)) + ".png"
    driver.save_full_page_screenshot(name_news)
    driver.close()


#if __name__ == '__main__':

def main(k):
    # raspador_palavras_chave(k,urls[1])
    #raspador_palavras_chave2(k,urls[0])
    raspador_palavras_chave(k,urls[2])
    new_list = list(dict.fromkeys(links_raspados))
    if 'https://markets.businessinsider.comhttps://www.insider.com/news' in new_list:
     new_list.remove('https://markets.businessinsider.comhttps://www.insider.com/news')
    sorted(new_list)
    print(new_list)
    for item in new_list:
     captura_tela(item)

