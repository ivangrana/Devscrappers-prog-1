from bs4 import BeautifulSoup
import requests
from aux import links

pagina = requests.get(links[1])

soup = BeautifulSoup(pagina.text,'html.parser')

#Parte do código que raspa a taxa de conversão
part_1 = soup.find(class_='ccOutputTrail').previous_sibling
part_2 = soup.find(class_='ccOutputTrail').get_text(strip = True)
taxa = "{}{}".format(part_1,part_2)
taxa = float(taxa)

def conversao(taxa,valor): #funcao que faz a conversao e devolve o valor final
    final = valor*taxa
    return final


def valor_final():
    valor = float(input("entre o valor em {} para ser convertido -> "))
    valor_final = conversao(taxa,valor)
    print("Valor em -> ",str(round(valor_final,2)))
    
valor_final()
