from bs4 import BeautifulSoup
import requests
from aux import links,par

k = 'Y'
while k == 'Y' or k == 'y':
    print("Taxas de conversao disponiveis(moeda a ser convertida -> Moeda desejada):")
    print("0 - BRL -> USD\n1 - USD -> BRL\n2 - BRL -> EUR\n3 - EUR -> BRL\n4 - BRL -> GBP\n5 - BRL -> ARS\n6 - ARS -> BRL\n7 - USD -> ARS\n8 - ARS -> USD")
    escolha = input("Escolha a paridade para converter:")

    pagina = requests.get(links[escolha])

    soup = BeautifulSoup(pagina.text,'html.parser')

    part_1 = soup.find(class_='ccOutputTrail').previous_sibling
    part_2 = soup.find(class_='ccOutputTrail').get_text(strip = True)
    taxa = "{}{}".format(part_1,part_2)
    taxa = float(taxa)

    def conversao(taxa,brl):
        final = brl*taxa
        return final

    moeda = par[int(escolha)]

    brl = float(input("entre o valor em {} para ser convertido -> ".format(moeda[0])))
    valor_final = conversao(taxa,brl)
    print("Valor em {} -> ".format(moeda[1]) ,str(round(valor_final,2)))
    k = input("Deseja realizar mais uma conversao ?(Y/N): ")
