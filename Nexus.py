# -*- coding: utf-8 -*-

"""
Copyright (C) 2010 by Victor von Rhein
victor@caern.de

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


import os
import sys
import time

from PySide.QtCore import *
from PySide.QtGui import *
from PySide.QtSvg import *
# Hiermit kann ich weiterhin ich die Syntax der Signale und Slots so belassen, wie sie in PyQt vorgeschrieben ist.
from PySide.QtCore import Signal as pyqtSignal
from PySide.QtCore import Slot as pyqtSlot

from MainWindow import Ui_MainWindow
from Settings import Settings
from Random import Random
from Dice import DieResult
from DicePool import InstantRoll, ExtendedRoll
from RollingDieWidget import RollingDieWidget

from resources import resource_rc




PROGRAM_NAME = "DiceRoller WoD"
PROGRAM_VERSION_MAJOR = 0
PROGRAM_VERSION_MINOR = 2
PROGRAM_VERSION_CHANGE = 2
PROGRAM_DESCRIPTION = "A dice roller for the W10-System (World of Darkness)"

PROGRAM_LANGUAGE_PATH = "lang"

CONFIG_FILE = "config.cfg"

DICEROLL_TIMER_INTERVAL = 50
DICEROLL_TIMER_DELAY = 400

SIDES_DIE = 10
MAX_DICE_IN_DISPLAY = 10




def getPath():
	"""
	Get the path to this script no matter how it's run.
	"""

	#Determine if the application is a py/pyw or a frozen exe.
	if hasattr(sys,  'frozen'):
		# If run from exe
		dir_path = os.path.dirname(sys.executable)
	elif '__file__' in locals():
		# If run from py
		dir_path = os.path.dirname(__file__)
	else:
		# If run from command line
		dir_path = sys.path[0]
	return dir_path




class Nexus(QMainWindow):
	"""
	Die Hauptklasse des Programms.

	In dieser Klasse wird die GUI gesteuert und die Würfelwürfe aufgerufen.
	"""

	dicePoolChanged = pyqtSignal(int)
	xAgainChanged = pyqtSignal(int)
	cursed = pyqtSignal(bool)


	def __init__(self,  parent=None):
		"""
		Konstruktor 
		"""

		self.translator_app = QTranslator()
		self.translator_qt = QTranslator()

		QApplication.installTranslator( self.translator_app )
		QApplication.installTranslator( self.translator_qt )

		QMainWindow.__init__(self,  parent)

		QCoreApplication.setOrganizationName("Caern")
		QCoreApplication.setOrganizationDomain("www.caern.de")
		QCoreApplication.setApplicationName("DiceRoller WoD")
		QCoreApplication.setApplicationVersion(str(PROGRAM_VERSION_MAJOR) +
			"." +
			str(PROGRAM_VERSION_MINOR) +
			"." +
			str(PROGRAM_VERSION_CHANGE)
		)
		QApplication.setWindowIcon(QIcon(":/icons/logo/WoD.png"))

		self.ui = Ui_MainWindow()
		self.ui.setupUi(self)
		
		self.createInfo()

		self.instantRoll = InstantRoll()
		self.extendedRoll = ExtendedRoll()

		# Dieser Zähler bestimmt, wie der rollende Würfel angezeigt wird.
		self.timerDice = QTimer()
		# Verzögert die tatsächliche Ausführung des Würfelwurfs.
		self.timerRoll = QTimer()
		
		self.populateUi()
		self.createLanguageMenu()
		self.createConnections()
		self.initializing()

		self.setWindowTitle(QCoreApplication.applicationName())

		self.retranslateUi()
		
		## Die von der letzten Benutzung gespeicherte Größe und Position auf dem Bildschirm laden.
		#self.readSettings()


	#def closeEvent(self, event):
		#"""
		#Diese Funktion wird aufgerufen, wann immer das Programm geschlossen wird.
		#Die Idee dahinter ist, vor dem Beenden, Größe und Position des Fensters zu speichern.
		#"""
		#self.writeSettings()
		#event.accept()


	def createInfo(self):
		"""
		Erzeugt Tooltips und Hilfe für die einzelnen Teile des Programms.
		"""

		self.ui.action_houserules.setStatusTip(self.ui.action_houserules.toolTip())


	def createLanguageMenu(self):
		"""
		Erzeugt das Menü zum Umschalten zwischen den möglichen Sprachen.
		"""

		self.menu_language = QMenu( self.tr("&Language") )
		self.actionGroup_language = QActionGroup(self)

		self.langPath = getPath() + "/" + PROGRAM_LANGUAGE_PATH
		self.dir_qm = QDir( self.langPath );
		self.fileNames = self.dir_qm.entryList( ["DiceRoller-WoD_*.qm"]);

		# Englisch hat keine qm-Datei,  also muß es von Hand hinzugefügt werden.
		self.action = QAction( "&1 English",  self.actionGroup_language )
		self.action.setCheckable( True )
		self.action.setData( "en" )
		self.action.setChecked( True )

		self.menu_language.addAction( self.action )
		self.actionGroup_language.addAction( self.action )

		iter = 0
		for i in self.fileNames:
			self.trFilename = unicode(i)
			self.locale = unicode(i)
			self.locale = self.locale[(self.locale.find( "_" )+1):(self.locale.find( "." ))]

			self.translator = QTranslator()
			self.translator.load( self.trFilename,  self.dir_qm.absolutePath() )
			self.language = self.translator.translate( "MainWindow",  "English" )

			self.action = QAction( "&" + str(iter + 2) + " " + self.language,  self.actionGroup_language )
			self.action.setCheckable( True )
			self.action.setData( self.locale )

			self.menu_language.addAction ( self.action )
			self.actionGroup_language.addAction ( self.action )

			iter += 1

		self.actionGroup_language.triggered.connect(self.switchLanguage)

		self.ui.menuBar.insertMenu(self.ui.menuHelp.menuAction(),  self.menu_language)


	def switchLanguage( self,  action ):
		"""
		Schaltet zwischen den einzelnen Sprachen um.
		"""

		self.locale = str(action.data())
		self.qmPath = getPath() + "/" + PROGRAM_LANGUAGE_PATH

		if self.translator_app.load( "DiceRoller-WoD_" + self.locale,  self.qmPath ):
			qDebug("Hat DiceRoller-WoD_" + self.locale + " geladen.")

		if self.translator_qt.load( "qt_" + self.locale,  QLibraryInfo.location ( QLibraryInfo.TranslationsPath ) ):
			qDebug("Hat qt_" + self.locale + " geladen.")

		# Alle Texte neu setzen
		self.retranslateUi()
		# Seltsamerweise ist retranslate in Ui_MainWindow leer. Ich weiß nicht,  wieso das der Fall ist.
		self.ui.retranslateUi(self)


	def retranslateUi(self):
		"""
		Diese Funktion übersetzt alle Texte, welche nicht in der .ui-Datei festgelegt sind, sondern im Quellcode (hier) geschrieben wurden.
		"""

		self.menu_language.setTitle( self.tr( "&Language" ) )
		self.reset()


	def populateUi(self):
		self.rollingDie = RollingDieWidget(0)
		self.ui.horizontalLayout_dice.insertWidget(1, self.rollingDie)
		self.rollingDie.resize(self.rollingDie.renderer().defaultSize())


	def createConnections(self):
		"""
		Erstelle die Verbindungen zwischen den verschiedenen Klassen und Elementen des Programms.
		"""

		self.ui.action_about.triggered.connect(self.aboutApp)
		self.ui.action_aboutQt.triggered.connect(QApplication.aboutQt)
		self.ui.action_houserules.toggled.connect(self.setHouserules)
		self.ui.pushButton_roll.clicked.connect(self.roll)
		self.ui.spinBox_pool.valueChanged[int].connect(self.calcDicePool)
		self.ui.spinBox_pool.valueChanged.connect(self.reset)
		self.ui.spinBox_modifier.valueChanged[int].connect(self.calcDicePoolMod)
		self.ui.spinBox_modifier.valueChanged.connect(self.reset)
		self.ui.checkBox_rote.toggled.connect(self.instantRoll.setRote)
		self.ui.checkBox_rote.toggled.connect(self.extendedRoll.setRote)
		self.ui.checkBox_rote.toggled.connect(self.reset)
		self.ui.comboBox_xAgain.activated[int].connect(self.setXAgainThreshold)
		self.ui.comboBox_xAgain.activated.connect(self.reset)
		self.ui.groupBox_extended.toggled.connect(self.changeText)
		self.ui.radioButton_target.toggled.connect(self.changeText)
		self.ui.radioButton_maxRolls.toggled.connect(self.changeText)
		self.ui.groupBox_extended.toggled.connect(self.reset)
		self.ui.radioButton_target.toggled.connect(self.setExtendedMode)
		self.ui.spinBox_target.valueChanged[int].connect(self.extendedRoll.setTarget)
		self.ui.spinBox_target.valueChanged.connect(self.reset)
		self.ui.spinBox_maxRolls.valueChanged[int].connect(self.extendedRoll.setMaxRolls)
		self.ui.spinBox_maxRolls.valueChanged.connect(self.reset)
		self.ui.checkBox_rollsLimited.toggled.connect(self.extendedRoll.setLimited)
		self.ui.checkBox_rollsLimited.toggled.connect(self.reset)
		self.xAgainChanged.connect(self.instantRoll.setThreshold)
		self.xAgainChanged.connect(self.extendedRoll.setThreshold)
		self.cursed.connect(self.instantRoll.setCurse)
		self.cursed.connect(self.extendedRoll.setCurse)
		self.instantRoll.rolled.connect(self.setResultSuccesses)
		self.extendedRoll.rolled.connect(self.setResultSuccesses)
		self.extendedRoll.rollsNeeded.connect(self.setResultRolls)
		self.instantRoll.rollFinished.connect(self.setResult)
		self.extendedRoll.rollFinished.connect(self.setResult)

		self.dicePoolChanged.connect(self.changeDiceDisplay)

		self.timerDice.timeout.connect(self.displayDice)
		self.timerRoll.timeout.connect(self._executeRoll)


	def initializing(self):
		"""
		Initialisiert das Programm mit den Startwerten.
		"""

		self.ui.action_quit.setIcon(QIcon(":/icons/actions/exit.png"))
		self.ui.action_about.setIcon(QIcon(":/icons/logo/WoD.png"))
		self.ui.pushButton_quit.setIcon(self.ui.action_quit.icon())
		self.ui.pushButton_roll.setIcon(QIcon(":icons/W10_0.svg"))
		
		self.ui.action_quit.setMenuRole(QAction.QuitRole)
		self.ui.action_about.setText(self.tr(str("About %(appName)s..." % {"appName": QApplication.applicationName()})))
		self.ui.action_about.setMenuRole(QAction.AboutRole)

		self.ui.spinBox_pool.setValue(2)
		self.ui.checkBox_rote.setChecked(False)
		self.ui.comboBox_xAgain.setCurrentIndex(0)
		self.ui.spinBox_target.setValue(1)
		self.changeText()
		self.ui.radioButton_target.setChecked(True)
		self.ui.groupBox_extended.setChecked(False)
		self.ui.checkBox_rollsLimited.setChecked(True)


	def displayDice(self, value=None):
		"""
		@todo Der Würfel kann mehrmals in Folge das selbe Ergebnis anzeigen, was dazu führt, daß der Bildablauf zu stocken scheint.
		"""

		if (value == None):
			dieValue = Random.random(10)-1
		else:
			dieValue = value
		
		self.rollingDie.setFace(dieValue)
		self.rollingDie.resize(self.rollingDie.sizeHint())


	def changeDiceDisplay(self, number):
		"""
		Diese Funktion bestimmt, wieviele Würfel angezeigt werden.
		"""
		pass


	def aboutApp(self):
		"""
		Zeigt die Info-Nachricht an.
		"""

		self.appText = self.tr("""
			<h1>%1</h1>
			<h2>Version: %2</h2>
			<p>Copyright (C) 2011 by Victor von Rhein<br>
			EMail: victor@caern.de</p>
		""").arg(QCoreApplication.applicationName()).arg(QCoreApplication.applicationVersion())
		self.gnuText = self.tr("""
			<h2>GNU General Public License</h2>
			<p>This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation,  either version 3 of the License,  or (at your option) any later version.</p>
			<p>This program is distributed in the hope that it will be useful,  but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.</p>
			<p>You should have received a copy of the GNU General Public License along with this program.  If not,  see <a>http://www.gnu.org/licenses/</a>.</p>
		""")
		self.wodText = self.tr("""
			<h2>%1</h2>
			<p>%1,  %2,  the %3 and all referring terms and symbols are copyrighted by %4</p>
		""").arg("World of Darkness").arg("White Wolf").arg("White Wolf-Logo").arg("White Wolf Inc.")
		self.aboutText = self.appText + self.gnuText + self.wodText
		QMessageBox.about(self,  "About " + QCoreApplication.applicationName(),  self.aboutText )


	def roll(self):
		"""
		Der Wurf wird durchgeführt. Der tatsächliche Wurf wird aber von den Timern angestoßen.
		"""

		# Es wird ein rollender Würfel angezeigt.
		self.timerDice.start(DICEROLL_TIMER_INTERVAL)
		self.timerRoll.start(DICEROLL_TIMER_DELAY)


	def _executeRoll(self):
		"""
		Entscheidet vor dem eigentlichen Würfelwurf, ob ein normaler oder ein erweiterter Wurf notwendig ist und führt diesen aus.
		"""

		if self.ui.groupBox_extended.isChecked():
			#qDebug("Checked")
			self.extendedRoll.roll()
		else:
			#qDebug("Not Checked")
			self.instantRoll.roll()

		# Die Anzeige des rollenden Würfels wird angehalten
		self.timerDice.stop()
		self.timerRoll.stop()


	def calcDicePool(self, value):
		"""
		Berechnet die Größe des zur Verfügung stehenden Würfelpools, welcher von den Würfeln und den Modifikatoren abhängt.
		"""

		self.instantRoll.poolSize = value + self.ui.spinBox_modifier.value()
		self.extendedRoll.poolSize = self.instantRoll.poolSize
		self.extendedRoll.limit = value
		
		self.dicePoolChanged.emit(self.instantRoll.poolSize)


	def calcDicePoolMod(self, value):
		"""
		Berechnet wie schon calcDicePool() die Größe des Würfelvorrats, allerdings werden dieser Funktion andere Argumente übergeben.
		"""

		self.instantRoll.poolSize = value + self.ui.spinBox_pool.value()
		self.extendedRoll.poolSize = value + self.ui.spinBox_pool.value()


	def setHouserules(self, value):
		#qDebug("Test" + str(value))
		self.extendedRoll.isHouserules = value


	def setXAgainThreshold(self, value):
		"""
		Legt fest, bei welchem Ergebnis weitergewürfelt werden kann und wann dies überhaupt nicht der Fall sein sollte oder gar Erfolge abgezogen werden können.
		"""

		self.__threshold = 0
		if (value < 3):
			self.__threshold = 10 - value	# Index 0 entspricht 10 again, 1 entspricht 9 again etc.
		else:
			self.__threshold = 11	# Index 3 entspricht "no reroll"

		self.xAgainChanged.emit(self.__threshold)

		if (value > 3):
			self.cursed.emit(True)	# Kein reroll und 1er werden Abgezogen.
		else:
			self.cursed.emit(False)	# 1er werden nicht abgezogen.


	def setExtendedMode(self, sw):
		"""
		Legt den Modus fest, mit welchem der erweiterte Wurf durchgeführt wird. Entweder wird auf ein Ergebnishingewürfelt, oder nach einer bestimmten Anzahl würde die Anzahl der Erfolge gezählt.
		"""

		if (sw):
			self.extendedRoll.isResultInRolls = False
		else:
			self.extendedRoll.isResultInRolls = True


	def setResult(self, value):
		"""
		Schreibt das Ergebnis des Wurfs in die GUI. Dabei wird auch je nach Erfolgsqualität bei dem dargestellten Würfel eine andere Augenzahl gezeigt.
		"""

		self.ui.statusBar.showMessage(self.tr("Result of diceroll is displayed."))

		if (value == DieResult.dramaticFailure):
			self.ui.label_resultText.setText(self.tr(str("Dramatic Failure")))
			self.ui.label_result.setPixmap(QPixmap(":/icons/actions/cnrdelete-all1.png"))
			self.displayDice(1)
		elif (value == DieResult.failure):
			self.ui.label_resultText.setText(self.tr(str("Failure")))
			self.ui.label_result.setPixmap(QPixmap(":/icons/actions/fileclose.png"))
			self.displayDice(Random.random(2, 7))
		elif (value == DieResult.success):
			self.ui.label_resultText.setText(self.tr(str("Success")))
			self.ui.label_result.setPixmap(QPixmap(":/icons/actions/ok.png"))
			self.displayDice(Random.random(8, 9))
		else:
			self.ui.label_resultText.setText(self.tr(str("Exceptional Success")))
			self.ui.label_result.setPixmap(QPixmap(":/icons/actions/bookmark.png"))
			self.displayDice(0)


	def setResultRolls(self, value):
		"""
		Zeigt in der GUI an, wieviele Würfe nötig waren.
		"""

		if (self.ui.groupBox_extended.isChecked() and self.ui.radioButton_target.isChecked()):
			self.ui.label_successesNumber.setText(str(value))


	def setResultSuccesses(self, value):
		"""
		Zeigt in der GUI an, wieviele Erfolge erzielt wurden.
		"""

		if (not self.ui.groupBox_extended.isChecked() or not self.ui.radioButton_target.isChecked()):
			self.ui.label_successesNumber.setText(str(value))


	def changeText(self):
		"""
		Verändert den Text in der Statuszeile.
		"""

		if (self.ui.groupBox_extended.isChecked() and self.ui.radioButton_target.isChecked()):
			self.ui.label_successes.setText(self.tr("Number of rolls needed:"))
		else:
			self.ui.label_successes.setText(self.tr("Number of successes:"))


	def reset(self):
		"""
		Setzt das Programm auf einen definierten Startwert zurück.
		"""

		self.ui.label_result.setPixmap(QPixmap(":/icons/actions/fileclose.png"))
		self.ui.label_resultText.setText(self.tr("No result yet!"))
		self.ui.label_successesNumber.setText(str(0))
		self.ui.statusBar.showMessage(self.tr("Press the Button to roll the dice!"))


	#def writeSettings(self):
		#"""
		#Speichert Größe und Position des Fensters in der Konfigurationsdatei.
		#"""

		#settings = Settings( getPath() + "/" + CONFIG_FILE )

		#settings.beginGroup( "MainWindow" )
		#settings.setValue( "size", self.size() )
		#settings.setValue( "pos", self.pos() )
		#settings.setValue( "state", self.saveState() )
		#settings.endGroup()


	#def readSettings(self):
		#"""
		#Liest Größe und Position des Fensters aus der Konfigurationsdatei.
		#"""

		#settings = Settings( getPath() + "/" + CONFIG_FILE )

		#settings.beginGroup( "MainWindow" )
		#self.resize( settings.value( "size", QSize( 460, 270 ) ).toSize() )
		#self.move( settings.value( "pos", QPoint( 0, 0 ) ).toPoint() )
		#self.restoreState( settings.value( "state" ).toByteArray() )
		#settings.endGroup()
