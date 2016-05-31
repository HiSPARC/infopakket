# Recept station layout

Haal de station layout op uit de API en plot

```python
import matplotlib.pyplot as plt
%matplotlib notebook
```

```python
from datetime import datetime
from math import sin, cos, radians
from sapphire import Station, datetime_to_gps
```

```python
s = Station(501)
layout = s.station_layout(datetime_to_gps(datetime(2016, 1, 1)))
```

De indeling van de station layout tsv is alsvolgt:
```
# This data contains the following columns:
#
# timestamp: time the layout was measured in seconds after 1970-1-1 [UNIX
timestamp]
# per detector (4x):
#     radius: distance to detector from GPS, in plane of GPS [meters]
#     alpha: angle between detector and true north as seen from GPS [degrees]
#     height: altitude of the detector above plane of GPS [meters]
#     beta: angle of the long side of the scintillator to true north [degrees]
#

```

layout is een lijst met daarin per detector: [radius, alpha, height, beta]

```python
detectors = []
for detector in layout:
    r, alpha, z, beta = detector
    x_det = r*sin(radians(alpha))
    y_det = r*cos(radians(alpha))
    detectors.append((x_det, y_det))
```

```python
detectors
```

```python
xs, ys = zip(*detectors)
max(ys)
plt.figure()
plt.plot(0,0, 'ro')
plt.text(0, 0, 'GPS')
for number, (x, y) in enumerate(detectors):
    plt.plot(x, y, 'xb')
    plt.text(x, y, str(number))
plt.xlim((min(xs)-5, max(xs)+5))
plt.ylim((min(ys)-5, max(ys)+5))
plt.ylabel('distance [m] north up -->')
plt.xlabel('distance [m] east left -->')
plt.grid(True)
```
