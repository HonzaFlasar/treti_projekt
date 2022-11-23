"""
projekt3_Jan_Flasar.py třetí projekt do Engeto online Python Akademie

autor: Jan Flašar
email: honza.flasar@volny.cz
discord: Honza #2485
"""

import sys
import csv
import requests
import bs4
from bs4 import BeautifulSoup

"""
první část, první scraping url adres z obecné adresy
"""

# spuštění pomocí argumentů
if len(sys.argv) != 3:
    print(f"\nSkript '{sys.argv[0]}' vyžaduje první argument URL a druhý argument jméno výstupního souboru. \nUkončuji program.")
    quit()
elif "https://volby.cz/pls/" not in sys.argv[1] or ".csv" not in sys.argv[2]:
    print("První zadaný argument není požadovaná URL adresa nebo druhý argument není tabulka výsledků. \nUkončuji program.")
    quit()
else:
    vstupni_url = sys.argv[1]
    vystupni_soubor = sys.argv[2]
    print("Spouštím program.")

url = vstupni_url
print("Probíhá vyhledávání volebních výsledků. \nStahuji data z URL ", url, "\nProsím čekejte.")

def najdi_url_obci():
    seznam_url = []
    soup = zpracuj_odpoved_serveru(url)
    #print(zpracuj_odpoved_serveru(url)) #vypíše celou stránku
    #print(najdi_Prerov(soup)) #hrubý text včetně tagů
    prerov_soup = najdi_Prerov(soup)
    webovka = "https://www.volby.cz/pls/ps2017nss/"

    for obec in prerov_soup:
        url_obce = obec.a["href"]
        seznam_url.append(webovka + url_obce)  # ukládá kompletní adresu do seznamu
    return seznam_url

def zpracuj_odpoved_serveru(url: str):
    # odešli požadavek na url a vrácené HTML parsuj pomocí BS
    odpoved = requests.get(url)
    return BeautifulSoup(odpoved.text, 'html.parser')

def najdi_Prerov(soup):
    Prerov = soup.find("div", {"class": "topline"})
    return Prerov.find_all("td", {"class": "cislo"})

seznam_url = najdi_url_obci()
jedna_url = seznam_url[0]
#print(jedna_url)

def zpracuj_jednu_url():
    soup = zpracuj_odpoved_serveru(jedna_url)
    strany = soup.find("div", {"class": "topline"})
    return strany.find_all("td", {"class": "overflow_name"})

seznam_stran = [] #ukládání názvů do seznamu
strany_skarede = zpracuj_jednu_url()
for strana in strany_skarede:
    seznam_stran.append(strana.text)
#print(seznam_stran)

"""
Konec první části, je hotový seznam URL pro všechny obce okresu Přerov a seznam všech kandidujících stran.
Následuje iterování a vytažení dat z každé jednotlivé obce.
"""

def main():  # definice funkce pro celý text
    jmeno_souboru = vystupni_soubor
    hlavicka = ["Kód obce", "Název obce", "Voliči", "Obálky", "Platné hlasy"] + seznam_stran
    csv_soubor = open(jmeno_souboru, mode="w", encoding="utf-8", newline='')
    csv_zapisovac = csv.writer(csv_soubor)
    csv_zapisovac.writerow(hlavicka)
    #print(hlavicka)

    seznam_url = najdi_url_obci()
    for url in seznam_url:
        soup = zpracuj_odpoved_serveru(url)
        hlasy_vsechny = najdi_hlasy1(soup) + najdi_hlasy2(soup) #spojení dvou funkcí pro dvě tabulky výsledků
        #print(hlasy) # 105 řádků obcí, každá 25 hodnot odevzdaných hlasů
        hlasy_stran = []
        for hlas in hlasy_vsechny:
            hlasy_stran.append(hlas.text)

        obec = najdi_obce(soup)
        #print(obec)
        # výstupní soubor - zapisování obcí
        radek_tabulky = [url[-18:-12], obec[11], obec[32], obec[33], obec[36]] + hlasy_stran
        #print(radek_tabulky)
        csv_zapisovac.writerow(radek_tabulky)

    csv_soubor.close()  # řádné zavření souboru
    print(f"Uloženo do {jmeno_souboru}. \nUkončuji program.")
    # print(najdi_Prerov(soup))
    # print(najdi_strany(soup))

def najdi_obce(soup):
    Prerov = soup.find("div", {"class": "topline"})
    return Prerov.text.replace("Obec: ", " ").replace("\xa0", " ").splitlines()

def najdi_strany(soup): # try, except jako ignorování chyby AttributeError
    try:
        strany = soup.find("div", {"class": "topline"})
        return strany.find_all("td", {"class": "overflow_name"})
    except AttributeError:
        print("Chyba pro URL", url)

def najdi_hlasy1(soup): # první tabulka počtu hlasů stran
    hlasy1 = soup.find("div", {"class": "topline"})
    return hlasy1.find_all("td", {"class": "cislo", "headers": "t1sa2 t1sb3"})

def najdi_hlasy2(soup): # druhá tabulka počtu hlasů stran
    hlasy2 = soup.find("div", {"class": "topline"})
    return hlasy2.find_all("td", {"class": "cislo", "headers": "t2sa2 t2sb3"})

if __name__ == "__main__":
    main()