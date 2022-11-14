# Interacties van elektronen en fotonen

In het elektromagnetisch deel van de
deeltjeslawine ontstaan deeltjes onder andere door Compton scattering. Compton
scattering beschrijft de verstrooiing van elektronen aan fotonen. In het
algemeen is deze verstrooiing te beschrijven met het onderstaande Feynman
diagram. 

<img src="Feynman.png" width="22%"> 

In het diagram zien we de
interactie van een elektron met twee fotonen. Dit moet omdat iedere interactie
tussen elektronen en fotonen relatief is ten opzichte van de waarnemer. Het is
dus van belang dat we de scattering door verschillende waarnemers kunnen
bekijken. Dit gaat met een relativistische transformatie. (Als een elektron in
de buurt van een elektrisch geladen kern komt, is de elektrische kracht te
beschouwen als een uitwisseling van fotonen.)

Eerst halen we de volgende bibliotheken op:

```python
import numpy as np
import matplotlib.pyplot as plt
%matplotlib inline
```

## Relativiteit

In het geval van deeltjeslawines moeten de interacties met
behulp van de relativiteitsleer worden bekeken. In dit geval weten we dat
$\beta=v/c$ en de Lorentz variabele $\gamma=1/\sqrt{1-\beta^2}$. De Lorentz
variabele $\gamma$ is dus te schrijven als een functie van $\beta$.

## Deeltje
De toestand van een deeltje is vast te leggen met een 'viervector'.
Achtereenvolgens worden hier de tijd en de snelheden in drie richtingen of de
energie en de impuls (massa maal snelheid) opgeschreven. 

De energie van deeltjes is te schrijven als $E_e=\gamma_e{m_ec}^2$, de impuls is
$P_e=\beta_e\gamma_e{m_ec}=\beta_e{E_e/c}$. Voor $c$ wordt vaak 1 lichtjaar/jaar
gebruikt. Met wat wiskunde valt in dit geval ($c=1$) af te leidden dat:
$m^2=E^2-p^2$. We maken een functie die de viervector voor een bewegend deeltje:

```python
def maakDeeltje(m, p):
    """
    param m: De rustmassa van het deeltje (in eV)
    param p: Een vector voor de impuls van het deeltje (in eV) bijvoorbeeld [1e3, 1e2, -1e1]
    returns: De viervector [E, p_x, p_y, p_z] van het deeltje.
    """
    p = np.array(p)
    E = (m ** 2 + np.sum(p ** 2)) ** .5
    return np.array([E, *p])
```

We kunnen nu ook $\beta$ van dit deeltje bepalen, dit is te schrijven als een
vector met een $x$, $y$ en $z$-component:

```python
def getBeta(deeltje):
    """
    param deeltje: de viervector waarmee het deeltje beschreven wordt.
    returns beta: een drie dimensionale vector voor beta van het deeltje.
    """
    return deeltje[1:] / deeltje[0] 
```

Als we $\beta$ kennen, is $\gamma$ te berekenen:

```python
def getGamma(beta):
    """
    param beta: a 3d vector defining beta
    returns: gamma
    """
    beta = np.array(beta)
    gamma = 1 / (np.sqrt(1 - np.sum(beta ** 2)))
    return gamma
```

```python
elektron = maakDeeltje(.5e6, [1e6, 0, 0])
print('elektron', elektron)
```

```python
beta = getBeta(elektron)
print(beta)
```

```python
foton = maakDeeltje(0, [-.4e6, 0, 0])
print('foton', foton)
```

```python
print(getBeta(foton))
```

## Waarnemers

We kunnen van waarnemer wisselen met behulp van een matrix.
Normaal worden er twee soorten waarnemers gedefinieerd:

* De waarnemer die aan het coordinaten systeem van het laboratorium wordt gekoppeld.
* De waarnemer die aan het zwaartepunt (center of mass) van de deeltjes wordt gekoppeld.

In dit
geval zijn er dus twee matrixes, van lab naar center en van center naar lab. We
nemen de beta en gamma ($\beta$ en $\gamma$) van het zwaartepunt van de botsende
deeltjes (met de bijbehorende waarnemer) volgens de waarnemer in het lab frame.

```python
beta = getBeta(elektron)
gamma = getGamma(beta)
print(beta, gamma)
```

```python
def maak_transformatie_matrix(gamma, beta):
    """
    Deeltjes hebben in dit geval alleen een beta (v/c) langs de x-as, 
    dit is dus geen vector maar een getal: -1<beta<1.
    """
    return np.matrix([[gamma, -beta * gamma, 0, 0],
                      [-beta * gamma, gamma, 0, 0],
                      [0, 0, 1, 0],
                      [0, 0, 0, 1]])
```

De $\beta$ in dit geval is de $\beta(=v/c)$ van de ene waarnemer ten opzichte
van de andere waarnemer. Volgens de relativiteitsleer geldt natuurlijk:
$\beta_{A,B}=-\beta_{B,A}$.

```python
beta2center = getBeta(elektron)[0]
gamma2center = getGamma(beta2center)
Lab2Center = maak_transformatie_matrix(gamma2center, beta2center) 
Center2Lab = maak_transformatie_matrix(gamma2center, -beta2center)
```

Heen en weer transformeren levert de eenheidsmatrix op.

```python
print(Lab2Center * Center2Lab)
```

We kunnen het elektron nu ook bekijken volgens een waarnemer in het zwaartepunt.
Deze beweegt dus met het deeltje mee.

```python
print(elektron * Lab2Center)
```

De impuls langs de $x$-as (het tweede getal) is verwaarloosbaar. De snelheid ten
opzichte van deze waarnemer is dus ook 0.

Fotonen om ons heen bestaan hoodzakelijk uit zichtbaar licht
($E_{foton}\approx2\mathrm{eV}$). Deze fotonen kunnen interacties aangaan met
(hoogenergetische) elektronen. In dit geval is er sprake van een transformatie
van het lab frame naar center of mass frame.

```python
print(maakDeeltje(0, [-2, 0, 0]) * Center2Lab)
```

## Interacties in het zwaartepunt

Compton scattering is een bijzonder geval de
interactie van een elektron en een foton. In dit geval is de energie van een van
de fotonen verwaarloosbaar. De som van de energie en impuls voor en na de
interactie moet hetzelfde blijven. 

Relativistiche interacties van deeltjes
worden in eerste instantie beschreven in het massa centrale systeem ($\Sigma
P=0$). We beschouwen fotonen en elektronen die langs de $x$-as bewegen.

De energie van de fotonen is $E_f=h\nu$ ($E=hf$), de impuls is $P_f=h/\lambda_f=E_f/c$.

Het voordeel van dit massa centraal systeem is dat de
som van de impulsen hier ook 0kgm/s is. Bijgevolg geldt voor deze waarnemer voor
de interactie: $P_{f}=-P_{e}$ en $E_{tot}=E_{f}+E_{e}$. Eerst maken we een
foton:

```python
m_foton = 0
p_foton = np.array([2, 0 ,0])
foton_voor = maakDeeltje(0, p_foton)
```

```python
m_elektron = .5e6 # eV
p_elektron = -p_foton
elektron_voor = maakDeeltje(m_elektron, p_elektron)
```

```python
print(p_foton + p_elektron)
```

Bij een massacentrale botsing blijft de som van de impulsen 0eV. De richting
waarin de deeltjes na de interactie wegschieten is echter niet bekent. De
deeltjes kunnen bijvoorbeeld loodrecht op de eerste richting wegschieten:

```python
p_foton = np.array([*p_foton[1:], p_foton[0]]) 
p_elektron = np.array([*p_elektron[1:], p_elektron[0]])
```

```python
foton_na = maakDeeltje(0, p_foton)
elektron_na = maakDeeltje(m_elektron, p_elektron)
```

```python
print('foton voor' ,foton_voor)
print('foton na', foton_na)
print('elektron voor' ,elektron_voor)
print('elektron na', elektron_na)
```

## Transformatie naar de waarnemer in het lab frame

Deze botsing is te
verplaatsen van het zwaartepunt frame naar het lab frame. We kiezen dus een
nieuwe waarnemer, deze transformatie is met een matrix te beschrijven.

We nemen
aan dat het deeltje langs de $x$-as beweegt $\beta=0.9$. Dit wordt ook wel een
'(Lorentz-)boost' langs de $x$-as genoemd.

```python
beta = 0.9
gamma = getGamma(beta)

Center2Lab = np.matrix([[gamma, -beta * gamma, 0, 0],
                        [-beta * gamma, gamma, 0, 0],
                        [0, 0, 1, 0],
                        [0, 0, 0, 1]])
```

```python
foton_voor = foton_voor * Center2Lab
foton_na = foton_na * Center2Lab
elektron_voor = elektron_voor * Center2Lab
elektron_na = elektron_na * Center2Lab
```

```python
print('foton voor' ,foton_voor)
print('foton na', foton_na)
print('elektron voor' ,elektron_voor)
print('elektron na', elektron_na)
```

Bij bestudering blijkt dat er een laagenergetisch foton op een hoogenergetisch
elektron botst. Een klein deel van de energie van het elektron wordt
overgedragen in een 'afgestraald' foton. In dit geval is de energie van het
foton te klein voor paarvorming (er onstaat dan een elektron positron paar). Dit
soort interacties komt daarom ook voor in de staart van een kosmische
deeltjeslawine.

## Van bijzonder naar algemeen

Hiervoor is het bijzondere geval besproken van
twee deeltjes die loodrecht op de inkomende deeltjes wegvliegen. In de praktijk
weten we niet naar welke kant de deeltjes wegvliegen. We maken eerst deeltjes
die met elkaar interacteren:

```python
p_foton = np.array([2, 0 ,0])
foton_voor = maakDeeltje(0, p_foton)
p_elektron = -p_foton
elektron_voor = maakDeeltje(m_elektron, p_elektron)
```

Hiervoor is het bijzondere geval besproken van twee deeltjes die loodrecht op de
inkomende deeltjes wegvliegen. In de praktijk weten we niet naar welke kant de
deeltjes wegvliegen. In het massa centrale systeem moeten de deeltjes echter wel
in tegengestelde richting wegvliegen. We nemen aan dat de hoek tussen aankomende
en wegvliegende deeltjes $\theta$ is. We maken eerst een array met mogelijke
hoeken:

```python
thetas = np.arange(0, np.pi, np.pi / 36) + np.pi / 72
```

We gaan uit hetzelfde elektron en foton voor de botsing. Mogelijke elektron-
foton paren na de botsing zijn als functie van $\theta$ te schrijven:

```python
fotons_na = []
elektrons_na = []
for theta in thetas:
    p_foton = np.array([np.sin(theta), np.cos(theta), 0])
    p_elektron = -p_foton
    fotons_na.append(maakDeeltje(0, p_foton))
    elektrons_na.append(maakDeeltje(m_elektron, p_elektron))
```

De $x$-component van de impuls van het foton is voor de hoeken $\theta$ uit de
array te halen:

```python
print(np.array(fotons_na)[:,1])
```

Nu is bijvoorbeeld ook de impuls van de $x$-richting tegen de $y$-richting van
het foton uit te zetten:

```python
plt.plot(np.array(fotons_na)[:,1],np.array(fotons_na)[:,2])
```

```python
np.array(fotons_na)[:,1]
```

We wisselen van waarnemer:

```python
fotons_na = fotons_na * Center2Lab
elektron_na = elektrons_na * Center2Lab
```

We kunnen nu een array opvragen van de energie van het foton voor de
verschillende hoeken $\theta$:

```python
np.array(fotons_na)[:,0]
```

De energie van elektronen en fotonen na de interactie is nu als functie van
$\theta$ te plotten.

```python
plt.plot(np.degrees(thetas), np.array(fotons_na)[:,0], label ='foton')
plt.plot(np.degrees(thetas), np.array(elektrons_na)[:,0], label='elektron')
plt.xlabel(r'$\theta$ [degrees]')
plt.ylabel('log($E$)')
plt.legend()
plt.yscale('log')
```
