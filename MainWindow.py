# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MainWindow.ui'
#
# Created: Tue Nov 22 13:33:30 2011
#      by: pyside-uic 0.2.11 running on PySide 1.0.6
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_MainWindow(object):
	def setupUi(self, MainWindow):
		MainWindow.setObjectName("MainWindow")
		MainWindow.resize(471, 274)
		sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
		MainWindow.setSizePolicy(sizePolicy)
		self.centralWidget = QtGui.QWidget(MainWindow)
		self.centralWidget.setObjectName("centralWidget")
		self.verticalLayout_4 = QtGui.QVBoxLayout(self.centralWidget)
		self.verticalLayout_4.setObjectName("verticalLayout_4")
		self.horizontalLayout_4 = QtGui.QHBoxLayout()
		self.horizontalLayout_4.setObjectName("horizontalLayout_4")
		self.verticalLayout = QtGui.QVBoxLayout()
		self.verticalLayout.setObjectName("verticalLayout")
		self.horizontalLayout_2 = QtGui.QHBoxLayout()
		self.horizontalLayout_2.setObjectName("horizontalLayout_2")
		self.formLayout = QtGui.QFormLayout()
		self.formLayout.setObjectName("formLayout")
		self.label_diceNumber = QtGui.QLabel(self.centralWidget)
		self.label_diceNumber.setObjectName("label_diceNumber")
		self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.label_diceNumber)
		self.spinBox_pool = QtGui.QSpinBox(self.centralWidget)
		self.spinBox_pool.setMinimum(0)
		self.spinBox_pool.setMaximum(999)
		self.spinBox_pool.setProperty("value", 10)
		self.spinBox_pool.setObjectName("spinBox_pool")
		self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.spinBox_pool)
		self.label = QtGui.QLabel(self.centralWidget)
		self.label.setObjectName("label")
		self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.label)
		self.spinBox_modifier = QtGui.QSpinBox(self.centralWidget)
		self.spinBox_modifier.setMinimum(-99)
		self.spinBox_modifier.setObjectName("spinBox_modifier")
		self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.spinBox_modifier)
		self.horizontalLayout_2.addLayout(self.formLayout)
		self.verticalLayout_2 = QtGui.QVBoxLayout()
		self.verticalLayout_2.setObjectName("verticalLayout_2")
		self.comboBox_xAgain = QtGui.QComboBox(self.centralWidget)
		self.comboBox_xAgain.setObjectName("comboBox_xAgain")
		self.comboBox_xAgain.addItem("")
		self.comboBox_xAgain.addItem("")
		self.comboBox_xAgain.addItem("")
		self.comboBox_xAgain.addItem("")
		self.comboBox_xAgain.addItem("")
		self.verticalLayout_2.addWidget(self.comboBox_xAgain)
		self.checkBox_rote = QtGui.QCheckBox(self.centralWidget)
		self.checkBox_rote.setObjectName("checkBox_rote")
		self.verticalLayout_2.addWidget(self.checkBox_rote)
		spacerItem = QtGui.QSpacerItem(0, 0, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
		self.verticalLayout_2.addItem(spacerItem)
		self.horizontalLayout_2.addLayout(self.verticalLayout_2)
		self.verticalLayout.addLayout(self.horizontalLayout_2)
		spacerItem1 = QtGui.QSpacerItem(0, 0, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
		self.verticalLayout.addItem(spacerItem1)
		self.pushButton_roll = QtGui.QPushButton(self.centralWidget)
		self.pushButton_roll.setMinimumSize(QtCore.QSize(0, 50))
		font = QtGui.QFont()
		font.setPointSize(18)
		self.pushButton_roll.setFont(font)
		self.pushButton_roll.setIconSize(QtCore.QSize(32, 32))
		self.pushButton_roll.setObjectName("pushButton_roll")
		self.verticalLayout.addWidget(self.pushButton_roll)
		self.horizontalLayout_4.addLayout(self.verticalLayout)
		self.groupBox_extended = QtGui.QGroupBox(self.centralWidget)
		self.groupBox_extended.setCheckable(True)
		self.groupBox_extended.setObjectName("groupBox_extended")
		self.verticalLayout_3 = QtGui.QVBoxLayout(self.groupBox_extended)
		self.verticalLayout_3.setObjectName("verticalLayout_3")
		self.gridLayout = QtGui.QGridLayout()
		self.gridLayout.setObjectName("gridLayout")
		self.spinBox_target = QtGui.QSpinBox(self.groupBox_extended)
		self.spinBox_target.setEnabled(False)
		self.spinBox_target.setMinimum(1)
		self.spinBox_target.setMaximum(9999)
		self.spinBox_target.setObjectName("spinBox_target")
		self.gridLayout.addWidget(self.spinBox_target, 0, 1, 1, 1)
		self.radioButton_maxRolls = QtGui.QRadioButton(self.groupBox_extended)
		self.radioButton_maxRolls.setObjectName("radioButton_maxRolls")
		self.gridLayout.addWidget(self.radioButton_maxRolls, 1, 0, 1, 1)
		self.spinBox_maxRolls = QtGui.QSpinBox(self.groupBox_extended)
		self.spinBox_maxRolls.setEnabled(False)
		self.spinBox_maxRolls.setMinimum(1)
		self.spinBox_maxRolls.setMaximum(9999)
		self.spinBox_maxRolls.setObjectName("spinBox_maxRolls")
		self.gridLayout.addWidget(self.spinBox_maxRolls, 1, 1, 1, 1)
		self.radioButton_target = QtGui.QRadioButton(self.groupBox_extended)
		self.radioButton_target.setObjectName("radioButton_target")
		self.gridLayout.addWidget(self.radioButton_target, 0, 0, 1, 1)
		self.verticalLayout_3.addLayout(self.gridLayout)
		spacerItem2 = QtGui.QSpacerItem(0, 0, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
		self.verticalLayout_3.addItem(spacerItem2)
		self.checkBox_rollsLimited = QtGui.QCheckBox(self.groupBox_extended)
		self.checkBox_rollsLimited.setObjectName("checkBox_rollsLimited")
		self.verticalLayout_3.addWidget(self.checkBox_rollsLimited)
		self.horizontalLayout_4.addWidget(self.groupBox_extended)
		self.verticalLayout_4.addLayout(self.horizontalLayout_4)
		self.horizontalLayout = QtGui.QHBoxLayout()
		self.horizontalLayout.setObjectName("horizontalLayout")
		self.label_result = QtGui.QLabel(self.centralWidget)
		self.label_result.setText("")
		self.label_result.setPixmap(QtGui.QPixmap(":/actions/actions/fileclose.png"))
		self.label_result.setObjectName("label_result")
		self.horizontalLayout.addWidget(self.label_result)
		self.label_resultText = QtGui.QLabel(self.centralWidget)
		self.label_resultText.setObjectName("label_resultText")
		self.horizontalLayout.addWidget(self.label_resultText)
		spacerItem3 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
		self.horizontalLayout.addItem(spacerItem3)
		self.label_successes = QtGui.QLabel(self.centralWidget)
		self.label_successes.setObjectName("label_successes")
		self.horizontalLayout.addWidget(self.label_successes)
		self.label_successesNumber = QtGui.QLabel(self.centralWidget)
		font = QtGui.QFont()
		font.setPointSize(24)
		self.label_successesNumber.setFont(font)
		self.label_successesNumber.setObjectName("label_successesNumber")
		self.horizontalLayout.addWidget(self.label_successesNumber)
		self.verticalLayout_4.addLayout(self.horizontalLayout)
		self.horizontalLayout_3 = QtGui.QHBoxLayout()
		self.horizontalLayout_3.setObjectName("horizontalLayout_3")
		spacerItem4 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
		self.horizontalLayout_3.addItem(spacerItem4)
		self.pushButton_quit = QtGui.QPushButton(self.centralWidget)
		self.pushButton_quit.setObjectName("pushButton_quit")
		self.horizontalLayout_3.addWidget(self.pushButton_quit)
		self.verticalLayout_4.addLayout(self.horizontalLayout_3)
		self.frame_dice = QtGui.QFrame(self.centralWidget)
		self.frame_dice.setFrameShape(QtGui.QFrame.NoFrame)
		self.frame_dice.setFrameShadow(QtGui.QFrame.Raised)
		self.frame_dice.setObjectName("frame_dice")
		self.horizontalLayout_dice = QtGui.QHBoxLayout(self.frame_dice)
		self.horizontalLayout_dice.setObjectName("horizontalLayout_dice")
		spacerItem5 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
		self.horizontalLayout_dice.addItem(spacerItem5)
		spacerItem6 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
		self.horizontalLayout_dice.addItem(spacerItem6)
		self.verticalLayout_4.addWidget(self.frame_dice)
		MainWindow.setCentralWidget(self.centralWidget)
		self.statusBar = QtGui.QStatusBar(MainWindow)
		self.statusBar.setObjectName("statusBar")
		MainWindow.setStatusBar(self.statusBar)
		self.menuBar = QtGui.QMenuBar(MainWindow)
		self.menuBar.setGeometry(QtCore.QRect(0, 0, 471, 21))
		self.menuBar.setObjectName("menuBar")
		self.menu_File = QtGui.QMenu(self.menuBar)
		self.menu_File.setObjectName("menu_File")
		self.menuHelp = QtGui.QMenu(self.menuBar)
		self.menuHelp.setObjectName("menuHelp")
		self.menuExtras = QtGui.QMenu(self.menuBar)
		self.menuExtras.setObjectName("menuExtras")
		MainWindow.setMenuBar(self.menuBar)
		self.action_quit = QtGui.QAction(MainWindow)
		self.action_quit.setObjectName("action_quit")
		self.action_about = QtGui.QAction(MainWindow)
		self.action_about.setObjectName("action_about")
		self.action_houserules = QtGui.QAction(MainWindow)
		self.action_houserules.setCheckable(True)
		self.action_houserules.setObjectName("action_houserules")
		self.action_aboutQt = QtGui.QAction(MainWindow)
		self.action_aboutQt.setObjectName("action_aboutQt")
		self.menu_File.addAction(self.action_quit)
		self.menuHelp.addAction(self.action_about)
		self.menuHelp.addAction(self.action_aboutQt)
		self.menuExtras.addAction(self.action_houserules)
		self.menuBar.addAction(self.menu_File.menuAction())
		self.menuBar.addAction(self.menuExtras.menuAction())
		self.menuBar.addAction(self.menuHelp.menuAction())
		self.label_diceNumber.setBuddy(self.spinBox_pool)
		self.label.setBuddy(self.spinBox_modifier)

		self.retranslateUi(MainWindow)
		QtCore.QObject.connect(self.action_quit, QtCore.SIGNAL("activated()"), MainWindow.close)
		QtCore.QObject.connect(self.pushButton_quit, QtCore.SIGNAL("clicked()"), MainWindow.close)
		QtCore.QObject.connect(self.radioButton_target, QtCore.SIGNAL("toggled(bool)"), self.spinBox_target.setEnabled)
		QtCore.QObject.connect(self.radioButton_maxRolls, QtCore.SIGNAL("toggled(bool)"), self.spinBox_maxRolls.setEnabled)
		QtCore.QMetaObject.connectSlotsByName(MainWindow)
		MainWindow.setTabOrder(self.spinBox_pool, self.spinBox_modifier)
		MainWindow.setTabOrder(self.spinBox_modifier, self.comboBox_xAgain)
		MainWindow.setTabOrder(self.comboBox_xAgain, self.checkBox_rote)
		MainWindow.setTabOrder(self.checkBox_rote, self.groupBox_extended)
		MainWindow.setTabOrder(self.groupBox_extended, self.checkBox_rollsLimited)

	def retranslateUi(self, MainWindow):
		MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "DiceRoller", None, QtGui.QApplication.UnicodeUTF8))
		self.label_diceNumber.setText(QtGui.QApplication.translate("MainWindow", "&Dice", None, QtGui.QApplication.UnicodeUTF8))
		self.spinBox_pool.setToolTip(QtGui.QApplication.translate("MainWindow", "The number of dice for this pool without any Modifiers.", None, QtGui.QApplication.UnicodeUTF8))
		self.label.setText(QtGui.QApplication.translate("MainWindow", "&Modifier", None, QtGui.QApplication.UnicodeUTF8))
		self.spinBox_modifier.setToolTip(QtGui.QApplication.translate("MainWindow", "The Modifiers for this roll.", None, QtGui.QApplication.UnicodeUTF8))
		self.comboBox_xAgain.setToolTip(QtGui.QApplication.translate("MainWindow", "The reroll-property for this roll.", None, QtGui.QApplication.UnicodeUTF8))
		self.comboBox_xAgain.setItemText(0, QtGui.QApplication.translate("MainWindow", "10 again", None, QtGui.QApplication.UnicodeUTF8))
		self.comboBox_xAgain.setItemText(1, QtGui.QApplication.translate("MainWindow", "9 again", None, QtGui.QApplication.UnicodeUTF8))
		self.comboBox_xAgain.setItemText(2, QtGui.QApplication.translate("MainWindow", "8 again", None, QtGui.QApplication.UnicodeUTF8))
		self.comboBox_xAgain.setItemText(3, QtGui.QApplication.translate("MainWindow", "no reroll", None, QtGui.QApplication.UnicodeUTF8))
		self.comboBox_xAgain.setItemText(4, QtGui.QApplication.translate("MainWindow", "subtract 1s", None, QtGui.QApplication.UnicodeUTF8))
		self.checkBox_rote.setToolTip(QtGui.QApplication.translate("MainWindow", "Activate the Rote-ability (allowing you to reroll all unsuccessfule dice).", None, QtGui.QApplication.UnicodeUTF8))
		self.checkBox_rote.setText(QtGui.QApplication.translate("MainWindow", "&Rote-property", None, QtGui.QApplication.UnicodeUTF8))
		self.pushButton_roll.setToolTip(QtGui.QApplication.translate("MainWindow", "Press Button to roll the dice.", None, QtGui.QApplication.UnicodeUTF8))
		self.pushButton_roll.setText(QtGui.QApplication.translate("MainWindow", "&Roll", None, QtGui.QApplication.UnicodeUTF8))
		self.groupBox_extended.setToolTip(QtGui.QApplication.translate("MainWindow", "Rolls an Extended Roll, gathering successes over multiple rolls of the pool.", None, QtGui.QApplication.UnicodeUTF8))
		self.groupBox_extended.setTitle(QtGui.QApplication.translate("MainWindow", "&Extdended roll", None, QtGui.QApplication.UnicodeUTF8))
		self.spinBox_target.setToolTip(QtGui.QApplication.translate("MainWindow", "The target number for the extended roll.", None, QtGui.QApplication.UnicodeUTF8))
		self.radioButton_maxRolls.setText(QtGui.QApplication.translate("MainWindow", "maximum Rolls", None, QtGui.QApplication.UnicodeUTF8))
		self.spinBox_maxRolls.setToolTip(QtGui.QApplication.translate("MainWindow", "The target number for the extended roll.", None, QtGui.QApplication.UnicodeUTF8))
		self.radioButton_target.setText(QtGui.QApplication.translate("MainWindow", "Target Number", None, QtGui.QApplication.UnicodeUTF8))
		self.checkBox_rollsLimited.setToolTip(QtGui.QApplication.translate("MainWindow", "Limits the roll to only so many rolls as you have dice in the pool (not counting any modifiers, be they positive or negative).", None, QtGui.QApplication.UnicodeUTF8))
		self.checkBox_rollsLimited.setText(QtGui.QApplication.translate("MainWindow", "Rolls &Limited", None, QtGui.QApplication.UnicodeUTF8))
		self.label_resultText.setText(QtGui.QApplication.translate("MainWindow", "No Result", None, QtGui.QApplication.UnicodeUTF8))
		self.label_successes.setText(QtGui.QApplication.translate("MainWindow", "Successes:", None, QtGui.QApplication.UnicodeUTF8))
		self.label_successesNumber.setText(QtGui.QApplication.translate("MainWindow", "0", None, QtGui.QApplication.UnicodeUTF8))
		self.pushButton_quit.setText(QtGui.QApplication.translate("MainWindow", "&Quit", None, QtGui.QApplication.UnicodeUTF8))
		self.menu_File.setTitle(QtGui.QApplication.translate("MainWindow", "&File", None, QtGui.QApplication.UnicodeUTF8))
		self.menuHelp.setTitle(QtGui.QApplication.translate("MainWindow", "&Help", None, QtGui.QApplication.UnicodeUTF8))
		self.menuExtras.setTitle(QtGui.QApplication.translate("MainWindow", "E&xtras", None, QtGui.QApplication.UnicodeUTF8))
		self.action_quit.setText(QtGui.QApplication.translate("MainWindow", "Quit", None, QtGui.QApplication.UnicodeUTF8))
		self.action_quit.setToolTip(QtGui.QApplication.translate("MainWindow", "Quit the program.", None, QtGui.QApplication.UnicodeUTF8))
		self.action_quit.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+Q", None, QtGui.QApplication.UnicodeUTF8))
		self.action_about.setText(QtGui.QApplication.translate("MainWindow", "About...", None, QtGui.QApplication.UnicodeUTF8))
		self.action_about.setToolTip(QtGui.QApplication.translate("MainWindow", "About DiceRoller-WoD.", None, QtGui.QApplication.UnicodeUTF8))
		self.action_houserules.setText(QtGui.QApplication.translate("MainWindow", "&Houserules", None, QtGui.QApplication.UnicodeUTF8))
		self.action_houserules.setToolTip(QtGui.QApplication.translate("MainWindow", "The houserule of the programmes group will be used: In Extended rolls, an exceptional success is achieved, whenever any roll during the process shows 5 successes or more.", None, QtGui.QApplication.UnicodeUTF8))
		self.action_aboutQt.setText(QtGui.QApplication.translate("MainWindow", "About Qt...", None, QtGui.QApplication.UnicodeUTF8))

