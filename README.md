# ASDF Sextant

Landing page for all things **ASDF**: https://seismic-data.org

> This is **A**daptable **S**eismic **D**ata **F**ormat - if you are looking
> for the **A**dvanced **S**cientific **D**ata **F**ormat, go here:
> https://asdf.readthedocs.io/en/latest/

This is an experimental graphical user interface intended to enable the
interactive exploration of ASDF files. It is best suited to deal with
earthquake data.

![Imgur](http://i.imgur.com/dR6T2XE.png)
![Imgur](http://i.imgur.com/Zk97r3K.png)
![Imgur](http://i.imgur.com/BRvdjoL.png)

## Installation

```bash
$ conda install pyasdf pyside2
$ pip install asdf-sextant
```

It is important to install `pyside2` via `conda` if you use `conda` -
otherwise it is easy to install some version of Qt with `conda` and another
via `pip` which just crashes.

## Usage

Start it with:

```bash
$ asdf-sextant
```

Alternatively you can directly open a file with it:

```bash
$ asdf-sextant filename.h5
```

## Dev

### Dependencies

The GUI has the following dependencies:

- `Python 3.7 or 3.8`
- `pyasdf`
- `pyside2`
- `pyqtgraph>=0.11.0rc0`
- `qdarkstyle`

### Misc

Rebuild the UI file in case its necessary with:

```
pyside2-uic -g python --output=asdf_sextant_window.py asdf_sextant_window.ui
```
