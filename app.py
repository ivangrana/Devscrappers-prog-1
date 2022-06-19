from flask import Flask,render_template,request  
import requests as rqs
from bs4 import BeautifulSoup as bs

app = Flask(__name__)

@app.route("/")

@app.route("/home")
def home():
    return render_template("index.html")

@app.route("/result", methods=['POST','GET'])
def result():
    output = request.form.to_dict()
    print(output)
    name = output["name"]
     #lista_links = open('lista.txt','w')
    #urls = ['https://dol.com.br']
    link = output["link"]
    keyword = output["keyword"]#palavras-chaves para a busca
#for j in link:
     #urls que serão mineradas
    reqs = rqs.get(link) #request do link
    soup = bs(reqs.text, 'html.parser')  #criação do objeto beautifulSoup
    '''
    for k in palavras_chaves:
     for link in soup.find_all('a'):
       try:
           if 'noticias' not in link.get('href'):
             pass
           elif (k in link.get('href')): #inserção das palavras chaves
            #lista_links.write('https://dol.com.br' + link.get('href') + '\n')
       except:
        pass
        '''
    
    return render_template("index.html", name=name, link=link, keyword=keyword,text = soup)

if __name__ == '__main__':
    app.run(debug= True, port=8000)