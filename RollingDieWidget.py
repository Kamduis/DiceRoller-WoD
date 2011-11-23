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




WIDGET_SIZE = 80




class RollingDieWidget(QGraphicsView):
	"""
	Stellt das Bild eines "rollenden" Würfels dar. Diese Klasse setzt derzeit einen W6 oder W10 voraus. Nur für diese Würfel existieren Bilder.
	"""

	faceChanged = Signal(int)
	facesChanged = Signal(int)


	def __init__(self, faces=10, face=1, parent=None):
		QGraphicsView.__init__(self, parent)

		self.__faces = faces
		self.__face = face
		self.__renderer = QSvgRenderer(":icons/W" + str(faces) + ".svg")
		self.__dieSides = []

		self.__scene = QGraphicsScene()
		self.setScene(self.__scene)
		self.resize(WIDGET_SIZE, WIDGET_SIZE)

		#self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
		#self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
		self.setFrameShape(QFrame.NoFrame)
		self.setStyleSheet("background: transparent;");

		# Den Würfel anzeigen.
		self.__changeDie(faces)
		self.__displayFace(face)

		self.facesChanged.connect(self.__changeDie)
		self.faceChanged.connect(self.__displayFace)


	def getFace(self):
		return self.__face


	def setFace(self, face):
		if (type(face) in (float, int) and self.__face != face):
			self.__face = face
			self.faceChanged.emit(face)


	# folgende Zeile erzeugt das Property-Attribut
	face = property(getFace, setFace)


	def getFaces(self):
		return self.__faces


	def setFaces(self, faces):
		if (type(faces) in (float, int) and self.__faces != faces):
			self.__faces = faces
			self.facesChanged.emit(faces)


	# folgende Zeile erzeugt das Property-Attribut
	faces = property(getFaces, setFaces)


	def __displayFace(self, value):
		"""
		Zeigt die ausgewählte Seite des Würfels an.
		"""

		# Die anzuzeigende Augenzahl muß natürlich auf dem Würfel vorhanden sein.
		if (type(value) in (float, int) and value in xrange(self.faces)):
			for item in self.__scene.items():
				self.__scene.removeItem(item)

			# Die 1. Würfelseite ist die 1, allerdings ist diese an Indexposition 0 gespeichert.
			self.__scene.addItem(self.__dieSides[value-1])
			self.resize(WIDGET_SIZE, WIDGET_SIZE)
			#self.fitInView(self.__dieSides[value-1])


	def __changeDie(self, value):
		"""
		Zeigt den Würfel mit der passenden Seitenzahl an.
		"""

		if self.__dieSides:
			del self.__dieSides[:]

		for i in xrange(value):
			self.__WXX_x = QGraphicsSvgItem()
			self.__WXX_x.setSharedRenderer(self.__renderer)
			self.__WXX_x.setElementId("layer" + str(i+1))
			self.__dieSides.append(self.__WXX_x)

		# Ist die zuvor angezeigt Augenzahl höher als die Seitenzahl des neuen Würfels, muß auf dessen Maximal-Augenzahl umgeschalten werden.
		if self.__face > value:
			setFace(value)




#class RollingDieWidget(QSvgWidget):
	#"""
	#Stellt das Bild eines Rollenden Würfels dar
	#"""

	#faceChanged = Signal(int)

	#__W10 = (
		#":icons/W10_0.svg",
		#":icons/W10_1.svg",
		#":icons/W10_2.svg",
		#":icons/W10_3.svg",
		#":icons/W10_4.svg",
		#":icons/W10_5.svg",
		#":icons/W10_6.svg",
		#":icons/W10_7.svg",
		#":icons/W10_8.svg",
		#":icons/W10_9.svg",
	#)


	#def __init__(self, face=0, parent=None):
		#QSvgWidget.__init__(self, parent)

		#self.__face = face
		#self.load(self.__W10[face])

		#self.faceChanged.connect(self.display)


	#def getFace(self):
		#return self.__face


	#def setFace(self, face):
		#if (type(face) in (float, int) and self.__face != face):
			#self.__face = face
			#self.faceChanged.emit(face)


	## folgende Zeile erzeugt das Property-Attribut
	#face = property(getFace, setFace)


	#def display(self, value):
		#self.load(self.__W10[value])




