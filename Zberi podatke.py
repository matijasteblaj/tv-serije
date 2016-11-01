import os
import re
import csv

def zberi_podatke(ime_datoteke):
    '''Zbere podatke o tv seriji iz njene datoteke.'''
    os.chdir('../imdb')
    with open(ime_datoteke, 'r') as f:
        vsebina = f.read()
    vzorec_serij = re.compile(
        r'"ratingValue">(?P<ocena>.*?)</span>.*?
        r'data-tconst="tt(?P<id>\d){7}".*?'
        r'<h1 itemprop="name" class="">(?P<naslov>.*?)&nbsp;.*?'
        r'datetime="PT56M">.*?(?P<dolzina>\d{1,3}min).*?</time>.*?'
        r'itemprop="genre">(?P<zanr>.*?)</span></a>.*?'
        r'>TV Series (?P<leto>\(.*?\)).*?'
        r'"bp_sub_heading">(?P<epizode>\d+) episodes?</span>.*?'
    
