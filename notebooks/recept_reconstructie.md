# Recept Richtingsreconstructie

Richtingsrecontructie op basis van aankomsttijden van deeltjes is mogelijk als
er 3 tijden zijn gemeten. In het geval van HiSPARC meetstations, is dat mogelijk
bij stations met 4 detectoren.

```{.python .input}
import tables
from sapphire import download_data
from datetime import datetime
```

```{.python .input}
FILENAME = 's501.h5'
data = tables.open_file(FILENAME, 'a')
```

We downloaden data van het "vier-plaat" station 501; Een station met vier
detectoren:

```{.python .input}
if '/s501' not in data:
    download_data(data, '/s501', 501, start=datetime(2016, 1, 1), end=datetime(2016,1,2))
```

```{.python .input}
print data
```

We gebruiken de SAPPHiRE class `ReconstructESDEvents`:

```{.python .input}
from sapphire import ReconstructESDEvents
rec = ReconstructESDEvents(data, '/s501', 501)
```

De function `reconstruct_directions()` reconstrueert de richtingen (hoeken) van
elk event uit de aankomsttijden per detector en slaat de uitkomst op in:
- `rec.theta`: een array met de zenith hoek per event
- `rec.phi`: een array met de azimuth hoek per event

De hoeken kunnen ook meteen opgeslagen worden in het HDF5 bestand. Dit wordt in
de volgende paragraaf toegelicht.

Eerst reconstrueren we de aankomstrichting van de events:

```{.python .input}
rec.reconstruct_directions()
```

Hieronder staan de eerste twintig zenithoeken. 'nan' (NaN) betekent:
Not-a-number: De reconstructie was niet mogelijk. Ofwel er was onvoldoende
informatie, bijvoorbeeld slechts twee aankomsttijden. Ofwel de oplossing was
niet fysisch:

```{.python .input}
rec.theta[:20]
```

Met behulp van de functie `numpy.isnan()` kunnen we de NaNs verwijderen:

```{.python .input}
from numpy import isnan
zenith = [a for a in rec.theta if not isnan(a)]
azimuth = [a for a in rec.phi if not isnan(a)]
print "Er zijn %d events succesvol gereconstrueerd." % len(zenith)            
```

Nu bevat de array `zenith` slechts hoeken (in radialen):

```{.python .input}
zenith[:5]
```

## Plotten

We maken een polar-plot van de hoeken theta en phi (zenit, azimut) van de
(succesvol) gereconstrueerde events, en een histrogram van de zenithoeken.

```{.python .input}
import matplotlib.pyplot as plt
%matplotlib inline
```

We rekenen de hoeken om naar graden:

```{.python .input}
from numpy import degrees
zenith = degrees(zenith)
azimuth = degrees(azimuth)
```

Polar plot van zenit en azimuth:

```{.python .input}
ax = plt.subplot(polar=True)
ax.scatter(zenith, azimuth)
```

Histogram van de zenithoeken:

```{.python .input}
from numpy import arange
plt.hist(zenith, bins=arange(0,90., 5.), histtype='step')
plt.xlabel('zenith angle (degrees)')
plt.ylabel('counts')
plt.title('Zenith histrogram station 501.')
```

# Opslaan van reconstructies in het HDF5 bestand

De SAPPHiRE reconstructie class `ReconstructESDEvents` kan de reconstructies ook
direct opslaan in het HDF5 bestand waar de events in zijn opgeslagen:

```{.python .input}
rec = ReconstructESDEvents(data, '/s501', 501)
rec.reconstruct_and_store()
```

Er waren nu twee progressbars te zien: De eerste voor richting reconstructie en
de tweede voor core recontructie. We richten ons hier op de richtingen en laten
de core reconstructie buiten beschouwing.

naast `rec.theta` en `rec.phi` is er nu ook een nieuwe groep
`/s501/reconstructions` in het hdf5 bestand:

```{.python .input}
rec_tabel = data.root.s501.reconstructions
print rec_tabel
```

De gereconstrueerde hoeken zijn nu ook opgeslagen op disk, in het HDF5 bestand.

De kolommen 'zenith' en 'azimuth' bevatten de gereconstrueerde hoeken (of NaN):

# Opgave

Maak een histogram van de zenithoeken en een polarplot van de azimuth en
zenithhoeken, zoals in het voorbeeld hierboven. Gebruik de `zenith` en `azimuth`
kolommen uit de groep `/s501/reconstructions` uit het HDF5 bestand.

*Hints*:
- gebruik: `.col('zenith')` om een kolom in te laden.
- gebruik  `.compress(~isnan(...))` om te NaNs verwijderen.

```{.python .input}
zenith = rec_tabel.col('zenith')
azimuth = rec_tabel.col('azimuth')
```

```{.python .input}
zenith = zenith.compress(~isnan(zenith))
azimuth = azimuth.compress(~isnan(azimuth))
print "Er zijn %d events succesvol gereconstrueerd." % len(zenith)            
```

```{.python .input}
zenith = degrees(zenith)
azimuth = degrees(azimuth)
```

```{.python .input}
ax = plt.subplot(polar=True)
ax.scatter(zenith, azimuth)
```

```{.python .input}
plt.hist(zenith, bins=arange(0,90., 5.), histtype='step')
plt.xlabel('zenith angle (degrees)')
plt.ylabel('counts')
plt.title('Zenith histrogram station 501.')
```
