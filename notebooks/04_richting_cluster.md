# 4 Richtingreconstructie met een cluster

Deze notebooks werken alleen met Python 3.

Richtingreconstructie is nauwkeuriger als er een aantal stations dicht bij
elkaar liggen. Deze stations zijn (een onderdeel van) een cluster. Als meerdere
stations een event meten, wordt dit een coincidentie genoemd.

Eerst worden enkele modules geimporteerd:
* tables: deze module bevat methoden om met tabellen te werken.
* datetime: deze module geeft een standaard format voor datum en tijd.
* matplotlib: een module waarmee plotjes gemaakt kunnen worden.
* sapphire: de HiSPARC module waarmee gegevens van meetstations op te halen
zijn.

```python
import tables
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt
%matplotlib inline
from sapphire import download_coincidences, ReconstructESDCoincidences
```

Voordat we op zoek kunnen naar coincidenties, moeten we de meetgegevens ophalen.
HiSPARC gegevens moeten in een tabel worden geplaatst. Met de 'with' opdracht
wordt hieronder een .h5 bestand voor de tabel op een usb-stick, harde schijf
o.i.d. aangemaakt. Deze wordt daarna met gegevens gevuld. Tot slot wordt het
bestand afgesloten.

```python
with tables.open_file('data_coincidences.h5', 'w') as data:
    download_coincidences(
        data,
        stations=[501, 502, 508],
        start=datetime(2015, 12, 1),
        end=datetime(2016, 1, 31),
        n=3,
    )
```

Als de meetgegevens opgeslagen zijn, kunnen we deze bewerken. De bewerkte
gegevens worden in een variabele `rec` opgeslagen.

```python
with tables.open_file('data_coincidences.h5', 'a') as data:
    rec = ReconstructESDCoincidences(data, overwrite=True, progress=True)
    rec.reconstruct_and_store()
```

De richtingreconstructie levert `rec.theta ` en `rec.phi` lijsten met
respectievelijk alle gereconstrueerde
zenit- en azimuthoeken. Deze hoeken zijn `NaN` (Not A Number) als de richting
niet gereconstrueerd kon worden.

Met behulp van de functie `np.isnan()` kunnen we de NaNs verwijderen:

```python
zenit = [a for a in rec.theta if not np.isnan(a)]
azimut = [a for a in rec.phi if not np.isnan(a)]
print("Er zijn %d events succesvol gereconstrueerd." % len(zenit))            
```

Deze gegevens zijn in een met matplotlib in een polar plot af te beelden.
Bovenaan is aangegeven hoe matplotlib wordt geimporteerd. Alle gereconstrueerde
coordinaten bestaande uit een azimuth- (phi) en zenith-hoek (theta) worden in
een plot afgebeeld.

```python
plt.figure(1)
ax = plt.subplot(111, polar=True)
plt.scatter(azimut, zenit)
plt.show()
```

Er is ook een verdeling van het aantal events als functie van de zenith-hoek te
maken. De waarden worden verdeeld over van te voren vastgestelde intervallen.
Deze intervallen worden bins genoemd. in de eerste regel worden de bins tussen 0
en pi/2 gedefinieerd (0 tot 90 graden), de breedte is 0.5 graad.

```python
bins = np.arange(0, np.pi/2., np.pi/180.)
plt.figure(2)
plt.hist(zenit, bins, histtype='step')
plt.show()
```

De code is op te slaan met "`%save this 1-7`". Voor "`this`" kan iedere naam
worden ingevuld, "`1-7`" geeft aan welke cellen worden opgeslagen. Het bestand
"`this.py`" wordt opgeslagen.

```python
%save this 1-7
```

Met "`%run this.py`" wordt het opgeslagen bestand uitgevoerd.

```python
#%run this.py
```
