import os
import re
import csv

def zberi_podatke(ime_datoteke):
    '''Zbere podatke o tv seriji iz njene datoteke.'''
    if not ime_datoteke[-4:] == '.txt':
        ime_datoteke += '.txt'
    trenutna_pot = os.getcwd()
    trenutna_mapa = trenutna_pot.split('\\')[-1]
    os.chdir('../imdb')
    with open(ime_datoteke, 'r') as f:
        vsebina = f.read()
    vzorec_serij = re.compile(
##        r'itemprop="ratingValue">(?P<ocena>.*?)</span>.*?'
##        r'data-tconst="tt(?P<id>\d{7})".*?'
##        r'<h1 itemprop="name" class="">(?P<naslov>.*?)&nbsp;.*?'
##        r'datetime="PT56M">.*?(?P<dolzina>\d{1,3}min).*?</time>.*?'
##        r'title="See more release dates" >.*?(?P<leto>\(.*?\)).*?'
##        r'"bp_sub_heading">(?P<epizode>\d+) episodes?</span>.*?'
##        r'episodes\?season=(?P<sezone>\d+).*?'
        r'Series cast summary:(?P<igralci_raw>.*?)>See full cast</a>.*?'
        r'<h2>Storyline</h2>.*?<p>\s*?(?P<opis_raw>.*?)<.*?'
        r'>Genres:(?P<zanri_raw>.*?)</div>.*?'
##        r'>Country:(?P<drzave_raw>.*?)</div>.*?'
        r'>Language:.*?itemprop=\'url\'>(?P<jezik>.*?)</a>.*?',#tu je tezava
        flags=re.DOTALL)
    print('Do tuki dela')
    for stvar in re.finditer(vzorec_serij, vsebina):
        print('dela?')
        for i in range(1, 5):
            print(stvar.group(i))
    os.chdir('../' + trenutna_mapa)
        
        
    
