# Recept: Download events van een station

```python
# dit notebook werkt onder Python 2 en 3
from __future__ import division, print_function
```

We maken een HDF5 bestand 'data.h5' en downloaden 3 dagen data (events) van
station 501:


```python
import tables
data = tables.open_file('data.h5', 'a')
```

De opties open_file zijn:
- 'a': append: Open het bestand, zodat er data kan worden toegevoegd
- 'w': write: Overschrijf het bestand. Alle bestaande data in het bestand wordt
overschreven.
- 'r': read: Alleen lezen.

Start en eindtijdstippen:


```python
from datetime import datetime
start = datetime(2016, 1, 1)
end = datetime(2016, 1, 3)
```


```python
from sapphire import download_data
download_data(data, '/s501', 501, start, end)
```

De events zijn opgeslagen in de tabel '/s501/events' (data.root.s501.events)


```python
print(data)
```


```python
events = data.root.s501.events[:5]
print(events)
```


```python
data.close()
```

# Coincidenties downloaden

Coincidenties tussen HiSPARC stations (binnen een afstand van 1000 m) worden
automatisch bepaald door de publieke database ([http://data.hisparc.nl/).
Het downloaden van coincidenties gaat alsvolgt:


```python
import tables
FILENAME = 'data.h5'
data = tables.open_file(FILENAME, 'a')
```


```python
from datetime import datetime
start = datetime(2016, 1, 1)
end = datetime(2016, 1, 2)
```


```python
from sapphire import download_coincidences
download_coincidences(data, stations=[502, 505, 504, 509], start=start, end=end, n=3)
```

We hebben nu coincidenties tussen stations 502, 505, 504 en 509, waarbij
minstens 3 stations betrokken waren gedownload.

De tabel `coincidences` in de groep `coincidences` bevat de informatie die we
zoeken:


```python
print(data.root.coincidences.coincidences)
```

Meer informatie over het koppelen van station events aan coincidenties is te
vinden in het recept over CoincidenceQuery.

## Opgave
Rond de jaarwisseling 2015-2016 is er iets vreemds gebeurd rondom de
meetstations in Middelharnis (3201-3203).

Download de data van een uur voor en een uur na de jaarwisseling in het HDF5
bestand 'middelharnis.h5'


```python
import tables
from sapphire import download_data
from datetime import datetime

start = datetime(2015, 12, 31, 23)
end = datetime(2016, 1, 1, 1)
stations = [3201, 3202, 3203]

with tables.open_file('middelharnis.h5', 'w') as data:

    for station in stations:
        print('station: %d.' % station)
        path = '/s%d' % station
        download_data(data, path, station, start, end)

    print(data)
```
