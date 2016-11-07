# Python Introductie

Dit is een zeer incomplete python introductie, waarin een aantal belangrijke
aspecten van de scripttaal `python` worden toegelicht, bedoeld voor lezers met
redelijk wat ervaring in een taal als `Java` of `C\C++\C#`.

Het is zeker niet bedoeld als een complete introductie van `python` voor
beginners.

Andere bronnen:
- Een zeer leesbaar boek over Python is `Think Python` (gratis downloadbaar
in PDF en HTML): http://greenteapress.com/wp/think-python/
- Een online interactieve basis introductie van Python:
https://www.codecademy.com/learn/python
- **Aanrader**: Het UvA practicum "Programmeren voor Natuur- en Sterrenkunde"
heeft zeer bruikbare (natuurkundige) opdrachten in Python:
https://progns.mprog.nl/ (klik bovenaan op Archive)

## Python 2 en 3

Deze notebooks werken onder python 2 en 3. Helaas zijn er verschillen tussen python 2 en 3, waardoor python 2 code niet zomaar onder python 3 werkt. Twee opvallende verschillen tussen python 2 en 3 zijn:

- `print`: Python 2: `print 'hallo'`. Python 3: `print('hallo')`
- `division`: Python 2: `3 / 2 == 1`. Python 3: `3 / 2 == 1.5`

Door `from __future__ import division, print_function` gedraagd python 2 zich als python 3.  

```python
# dit notebook werkt onder Python 2 en 3
from __future__ import division, print_function
```
## Hello, World!

In `python` ziet deze klassieker er zo uit: (Druk Ctrl-Enter in de cel
hieronder)

```{.python .input  n=2}
print('Hello, World!')
```

## Blokken: Inspringen

Blokken code worden in `python` ingegesprongen:

```{.python .input  n=6}
getal = input('Geef een getal: ')
if getal > 10:
    print('Groter dan tien!')
elif getal < 0:
    print('Negatief!')
else:
    print('Tussen nul en tien!')
    if getal % 2 == 0:
        print('En het getal is even!')
```

## Variabelen

Variabelen (objecten) hoeven niet gedeclareerd te worden met een `type`, maar ze
hebben wel een `type`

```{.python .input  n=7}
a = 3
b = 5.7
c = 'Hallo!'
type(a), type(b), type(c)
```

## Lijsten

Lijsten zijn een belangrijk `type` in `python`:

```{.python .input}
personen = ['Tom', 'Klaas', 'Piet', 'Jan', 'Wouter', 'Joop', 'Karel']
```

Voor de lengte van een lijst gebruiken we `len()`:

```{.python .input}
len(personen)
```

Een item toevoegen kan met append:

```{.python .input}
personen.append('Mieke')
personen
```

De items van lijsten kunnen we bekijken met [index]:
Let op: Python telt vanaf 0.

```{.python .input}
personen[1]
```

Er zijn veel mogelijkheden met behulp van de index:

```{.python .input}
print("item 1 tot 5", personen[1:5])
print("Vanaf het tweede item:", personen[1:])
print("Vanaf 0 tot 8, stapgrootte 2", personen[0:8:2])
print("Het laatste item:", personen[-1])
```

```{.python .input}
if 'Karel' in personen:
    print("Karel zit in de lijst.")
else:
    print("Karel zit niet in de lijst")
```

## range

range() maakt een lijst gehele getallen (integers):

```{.python .input}
print("Tot 10:\t\t", range(10))
print("Vanaf 5 tot 10:\t", range(5, 10))
print("tot 10, stap 2:", range(0, 10, 2))
```

### help() en ?
Voor meer informatie over een python functie gebruiken we de functie `help()`:

```{.python .input}
help(range)
```

range? laat een pop-up zien met vergelijkbare informatie.

```{.python .input}
range?
```

# Loopen met `for`

Het statement `for` wordt gebruikt om te loopen:

```{.python .input}
for getal in range(5):
    print(getal)
```

```{.python .input}
for getal in range(1,50):
    if getal % 7 == 0:
        print("Het getal %d is deelbaar door 7" % getal)
```

`for` kan geinterpreteerd worden als `foreach` (voor elk item, doe:)
Dit betekent dat we niet alleen maar over getallen kunnen loopen, zoals in veel
andere talen gebruikelijk, maar over *alle* lijst-achtige objecten:

```{.python .input}
for persoon in personen:
    print(persoon)
```

## List comprehensions

In `python` kom je vaak een wiskundige manier van het definieren van lijsten
tegen:

```{.python .input}
[x**2 for x in range(10)]
```

Een dergelijke syntax heet een `list comprehension` en is in feite een snelle
(en mits juist gebruikt, leesbare) manier om het volgende te schrijven:

```{.python .input}
lijst = []
for x in range(10):
    lijst.append(x**2)
lijst  
```

# Functies

Een functie definieren we in `python` alsvolgt:

```{.python .input}
def is_priem(getal):
    """Test of getal een priemgetal is

    Dit is een zeer inefficiente implementatie

    """
    for deler in range(2, getal):
        if not getal % deler:
            return False

    return True
```

Een functie roepen we aan met `functie(paramter1, parameter2, ...)`:

```{.python .input}
for getal in range(100):
    if is_priem(getal):
        print(getal,)
```

Het commentaar tussen de """ is belangrijk. Deze zogenaamde 'docstring' is
beschikbaar via `help()` of het vraagteken:

```{.python .input}
help(is_priem)
```

# Numpy

Numpy is een bibliotheek met wiskundige functies die werken op `array's`
(lijsten, matrices) van `floats`. Omdat de bewerkingen in `C` en `FORTRAN`
geimplementeerd zijn, zijn numpy functies vaak veel sneller dan alternatieven
uit `math`.

```{.python .input}
import numpy as np
```

```{.python .input}
np.arange(0.1, 3.0, 0.2)
```

```{.python .input}
np.linspace(0.1, 3.0, 20)  # hetzelfde interval in 20 stappen
```

### Numpy snelheid:

Een van de krachten van `numpy` is het uitvoeren van operaties op een vector:

```{.python .input}
%timeit [2*x for x in range(10000)]
```

```{.python .input}
%timeit 2*np.arange(10000)
```

In het bovenstaande voorbeeld wordt in de `list-comprehension` in python
'gelooped' over 10.000 getallen. Het `numpy` alternatief verwerkt de array in
zijn geheel, zonder de loop en is daarom >100x sneller.

## Matrices en Lineaire algebra

```{.python .input}
matrix = np.arange(9).reshape(3,3)
matrix
```

```{.python .input}
matrix[1] # tweede rij
```

```{.python .input}
matrix[:, 0] # eerste kolom
```

```{.python .input}
np.transpose(matrix)
```

```{.python .input}
np.linalg.det(matrix)
```

```{.python .input}
Ook hier geeft `help()` snel veel informatie:
```

```{.python .input}
help(np.linalg)
```

# Plotten

Een belangrijke stap in het data verwerken is plotten:

```{.python .input}
import matplotlib.pyplot as plt
%matplotlib notebook
```

```{.python .input}
x = np.linspace(0, 10., 100)
y = np.sin(x)
```

```{.python .input}
plt.plot(x, y, 'b-')
plt.xlabel('x')
plt.ylabel('y')
plt.ylim(-1.1,1.1)
plt.title('f(x) = sin(x)')
plt.show()
```
