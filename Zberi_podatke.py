import os
import re
import csv
import Shrani_strani as ss

vzorec_serij = re.compile(
        r'itemprop="ratingValue">(?P<ocena>.*?)</span>.*?'
        r'itemprop="ratingCount">(?P<st_glasov>.*?)</span>.*?'
        r'data-tconst="tt(?P<id>\d{7})".*?'
        r'<h1 itemprop="name" class=".*?">(?P<naslov>.*?)&nbsp;.*?'
        r'datetime=".*?">.*?(?P<dolzina>\d{1,3}\D{1,3}).*?</time>.*?'
        r'>TV .*?Series \((?P<leto>.*?)\).*?'
        r'"bp_sub_heading">(?P<epizode>\d+) episodes?</span>.*?'
        r'<div class="summary_text" itemprop="description">\W+(?P<opis>.*?[\.|!]).*?'
        r'<h2>Cast</h2>(?P<igralci>.*?)See full cast.*?'
        r'Genres:</h4>(?P<zanri>.*?)</div>.*?'
        r'Country:</h4>(?P<drzave>.*?)</div>.*?'
        ,flags = re.DOTALL)

def predelaj_podatke(serija):
    seznam_let = re.findall(r'[12][90]\d{2}', serija['leto'])
    k=''
    if len(seznam_let) == 2:
        k = seznam_let[-1]
    serija['leto'] = (seznam_let[0] + '-' + k)
    for x in ['h', 'min']:
        if x in serija['dolzina']:
            h = 1
            if x == 'h':
                h = 60
            cas = h * int(serija['dolzina'].replace(x, ''))
    serija['epizode'] = int(serija['epizode'])
    if cas > 90:
        cas = cas // serija['epizode']
    serija['dolzina'] = cas
    serija['ocena'] = float(serija['ocena'])
    serija['drzave'] = re.findall(r'itemprop=.*?url.*?>(.*?)</a>',
                                  serija['drzave'])
    serija['st_glasov'] = int(serija['st_glasov'].replace(',', ''))
    serija['zanri'] = re.findall(r'stry_gnr"\W*> (\D+?)</a>',
                               serija['zanri'])
    i = re.findall(
        r'itemprop="name">(.*?)</span>.*?'
        r'&nbsp;(.*?)\n'
        ,serija['igralci'], flags = re.DOTALL)
    j = []
    for (x,y) in i:
        y1 = y
        if '<' in y:
            y1=((y.split('>')[1]).split('<')[0])
        j.append((x,y1))
    serija['igralci'] = j
    linki = re.findall(
        r'<.*?>.*?',
        serija['opis'])
    for link in linki:
        serija['opis'] = serija['opis'].replace(link, '')
    serija['opis'] = serija['opis'].replace('&quot;', '')
    return serija
    
def zberi_podatke(ime_datoteke):
    '''Zbere podatke o tv seriji iz njene datoteke in vrne slovar vrednosti.'''
    with open(ime_datoteke, 'r', encoding='utf-8') as f:
        vsebina = f.read()
    for stvar in re.finditer(vzorec_serij, vsebina):
        serija = stvar.groupdict()
    return predelaj_podatke(serija)

def seznam_serij():
    n = ss.trenutna_mapa()
    serije = []
    os.chdir('../imdb')
    with open('vse_serije.txt', 'r', encoding='utf-8') as g:
        text = g.read().strip(',')
    for sifra in (text.split(',')):
        if sifra in ['1230180', '3358020', '1493239']:
            continue
        serije.append(zberi_podatke(sifra + '.txt'))
    os.chdir('../' + n)
    return serije

def naredi_csv():
    with open('serije.csv', 'w') as f:
        writer = csv.DictWriter(f, fieldnames =
                                ['id', 'naslov','opis', 'zanri','leto',
                                 'drzave', 'dolzina', 'epizode', 'ocena',
                                 'st_glasov', 'igralci'])
        writer.writeheader()
        for serija in seznam_serij():
            writer.writerow(serija)
    
