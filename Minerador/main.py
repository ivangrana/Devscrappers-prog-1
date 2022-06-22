from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import ui
from selenium.webdriver import ActionChains
from PIL import Image
import pytesseract
import numpy as np
import requests
from bs4 import BeautifulSoup
import random

# def raspador(filename):
#     filename = 'exemplo.png'

#     img1 = np.array(Image.open(filename))

#     texto_raspado = pytesseract.image_to_string(img1)

#     print(texto_raspado)

palavras_chaves = ["crypto"]
links_raspados = []
new_list = []

def raspador_palavras_chave():
  urls = ['https://markets.businessinsider.com/']
  for j in urls:
  #urls que serão mineradas
    reqs = requests.get(j) #request do link
    soup = BeautifulSoup(reqs.text, 'html.parser')  #criação do objeto beautifulSoup
    for k in palavras_chaves:
     for link in soup.find_all('a'):
       try:
           if ('news' not in link.get('href') or (len(link) < 2)):
             pass
           elif (k in link.get('href')): #inserção das palavras chaves
            links_raspados.append('https://markets.businessinsider.com' + link.get('href'))
       except:
        pass
  


def captura_tela(item):
    driver = webdriver.Firefox()

    driver.get(item)

    action = ActionChains(driver)
    
    name_news = str(random.randint(10,10000)) + ".png"
    driver.save_full_page_screenshot(name_news)
    driver.close()


if __name__ == '__main__':
    
    raspador_palavras_chave()
    new_list = list(dict.fromkeys(links_raspados))
    for item in new_list:
     captura_tela(item)
  
  
