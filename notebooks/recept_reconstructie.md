# Recept Richtingsreconstructie 

Richtingsrecontructie op basis van aankomsttijden van deeltjes is mogelijk als
er 3 tijden zijn gemeten. In het geval van HiSPARC meetstations, is dat mogelijk
bij stations met 4 detectoren.

```python
import tables
from sapphire import download_data
from datetime import datetime
```

```python
FILENAME = 's501.h5'
data = tables.open_file(FILENAME, 'a')
```

We downloaden data van het "vier-plaat" station 501; Een station met vier
detectoren:

```python
if '/s501' not in data:
    download_data(data, '/s501', 501, start=datetime(2016, 1, 1), end=datetime(2016,1,2))
```

```python
print data
```

We gebruiken de SAPPHiRE class `ReconstructESDEvents`:

```python
from sapphire import ReconstructESDEvents
rec = ReconstructESDEvents(data, '/s501', 501)
```

De function `reconstruct_directions()` reconstrueert de richtingen (hoeken) van
elk event uit de aankomsttijden per detector en slaat de uitkomst op in:
- `rec.theta`: een array met de zenith hoek per event
- `rec.phi`: een array met de azimuth hoek per event

De hoeken kunnen ook meteen opgeslagen worden in het HDF5 bestand. Dit wordt in
de volgende paragraaf toegelicht.

Eerst reconstrueren we de aankomstrichting van de events:

```python
rec.reconstruct_directions()
```

Hieronder staan de eerste twintig zenithoeken. 'nan' (NaN) betekent:
Not-a-number: De reconstructie was niet mogelijk. Ofwel er was onvoldoende
informatie, bijvoorbeeld slechts twee aankomsttijden. Ofwel de oplossing was
niet fysisch:

```python
rec.theta[:20]
```

Met behulp van de functie `numpy.isnan()` kunnen we de NaNs verwijderen:

```python
from numpy import isnan
zenith = [a for a in rec.theta if not isnan(a)]
azimuth = [a for a in rec.phi if not isnan(a)]
print "Er zijn %d events succesvol gereconstrueerd." % len(zenith)            
```

Nu bevat de array `zenith` slechts hoeken (in radialen):

```python
zenith[:5]
```

## Plotten

We maken een polar-plot van de hoeken theta en phi (zenit, azimut) van de
(succesvol) gereconstrueerde events, en een histrogram van de zenithoeken.

```python
import matplotlib.pyplot as plt
%matplotlib inline
```

We rekenen de hoeken om naar graden:

```python
from numpy import degrees
zenith = degrees(zenith)
azimuth = degrees(azimuth)
```

Polar plot van zenit en azimuth:

```python
ax = plt.subplot(polar=True)
ax.scatter(zenith, azimuth)
```

Histogram van de zenithoeken:

```python
from numpy import arange
plt.hist(zenith, bins=arange(0,90., 5.), histtype='step')
plt.xlabel('zenith angle (degrees)')
plt.ylabel('counts')
plt.title('Zenith histrogram station 501.')
```

# Opslaan van reconstructies in het HDF5 bestand

De SAPPHiRE reconstructie class `ReconstructESDEvents` kan de reconstructies ook
direct opslaan in het HDF5 bestand waar de events in zijn opgeslagen:

```python
rec = ReconstructESDEvents(data, '/s501', 501)
rec.reconstruct_and_store()
```

Er waren nu twee progressbars te zien: De eerste voor richting reconstructie en
de tweede voor core recontructie. We richten ons hier op de richtingen en laten
de core reconstructie buiten beschouwing.

naast `rec.theta` en `rec.phi` is er nu ook een nieuwe groep
`/s501/reconstructions` in het hdf5 bestand:

```python
rec_tabel = data.root.s501.reconstructions
print rec_tabel
```

De gereconstrueerde hoeken zijn nu ook opgeslagen op disk, in het HDF5 bestand.

De kolommen 'zenith' en 'azimuth' bevatten de gereconstrueerde hoeken (of NaN):

# Opgave

Maak een histogram van de zenithoeken en een polarplot van de azimuth en
zenithhoeken, zoals in het voorbeeld hierboven. Gebruik de `zenith` en `azimuth`
kolommen uit de groep `/s501/reconstructions` uit het HDF5 bestand.

*Hints*:
- gebruik: `.col('zenith')` om een kolom in te laden.
- gebruik  `.compress(~isnan(...))` om te NaNs verwijderen.

```python
zenith = rec_tabel.col('zenith')
azimuth = rec_tabel.col('azimuth')
```

```python
zenith = zenith.compress(~isnan(zenith))
azimuth = azimuth.compress(~isnan(azimuth))
print "Er zijn %d events succesvol gereconstrueerd." % len(zenith)            
```

```python
zenith = degrees(zenith)
azimuth = degrees(azimuth)
```

```python
ax = plt.subplot(polar=True)
ax.scatter(zenith, azimuth)
```

```python
plt.hist(zenith, bins=arange(0,90., 5.), histtype='step')
plt.xlabel('zenith angle (degrees)')
plt.ylabel('counts')
plt.title('Zenith histrogram station 501.')
```

# Discrete oplossingen.

Selecteer events met 3 detectoren/tijden.
Dat zou discrete oplossingen moeten opleveren

Maar dat is niet zo!?!?!?!

```python
if '/bigdata' not in data:
    download_data(data, '/bigdata', 501, start=datetime(2016, 1, 1), end=datetime(2016, 1, 10))
```

```python
def filter_3_detectors(event):
    t = [event['t1'], event['t2'], event['t3'], event['t4']]
    t = [x for x in t if x >= 0.]
    if len(t) == 3:
        return True
    else:
        return False
```

```python
events = data.root.bigdata.events.read()
```

```python
from sapphire.utils import pbar
filter = [filter_3_detectors(event) for event in pbar(events)]
events = events.compress(filter)
```

```python
t1 = events['t1']
t2 = events['t2']
t3 = events['t3']
t4 = events['t4']
```

```python
def check_2_5ns(event):
    """assert arrival times are multiples of 2.5 ns"""
    t = [event['t1'], event['t2'], event['t3'], event['t4']]
    t = [x for x in t if x >= 0.]
    
    for time in t:
        assert not time % 2.5
    diff = t[0] - t[1] - t[2]
    assert not diff % 2.5
        
for event in pbar(events):
    check_2_5ns(event)
```

```python
from sapphire import HiSPARCStations
s501 = HiSPARCStations([501]).get_station(501)
from sapphire.analysis.direction_reconstruction import EventDirectionReconstruction
eventrec = EventDirectionReconstruction(s501)
```

```python
#from sapphire.analysis.direction_reconstruction import DirectAlgorithm
#eventrec.direct = DirectAlgorithm
#eventrec.fit = None
theta, phi, _ = eventrec.reconstruct_events(events, offsets=[0., 0., 0., 0.])
```

```python
zenith = [a for a in theta if not isnan(a)]
azimuth = [a for a in phi if not isnan(a)]
zenith = degrees(zenith)
azimuth = degrees(azimuth)
```

```python
ax = plt.subplot(polar=True)
ax.scatter(zenith, azimuth)
```

```python

```
