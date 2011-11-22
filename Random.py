# -*- coding: utf-8 -*-

"""
Copyright (C) 2010 by Victor von Rhein
victor@caern.de

This file is part of DiceRoller-WoD.

DiceRoller-WoD is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

DiceRoller-WoD is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with DiceRoller-WoD.  If not, see <http://www.gnu.org/licenses/>.

@package DiceRoller-WoD
"""




from PySide.QtCore import *




class Random(QObject):
	qsrand(QTime.currentTime().msec())

	
	def __init__(self, parent=None):
		pass


	#@staticmethod
	#def random(valMax):
		#"""
		#Gibt einen zufälligen Wert zwischen 1 und valMax zurück. [1, valMax]
		#"""
		
		#return 1 + qrand() % valMax


	@staticmethod
	def random(valA, valB=0):
		"""
		Gibt einen zufälligen Wert zwischen valMin und valMax zurück. [valMin, valMax]
		Sollte valB nicht angegeben werden, wird es als 0 angenommen.
		"""
		
		if (valB < valA):
			valueMin = valB
			valueMax = valA
		else:
			valueMin = valA
			valueMax = valB
			
		return valueMin + (qrand() % (valueMax - valueMin + 1))