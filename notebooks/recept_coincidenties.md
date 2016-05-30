# Recept Coincidenties bepalen
Coincidenties tussen meetstations worden automatisch bepaald door de publieke
database. Ze kunnen eenvoudig worden gedownload, zoals in een eerder notebook is
beschreven.

Data van teststations wordt echter niet meegenomen in het bepalen van
coincidenties. In dit notebook worden coincidenties tussen de een teststation en
nabijgelegen meetstations bepaald aan de hand van gedownloade events van de
betreffende stations.

```python
from datetime import datetime
import tables
from sapphire import download_data
```

Teststation 599 bevindt zich in de buurt van meetstation 501 en 510 (Nikhef,
Science Park, Amsterdam)
We bepalen de coincidenties tussen deze drie stations op 1 Mei 2016:

Om het aantal coincidenties wat te beperken, downloaden we alleen data tussen
0:00 en 3:00.

```python
STATIONS = [501, 510, 599]
START = datetime(2016, 5, 1)
END = datetime(2016, 5, 1, 3)
FILENAME = 'coinc_with_s599.h5'
```

```python
data = tables.open_file(FILENAME, 'a')
```

Eerst downloaden we de events per station:

```python
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

```python
print data
```

## Coincidenties bepalen tussen events
We gebruiken de SAPPHiRE class `CoincidencesEDS` om coincidenties tussen events
in de drie eventtabellen te bepalen:

```python
from sapphire import CoincidencesESD
coin = CoincidencesESD(data, '/coincidences', station_groups, overwrite=True)
coin.search_and_store_coincidences(station_numbers=STATIONS)
```

```python
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

```python
coinc_tabel = data.root.coincidences.coincidences
print coinc_tabel
```

```python
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

```python
s501 = coincidences['s501']
s510 = coincidences['s510']
s599 = coincidences['s599']
```

De functie `sum()` telt alle waarden die `True` zijn op:

```python
print "Er zijn %d events van station 501 betrokken bij coincidenties tussen 501, 510 en/of 599" % sum(s501)
```

```python
print "Er zijn %d coincidenties tussen 501, 510 en 599" % sum(s510 & s501 & s599)
```

# Opgave

Bepaal het aantal coincidenties tussen 501 en 599 waar 510 niet bij betrokken
is.

*Hint:* gebruik de tilde: ~ voor het tegengestelde van een array.

```python
sum(s501 & s599 & ~s510)
```

# Filteren van coincidenties

Door gebruik te maken van `compress()` en de kolommen `s501`, `s510` en `s599`
kunnen we coincidenties filteren op de betrokken stations:

```python
coinc_510_501 = coincidences.compress(s501 & s510)
coinc_510_501
```

In deze selectie zitten ook coincidenties tussen 501, 510 en 599:

```python
print "Er zijn %d coincenties tussen 510 en 511 waarbij ook 599 betrokken is" % sum(coinc_510_501['s599'])
```

Dit komt natuurlijk overeen met het eerder gevonden aantal coincidenties tussen
501, 510 en 599.

We kunnen 599 ook uitsluiten:

```python
coinc_510_501_zonder599 = coincidences.compress(s501 & s510 & ~s599)
coinc_510_501_zonder599
```

# Events aan coincidenties koppellen: CoincidenceQuery

We kunnen ook de events bij een coincidentie zoeken. Dit is niet triviaal. De
tijdstempel van een coincidentie hoort bij het eerste event, maar dit kan
telkens een ander event zijn uit een groep stations. De `/coincidence` group
bevat informatie in `c_index` en `s_index` om e.e.a. te koppelen. Maar ook via
deze weg is enig programmeer werk.

SAPPHiRE CoincidenceQuery kan het bijelkaar zoeken van coincidenties
automatiseren:

```python
data.close()
```

CoincidenceQuery opent zelf een HDF5 bestand, we hebben het bestand daarom
gesloten.

We initialiseren CoincidenceQuery. Als argument geven we alleen het bestandsnaam
op:

```python
from sapphire import CoincidenceQuery
cq = CoincidenceQuery(FILENAME)
```

Eerst maken we een lijst van alle concidenties (in dit geval tussen stations
501, 510 en 599):

```python
coincidences = cq.all(STATIONS, iterator=True)
```

Nu gebruiken we de functie `all_events`:

Deze functie geeft een lijst van coincidenties. Elke concidentie is een lijst
van tuples, met telkens het stationnummer en het bijbehorende event.

Met een dubelle for-loop kunnen we de informatie "uitpakken":

```python
for id, coinc in enumerate(cq.all_events(coincidences)):
    print "Coincidentie: %d" % id
    for station, event in coinc:
        print "Station: %d. Event id: %d. Timestamp: %d " % (station, event['event_id'], event['ext_timestamp'])
```

Met `finish()` sluiten we CoincidenceQuery en wordt ook het HDF5 bestand
gesloten.

```python
cq.finish()
```

# Opgave

Het SciencePark in Amsterdam heeft 11 meetstations. Er zijn slechts enkele
coincidenties per dag, waarbij alle stations betrokken worden.

Bepaal de extended timestamps van events in coincidenties met 9 of meer
meetstations op een willekeurige dag in 2016.

Kijk eerst op http://data.hisparc.nl hoeveel coincidenties er die dag waren.
Niet alle stations hebben elke dag data en station 507 staat binnen!

```python

```
