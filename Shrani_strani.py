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
    '''V mapo imdb shrani tekst html strani iz url-ja url, v datoteko ime.txt'''
    if os.path.isfile(ime):
        return
    m = trenutna_mapa()
    os.chdir('../imdb')
    r = requests.get(url, headers={'Accept-Language':'en'})
    with open(ime + '.txt', 'w') as f:
        f.write(str(r.text.encode('utf8')))
    os.chdir('../' + m)

def potegni_serije():
    '''Iz datoteke list.txt iz mape imdb najde in shrani vseh 250 spletnih
    strani serij v mapo imdb, pod njihovimi siframi, naredi legenda.txt,
    kjer za vsako sifro pise, na katero serijo se nanasa.'''
    m = trenutna_mapa()
    naredi_mapo()
    shrani_html('http://www.imdb.com/chart/toptv/',
                'list')
    os.chdir('../imdb')
    with open('list.txt', 'r') as f:
        text = f.read()
    slovar_serij = {}
    for stvar in re.finditer(r'.*?\d+\.\\n *?<a href="(/title/tt(\d+)/).*?>(.*?)</a>', text):
        shrani_html('http://www.imdb.com' + stvar.group(1), stvar.group(2))
        slovar_serij[stvar.group(2)] = stvar.group(3)
    with open('legenda.txt', 'w') as g:
        for sifra in slovar_serij:
            g.write(sifra + ':' + slovar_serij[sifra] + ',')
    os.chdir('../' + m)

        
