import re
import os
import requests
import sys

def trenutna_mapa():
    '''Vrne mapo trenutnega delovnega direktorija.'''
    trenutna_pot = os.getcwd()
    return (trenutna_pot.split('\\')[-1])

def naredi_mapo():
    '''Naredi mapo imdb v mapi eno stopnjo višje od trenutne poti.'''
    m = trenutna_mapa()
    os.chdir('../')
    os.makedirs('imdb', exist_ok=True)
    os.chdir(m)

def shrani_html(url, ime):
    '''V trenutno mapo shrani tekst html strani iz url-ja url,
    v datoteko ime.txt, ce ta se ne obstaja.'''
    if os.path.isfile(ime):
        return
    r = requests.get(url, headers={'Accept-Language':'en'})
    with open(ime + '.txt', 'w', encoding ='utf-8') as f:
        f.write(r.text)
    print(ime, 'shranjeno')

def potegni_serije():
    '''Iz datoteke list.txt iz mape imdb najde in shrani vseh 250 spletnih
    strani serij v mapo imdb, pod njihovimi siframi, naredi vse_serije.txt,
    kjer so napisane sifre vseh shranjenih serij.'''
    m = trenutna_mapa()
    naredi_mapo()
    os.chdir('../imdb')
    shrani_html('http://www.imdb.com/chart/toptv/',
                'list')
    with open('list.txt', 'r') as f:
        text = f.read()
    with open('vse_serije.txt', 'w') as g:
        for stvar in re.finditer(
            r'.*?\d{1,3}\W*?<a href="(/title/tt(\d+)/)\?.*?', text):
            shrani_html('http://www.imdb.com' + stvar.group(1), stvar.group(2))
            g.write(stvar.group(2) + ',')
    os.chdir('../' + m)

        
