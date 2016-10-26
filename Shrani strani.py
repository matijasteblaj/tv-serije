import re
import os
import requests
import sys

def naredi_mapo():
    #Naredi mapo imdb v mapi eno stopnjo višje od trenutne poti
    trenutna_pot = os.getcwd()
    trenutna_mapa = trenutna_pot.split('\\')[-1]
    os.chdir('../')
    os.makedirs('imdb', exist_ok=True)
    os.chdir(trenutna_mapa)

def shrani_html(url, ime):
    #V mapo imdb shrani tekst html strani iz url-ja url, v datoteko ime.txt
    trenutna_pot = os.getcwd()
    trenutna_mapa = trenutna_pot.split('\\')[-1]
    os.chdir('../imdb')
    r = requests.get(url)
    with open(ime + '.txt', 'w') as f:
        f.write(str(r.text.encode('utf8')))
    os.chdir('../' + trenutna_mapa)

def potegni_serije():
    naredi_mapo()
    shrani_html('http://www.imdb.com/chart/toptv/?sort=rk,asc&mode=simple&page=1',
                'list')
    os.chdir('../imdb')
    with open('list.txt', 'r') as f:
        f.read()
