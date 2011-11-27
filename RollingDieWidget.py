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
from PySide.QtGui import *
from PySide.QtSvg import *

import Error
from Random import Random
from FuncName import *




WIDGET_SIZE = 50




class RollingDieWidget(QLabel):
	"""
	Stellt das Bild eines "rollenden" Würfels dar. Diese Klasse setzt derzeit einen W6 oder W10 voraus. Nur für diese Würfel existieren Bilder.
	"""

	faceChanged = Signal(int)
	dieChanged = Signal(int)


	def __init__(self, die=10, face=1, parent=None):
		QLabel.__init__(self, parent)

		self.__die = die
		self.__face = face
		self.__dieSides = []

		self.setScaledContents(True)
		self.setMaximumSize(WIDGET_SIZE, WIDGET_SIZE)
		#self.resize(10,10)
		#self.setSizePolicy(QSizePolicy.Ignored,QSizePolicy.Ignored)
		#self.setSizePolicy(QSizePolicy.Fixed,QSizePolicy.Fixed)

		self.__changeDie(die)
		self.__showFace(face)

		self.dieChanged.connect(self.__changeDie)
		self.faceChanged.connect(self.__showFace)


	def face(self):
		return self.__face


	def setFace(self, face):
		if (type(face) in (float, int) and self.__face != face):
			self.__face = face
			self.faceChanged.emit(face)


	def die(self):
		return self.__die


	def setDie(self, die):
		if (type(die) in (float, int) and self.__die != die):
			self.__die = die
			self.dieChanged.emit(die)


	def __changeDie(self, die):
		"""
		Tauscht den aktuellen Würfel gegen einen Würfel mit der angegebenen Seitenzahl aus.
		"""

		for i in xrange(die):
			# Der Iterator läuft von 0 ab, aber Würfel beginnen mit der Augenzahl 1.
			# Dies gilt auch für den W10, der zwar theoretisch die Augenzahl 0 besitzt, aber wir betonen, dies sei Augenzahl 10.
			self.__dieSides.append(":icons/W%(die)i_%(face)i.svg" % {"die": die, "face": i+1})

		# Wird die Würfel getauscht, wird immer die Zahl 1 angezeigt, die einzige Zahl die jeder Würfel besitzt.
		self.__showFace(1)


	def __showFace(self, face):
		"""
		Zeigt die Würfelseite mit der angegebenen Augenzahl an.
		"""

		# Es wird die absolute Augenazhl angegeben, aber die tatsächliche Indexposition dieser Würfelseite ist um 1 Stelle kleiner.
		self.setPixmap(self.__dieSides[face-1])
		#print self.__class__, funcName(), self.__dieSides[face-1]




MAX_DICE_IN_DISPLAY = 10
MAX_DICE_IN_ROW = 10




class RollingDiesWidget(QWidget):
	"""
	Stellt mehrere "rollende"" Würfel dar.
	"""

	numberChanged = Signal(int)


	def __init__(self, number=1, die=10, parent=None):
		QWidget.__init__(self, parent)

		self.__layout = QGridLayout()
		self.setLayout(self.__layout)
		
		self.__numOfDies = number
		self.__die = die
		self.__buildMatrix(self.__numOfDies)
		
		self.numberChanged.connect(self.__buildMatrix)
		
		
	def number(self):
		return self.__numOfDies
		
	
	def setNumber(self, number):
		if self.__numOfDies != number:
			self.__numOfDies = number
			
			self.numberChanged.emit(number)


	def __buildMatrix(self, numOfDies):
		"""
		Baut die Matrix aus Würfeln auf.
		"""
		
		# Es wird nur gelöscht, was gelöscht werden muß. Danach muß nur der fehlende Rest aufgefüllt werden.
		print self.__layout.count()
		if self.__layout.count() > numOfDies:
			rows = range(self.__layout.rowCount())
			columns = range(self.__layout.columnCount())
			for i in rows[::-1]:
				# Für den Schleifenabbruch
				breakLoop = False

				for j in columns[::-1]:
					print "Index %(row)i, %(column)i" \
						% {
							"row": i, 
							"column": j,
						}

					dieWidget = self.__layout.itemAtPosition(i, j)
					# Wenn die letzte Zeile des GridLayouts nicht gefüllt ist, marschiert diese verschlachtelte Schleife dennoch über jede einzelne Zelle. Aus leeren Zellen soll natürlich nichts entfernt und gelöscht werden.
					if type(dieWidget) == type(None):
						continue

					# Raus aus dem Layout heißt nicht, daß das Bild verschwindet.
					self.__layout.removeItem(dieWidget)
					# Jetzt kann der Garbage Collector den Würfel entfernen.
					dieWidget.widget().setParent(None)
					del dieWidget
					
					# Aufhören, wenn keine Würfel mehr entfernt werden müssen.
					if self.__layout.count() <= numOfDies:
						breakLoop = True
						print self.__layout.count()
						break
					
				if breakLoop:
					break

		# Leere Zeilen werden nicht einfach aus dem Layout gelöscht, also muß ich aufpassen, wie ich sie zähle.
		print self.__layout.rowCount(), self.__layout.columnCount()
		self.__diceShown = self.__layout.count()
		self.__indexOfRow = self.__diceShown / MAX_DICE_IN_ROW
		self.__indexOfColumn = self.__diceShown % MAX_DICE_IN_ROW

		print "Index %(row)i, %(column)i" \
			% {
				"row": self.__indexOfRow, 
				"column": self.__indexOfColumn,
			}

		while self.__diceShown < numOfDies:
			self.__rollingDie = RollingDieWidget(self.__die, 1)
			self.__layout.addWidget(self.__rollingDie, self.__indexOfRow, self.__indexOfColumn)
			
			self.__diceShown += 1
			
			# Ist die Zeile voll, muß mit der nächsten begonnen werden.
			if self.__indexOfColumn < MAX_DICE_IN_ROW - 1:
				self.__indexOfColumn += 1
			else:
				self.__indexOfColumn = 0
				self.__indexOfRow += 1

