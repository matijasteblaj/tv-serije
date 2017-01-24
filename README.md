# TV-Serije

Ta repozitorij vsebuje moj projekt pri Programiranju 1 - zajem in analizo podatkov o najbolj popularnih TV serijah.

#Zajeti podatki:
- naslov
- kratek opis
- žanri
- leta izida
- dolžine epizod
- število epizod
- ocena, število glasov
- igralci (in vloge)

#Analiza:
- najbolj pogosti žanri serij po državah
- ocene serij po državah
- povezave ocen, dolžin, starosti serij
- uspešnost igralcev z večimi vlogami proti igralcem z eno vlogo
- najbolj pogosto ime igralcev
- primerjava količine serij z ocenjenostjo in gledanostjo
- ...

Postopek priprave podatkov:
Datoteke Shrani_strani.py in Zberi_podatke.py damo v neko skupno mapo. Iz datoteke Shrani_strani.py poženemo funkcijo potegni_serije(), kar nam sname spletne strani, nato pa poženemo funkcijo pripravi_datoteke() iz datoteke Zberi_podatke.py. Jupyter notebook poženemo iz mape, v katerem sta prejšnji .py datoteki.
