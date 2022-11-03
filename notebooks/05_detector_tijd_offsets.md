# Recept: Detector tijd offsets

Deze notebooks werken alleen met Python 3.

Tijdsverschillen tussen detectoren

```python
import numpy as np
import matplotlib.pyplot as plt
%matplotlib inline
```

## Events

1 dag data van station 501

```python
FILENAME = 'events.h5'
station = 501
```

```python
from datetime import datetime
start = datetime(2015, 5, 1)
end = datetime(2015, 5, 2)
```

```python
import tables
data = tables.open_file(FILENAME, 'a')
```

```python
from sapphire import download_data
if '/events' not in data:
    print('downloading events')
    download_data(data, '/', station, start, end)
else:
    print('events already downloaded.')
```

```python
events = data.root.events
events
```

## Bepalen van tijdsverschil

```python
t1 = events.col('t1')
t3 = events.col('t3')
```

```python
dt = t3 - t1
_ = plt.hist(dt, bins = 50, histtype='step')
```

In het histogram valt op dat er *vreemde* pieken te zien zijn rond dt = 0 en dt
= 1000 en dt = -1000.

Dit komt omdat er veel events zijn waarbij detector 1 en 3 geen deeltjes hebben
detecteerd, of niet allebei. Als er geen aankomsttijd van een deeltje
gereconstrueerd kon worden is de aankomsttijd `t = -999`. Allereerst filteren we
de tijdsverschillen daarom op `t > 0.`. Vervolgens filteren we de data op
`pulshoogte > 200 (ADC)`, zodat er we alleen events overhouden waarbij de
deeltjes dichtheid in de detector voldoende groot is:

```python
ph = events.col('pulseheights')
ph1 = ph[:, 0]
ph3 = ph[:, 2]
dt_1_3 = dt.compress((t1 > 0.) & (t3 > 0.) & (ph1 > 200.) & (ph3 > 200.))
_ = plt.hist(dt_1_3, bins=50, histtype='step')
```

We zien `data` rond dt = 0 en ruis daarom heen. We plotten nu alleen
tijdsverschillen kleiner dan ongeveer 100 ns:

```python
bins=np.arange(-100, 100, 5)
n, _, _ = plt.hist(dt_1_3, bins=bins, histtype='step')
```

Het tijdsverschillen zijn ongeveer normaal verdeeld, maar het gemiddelde is niet
0. De verschuiving van het gemiddelde is de `tijd offset`, of hier 'detector
tijd offset'

## Detector tijd offset bepalen uit het histogram

Het gemiddelde is:

```python
np.mean(dt_1_3)
```

We kunnen ook een normale verdeling fitten:

```python
def gauss(x, N, mu, sigma):
    """Gaussian distribution"""
    return N * np.exp(-0.5 * ((x - mu) / sigma) ** 2)
```

```python
from scipy.optimize import curve_fit
x = (bins[:-1] + bins[1:]) / 2
popt, pcov = curve_fit(gauss, x, n)
```

De parameter `popt` bevat de parameters uit de fit:

```python
N, mu, sigma = popt
mu, sigma
```

```python
plt.hist(dt_1_3, bins=bins, histtype='step')
plt.plot(bins, gauss(bins, N, mu, sigma), 'r--')
plt.legend(['fit','dt'])
plt.xlabel('t3 - t1 [ns]')
plt.ylabel('counts')
plt.xlim((-60, 70))
```

## Detector tijd offsets ophalen mbv de API

De publieke database (http://data.hisparc.nl) bepaalt dagelijks de detector tijd
offsets voor alle stations.

De informatie is via de API beschikbaar:

```python
from sapphire import Station
s501 = Station(501)
```

```python
from sapphire.transformations.clock import datetime_to_gps
ts = datetime_to_gps(datetime(2016,5,1))
ts
```

```python
s501.detector_timing_offset(ts)
```

```python
o1, o2, o3, o4 = s501.detector_timing_offset(ts)
print("De detector tijd offset tussen detector 3 en 1 op is: %2.1f ns (t = %d)" % ((o3 - o1), ts))
```

```python
data.close()
```
