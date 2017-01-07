import os
import re
import csv
import Shrani_strani as ss

vzorec_serij = re.compile(
        r'itemprop="ratingValue">(?P<ocena>.*?)</span>.*?'
        r'itemprop="ratingCount">(?P<st_glasov>.*?)</span>.*?'
        r'data-tconst="tt(?P<id>\d{7})".*?'
        r'<h1 itemprop="name" class="">(?P<naslov>.*?)&nbsp;.*?'
        r'datetime=".*?">.*?(?P<dolzina>\d{1,3})min.*?</time>.*?'
        r'>TV .*?Series (?P<leto>\(.*?\)).*?'
        r'"bp_sub_heading">(?P<epizode>\d+) episodes?</span>.*?'
        r'<div class="summary_text" itemprop="description">\\n\s+(?P<opis>.*?)\\n.*?'
        r'<h2>Cast</h2>(?P<igralci>.*?)See full cast.*?'
        r'Genres:</h4>(?P<zanri>.*?)</div>.*?'
        r'Country:</h4>(?P<drzave>.*?)</div>.*?'
        ,flags = re.DOTALL)

def predelaj_podatke(serija):
    seznam_let = re.findall(r'[12][90]\d{2}', serija['leto'])
    print(serija['leto'], seznam_let)
    k=''
    if len(seznam_let) == 2:
        k = seznam_let[-1]
    serija['leto'] = (seznam_let[0] + '-' + k)
    serija['dolzina'] = int(serija['dolzina'])
    serija['epizode'] = int(serija['epizode'])
    serija['ocena'] = float(serija['ocena'])
    seznam_drzav = re.findall(r'itemprop=.*?url.*?>(.*?)</a>', serija['drzave'])
    serija['drzave'] = seznam_drzav #dokoncaj za ostale sklope!
    return serija
    
def zberi_podatke(ime_datoteke):
    '''Zbere podatke o tv seriji iz njene datoteke.'''
    m = ss.trenutna_mapa()
    os.chdir('../imdb')
    with open(ime_datoteke, 'r') as f:
        vsebina = f.read()
    for stvar in re.finditer(vzorec_serij, vsebina):
        serija = stvar.groupdict()
    pr_serija = predelaj_podatke(serija)
    for x in ['id', 'leto', 'dolzina', 'epizode', 'ocena', 'drzave']:
        print(x, ':', pr_serija[x])
##    for x in serija[0]:
##        print (x, ':', serija[0][x])
    os.chdir('../' + m)
    
    
    
