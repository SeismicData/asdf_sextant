# ASDF Sextant

Landing page for all things **ASDF**: https://seismic-data.org

> This is **A**daptable **S**eismic **D**ata **F**ormat - if you are looking for the **A**dvanced **S**cientific **D**ata **F**ormat, go here: https://asdf.readthedocs.io/en/latest/


This is an experimental graphical user interface intended to enable the interactive exploration of ASDF files. It can mostly deal with earthquake event data sets and is currently not really suited to explore large noise data sets but we will add this capability in the near future.

![Imgur](http://i.imgur.com/dR6T2XE.png)
![Imgur](http://i.imgur.com/Zk97r3K.png)
![Imgur](http://i.imgur.com/BRvdjoL.png)

## Installation

### Dependencies

The GUI as the following dependencies:

* `Python 2.7, 3.3, or 3.4`
* `pyasdf`
* `PyQt`
* `pyqtgraph`
* `qdarkstyle`
* `pydot`
* `graphviz` *(Not a Python package)*

Same deal as always: If you know what you are doing install the dependencies in any way that works for you. Otherwise install the latest `pyasdf` version  according to these instructions:

http://seismicdata.github.io/pyasdf/installation.html

and install the remaining dependencies with

```bash
$ conda install pyqt
$ pip install pyqtgraph qdarkstyle
```

Under Python 2, install `pydot` with

```bash
$ pip install pydot
```

`pydot` has no proper Python 3  packages, thus do

```bash
$ pip install https://github.com/nlhepler/pydot/archive/master.zip
```

#### graphviz

You furthermore need `graphviz` to view the provenance graphs. It is available for all systems and installation should be simple. Examples are:

```bash
$ sudo apt-get install graphviz  # Debian/Ubuntu
$ brew install graphviz          # OSX with Homebrew
```


#### Pyqtgraph Bug

There is a bug in the current version of pyqtgraph that shows an extra axis. Not a major issue but annoying. You can fix your local version by applying this patch:

https://github.com/pyqtgraph/pyqtgraph/commit/9df4df55c49ace05020e6b7c52128fdce09e2a8d

Alternatively you can just install pyqtgraph from the latest Github master.

### GUI

It has no installer as of now - just clone it with git.

```bash
$ git clone https://github.com/SeismicData/asdf_sextant.git
$ cd asdf_sextant
```

## Usage

Start it with

```bash
$ python main.py
```
