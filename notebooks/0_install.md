{
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# Installeer bibliotheken\n",
    "\n",
    "Voor het gebruiken van de notebooks van HiSPARC zijn een aantal python bibliotheken (`modules`) nodig. Vaak zijn deze al geinstalleerd, maar soms moet een deel nog geinstalleerd worden.\n",
    "\n",
    "Dit notebook controleert of de bibliotheken geinstalleerd zijn, zoniet, dan worden ze geinstalleerd met pip.\n",
    "\n",
    "Voer dit hele notebook uit met `Run All`"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {
    "collapsed": true
   },
   "outputs": [],
   "source": [
    "import sys, importlib"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {
    "collapsed": true
   },
   "outputs": [],
   "source": [
    "def install(package):\n",
    "    \"\"\"Probeer package te importeren, als dat niet lukt: pip install package\"\"\"\n",
    "   \n",
    "    # soms is de naam op PyPI (pip) anders dan de python package naam:\n",
    "    package_to_pypi = {'sapphire': 'hisparc-sapphire'}\n",
    "    pypi_package_name = package_to_pypi.get(package, package)\n",
    "    \n",
    "    print('\\n***{package}***\\n'.format(package=package))\n",
    "    try:\n",
    "        pkg = importlib.import_module(package)\n",
    "        return '{package} versie {version} reeds geinstalleerd.'.format(\n",
    "            package=package, version=pkg.__version__)\n",
    "    except ImportError:\n",
    "        print('We installeren {package} en dependencies.\\n'.format(package=package))\n",
    "        !{sys.executable} -m pip install {pypi_package_name}"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "packages = ['numpy', 'matplotlib', 'sapphire', 'matplotlib', 'smopy']\n",
    "\n",
    "for package in packages:\n",
    "    print(install(package))"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {
    "collapsed": true
   },
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python [default]",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.6.1"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 2
}
