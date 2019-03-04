
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
import csv

browser = webdriver.Chrome()
csvfile = open('data.csv', 'a')
csvwriter = csv.writer(csvfile)
browser.get('https://investia.ca/trouver-conseiller')
browser.find_element_by_id('CodePostalVille').send_keys('H7K1S5') # On trouve le txtbox pour input le code postal.
sleep(2) # J'ai dû mettre des délais, sinon rien de fonctionnait!
TrouverConseillers = browser.find_element_by_xpath('//*[@id="formBlocConseiller"]/button')
TrouverConseillers.click() 
sleep(5) # On a appuyé sur le bouton... on attend que le JavaScript récupère les courtiers et les affiches..
nextbtn = browser.find_element_by_xpath('//*[@id="moreResultsButton"]')

while(nextbtn.text == 'Voir plus de conseillers'):  # Tant que le bouton "Voir plus de conseillers" est présent..
    nextbtn.click()                                 # .. On continue d'appuyer jusqu'à ce qu'il ne soit plus là. (Tous les résultats sont affichés)
    sleep(2)
    nextbtn = browser.find_element_by_xpath('//*[@id="moreResultsButton"]')

html = browser.page_source 
soup = BeautifulSoup(html) # On donne le contenu à bs4 une fois tous les résultats affichés.
RawCourtier = soup.find_all("div", {"class": "commun-bloc-contact simple"}) 
for i in RawCourtier: # On "scrap" la page à la recherche des infos désirées.
    print("******") # Print seulement pour débuggage.
    Nom = i.find("h3").text.strip()
    Telephone = i.find("p").text.strip()
    Mail = i.find("a", {"role":"button"}).attrs['data-utag-name']
    csvwriter.writerow([Nom, Telephone, Mail]) # On écrit le data au fur et en csv.

csvfile.close()


