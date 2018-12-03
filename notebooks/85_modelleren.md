## Het schrijven van simulaties: Modelleren
Het notebook voor een simulatie
bestaat uit een aantal blokken. Eerst worden enkele noodzakelijke bibliotheken
geimporteerd:

```python
import numpy as np
import matplotlib.pyplot as plt
%matplotlib inline 
# De laatste regel zorgt dat de plots in het notebook komen.
```

We maken een eenvoudig model voor een vallend voorwerp. Bij dit model zijn de
volgende startwaarden nodig. Dit blok is in de praktijk beter te vullen nadat
het model geschreven is.

```python
t=0
dt = 0.001 
m = 0.1
g = -9.8
cw = 1
rho = 1.028 
A = 0.01 
v=0
z = 5
```

Het model is met een 'while' lus te maken. Zolang de tijd kleiner is dan de
eindtijd blijft de lus doorgaan. We willen later een grafieken voor de snelheid
en de plaats als functie van de tijd maken. Hiervoor moeten eerst (lege) lijsten
gemaakt worden. Als dit gebeurd is moeten de startwaarden hierboven worden
aangepast. Begin door alle onbekende grootheden aan de linkerkant van de
opdracht zonodig een waarde te geven.

```python
eindtijd = 1
tijden = [t] # de lijst 'tijden' met een begintijd is gemaakt
snelheden = [v] # en 'snelheden'
plaatsen = [z] # en 'plaatsen' ook
while t < eindtijd:
    # begin model
    t = t + dt
    Fz = m * g
    Fw = .5 * cw * rho * A * v ** 2
    a=(Fz + Fw) / m
    dv = a * dt
    v = v + dv
    dz = v * dt
    z = z + dz
    # eind model
    # begin van het vullen van de lijsten
    snelheden.append(v) # voegt een snelheid toe aan de lijst met snelheden.
    plaatsen.append(z) # voegt een plaats toe aan een lijst met plaatsen.
    tijden.append(t) # voegt de tijd toe aan een lijst met tijden.
    # eind van het vullen van lijsten
```

Uiteindelijk zijn er grafieken te maken. Met behulp van de python matplotlib
documentatie zijn de grafieken helemaal aan eigen wensen aan te passen.

```python
plt.figure(figsize=(10,10))
plt.plot(tijden, snelheden)
plt.title('De snelheid als functie van de tijd')
plt.xlabel('tijd [s]')
plt.ylabel('snelheid [m/s]')
```

```python
plt.figure(figsize=(10,10))
plt.plot(tijden, plaatsen)
plt.title('De plaats als functie van de tijd')
plt.xlabel('tijd [s]')
plt.ylabel('hoogte [m]')
```

Voor gevorderden:

```python
Ekin = 1 / 2 * m * np.array(snelheden) ** 2
Epot = -m * g * np.array(plaatsen)
```

```python
plt.figure(figsize=(10,10))
plt.plot(tijden, Ekin, label = 'Kinethisch')
plt.plot(tijden, Epot, label = 'Potentieel')
plt.title('De energie als functie van de tijd')
plt.xlabel('Tijd [s]')
plt.ylabel('Energie [J]')
plt.legend()
```
