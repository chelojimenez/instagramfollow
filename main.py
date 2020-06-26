from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager


# from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
import time
from time import sleep
import random
import sys

archivo = open("cuenta.txt", "r")
usuario = archivo.readline()
contrasena = archivo.readline()
archivo2 = open("hashtags.txt", "r")
lineas = archivo2.readlines()
hashtags = []
for tag in lineas:
    hashtags.append(tag)


class InstagramBot:
    def __init__(self, username, password):
        self.username = username
        # self.driver = webdriver.Chrome("chromedriver.exe")
        self.driver = webdriver.Chrome(ChromeDriverManager().install())
        self.numero_de_likes = 0

    def closeBrowser(self):
        self.driver.close()

    def login(self):
        # Crear el Driver
        driver = self.driver
        # Ir a instagram
        driver.get('https://www.instagram.com/accounts/login/?hl=en')
        # Esperar un ratito
        sleep(2)
        # Enviar nombre de usuario
        driver.find_element_by_xpath(
            '/html/body/div[1]/section/main/div/article/div/div[1]/div/form/div[2]/div/label/input').send_keys(usuario)
        # Enviar contrasena
        driver.find_element_by_xpath(
            "/html/body/div[1]/section/main/div/article/div/div[1]/div/form/div[3]/div/label/input").send_keys(contrasena)
        # Iniciar Sesion
        driver.find_element_by_xpath(
            '/html/body/div[1]/section/main/div/article/div/div[1]/div/form/div[3]/div/label/input').send_keys(Keys.ENTER)
        # NOT NOW
        notNowButton = WebDriverWait(self.driver, 15).until(
            lambda d: d.find_element_by_xpath('//button[text()="Not Now"]'))
        notNowButton .click()
        sleep(1)

    def like_photo(self, hashtag):
        driver = self.driver
        driver.get("https://www.instagram.com/explore/tags/" +
                   hashtag + "/?hl=en")
        sleep(2)
        # Buscando imagenes
        pic_hrefs = []
        for i in range(1, 7):
            try:
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                sleep(2)
                # get tags
                hrefs_in_view = driver.find_elements_by_tag_name('a')
                # finding relevant hrefs
                hrefs_in_view = [elem.get_attribute('href') for elem in hrefs_in_view
                                 if '.com/p/' in elem.get_attribute('href')]
                # building list of unique photos
                [pic_hrefs.append(href) for href in hrefs_in_view if href not in pic_hrefs]
                #print("Check: pic href length " + str(len(pic_hrefs)))
            except Exception:
                continue
        #Liking photos 
        unique_photos = len(pic_hrefs)
        print("unique_photos", unique_photos)
        for pic_href in pic_hrefs:
            driver.get(pic_href)
            sleep(2)
            rand = random.randint(2,6)
            print("Esperando", rand, "segundos")
            #driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            try:
                sleep(rand)
                #like_button = lambda: driver.find_element_by_xpath('//span[@aria-label="Like"]').click()                
                #like_button = driver.find_element_by_link_text("Like").click()
                like_button = driver.find_element_by_xpath('/html/body/div[1]/section/main/div/div[1]/article/div[2]/section[1]/span[1]/button').click()
                #like_button.click()
                print("numero de likes", numero_de_likes)
                self.numero_de_likes += 1
            except Exception as e:
                print("hashtag", hashtag, "in except")
                time.sleep(2)
            



my_bot = InstagramBot(usuario, contrasena)
my_bot.login()
[my_bot.like_photo(tag) for tag in hashtags]
print(self.numero_de_likes)



