from flask import Flask,render_template,request  
import requests as rqs
from bs4 import BeautifulSoup as bss
import Minerador.main as mn


app = Flask(__name__)

@app.route("/")

@app.route("/actions",methods=['POST','GET'])
def action():
    return render_template("index.html")

@app.route("/result", methods=['POST','GET'])
def result():
    output = request.form.to_dict()
    print(output)
    #link = output["link"]
    keyword = [output["keyword"]]#palavras-chaves para a busca
    emailUser = output["emailUser"]
    mn.main(keyword,emailUser)
    #print(mn.raspadorValendo(keyword))
    #reqs = rqs.get(link) #request do link
    #soup = bs(reqs.text, 'html.parser')  #criação do objeto beautifulSoup
    return render_template("receive.html",keyword=keyword,emailUser=emailUser)

if __name__ == '__main__':
    app.run(debug= True, port=8000)
