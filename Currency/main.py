from bs4 import BeautifulSoup
import requests

links = ['https://www.x-rates.com/calculator/?from=BRL&to=USD&amount=1',
         'https://www.x-rates.com/calculator/?from=USD&to=BRL&amount=1',
         'https://www.x-rates.com/calculator/?from=BRL&to=EUR&amount=1',
         'https://www.x-rates.com/calculator/?from=EUR&to=BRL&amount=1',
         'https://www.x-rates.com/calculator/?from=BRL&to=GBP&amount=1',
         'https://www.x-rates.com/calculator/?from=BRL&to=ARS&amount=1',
         'https://www.x-rates.com/calculator/?from=ARS&to=BRL&amount=1',
         'https://www.x-rates.com/calculator/?from=BRL&to=ARS&amount=1',
         'https://www.x-rates.com/calculator/?from=USD&to=ARS&amount=1',
         'https://www.x-rates.com/calculator/?from=ARS&to=USD&amount=1']


pagina = requests.get(links[1])

soup = BeautifulSoup(pagina.text,'html.parser')

#Parte do código que raspa a taxa de conversão
part_1 = soup.find(class_='ccOutputTrail').previous_sibling
part_2 = soup.find(class_='ccOutputTrail').get_text(strip = True)
taxa = "{}{}".format(part_1,part_2)
taxa = float(taxa)

def conversao(taxa,valor): #funcao que faz a conversao e devolve o valor final
    final = valor*taxa
    return round(final,2)

