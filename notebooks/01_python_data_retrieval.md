# 1 Python data retrieval

Deze notebooks werken alleen met Python 3.

## Inleiding

Het notebook 'Data retrieval met python' is het eerste notebook van een serie.
In dit notebook wordt beschreven hoe HiSPARC data met de HiSPARC sapphire module
voor python op te halen is. De installatie van sapphire is beschreven op:
[https://docs.hisparc.nl/sapphire/installation.html#installing-the-prerequisites](https://docs.hisparc.nl/sapphire/installation.html#installing-the-prerequisites)

Nadat deze installatie is voltooid, kan de sapphire module in python geladen
worden. (Klik met de muis in de onderstaande code-cel en druk op shift-enter):

```python
import sapphire
```

Boven deze regel staat als het goed is de code-cel met "`import sapphire`".
Wordt een foutcode afgebeeld, dan is de installatie niet gelukt. De sapphire
module bevat onder andere de "`quick_download`" functie. Deze functie maakt het
mogelijk om data (meetgegevens) uit de HiSPARC data-server op te halen.

Aan de functie wordt het stationsnummer als parameter meegegeven. Hieronder
wordt data voor station 102 opgehaald. Uiteraard is deze opdracht aan te passen
zodat er data van een andere station opgehaald wordt. (Dit doen we weer door in
de code- cel te klikken en op shift-enter te drukken).

```python
from sapphire import quick_download
data = quick_download(102)
```

Na enige tijd verschijnt hierboven een regel zoals:
"`100%|############################################################|Time: 0:00:06`"

Soms is de download zo snel dat deze regel niet wordt afgedrukt.

De variabele "`data`" bevat nu een set meetgegevens. Deze set is af te drukken.

```python
print(data)
```

Het "`data`" bestand heeft een hierarchise opbouw. In "`data`" zit een
RootGroup, deze is te benaderen met "`data.root`". Hierin zit weer een groep
"`s102`", deze is te benaderen met "`data.root.s102`". Hierin zit een tabel
"`events`".

## Werken met een events tabel

Voor het gemak maken we een variable `events` die naar de eventstabel van
station 102 wijst:

```python
event_tabel = data.root.s102.events
event_tabel
```

Dit is een tabel van 46329 regels. Elke regel is een event.

De informatie van het eerste event is op te halen met:

```python
event_tabel[0]
```

Het **tweede** event: (Let op, python telt vanaf 0 en niet vanaf 1)

```python
event_tabel[1]
```

De informatie in een event bestaat uit een lijst getallen. Deze getallen hebben
de volgende betekenis:

1. event_id: Het unieke nummer van het event in deze dataset.
1. timestamp: De tijd in hele seconden (GPS) waarop de trigger van het event plaatsvond.
1. nanoseconds: De tijd in nanoseconden waarop de trigger van het event plaatsvond.
1. ext_timestamp: Dit getal is vrij groot, namelijk de twee vorige achter elkaar.
1. pulseheights: Een array met pulshoogten, "`-1`" betekent dat er geen detector was.
1. integrals: Een array met pulsoppervlakten, "`-1`" betekent ook hier dat er geen detector was.
1. n1: Het aantal MIPS's (Minimal Ionising Particles) dat in detector 1 is gereconstrueerd.
1. n2
1. n3
1. n4
1. t1: De gereconstrueerde detectietijden vanaf het begin van het opgeslagen signaal voor detector 1.
1. t2
1. t3
1. t4
1. t_trigger: Het moment van de GPS-tijdstempel vanaf het begin van het opgeslagen signaal.

In het
werkblad [https://docs.hisparc.nl/infopakket/pdf/traces.pdf](https://docs.hisparc.nl/infopakket/pdf/traces.pdf)
wordt de natuurkundige betekenis van deze
getallen beschreven.  De afbeeldingen in dit werkblad zijn afkomstig uit het
interactieve werkblad [https://data.hisparc.nl/media/jsparc/jsparc.html](https://data.hisparc.nl/media/jsparc/jsparc.html).
Let op, computers tellen vanaf "`0`" en niet vanaf "`1`"

### Werken met kolomnamen

Een kolom zoals 'event_id', 'timestamp' of 't1' kan opgevraagd worden door de
index van de kolom (0, 1, 2, ...) of door de kolomnaam. Door gebruik te maken
van de kolomnaam wordt de code veel beter leesbaar:

```python
first_event = event_tabel[0]
first_event['timestamp']
```

Het aantal gereconstrueerde deeltjes in detector 1 (het zevende getal) bij het
eerste event is dus te vinden met:

```python
event_tabel[0][6]  # 7de kolom van 1ste rij
```

en:

```python
first_event = event_tabel[0]
first_event['n1']
```

De tweede code is weliswaar langer, maar veel beter leesbaar.

```python
print(first_event['n1'])
print(event_tabel[0][6])
```

Een array met pulshoogten in ADC-waarden is in dit geval te vinden met:


```python
first_event['pulseheights']
```

Merk op dat de pulshoogtes van detector 3 en 4 de waarde '-1' hebben. De waarde
'-1' betekent dat de pulsehoogte niet bepaald kon worden; Station 102 heeft
slechts twee detectoren.

De eerste pulshoogte is te vinden met:

```python
print("pulshoogte detector 1: %d ADC" % first_event['pulseheights'][0])
```

### Eventkolommen gebruiken

Vaak is het eenvoudiger om de hele *kolom* `n1` in
een keer te bekijken:

De variabele `n1` wijst naar de kolom `n1` en we bekijken
de eerste 30 regels (events):

```python
n1 = event_tabel.col('n1')
n1[:30]
```

We kunnen nu de data uit een hele kolom verwerken en/of plotten:


```python
import matplotlib.pyplot as plt
import numpy as np
%matplotlib inline
```

```python
n1 = event_tabel.col('n1')
plt.hist(n1, bins=np.arange(0.3, 5., .1), histtype='step')
plt.title('Station 102: Number of particles in detector 1')
plt.xlabel('number of particles (MIP)')
plt.ylabel('counts')
```

Merk op dat:


```python
event_tabel['n1']
```

niet werkt, omdat event_tabel een (database) tabel is en geen *array*.

We kunnen wel eerst alle rijen uit de tabel inlezen:

```python
events = event_tabel.read()
```

Dan kunnen we de kolom wel selecteren: (maar we hebben nu de **gehele** tabel in
het geheugen!)

```python
events['n1']
```

## Opgave

Maak een histogram van de pulshoogtes van detector 1 en 2 van station 102.

Een voorbeeld is hier te zien: https://data.hisparc.nl/show/stations/102

```python
ph = event_tabel.col('pulseheights')
ph1 = ph[:, 0]
ph2 = ph[:, 1]
```

'pulseheights' is een *matrix*:
- `[:, 0]` is de gehele eerste rij, dwz de pulshoogtes per event van detector 0
- `[:, 1]` is de gehele tweede rij, dwz de pulshoogtes per event van detector 1

```python
plt.figure()
plt.hist(ph1, bins=np.arange(0, 2000., 20.), histtype='step', log=True)
plt.hist(ph2, bins=np.arange(0, 2000., 20.), histtype='step', log=True)
plt.title('Station 102: Pulseheights')
plt.xlabel('Pulseheight (ADC)')
plt.ylabel('counts')
plt.legend(['detector 1', 'detector 2' ])
plt.ylim(10, 1e4)
```

```python
data.close()
```
