# 2 HiSPARC-API
## Inleiding
Informatie over en van meetstations (configuraties, events, coincidenties) is op
te halen via de publieke database op http://data.hisparc.nl

Dit notebook gaat over het ophalen en verwerken van gegevens van meetstations
GPS posities, hardwareserienummers, detector tijdoffsets en PMT spanning via de
**HiSPARC API**.

Via de API kan door middel van een URL informatie uit de publieke database over
stations worden opgevraagd:
- http://data.hisparc.nl/api/clusters/  (de clusters in het netwerk in JSON)
- http://data.hisparc.nl/api/station/22/  (informatie over station 22 in JSON)
- http://data.hisparc.nl/show/source/gps/501/  (De GPS posities van station 501,
in TSV)

Bovenstaande links zijn ook te vinden als links op http://data.hisparc.nl.
Meer informatie over de HiSPARC API is te vinden via:
http://docs.hisparc.nl/publicdb/api_tutorial.html

In SAPPHiRE is de informatie uit de API op twee manieren beschikbaar:
1. Direct uitlezen van API informatie via `Station()` en `Network()`
2. Analyse van groepen van stations (clusters) via `HiSPARCStations()` en
`HiSPARCNetwork()`

## Uitlezen van de API via Network() en Station()

```python
from sapphire import Network, Station
```

### Network()

Network is voor het ophalen van informatie over het netwerk via de API:

```python
network = Network()
print network.station_numbers()
```

```python
print network.clusters()
```

```python
print network.station_numbers(cluster=2000)
```

### Station()
`Station()` kan informatie over een meetstation uit de API lezen.

De informatie uit de URL http://data.hisparc.nl/api/station/22/ (informatie over
meetstation 22, St. Ignatius, Adam) kunnen we ook met Station() opvragen:

```python
print Station(22).info
```

Een belangrijke eigenschap is de plaats waar een station zich bevindt.

Deze informatie is te vinden via de API met de URL:
http://data.hisparc.nl/show/source/gps/22/

Via Station():

```python
print Station(22).gps_locations
```

Dit zijn *alle* GPS posities van meetstation 22.

We zien hier een array met daarin een aantal lijsten. Het eerste item op iedere
regel legt vast vanaf welke moment, een GPS-tijdstempel, een station volgens de
HiSPARC database op een plaats stond. Na dit GPS-tijdstempel zijn
achtereenvolgens de lengte, breedte en hoogte van het station volgens GPS-84
gegeven.
([https://nl.wikipedia.org/wiki/WGS_84](https://nl.wikipedia.org/wiki/WGS_84))

We kunnen ook de *huidige* locatie ophalen:

```python
from sapphire.transformations.clock import datetime_to_gps
from datetime import datetime

ts = datetime_to_gps(datetime.now())
print "timestamp: ", ts
print "GPS: ", Station(22).gps_location(ts)
```

# Opgave
Bepaal de GPS coordinaten van station 22 op 5 December 2012:

```python
ts = datetime_to_gps(datetime(2012, 12, 5))
print "timestamp: ", ts
print "GPS: ", Station(22).gps_location(ts)
```

## Clusters via HiSPARCStations() en HiSPARCNetwork()

### HiSPARCStations()
Met behulp van HiSPARCStations() kunnen we een cluster van een aantal
meetstations aanmaken. HiSPARCNetwork() maakt een cluster van alle meetstations
in het netwerk.

```python
from sapphire import HiSPARCStations, HiSPARCNetwork
```

We maken een cluster van vier meetstations:

```python
stations = [301, 303, 304, 305]
cluster = HiSPARCStations(stations)
```

Van het cluster kunnen we posities van meetstations, detectoren, maar ook
onderlinge afstanden e.d. eenvoudig bepalen.

```python
for station in cluster.stations:
    print station.number, station.get_lla_coordinates()
```

### set_timestamp()
Een essentiele eigenschap van een cluster is dat we een tijdstempel kunnen
opgeveven. De informatie die het cluster ophaalt en berekent is geldig op het
tijdstip dat overeenkomt met het tijdstempel.

In het geval van een coincidentie op timestamp 1368403200 willen we weten waar
de stations op dat gegeven tijdstip stonden:

```python
ts = 1368403200
cluster.set_timestamp(ts)
print "LLA coordinaten op timestamp = %d\n" % ts
for station in cluster.stations:
    print station.number, station.get_lla_coordinates()
```

# Opgave:

In Alphen a/d Rijn staat een driehoek van stations: [3301, 3302, 3303]

Maak een plot van de onderlinge ligging van de stations.

*hint:* `get_coordinates()` geeft de (x, y, z, alpha)-coordinaten van een
station in een cluster zoals HiSPARCStations(). (x,y,z) zijn in meter, alpha is
de orientatiehoek in graden.

```python
import matplotlib.pyplot as plt
%matplotlib inline

stations = [3301, 3302, 3303]
cluster = HiSPARCStations(stations)

for station in cluster.stations:
    x, y, z, alpha = station.get_coordinates()
    plt.plot(x, y, 'or', markersize=10)
    plt.text(x, y, station.number)
```

### HiSPARCNetwork()

Een cluster van het hele network kunnen we maken met HiSPARCNetwork(). Omdat
daarbij informatie van *alle* stations uit het netwerk via de API worden
opgehaald, is het aanmaken van HiSPARCNetwork() redelijk traag.

#### force_stale
Door gebruik te maken van de optie `force_stale=True` wordt die informatie
*niet* uit de API opgehaald, maar gelezen uit SAPPHiRE. Deze informatie is
mogelijk veroudert, maar wel veel sneller beschikbaar.

De optie 'force_stale' is ook beschikbaar voor Station(), Network() en
HiSPARCStations()

```python
network = HiSPARCNetwork(force_stale=True)
```

De *UserWarnings* kunnen hier genegeerd worden.

```python
print "De afstand tussen 505 en 509 is %.f m" % network.calc_distance_between_stations(505, 509)
```

Ook voor het hele netwerk kan een timestamp worden opgegeven:

```python
network.set_timestamp(datetime_to_gps(datetime(2015,3, 4)))
```

In combinatie met clusters maken we vaak gebruik van de functie
`itertools.combinations`:

```python
stations = [3, 22, 501, 509]
from itertools import combinations
for eerste, tweede in combinations(stations, 2):
    print eerste, tweede
```

# Opgave:

Maak een lijst van de onderlinge afstanden van meetstation in cluster Leiden,
waarvoor de afstand kleiner is dan 1000 m.


```python
from sapphire import Network, HiSPARCStations
stations = Network().station_numbers(cluster=2000)
cluster = HiSPARCStations(stations, force_stale=True)
for sn1, sn2 in combinations(stations, 2):
    d = cluster.calc_distance_between_stations(sn1, sn2)
    if d < 1000:
        print "De afstand tussen station %d en %d is %.f m." % (sn1, sn2, d)
    
```
