from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import ui
from selenium.webdriver import ActionChains
from PIL import Image
import pytesseract
import numpy as np

def raspador():
    filename = 'exemplo.png'

    img1 = np.array(Image.open(filename))

    texto_raspado = pytesseract.image_to_string(img1)

    print(texto_raspado)

def captura_tela(url):
    driver = webdriver.Firefox()

    #Botar o link do usuário aq
    driver.get(url)

    #driver.get('https://www.businessinsider.com/ukraine-eu-application-european-commission-recommends-candidate-status-2022-6')

    action = ActionChains(driver)
    
    #driver.execute_script("window.scrollTo(0, 230)") 

    driver.save_full_page_screenshot('exemplo.png')
    driver.close()
    

if __name__ == '__main__':
    captura_tela()
    raspador()