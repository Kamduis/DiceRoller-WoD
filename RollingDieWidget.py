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

from Error import ErrValue
from Random import Random




class RollingDieWidget(QSvgWidget):
	"""
	Stellt das Bild eines Rollenden Würfels dar
	"""

	faceChanged = Signal(int)

	__W10 = (
		":icons/W10_0.svg",
		":icons/W10_1.svg",
		":icons/W10_2.svg",
		":icons/W10_3.svg",
		":icons/W10_4.svg",
		":icons/W10_5.svg",
		":icons/W10_6.svg",
		":icons/W10_7.svg",
		":icons/W10_8.svg",
		":icons/W10_9.svg",
	)


	def __init__(self, face=0, parent=None):
		QSvgWidget.__init__(self, parent)

		self.__face = face
		self.load(self.__W10[face])

		self.faceChanged.connect(self.display)


	def getFace(self):
		return self.__face


	def setFace(self, face):
		if (type(face) in (float, int) and self.__face != face):
			self.__face = face
			self.faceChanged.emit(face)


	# folgende Zeile erzeugt das Property-Attribut
	face = property(getFace, setFace)


	def display(self, value):
		self.load(self.__W10[value])




