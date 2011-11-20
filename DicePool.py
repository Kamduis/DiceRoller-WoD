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




from PyQt4.QtCore import QObject, qDebug, pyqtSignal
from Dice import DieResult, DieWoD


from Error import ErrValue




class DicePool(QObject):
	thresholdChanged = pyqtSignal(int)
	poolSizeChanged = pyqtSignal(int)
	roteChanged = pyqtSignal(bool)
	curseChanged = pyqtSignal(bool)
	rulesChanged = pyqtSignal(bool)
	rolled = pyqtSignal(int)
	rollFinished = pyqtSignal(object)


	def __init__(self, parent=None):
		super(QObject, self).__init__()
		self.__die = DieWoD()

		self.__chance = False
		self.__rote = False
		self.__curse = False
		self.__poolSize = 0

		self.__die.thresholdChanged.connect(self.thresholdChanged.emit)
		self.__die.rollFinished.connect(self.modifySuccess)
		self.__die.rollFinished.connect(self.checkBotch)
		self.__die.exploded.connect(self.addExplosion)


	def getPoolSize(self):
		return self.__poolSize


	def setPoolSize(self, number):
		self.__newPoolSize = number
		
		if self.__newPoolSize < 1:
			#qDebug("Chance")
			self.__newPoolSize = 0
			self.__chance = True
		else:
			self.__chance = False

		if self.__poolSize != self.__newPoolSize:
			self.__poolSize = self.__newPoolSize
			#qDebug("Pool: " + unicode(self.__poolSize))
			self.poolSizeChanged.emit(self.__poolSize)


	# folgende Zeile erzeugt das Property-Attribut
	poolSize = property(getPoolSize, setPoolSize)


	def getThreshold(self):
		return self.__die.threshold


	def setThreshold(self, number):
		try:
			self.__die.threshold = number
			#qDebug("Threshold ist" + str(self.__die.threshold))
		except ErrValue, e:
			qDebug(e.msg + " Threshold remains unchanged.")


	# folgende Zeile erzeugt das Property-Attribut
	threshold = property(getThreshold, setThreshold)


	def setRote(self, flag):
		if self.__rote != flag:
			self.__rote = flag

			self.roteChanged.emit(self.__rote)


	def setCurse(self, flag):
		if self.__curse != flag:
			self.__curse = flag

			self.curseChanged.emit(self.__curse)


	def roll(self):
		self.__successes = 0
		self.__explosions = 0
		self.__botch = False

		self.rollDetails()

		#qDebug(unicode(self.__successes) + " Erfolge!")

		self.rolled.emit(self.__successes)


	def rollDetails(self):
		self.__realPoolSize = self.__poolSize
		if self.__realPoolSize < 1:
			self.__realPoolSize = 1

		# Sooft würfeln, wie ich Würfel im Pool habe
		for i in range(self.__realPoolSize):
			self.__die.roll()

		if self.__chance and self.__botch:
			#qDebug(unicode(self.__successes) + "Erfolge!\n PATZER!")
			self.rollFinished.emit(DieResult.dramaticFailure)
			return

		self.__rotePoolSize = self.__realPoolSize - self.__successes

		# Wenn self.__die rote-Eigenschaft aktiv ist, werden alle Mißerfolge noch einmal gewürfelt.
		# Hatten wir es aber mit einem Chance-Roll zu tun und der Mißerfolg war ein Patzer, wird auch nicht weitergewürfelt.
		if self.__rote:
			for i in range(self.__rotePoolSize):
				self.__die.roll()

		self.__tmpExplosions = 0

		# Wenn einer oder mehrere Würfel exploself.__dieren, werden self.__diese erneut gewürfelt. Dabei können sie natürlich wieder und wieder exploself.__dieren.
		while self.__explosions > 0:
			self.__tmpExplosions = self.__explosions
			self.__explosions = 0	# __explosions muß ich wieder zurücksetzen, da self.__die Würfel ja wieder exploself.__dieren können.

			for i in range(self.__tmpExplosions):
				self.__die.roll()

		if self.__successes < 1:
			self.rollFinished.emit(DieResult.failure)
		elif self.__successes < 5:
			self.rollFinished.emit(DieResult.success)
		else:
			self.rollFinished.emit(DieResult.exceptionalSuccess)


	def modifySuccess(self, value):
		if (value == DieResult.chanceSuccess or (value == DieResult.success and self.__poolSize > 0)):
			self.__successes += 1
		elif (self.__curse and value == DieResult.one):
			self.__successes -= 1


	def checkBotch(self, value):
		if (value == DieResult.one):
			self.__botch = True


	def addExplosion(self, flag):
		if (flag):
			self.__explosions += 1





class InstantRoll(DicePool):
	def __init__(self, parent=None):
		DicePool.__init__(self, parent)




class ExtendedRoll_Base(QObject):
	targetChanged = pyqtSignal(int)
	rolled = pyqtSignal(int)
	rollsNeeded = pyqtSignal(int)
	thresholdChanged = pyqtSignal(int)
	poolSizeChanged = pyqtSignal(int)
	roteChanged = pyqtSignal(bool)
	curseChanged = pyqtSignal(bool)
	rulesChanged = pyqtSignal(bool)
	rollFinished = pyqtSignal(object)


	def __init__(self, parent=None, target=1, poolsize=10):
		super(QObject, self).__init__()

		self._rolls = 0
		self._successes = 0
		self.__limit = 0
		self.__limited = False
		self.__maxRolls = 0

		self._dicePool = DicePool()

		self.__target = target
		self.__poolSize = poolsize
		
		self._exceptional = False
		self.__houserules = False

		self._dicePool.thresholdChanged.connect(self.thresholdChanged.emit)
		self._dicePool.poolSizeChanged.connect(self.poolSizeChanged.emit)
		self._dicePool.roteChanged.connect(self.roteChanged.emit)
		self._dicePool.curseChanged.connect(self.curseChanged.emit)
		self._dicePool.rulesChanged.connect(self.rulesChanged.emit)
		self._dicePool.rolled.connect(self.addSuccesses)
		self._dicePool.rollFinished.connect(self.stopRoll)		
		self._dicePool.rollFinished.connect(self.checkResult)


	def getPoolSize(self):
		return self._dicePool.poolSize


	def setPoolSize(self, number):
		#qDebug("Test")
		self._dicePool.poolSize = number


	# folgende Zeile erzeugt das Property-Attribut
	poolSize = property(getPoolSize, setPoolSize)


	def getThreshold(self):
		return self._dicePool.threshold


	def setThreshold(self, number):
		self._dicePool.threshold = number


	# folgende Zeile erzeugt das Property-Attribut
	threshold = property(getThreshold, setThreshold)


	def setRote(self, flag):
		self._dicePool.setRote(flag)


	def setCurse(self, flag):
		self._dicePool.setCurse(flag)


	def getTarget(self):
		return self.__target


	def setTarget(self, number):
		if (self.__target != number):
			self.__target = number
			self.targetChanged.emit(number)


	# folgende Zeile erzeugt das Property-Attribut
	target = property(getTarget, setTarget)


	def getLimit(self):
		return self.__limit


	def setLimit(self, number):
		if (self.__limit != number):
			self.__limit = number


	# folgende Zeile erzeugt das Property-Attribut
	limit = property(getLimit, setLimit)


	def getLimited(self):
		return self.__limited


	def setLimited(self, flag):
		if (self.__limited != flag):
			self.__limited = flag


	# folgende Zeile erzeugt das Property-Attribut
	isLimited = property(getLimited, setLimited)


	def getHouserules(self):
		return self.__houserules


	def setHouserules(self, flag):
		if self.__houserules != flag:
			self.__houserules = flag
			
			#qDebug("Hausregel ist " + str(self.__houserules))

			self.rulesChanged.emit(self.__houserules)


	# folgende Zeile erzeugt das Property-Attribut
	isHouserules = property(getHouserules, setHouserules)


	def roll(self):
		self.__continue = True
		self._successes = 0
		self._rolls = 0
		self._exceptional = False

		#qDebug("Erweiterter Würfelwurf beginnt!")

		# Wenn die Zahl der Würfe limitiert ist, darf man nicht öfter Würfeln als das Limit zuläßt. Aber einen Wurf muß man mindestens erlauben.
		# Außerdem wird nur sooft weitergewürfelt, wie kein Patzer fällt.
		while True:
			self._rolls += 1
			#qDebug(unicode(self._rolls) + ". Wurf.")

			self._dicePool.roll()

			if (
				not self.__continue or 
				self._successes >= self.target or 
				(self.isLimited and self._rolls >= self.limit)
			):
				break

		#qDebug("Insgesamt " + unicode(self._successes) + " Erfolge bei " + unicode(self._rolls) + " Würfen.")

		# Wieviele Erfolge wurden insgesamt erwürfelt.
		self.rolled.emit(self._successes)
		# Wieviele Würfe wurden durchgeführt.
		self.rollsNeeded.emit(self._rolls)

		# Erfolg ja/nein
		if (not self.__continue):
			self.rollFinished.emit(DieResult.dramaticFailure)
		else:
			if (self._successes < self.target):
				self.rollFinished.emit(DieResult.failure)
			elif (self.isHouserules):
				if (self._exceptional):
					self.rollFinished.emit(DieResult.exceptionalSuccesss)
				else:
					self.rollFinished.emit(DieResult.success)
			else:
				# Das hier ist die Standardregel. Ein Exceptional trifft nur dann zu, wenn das Ziel um 5 übertroffen wurde. Das aber ist eine doofe Regel. Ein Exceptional tritt dann ja kaum ein, da man im letzten Wurf mindestens \emph{6} Erfolge benötigt.
				if (self._successes > self.target + 4):
					self.rollFinished.emit(DieResult.exceptionalSuccess)
				else:
					self.rollFinished.emit(DieResult.success)


	def addSuccesses(self, number):
		self._successes += number


	def stopRoll(self, value):
		if (value == DieResult.dramaticFailure):
			self.__continue = False


	def checkResult(self, value):
		"""
		Diese Funktion überprüft, ob im Verlauf des Erweiterten wurfes, ein Exceptional Success gefallen ist.
		"""
		if (value == DieResult.exceptionalSuccess):
			self._exceptional = True




class ExtendedRoll(ExtendedRoll_Base):


	def __init__(self, parent=None, target=1, poolsize=10):
		ExtendedRoll_Base.__init__(self, parent, target, poolsize)

		self.__maxRolls = 0
		self.__rollsNumbered = False


	def getMaxRolls(self):
		return self.__maxRolls


	def setMaxRolls(self, number):
		"""
		Ist number = 0, wird der Wurf nicht auf maxRolls beschränkt.
		"""
		if (self.__maxRolls != number):
			self.__maxRolls = number


	# folgende Zeile erzeugt das Property-Attribut
	maxRolls = property(getMaxRolls, setMaxRolls)


	def getResultInRolls(self):
		return self.__rollsNumbered


	def setResultInRolls(self, sw):
		"""
		Legt fest, ob die Anzahl von Erfolgen bei maxRolls Würfen ermittelt (True), oder auf einen Zielwert hingewürfelt werden soll (False).
		In ersterem Fall wird sooft gewürfelt, wie maxRolls vorgibt, esseidenn rollsLimited ist True und der angegebene Würfelvorrat ist kleiner als maxRolls. Dann wird nur sooft gewürfelt, wie der Würfelwurf vorgibt.
		"""
		if (self.__rollsNumbered != sw):
			self.__rollsNumbered = sw


	# folgende Zeile erzeugt das Property-Attribut
	isResultInRolls = property(getResultInRolls, setResultInRolls)


	def roll(self):
		self.__continue = True
		self._successes = 0
		self._rolls = 0
		self._exceptional = False

		if self.isResultInRolls:
			#qDebug("Der Würfelwurf ist begrenzt auf " + str(self.maxRolls) + " Würfe")
			pass
		
		# Wenn die Zahl der Würfe limitiert ist, darf man nicht öfter Würfeln als das Limit zuläßt. Aber einen Wurf muß man mindestens erlauben.
		# Zudem kann maxRolls > 0 angegeben sein, dann darf auch nicht häufiger als dieser Wert gewürfelt werden. Es gilt aber der kleinere Wert von limit oder maxRolls
		# Außerdem wird nur sooft weitergewürfelt, wie kein Patzer fällt.
		while (True):
			self.__successesPerRoll = 0
			self._rolls += 1
			self._dicePool.roll()
			#qDebug("Bislang " + str(self._successes) + " Erfolge.")

			if (
				not self.__continue or 
				(not self.isResultInRolls and self._successes >= self.target) or 
				(self.isLimited and self._rolls >= self.limit) or 
				(self.isResultInRolls and self._rolls >= self.maxRolls)
			):
				break

		#qDebug("Insgesamt " + str(self._successes) + " Erfolge bei " + str(self._rolls) + " Würfen.")
		
		# Wieviele Erfolge wurden erzielt
		self.rolled.emit(self._successes)
		# Wieviele Würfe wurden benötigt.
		self.rollsNeeded.emit(self._rolls)

		# Erfolg ja/nein
		if (not self.__continue):
			self.rollFinished.emit(DieResult.dramaticFailure)
		else:
			if (self.isResultInRolls):
				# Diese Regeln treten in Kraft wenn die Anzahl der Würfe festgelegt ist.
				if (self._successes < 1):
					self.rollFinished.emit(DieResult.failure)
				elif (self._exceptional):
					self.rollFinished.emit(DieResult.exceptionalSuccess)
				else:
					self.rollFinished.emit(DieResult.success)
			else:
				if (self._successes < self.target):
					self.rollFinished.emit(DieResult.failure)
				elif (self.isHouserules):
					# Bei der Hausregel liegt immer dann ein außerordentlicher Erfolg vor, wenn wenigstens einzelner Wurf während des erweiterten Wurfs einen solchen zeigte.
					if (self._exceptional):
						self.rollFinished.emit(DieResult.exceptionalSuccess)
					else:
						self.rollFinished.emit(DieResult.success)
				else:
					# Das hier ist die Standardregel. Ein Exceptional trifft nur dann zu, wenn das Ziel um 5 übertroffen wurde. Das aber ist eine doofe Regel. Ein Exceptional tritt dann ja kaum ein, da man im letzten Wurf mindestens \emph{6} Erfolge benötigt.
					if (self._successes > self.target + 4):
						self.rollFinished.emit(DieResult.exceptionalSuccess)
					else:
						self.rollFinished.emit(DieResult.success)
