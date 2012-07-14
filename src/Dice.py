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
# Hiermit kann ich weiterhin ich die Syntax der Signale und Slots so belassen, wie sie in PyQt vorgeschrieben ist.
from PySide.QtCore import Signal as pyqtSignal
from PySide.QtCore import Slot as pyqtSlot

from src.Error import ErrValue
from src.Random import Random




class DieResult:
	unknown = 0
	dramaticFailure = 1
	one = 2
	failure = 3
	success = 4
	chanceSuccess = 5
	exceptionalSuccess = 6




class Die(QObject):
	"""
	Simuliert einen Würfel mit beliebig vielen Seiten.
	"""

	facesChanged = pyqtSignal(int)
	rolled = pyqtSignal(int)


	def __init__(self, parent=None, faces=6):
		QObject.__init__(self, parent)

		self.__faces = faces


	def getFaces(self):
		return self.__faces


	def setFaces(self, faces):
		if (type(faces) in (float, int) and self.__faces != faces):
			self.__faces = faces
			self.facesChanged.emit(faces)


	# folgende Zeile erzeugt das Property-Attribut
	faces = property(getFaces, setFaces)


	def roll(self):
		self._rollResult = Random.random(1, self.__faces)
		#qDebug("Ergebnis: " + str(self._rollResult))
		self.rolled.emit(self._rollResult)




class DieExploding(Die):
	"""
	Simuliert einen Würfel, der explodieren kann, also beim Erreichen eines bestimmten Ergebnisses und darüber automatisch. nocheinmal gewürfelt wird.
	"""

	thresholdChanged = pyqtSignal(int)
	exploded = pyqtSignal(bool)


	def __init__(self, parent=None, faces=6 ):
		Die.__init__(self, parent, faces)
		self.rolled.connect(self.checkExplosion)

		self._threshold = faces
		self._explosions = 0


	def getThreshold(self):
		return self._threshold


	def setThreshold(self, number):
		if self._threshold != number:
			self._threshold = number
			self.thresholdChanged.emit(self._threshold)


	# folgende Zeile erzeugt das Property-Attribut
	threshold = property(getThreshold, setThreshold)


	def checkExplosion(self, result):
		if result >= self._threshold:
			self.exploded.emit(True)
		else:
			self.exploded.emit(False)




class DieWoD(DieExploding):
	"""
	Der Würfel für die WoD: 10-seitig, kann explodieren und ab einer 8 zählt der Würfel als Erfolg.
	"""
	
	__successThreshold = 8
	__successThresholdChance = 10

	rollFinished = pyqtSignal(object)


	def __init__(self, parent=None):
		DieExploding.__init__(self, parent, 10)

		self.rolled.connect(self.checkSuccess)


	def setThreshold(self, number):
		if (type(number) in (float, int) and number >= self.__successThreshold):
			self._threshold = number
		else:
			raise ErrValue(number, "Reroll-threshold too low. Must be at least " + str(self.__successThreshold) + ".")


	# folgende Zeile erzeugt das Property-Attribut
	threshold = property(DieExploding.getThreshold, setThreshold)


	def checkSuccess(self, result):
		if result >= self.__successThreshold:
			if result >= self.__successThresholdChance:
				#qDebug("ERFOLG (auch bei Chanceroll)!")
				self.rollFinished.emit(DieResult.chanceSuccess)
			else:
				#qDebug("ERFOLG!")
				self.rollFinished.emit(DieResult.success)

		elif result == 1:
			#qDebug("FEHLSCHLAG (Gewürfelte '1')")
			self.rollFinished.emit(DieResult.one)
		else:
			#qDebug("FEHLSCHLAG")
			self.rollFinished.emit(DieResult.failure)