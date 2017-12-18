
# Installeer bibliotheken

Voor het gebruiken van de notebooks van HiSPARC zijn een aantal python bibliotheken (`modules`) nodig. Vaak zijn deze al geinstalleerd, maar soms moet een deel nog geinstalleerd worden.

Dit notebook controleert of de bibliotheken geinstalleerd zijn, zoniet, dan worden ze geinstalleerd met pip.

Voer dit hele notebook uit met `Run All`


```python
import sys, importlib
```


```python
def install(package):
    """Probeer package te importeren, als dat niet lukt: pip install package"""
   
    # soms is de naam op PyPI (pip) anders dan de python package naam:
    package_to_pypi = {'sapphire': 'hisparc-sapphire'}
    pypi_package_name = package_to_pypi.get(package, package)
    
    print('\n***{package}***\n'.format(package=package))
    try:
        pkg = importlib.import_module(package)
        return '{package} versie {version} reeds geinstalleerd.'.format(
            package=package, version=pkg.__version__)
    except ImportError:
        print('We installeren {package} en dependencies.\n'.format(package=package))
        !{sys.executable} -m pip install {pypi_package_name}
```


```python
packages = ['numpy', 'matplotlib', 'sapphire', 'matplotlib', 'smopy']

for package in packages:
    print(install(package))
```
