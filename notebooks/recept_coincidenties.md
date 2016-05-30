# Recept Coincidenties bepalen
Coincidenties tussen meetstations worden automatisch bepaald door de publieke
database. Ze kunnen eenvoudig worden gedownload, zoals in een eerder notebook is
beschreven.

Data van teststations wordt echter niet meegenomen in het bepalen van
coincidenties. In dit notebook worden coincidenties tussen de een teststation en
nabijgelegen meetstations bepaald aan de hand van gedownloade events van de
betreffende stations.

```{.python .input}
from datetime import datetime
import tables
from sapphire import download_data
```

Teststation 599 bevindt zich in de buurt van meetstation 501 en 510 (Nikhef,
Science Park, Amsterdam)
We bepalen de coincidenties tussen deze drie stations op 1 Mei 2016:

Om het aantal coincidenties wat te beperken, downloaden we alleen data tussen
0:00 en 3:00.

```{.python .input}
STATIONS = [501, 510, 599]
START = datetime(2016, 5, 1)
END = datetime(2016, 5, 1, 3)
FILENAME = 'coinc_with_s599.h5'
```

```{.python .input}
data = tables.open_file(FILENAME, 'a')
```

Eerst downloaden we de events per station:

```{.python .input}
station_groups = ['/s%d' % station for station in STATIONS]

for station, group in zip(STATIONS, station_groups):
    print "Station %d in group: %s." % (station, group),
    if group not in data:
        print "Downloading data: "
        download_data(data, group, station, START, END)
    else:
        print "group %s already in datafile." % group
```

De HDF5 file heeft nu 3 events tabellen:
- /s501/events
- /s510/events
- /s599/events

```{.python .input}
print data
```

## Coincidenties bepalen tussen events
We gebruiken de SAPPHiRE class `CoincidencesEDS` om coincidenties tussen events
in de drie eventtabellen te bepalen:

```{.python .input}
from sapphire import CoincidencesESD
coin = CoincidencesESD(data, '/coincidences', station_groups, overwrite=True)
coin.search_and_store_coincidences(station_numbers=STATIONS)
```

```{.python .input}
print data
```

De HDF5 file heeft nu een nieuwe group '/coincidences' met daarin:
    - coincidences (table): coincidenties tabel
    - c_index (array)
    - s_index (array)

De c_index en s_index arrays kunnen gebruikt worden om events en coincidenties
aan elkaar te koppelen. SAPPHiRE kan dit echter automatisch. Zie
`CoincidenceQuery` verderop.

De tabel `/coincidences/coincidences` ziet er als volgt uit:

```{.python .input}
coinc_tabel = data.root.coincidences.coincidences
print coinc_tabel
```

```{.python .input}
coincidences = coinc_tabel.read()
coincidences[:10]
```

Elke regel is een coincidentie.

De eerste kolommen geven informatie over de `timestamp` van de coincidentie.
Daarna volgen een aantal kolommen met informatie over de shower die door
reconstructies ingevuld kunnen worden, maar nu nog leeg zijn: `azimuth`,
`zenith`, `size` en `energy`.

Tenslotte volgen drie kolommen: `s501`, `s502` en `s599`. De kolommen bevatten
de waarden `True` of `False` en geven aan of het betreffende station betrokken
is in de coincidentie.

We kunnen deze kolommen gebruiken om coincidenties te filteren:

```{.python .input}
s501 = coincidences['s501']
s510 = coincidences['s510']
s599 = coincidences['s599']
```

De functie `sum()` telt alle waarden die `True` zijn op:

```{.python .input}
print "Er zijn %d events van station 501 betrokken bij coincidenties tussen 501, 510 en/of 599" % sum(s501)
```

```{.python .input}
print "Er zijn %d coincidenties tussen 501, 510 en 599" % sum(s510 & s501 & s599)
```

# Opgave

Bepaal het aantal coincidenties tussen 501 en 599 waar 510 niet bij betrokken
is.

*Hint:* gebruik de tilde: ~ voor het tegengestelde van een array.

```{.python .input}
sum(s501 & s599 & ~s510)
```

# Filteren van coincidenties

Door gebruik te maken van `compress()` en de kolommen `s501`, `s510` en `s599`
kunnen we coincidenties filteren op de betrokken stations:

```{.python .input}
coinc_510_501 = coincidences.compress(s501 & s510)
coinc_510_501
```

In deze selectie zitten ook coincidenties tussen 501, 510 en 599:

```{.python .input}
print "Er zijn %d coincenties tussen 510 en 511 waarbij ook 599 betrokken is" % sum(coinc_510_501['s599'])
```

Dit komt natuurlijk overeen met het eerder gevonden aantal coincidenties tussen
501, 510 en 599.

We kunnen 599 ook uitsluiten:

```{.python .input}
coinc_510_501_zonder599 = coincidences.compress(s501 & s510 & ~s599)
coinc_510_501_zonder599
```
