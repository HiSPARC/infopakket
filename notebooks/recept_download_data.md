# Recept: Download events van een station

We maken een HDF5 bestand 'data.h5' en downloaden 3 dagen data (events) van
station 202

```{.python .input  n=1}
import tables
data = tables.open_file('data.h5', 'a')
```

De opties open_file zijn:
- 'a': append: Open het bestand, zodat er data kan worden toegevoegd
- 'w': write: Overschrijf het bestand. Alle bestaande data in het bestand wordt
overschreven.
- 'r': read: Alleen lezen.

Start en eindtijdstippen:

```{.python .input  n=2}
from datetime import datetime
start = datetime(2016, 1, 1)
end = datetime(2016, 1, 3)
```

```{.python .input  n=3}
from sapphire import download_data
download_data(data, '/s202', 202, start, end)
```

De events zijn opgeslagen in de tabel '/s202/events' (data.root.s202.events)

```{.python .input  n=4}
print data
```

```{.python .input  n=5}
events = data.root.s202.events[:5]
print events
```

```{.python .input  n=6}
data.close()
```

# Opgave

Rond de jaarwisseling 2015-2016 is er iets vreemds gebeurd rondom de
meetstations in Middelharnis (3201-3203).

Download de data van een uur voor en een uur na de jaarwisseling in het HDF5
bestand 'middelharnis.h5'

```{.python .input  n=7}
import tables
from sapphire import download_data
from datetime import datetime

start = datetime(2015, 12, 31, 23)
end = datetime(2016, 1, 1, 1)
stations = [3201, 3202, 3203]

with tables.open_file('middelharnis.h5', 'w') as data:

    for station in stations:
        print 'station: %d.' % station
        path = '/s%d' % station
        download_data(data, path, station, start, end)

    print data
```

# Coincidenties downloaden

Coincidenties tussen HiSPARC stations (binnen een afstand van 1000 m) worden
automatisch bepaald door de publieke database ([http://data.hisparc.nl/).
Het downloaden van coincidenties gaat alsvolgt:

```{.python .input  n=5}
import tables
FILENAME = 'data.h5'
data = tables.open_file(FILENAME, 'a')
```

```{.python .input  n=12}
from datetime import datetime
start = datetime(2016, 1, 1)
end = datetime(2016, 1, 2)
```

```{.python .input  n=13}
from sapphire import download_coincidences
download_coincidences(data, stations=[502, 505, 504, 509], start=start, end=end, n=3)
```

```{.json .output n=13}
[
 {
  "name": "stderr",
  "output_type": "stream",
  "text": "100%|#############################################################|Time: 0:00:00\n"
 }
]
```

We hebben nu coincidenties tussen stations 502, 505, 504 en 509, waarbij
minstens 3 stations betrokken waren gedownload.

De tabel `coincidences` in de groep `coincidences` bevat de informatie die we
zoeken:

```{.python .input  n=18}
print data.root.coincidences.coincidences
```

```{.json .output n=18}
[
 {
  "name": "stdout",
  "output_type": "stream",
  "text": "/coincidences/coincidences (Table(4959,)) ''\n"
 }
]
```

Meer informatie over het koppelen van station events aan coincidenties is te
vinden in het recept over CoincidenceQuery.
