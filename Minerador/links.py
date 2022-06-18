import requests
from bs4 import BeautifulSoup

lista_links = open('lista.txt','w')
urls = ['https://businessinsider.com/']

palavras_chaves = ['ukraine']
for j in urls:
 #urls que serão mineradas
    reqs = requests.get(j) #request do link
    soup = BeautifulSoup(reqs.text, 'html.parser')  #criação do objeto beautifulSoup
    for k in palavras_chaves:
     for link in soup.find_all('a'):
       try:
           if '/' not in link.get('href'):
             pass
           elif (k in link.get('href')): #inserção das palavras chaves
            lista_links.write('' + link.get('href') + '\n')
       except:
        pass

lista_links.close()

filer = open('lista.txt','r')
lista = filer.readlines()
new_list = []
for k in lista:
    new_list.append(k[:-1])
    
new_list = list(dict.fromkeys(new_list))

filer.close()

arch = open('lista.txt','w')
for k in new_list:
    arch.write(str(k)+'\n')

arch.close()
