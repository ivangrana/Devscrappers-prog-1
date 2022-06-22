from flask import Flask,render_template,request  
import requests as rqs
from bs4 import BeautifulSoup as bss
import Minerador.main as mn

app = Flask(__name__)

@app.route("/")

@app.route("/home")
def home():
    return render_template("index.html")

@app.route("/result", methods=['POST','GET'])
def result():
    output = request.form.to_dict()
    print(output)
    #link = output["link"]
    keyword = [output["keyword"]]#palavras-chaves para a busca

    mn.main(keyword)
    #print(mn.raspadorValendo(keyword))
    #reqs = rqs.get(link) #request do link
    #soup = bs(reqs.text, 'html.parser')  #criação do objeto beautifulSoup
    return render_template("index.html",keyword=keyword)

if __name__ == '__main__':
    app.run(debug= True, port=8000)