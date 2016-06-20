# 3 Zenith-afhankelijkheid van een station.

Dit notebook sluit aan op het notebook 'HiSPARC_API'. Er wordt zowel informatie
van het station als van de metingen verwerkt.

Een HiSPARC-station meet deeltjes in een deeltjeslawine die wordt veroorzaakt
door een primair kosmisch deeltje. De deeltjes in de lawine bewegen globaal met
de lichtsnelheid. De interactie van het primaire deeltje vindt plaats op een
hoogte van tientallen kilometers. De doorsnede van de deeltjeslawine is slechts
enkele hectometers. We kunnen we er dus van uitgaan dat deeltjes globaal in een
vlak loodrecht op de snelheid van het primaire deeltje bewegen.


```python
import numpy as np
import sapphire
from sapphire import Station
detectors = Station(501).info['scintillators']
for detector in detectors:
    print detector
```

De *plattegrond* van een meetstation (detectorposities) is gedefinieerd door:

- 'alpha' : De hoek tussen de as gedefinieerd door de GPS-antenne en het midden
van de scintillatorplaat en het Noorden.
- 'beta' : De hoek tussen de lange zijde van de scintillatorplaat en het
Noorden.
- 'radius' : De afstand van GPS- antenne tot het midden van de detector.
- 'height' : De hoogte t.o.v de GPS- antenne

Een werkblad voor het maken van een stations-plattegrond is te vinden op:

[http://docs.hisparc.nl/infopakket/pdf/station_map.pdf](http://docs.hisparc.nl/infopakket/pdf/station_map.pdf)

### Afstanden
De afstand tussen twee detectoren is te bepalen met de cosinusregel. Dit is in
een functie te beschrijven:


```python
def afstand(detector_1, detector_2):
    '''Bepaal de afstand tussen twee detectoren'''
    c = detector_2['radius']
    b = detector_1['radius']
    alpha = np.radians(detector_2['alpha'] - detector_1['alpha'])
    return (b ** 2 + c ** 2 - 2 * b * c * np.cos(alpha)) ** .5
```

De afstand tussen detector 1 (telt als 0) en 4 (telt als 3) is nu te berekenen
met:


```python
print afstand(detectors[0], detectors[3])
```

### Aankomsttijden

In het recept *python data retrieval* zijn events van station 501 van een enkele
dag gedownload.
We openen nu deze data en controleren of de tabel '/s501/events' bestaat. Zo
niet, dan downloaden we de data alsnog


```python
import tables
data = tables.open_file('data.h5', 'a')
if '/s501/events' not in data:
    data = sapphire.quick_download(501)
else:
    print data.root.s501.events
```


```python
events = data.root.s501.events.read()
event = events[0]
print event
```


```python
tijdkolommen = ['t1', 't2', 't3', 't4'] 
for kolom in tijdkolommen:
    print event[kolom]
```

### Zenithoeken

Uit de tijdsverschillen tussen de aankomsttijden in detectoren is de zenithoek
te bepalen.

Voor een stations met 4 detectoren zijn er 6 combinaties, d.w.z. 6 zenithoeken:


```python
from itertools import combinations

def zenithoeken(event, detectors):
    ''' 
    De zenithoek is de hoek tussen het golf-front en de horizon, 
    of ook tussen de as naar het zenith en de as van de deeltjeslawine.
    
    parameters
    event: een enkel event uit de opgehaalde data
    detectors: de detectorinformatie uit de API
    
    returns
    een array met de hoek tussen de as door twee detectors en het deeltjes front.
    '''
    c = 0.2998  # in m/ns
    
    tijden = [event['t1'], event['t2'], event['t3'], event['t4']]
    detector_tijd_paren = zip(detectors, tijden)
    
    zenith = []
    for paar1, paar2 in combinations(detector_tijd_paren, 2):
        detector1, t1 = paar1
        detector2, t2 = paar2

        if t1 < 0. or t2 < 0.:
            continue

        schuine = afstand(detector1, detector2)
        overstaande = c * (t1 - t2) 
        
        angle = np.degrees(np.arcsin(overstaande / schuine))
        zenith.append(angle)
    return zenith
```


```python
print zenithoeken(event, detectors)
```

Omdat slechts 2 van de 4 detectoren (detector 3 en 4) deeltjes hebben
gedetecteerd is er slechts 1 zenithoek.


```python
for event in events[0:10]:
    print zenithoeken(event, detectors)
```

Hierboven zijn de gereconstrueerde hoeken voor de eerste 10 events voor alle
combinaties van 2 detectoren in een set van 4 detectoren berekend. De hoeken
zijn gedefinieerd als de hoek tussen de as door de detector en het hart van de
deeltjeslawine.

Voor events waarbij twee detectoren een of meer deeltjes hebben gedetecteerd is
er slechts 1 zenithoek. Voor events waarbij 3 detectoren zijn geraakt zijn er 3
zenithoeken. Als 4 detectoren meedoen, dan zijn er 6 zenithoeken.

Een beschrijving van de zenith-hoek is te vinden op: [http://docs.hisparc.nl/infopakket/pdf/richting_reconstructie.pdf](http://docs.hisparc.nl/infopakket/pdf/richting_reconstructie.pdf).
