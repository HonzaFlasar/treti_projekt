README.md

Projekt3_election_scraper.py
Jan Flašar - třetí projekt do Engeto online Python Akademie

Tento program extrahuje výsledky parlamentních voleb 2017 ve vybraném okrese.
Odkaz k nahlédnutí zde: https://www.volby.cz/pls/ps2017nss/ps3?xjazyk=CZ
Použité knihovny jsou uvedeny v souboru requirements.txt. Instalaci provádějte nejlépe v novém virtuálním prostředí
s nainstalovaným managerem.

Veškeré výsledky jsou zpracovány do výstupního souboru ve formátu .csv.

Spuštění programu:
Ke spuštění v příkazovém řádku je třeba zadat dva argumenty: správnou URL okresu a název výstupního souboru s příponou .csv.
Příklad pro okres Přerov:
1. argument: "https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=12&xnumnuts=7104"
2. argument: "vysledky_Prerov.csv"

Příkazový řádek pak vypadá takto: 
projekt3_election_scraper.py "https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=12&xnumnuts=7104" "vysledky_Prerov.csv"

Ukázka výstupního souboru csv:
Kód obce,Název obce,Voliči,Obálky,Platné hlasy,Občanská demokratická strana,Řád národa - Vlastenecká unie,
512231, Bělotín,1 453,790,784,59,3,0,45,3,18,79,15,7,8,1,1,42,2,12,247,0,0,108,0,2,1,1,126,4
512281, Beňov,548,382,371,32,0,0,25,0,29,32,3,1,10,0,0,16,0,1,127,0,1,39,0,3,0,2,49,1

Pro správné zobrazení v Excelu (nebo obdobně v závislosti na verzi):
Nový soubor -> Data -> Načíst externí data -> Z textu -> Importovat textový soubor -> oddělovač čárka, kódování UTF-8
