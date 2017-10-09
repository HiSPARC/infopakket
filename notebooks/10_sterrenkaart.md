
# Reconstructies op een hemelkaart
In dit notebook worden de richtingen van
deeltjeslawines bepaald en geplot op een projectie van de (sterren)hemel.


```
# dit notebook werkt onder Python 2 en 3
from __future__ import division, print_function
```


```
# importeer modules en functies
from datetime import datetime

import numpy as np
import matplotlib.pyplot as plt
%matplotlib inline

import tables
from sapphire import (download_coincidences, ReconstructESDCoincidences,
                      HiSPARCStations)
from sapphire.utils import pbar
from sapphire.transformations.celestial import zenithazimuth_to_equatorial
```

## Download data

Download coincidenties tussen stations van het Science Park.
We nemen coincidenties tussen negen stations in een periode van een maand. Door
deze voorwaarde kiezen we showers met een hoge energie, waarvoor het interessant
is om de aankomstrichting uit de ruimte te onderzoeken.


Open een HDF5 bestand,
waarin we onze data opslaan:


```
DATAFILE = 'coinc.h5'
```


```
data = tables.open_file(DATAFILE, 'w')
```

Definieer de dataset:

* STATIONS = lijst van stations
* START = eerste tijdstip
in `datetime`
* END = laatste tijdstip als `datetime`
* N = minimum aantal
stations per coincidentie

Tip: Gebruik `datetime?` om informatie te krijgen
over het datetime object.

Suggestie: Gebruik coincidenties tussen
(bijvoorbeeld) minimaal zes stations.


```
STATIONS = [501, 502, 503, 505, 506, 508, 509, 510, 511]
START = datetime(2016, 1, 1)
END = datetime(2016, 2, 1)
N = 9
```

Download coincidenties uit de ESD ([data.hisparc.nl](data.hisparc.nl)) en sla ze
op in het HDF5 bestand:


```
download_coincidences(data, stations=STATIONS, start=START, end=END, n=N)
```


```
print("Aantal showers (coincidenties n=%d stations): %d " % (N, len(data.root.coincidences.coincidences)))
```

## Reconstrueer richting van de showers
Reconstrueer en verwijder showers
waarvan de richting niet gereconstrueerd konden worden (Zowel de zenit-hoek als
azimut van die showers is NaN).


```
rec = ReconstructESDCoincidences(data, overwrite=True)
rec.reconstruct_and_store()
```


```
recs = data.root.coincidences.reconstructions.read()
theta = recs['zenith']
recs = recs.compress(~np.isnan(theta))
```

Maak een histrogram van de zenit-hoeken om de kwaliteit van de data te
controleren:


```
plt.hist(recs['zenith'], histtype='step')
plt.title('Zenit-hoek verdeling')
plt.xlabel('zenit-hoek (rad)')
plt.ylabel('aantal')
plt.show()
```

## Coordinatentransformatie naar rechte-klimming en declinatie

De richting van
de events (`zenit-hoek` en `azimut` ten opzicht van een ENU-assenstelsel in het
cluster) wordt getransformeerd naar rechte klimming en declinatie.

Voor de
coordinatentransformatie naar rechte-klimming en declinatie is de
positie van
ENU-assenstelsel van het cluster nodig:


```
lla = HiSPARCStations(STATIONS).get_lla_coordinates()
lat, lon, alt = lla
print(lat, lon)
```

Reken elk event om naar rechte klimming (RA) en declinatie (DEC). En schaal deze
naar (-pi, pi) voor het plotten. Sla de RA,DEC paren op in de lijst `events`


```
events = []
for rec in pbar(recs):
    timestamp = rec['ext_timestamp'] / 1.e9
    theta = rec['zenith']
    phi = rec['azimuth']
    r, d = zenithazimuth_to_equatorial(lat, lon, timestamp, theta, phi)
    events.append((r-np.pi, d))
events = np.array(events)
```

Histrogram ter controle:


```
ra = np.degrees(events[:,0])
plt.title('Histrogram van rechte klimming (ra)')
n, bins, _ = plt.hist(ra, histtype='step')  # n is het aantal events per bin
plt.xlabel('ra (graden)')
plt.ylabel('aantal')
plt.xlim([-180, 179])
plt.ylim([0, 1.2*max(n)])
plt.show()
```


```
dec = np.degrees(events[:, 1])
plt.title('Histrogram van declinatie (dec)')
n, bins, _ = plt.hist(dec, histtype='step')  # n is het aantal events per bin
plt.xlabel('dec (graden)')
plt.ylabel('aantal')
plt.xlim([-90, 89])
plt.ylim([0, 1.2*max(n)])
plt.show()
```

# Definitie van plots

Hier worden de plot functies `plot_events_on_mollweide()`
en `plot_events_polar()` gedefinieerd.


```
# RA, DEC tuples van het steelpan asterisme in het sterrenbeeld Grote Beer
steelpan = np.array([[13.792222, 49.3167], [13.398889, 54.9333], [12.900556, 55.95],
                     [12.257222, 57.0333], [11.896944, 53.7000], [11.030833, 56.3833],
                     [11.062222, 61.7500], [12.257222, 57.0333]])
# Melkweg contouren als lijst van RA, DEC paren.
# `milky_way.npy` heeft *geen* verbinding tussen RA 23h59 en 0h00 en `milky_way_polar.npy` wel.
try:
    mw_contour = np.load('milky_way.npy')
    mw_contour_polar = np.load('milky_way_polar.npy')
except:
    mw_contour = mw_contour_polar = []
```


```
def plot_events_on_mollweide(events, filename=None):
    """Plot events (een lijst van RA, DEC tuples) op een kaart in Mollweide projectie"""

    # Let op: De RA-as is gespiegeld. Alle RA coordinates worden gespiegeld (negatief)
    # geplot.

    events = np.array(events)

    fig = plt.figure(figsize=(15, 15))
    ax = fig.add_subplot(111, projection="mollweide")
    # let op: De RA as is gespiegeld:
    ax.set_xticklabels(['22h', '20h', '18h', '16h', '14h', '12h', '10h', '8h', '6h', '4h', '2h'], fontsize='large')
    ax.grid(True)

    # plot milky way contours
    for ra_mw, dec_mw in mw_contour:
        ax.plot(-ra_mw, dec_mw, color='grey')

    # plot steelpan in UMa
    ra_uma = np.radians(steelpan[:, 0] / 24 * 360 - 180.)
    dec_uma = np.radians(steelpan[:, 1])
    ax.plot(-ra_uma, dec_uma, color='red')
    ax.scatter(-ra_uma, dec_uma, color='red')

    # plot Polaris
    ax.scatter(0., np.radians(90.), color='red')

    # plot Galactic Center (RA 17h45, DEC -29)
    ax.scatter(-np.radians(17.75 / 24 * 360 - 180.), np.radians(-29), color='red', marker='*')

    # plot reconstructions
    ax.scatter(-events[:,0], events[:,1], marker='x')
    if filename:
        plt.savefig(filename, dpi=200)
```


```
def plot_events_polar(events, filename=None):
    """Plot events (een lijst van RA, DEC paren) op een hemelkaart van de noordelijke hemel"""

    # Let op: De RA-as is gespiegeld. Alle RA coordinates worden gespiegeld (negatief)
    # geplot.

    events = np.array(events)

    fig = plt.figure(figsize=(15,15))
    ax = fig.add_subplot(111, projection="polar")

    # let op: De RA as is gespiegeld:
    ax.set_xticklabels(['12h', '9h', '6h', '3h', '0h', '21h', '18h', '15h'], fontsize='large')
    ax.set_yticklabels(['80', '70', '60', '50', '40', '30', '20', '10', '0'])

    ax.grid(True)
    ax.set_theta_zero_location("W")


    # plot milky way contours
    for ra_mw, dec_mw in mw_contour_polar:
        ax.plot(-ra_mw, 90. - np.degrees(dec_mw), color='grey')

    # plot UMa
    ra_uma = np.radians(steelpan[:, 0] / 24 * 360 - 180)
    dec_uma = np.radians(steelpan[:, 1])
    ax.plot(-ra_uma, 90. - np.degrees(dec_uma), color='red')
    ax.scatter(-ra_uma, 90. - np.degrees(dec_uma), color='red')
    # plot Polaris
    ax.scatter(0., 0., color='red')

    # plot reconstructions
    ax.scatter(-events[:,0], 90. - np.degrees(events[:,1]), marker='x')
    ax.set_rmax(90.0)
    if filename:
        plt.savefig(filename, dpi=200)
    plt.show()
```

# Maak plots


```
plot_events_on_mollweide(events, filename='noordelijke hemel.png')
```


```
plot_events_polar(events, filename='noordelijke hemel.png')
```


```
data.close()
```
