# Recept: events aan coincidenties koppellen: CoincidenceQuery

We kunnen ook de events bij een coincidentie zoeken. Dit is niet triviaal. De
tijdstempel van een coincidentie hoort bij het eerste event, maar dit kan
telkens een ander event zijn uit een groep stations. De `/coincidence` group
bevat informatie in `c_index` en `s_index` om e.e.a. te koppelen. Maar ook via
deze weg is enig programmeer werk.

SAPPHiRE CoincidenceQuery kan het bijelkaar zoeken van coincidenties
automatiseren:

Eerst maken een HDF5-bestand en downloaden coincidenties:

```{.python .input}
import tables
FILENAME = 'data.h5'
data = tables.open_file(FILENAME, 'a')
```

```{.python .input}
from datetime import datetime
from sapphire import download_coincidences
download_coincidences(data, cluster='Science Park', start=datetime(2016, 1, 1), end=datetime(2016, 1, 2), n=3)
data.close()
```

CoincidenceQuery opent zelf het HDF5 bestand. We sluiten daarom eerst het
bestand:

```{.python .input}
data.close()
```

We initialiseren CoincidenceQuery. Als argument geven we alleen het bestandsnaam
op:

```{.python .input}
from sapphire import CoincidenceQuery
cq = CoincidenceQuery(FILENAME)
```

Eerst maken we een lijst van alle concidenties (in dit geval tussen stations
501, 510 en 599):

```{.python .input}
STATIONS = [501, 510, 509]
coincidences = cq.all(STATIONS, iterator=True)
```

Nu gebruiken we de functie `all_events`:

Deze functie geeft een lijst van coincidenties. Elke concidentie is een lijst
van tuples, met telkens het stationnummer en het bijbehorende event.

Met een dubelle for-loop kunnen we de informatie "uitpakken":

```{.python .input}
for id, coinc in enumerate(cq.all_events(coincidences)):
    print "Coincidentie: %d" % id
    for station, event in coinc:
        print "Station: %d. Event id: %d. Timestamp: %d " % (station, event['event_id'], event['ext_timestamp'])
```

Met `finish()` sluiten we CoincidenceQuery en wordt ook het HDF5 bestand
gesloten.

```{.python .input}
cq.finish()
```

# Opgave

Het SciencePark in Amsterdam heeft 11 meetstations. Er zijn slechts enkele
coincidenties per dag, waarbij alle stations betrokken worden.

Bepaal de extended timestamps van events in coincidenties met 9 of meer
meetstations op een willekeurige dag in 2016.

Kijk eerst op http://data.hisparc.nl hoeveel coincidenties er die dag waren.
Niet alle stations hebben elke dag data en station 507 staat binnen!
