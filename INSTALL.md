# Overview

## Requirements

DiceRoller-WoD requires [Python](http://http://www.python.org//) Version 2.7 or greater and [PyQt4](http://www.riverbankcomputing.co.uk/software/pyqt/download).

## Excecute

Start DiceRoller-WoD by downloading the sources into a seperate directory. The open a terminal an type: 

	python DiceRoller-WoD.py

In Windows a Doubleclick on DiceRoller-WoD.py may also start the Program.

## Frozen Executable

A frozen executable, no installation of Qt or PyQt is necessary, is available: [Package](https://github.com/downloads/GoliathLeviathan/DiceRoller-WoD/DiceRoller-WoD-linux_64.tar.gz)

### Creating a frozen Executable

To create a frozen executable for your own system, you need a working Version of DiceRoller-WoD (including Python 2.7 and PyQt4) and also [cxfreeze](http://cx-freeze.sourceforge.net/).

Then create a subfolder with the name "build" and enter the following command

	python setup.py build

After that you should find a working frozen executable in a subfolder of build.