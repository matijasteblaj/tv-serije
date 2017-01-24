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
    serija['leto'] = serija['leto'].strip()
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
        r'<a href="/name/nm(\d{7})/.*?'
        r'itemprop="name">(.*?)</span>.*?'
        r'&nbsp;(.*?)\n'
        ,serija['igralci'], flags = re.DOTALL)
    j = []
    for (x,y,z) in i:
        z1 = z
        if '<' in z:
            z1=((z.split('>')[1]).split('<')[0])
        j.append((x,y,z1))
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

def seznam_slovarjev(necesa='serij'):
    n = ss.trenutna_mapa()
    seznam = []
    os.chdir('../imdb')
    with open('vse_serije.txt', 'r', encoding='utf-8') as g:
        text = g.read().strip(',')
    for sifra in (text.split(',')):
        if sifra in ['1230180', '3358020', '1493239']:
            continue
        if necesa == 'serij':
            j = dict(zberi_podatke(sifra + '.txt'))
            del j['igralci']
            del j['zanri']
            del j['drzave']
            seznam.append(j)
        elif necesa == 'igralcev':    
            for (id_, ime, vloga) in zberi_podatke(sifra + '.txt')['igralci']:
                igralec = {}
                igralec['id'] = sifra
                igralec['id igralca'] = id_
                igralec['ime'] = ime
                igralec['vloga'] = vloga
                seznam.append(igralec)
        elif necesa == 'zanrov':
            for zanr in zberi_podatke(sifra + '.txt')['zanri']:
                zanr1 = {}
                zanr1['id'] = sifra
                zanr1['zanr'] = zanr
                seznam.append(zanr1)
        elif necesa == 'drzav':
            for drzava in zberi_podatke(sifra + '.txt')['drzave']:
                drzava1 = {}
                drzava1['id'] = sifra
                drzava1['drzava'] = drzava
                seznam.append(drzava1)
        elif necesa == 'let':
            l = zberi_podatke(sifra + '.txt')['leto']
            if '–' not in l:
                leto1={}
                leto1['id'] = sifra
                leto1['leto'] = int(l)
                seznam.append(leto1)
            elif '–' in l and len(l) == 5:
                for i in range(int(l.strip('–')), 2017):
                    leto1={}
                    leto1['id'] = sifra
                    leto1['leto'] = i
                    seznam.append(leto1)
            else:
                for i in range(int(l.split('–')[0]), int(l.split('–')[1])+1):
                    leto1={}
                    leto1['id'] = sifra
                    leto1['leto'] = i
                    seznam.append(leto1)
        else:
            return 'Ni veljaven parameter!(veljavni so: serij/zanrov/igralcev)'
    os.chdir('../' + n)
    return seznam

def naredi_csv(ime='serije',
               sez_slovarjev=seznam_slovarjev('serij'),
               imena_polj=['id', 'naslov','opis','leto', 'dolzina', 'epizode',
                           'ocena', 'st_glasov']):
    with open(ime + '.csv', 'w', encoding= 'utf-8') as f:
        writer = csv.DictWriter(f, fieldnames =imena_polj)
        writer.writeheader()
        for serija in sez_slovarjev:
            writer.writerow(serija)


def pripravi_datoteke():
    sez =[('serije', seznam_slovarjev('serij'), ['id', 'naslov','opis','leto', 'dolzina', 'epizode',
                           'ocena', 'st_glasov']),
        ('zanri', seznam_slovarjev('zanrov'), ['id', 'zanr']),
        ('drzave', seznam_slovarjev('drzav'), ['id', 'drzava']),
        ('igralci', seznam_slovarjev('igralcev'), ['id', 'id igralca',
                                                   'ime', 'vloga']),
        ('leta', seznam_slovarjev('let'), ['id', 'leto'])]
    for (a,b,c) in sez:
        naredi_csv(a, b, c)
