#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Copyright (C) 2010 by Victor von Rhein
goliath@caern.de

This file is part of DiceRoller-WoD.

DiceRoller-WoD is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation,  either version 3 of the License,  or
(at your option) any later version.

DiceRoller-WoD is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with DiceRoller-WoD.  If not,  see <http://www.gnu.org/licenses/>.

@package DiceRoller-WoD
"""


import sys

#from PyQt4.QtCore import Qt, QCoreApplication
#from PyQt4.QtGui import QWidget, QApplication

from Random import Random




if __name__ == "__main__":
	result = []
	for i in range(10000):
		result.append(Random.random(10))

	valuesPresent = list(set(result))

	numberOfResults = []
	for i in valuesPresent:
		numberOfResults.append(result.count(i))

	numberOfResults.sort()

	print numberOfResults

	print numberOfResults[len(numberOfResults)-1] - numberOfResults[0]

	sys.exit(0)