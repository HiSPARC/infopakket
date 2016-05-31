# Recept station map

Plot station (en detector) LLA coordinaten op OpenStreetMap tiles.

```{.python .input}
from sapphire import HiSPARCStations
import matplotlib.pyplot as plt
%matplotlib inline
```

Deze worksheet gebruikt `smopy` om OpenStreetMap tiles te downloaden en plotten.
`smopy` kan geinstalleerd worden met `pip install smopy`.

Helaas bevat de laatste versie van `smopy` (0.0.3) een aantal bugs, waardoor de
schaal van de kaarten niet klopt. Download daarom het bestand `smopy.py` [van
deze link (klik!)](https://gist.githubusercontent.com/tomkooij/34cbc1f8f1fb22a0a
0f1d0c4ce462618/raw/b44abd1e0eb32687defc3d1a444d044af08baeef/smopy.py) en sla
deze op in dezelfde map als dit notebook.

```{.python .input}
import smopy
```

Als deze import een fout oplevert, lees dan hierboven nogmaals!

```{.python .input}
def get_latlontext(cluster):
    """
    Create list of latitude, longitudes and (legend texts)
        of stations and detectors in a cluster
       
    cluster = HiSPARCStations object
    
    """
    latlon = []
    for station in cluster.stations:
        latitude, longitude, _ = station.get_lla_coordinates()
        latlon.append((latitude, longitude, station.number))
        for detector in station.detectors:
            latitude, longitude, _ = detector.get_lla_coordinates()
            latlon.append((latitude, longitude, None))
    return latlon
```

Bovenstaande functie maakt van een `HiSPARCStations` cluster object een lijst
met lla coordinaten.

Test:

```{.python .input}
print get_latlontext(HiSPARCStations([102], force_stale=True))
```

```{.python .input}
def plot_cluster_OSM(stations, plot_detectors=False, force_stale=True):
    """Plot cluster (station and detectors) on top of OSM tiles 
    
    cluster: (list of) station number(s)
    plot_detectors: if True: plot detectors
    force_stale: if True: do not get lla info from api, but use local data
    """
    
    if isinstance(stations, int):
        stations = [stations]
    
    cluster = HiSPARCStations(stations, force_stale=force_stale)
    
    latlon = get_latlontext(cluster)
    lat = [ll[0] for ll in latlon]
    lon = [ll[1] for ll in latlon]
    
    map = smopy.Map((min(lat), min(lon)), (max(lat), max(lon)), margin=.01)
    ax = map.show_mpl(figsize=(10,10), dpi=200)
    for px, py, label in latlon:
        x, y = map.to_pixels(px, py)
        if label is not None:
            ax.plot(x, y, 'or', ms=10, mew=2)
            ax.text(x, y, '  '+str(label))
        elif plot_detectors:  # detector
            ax.plot(x, y, 'xb', ms=10)
```

```{.python .input}
plot_cluster_OSM((102, 104, 105), plot_detectors=True)
```

```{.python .input}
plot_cluster_OSM(range(501, 512))
```

```{.python .input}
plot_cluster_OSM((501, 508, 510), plot_detectors=True)
```
