# Onderzoek de data van je eigen station

```python
STATION = 15  # gvdveen
```

```python
import sapphire
import matplotlib.pyplot as plt
import numpy as np
import datetime as dt
%matplotlib inline
```

```python
data = sapphire.quick_download(STATION)
```

Na enige tijd verschijnt hierboven een regel zoals:
"`100%|############################################################|Time: 0:00:06`"

Soms is de download zo snel dat deze regel niet wordt afgedrukt.

De variabele "`data`" bevat nu een set meetgegevens. Deze set is af te drukken.

```python
# Download data van een andere dag
# start = dt.datetime(2019, 3, 20)
# end = dt.datetime(2019, 3, 21)
# sapphire.download_data(data, '/s%d' % STATION, start, end)
```

```python
print(data)
```

Het "`data`" bestand heeft een hierarchise opbouw. In "`data`" zit een
RootGroup, deze is te benaderen met "`data.root`". Hierin zit weer een groep
"`s102`", deze is te benaderen met "`data.root.s102`". Hierin zit een tabel
"`events`".

## Werken met een events tabel
Voor het gemak maken we een variable
`events` die naar de eventstabel van het station wijst:

De tabel heeft een
bepaalde plaats het HDF5 data bestand: `/s????/events` waarbij `????` staat voor
het station nummer. Deze plaats heet een `node`:

```python
node_naam = '/s%d/events' % STATION
node_naam
```

```python
event_tabel = data.get_node(node_naam)
event_tabel
```

Dit is een tabel tienduizenden regels. Elke regel is een event.

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
werkblad [http://docs.hisparc.nl/infopakket/pdf/traces.pdf](http://docs.hisparc.nl/infopakket/pdf/traces.pdf)
wordt de natuurkundige betekenis van deze
getallen beschreven.  De afbeeldingen in dit werkblad zijn afkomstig uit het
interactieve werkblad [http://data.hisparc.nl/media/jsparc/jsparc.html](http://d
ata.hisparc.nl/media/jsparc/jsparc.html). Let op, computers tellen vanaf "`0`"
en niet vanaf "`1`"


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
print("pulshoogte detector 1: %d ADC (eerste event)" % first_event['pulseheights'][0])
```

## Timestamps
Vaak is het eenvoudiger om een hele *kolom* bijvoorbeeld `timestamp` in een keer te bekijken.

Eerst lezen we de hele tabel in het geheugen. Het object `events` is de gehele tabel:

```python
events = event_tabel.read()
```

De variabele `ts` wijst naar de kolom `timestamp` en we bekijken de eerste 30 regels (events):

```python
ts = events['timestamp']
ts[:30]
```

```python
ns = events['nanoseconds']
ns[:30]
```

```python
plt.figure(figsize=(10,4))
plt.hist(ns, histtype='step')
plt.ylabel('aantal')
plt.xlabel('nanoseconds deel van de timestamp')
plt.title('ESD Events van een enkele dag van station %d' % STATION)
```

```python
plt.figure(figsize=(10,4))
plt.hist(ts, bins=24, histtype='step')
plt.ylabel('aantal')
plt.xlabel('timestamp [s]')
plt.title('ESD Events van een enkele dag van station %d' % STATION)
```

```python
eerste_ts = ts[0]
eerste_ts
```

```python
# linker en rechter grenzen van bins van 1 uur (3600 s) breed vanaf de eerste timestamp (1 dag)
bins = [eerste_ts + 3600 * h for h in range(25)]
```

```python
plt.figure(figsize=(10,4))
plt.hist(ts, bins=bins, histtype='step')
plt.ylabel('aantal')
plt.xlabel('tijd vanaf middernacht [h]')
plt.xticks(bins, range(25))
plt.title('ESD Events van een enkele dag van station %d' % STATION)
```

# MIPs

```python
n1 = event_tabel.col('n1')
plt.figure(figsize=(10,4))
plt.hist(n1, bins=np.arange(0.3, 5., .1), histtype='step')
plt.title('Station %d: Number of particles in detector 1' % STATION)
plt.xlabel('number of particles (MIP)')
plt.ylabel('counts')
```

## Pulshoogte

Maak een histogram van de pulshoogtes van detector 1 en 2 van het
station.

Een voorbeeld is hier te zien: http://data.hisparc.nl/show/stations/15

```python
ph = event_tabel.col('pulseheights')
ph1 = ph[:, 0]
ph2 = ph[:, 1]
```

'pulseheights' is een *matrix*:
- `[:, 0]` is de gehele eerste rij, dwz de pulshoogtes per event van detector 0
- `[:, 1]` is de gehele tweede rij, dwz de pulshoogtes per event van detector 1

```python
plt.figure(figsize=(10,4))
plt.hist(ph1, bins=np.arange(0, 2000., 20.), histtype='step', log=True)
plt.hist(ph2, bins=np.arange(0, 2000., 20.), histtype='step', log=True)
plt.title('Station %d: Pulseheights' % STATION)
plt.xlabel('Pulseheight (ADC)')
plt.ylabel('counts')
plt.legend(['detector 1', 'detector 2' ])
plt.ylim(10, 1e4)
```
