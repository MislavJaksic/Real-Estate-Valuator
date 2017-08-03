#PyQt references(no explainations): http://pyqt.sourceforge.net/Docs/PyQt5/

#General: http://doc.qt.io/qt-5.6/index.html

#Examples: http://doc.qt.io/qt-5.6/qtexamplesandtutorials.html
#Great example: https://pythonprogramming.net/drop-down-button-window-styles-pyqt-tutorial/
#Video example: https://pythonschool.net/pyqt/switching-layouts/

#Basic, most useful modules: http://doc.qt.io/qt-5.6/qtmodules.html

from PyQt5.QtWidgets import QComboBox, QWidget, QLabel, QComboBox, QPushButton, QCheckBox
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWidgets import QFormLayout, QHBoxLayout, QVBoxLayout

import sys
import os
sys.path.insert(0, os.path.abspath('../..'))

from RealEstateValuationSystem.DatabaseControl.DatabaseController import DatabaseController
from RealEstateValuationSystem.DataAnalysis import DatasetConfig

import re

inputLabels = ['state', 'town', 'place', 'size', 'yearOfConstruction', 'yearOfLastAdaptation', 'numberOfRooms', 'floor', 'numberOfParkingSpaces']

checkBoxes = [
"onlyReliableHouses?", "anotherOption",
]
RESULTS = [
"number of data points", "model algo", "model mistake", "value of property",
]

class ValuateApartment(QMainWindow):
	
	def __init__(self):
		super(ValuateApartment, self).__init__()
		self.CreateInterface()
	
	def CreateInterface(self):
		self.CreateGUIElements()
		self.PositionGUIElements()
		
		self.setWindowTitle("Valuate Apartment")
		
		self.show()
		
	def CreateGUIElements(self):
		self.CreateInputLabels()
		self.CreateInputDropdownMenus()
		self.CreateCheckBoxes()
		self.CreateValuateButton()
		self.CreateOutputLabels()
		
	def CreateInputLabels(self):
		self.allInputLabels = []
		for name in inputLabels:
			self.allInputLabels.append(QLabel(name))
	
	def CreateInputDropdownMenus(self):
		self.allInputDropdownMenus = []
		self.db = DatabaseController()
		self.db.Open(DatasetConfig.conn)
		for name in inputLabels:
			menu = QComboBox()
			self.AddDataToDropdownMenu(menu, name)
			self.allInputDropdownMenus.append(menu)
		self.db.Close()
	
	def AddDataToDropdownMenu(self, menu, name):
		if name == 'state':
			data = self.db.GetDataIter({}, distinct='state')
		if name == 'town':
			data = self.db.GetDataIter({'state':self.allInputDropdownMenus[0].currentText()}, distinct='town')
			self.allInputDropdownMenus[0].currentIndexChanged[str].connect(self.Change_Town_DropdownMenu)
		if name == 'place':
			data = self.db.GetDataIter({'town':self.allInputDropdownMenus[1].currentText()}, distinct='place')
			self.allInputDropdownMenus[1].currentIndexChanged[str].connect(self.Change_Place_DropdownMenu)
		if name == 'size':
			data = [str(number) for number in xrange(5, 500, 1)]
		if name == 'yearOfConstruction':
			data = [str(number) for number in xrange(1940, 2018, 1)]
		if name == 'yearOfLastAdaptation':
			data = [str(number) for number in xrange(1940, 2018, 1)]
		if name == 'numberOfRooms':
			data = self.db.GetDataIter({}, distinct='numberOfRooms')
		if name == 'floor':
			data = self.db.GetDataIter({}, distinct='floor')
			data.remove(0)
		if name == 'numberOfParkingSpaces':
			data = [str(number) for number in xrange(0, 7, 1)]
		
		NaturalSort(data)
		menu.addItems(data)
		
	def Change_Town_DropdownMenu(self, selectedState):
		db = DatabaseController()
		db.Open(DatasetConfig.conn)
		data = db.GetDataIter({'state' : selectedState}, distinct='town')
		db.Close()
		
		NaturalSort(data)
		menu = self.allInputDropdownMenus[1] #change to a dict so you don't have to remember the position of the dropdown menu
		menu.clear()
		menu.addItems(data)
		
	def Change_Place_DropdownMenu(self, selectedState):
		db = DatabaseController()
		db.Open(DatasetConfig.conn)
		data = db.GetDataIter({'town' : selectedState}, distinct='place')
		db.Close()
		
		NaturalSort(data)
		menu = self.allInputDropdownMenus[2]
		menu.clear()
		menu.addItems(data)
	
	def CreateCheckBoxes(self):
		self.allOptionCheckBoxes = []
		for name in checkBoxes:
			self.allOptionCheckBoxes.append(QCheckBox(name))
	
	def CreateValuateButton(self):
		self.valuateButton = QPushButton('Valuate apartment')
		self.valuateButton.clicked.connect(self.Valuate)
	
	def Valuate(self):
		for dropdownMenu in self.allInputDropdownMenus:
			print dropdownMenu.currentText()
		for checkBox in self.allOptionCheckBoxes:
			print checkBox.checkState()
		
		customerData = {}
		for i in range(0, len(inputLabels)):
			try:
				customerData[inputLabels[i]] = [int(self.allInputDropdownMenus[i].currentText())]
			except:
				customerData[inputLabels[i]] = [self.allInputDropdownMenus[i].currentText()]
		price = PredictApartmentPrice(customerData)
		self.allOutputLabels[0].setText(self.allOutputLabels[0].text() + str(price[0]))
	
	def CreateOutputLabels(self):
		self.allOutputLabels = []
		for name in RESULTS:
			self.allOutputLabels.append(QLabel(name))
	
	
	#Interface design: 
	#the first column has labels and dropdown menus paired up and below them are check boxes
	#	customers input data through the dropdown menus and choose additional options through the check boxes
	#the second column has a valuate button
	#	customers will begin the valuation process by pressing it
	# the third column will display the results of the valuation
	def PositionGUIElements(self):
		self.CreateLayouts()
		self.AddElementsToLayoutAndNestLayouts()
		self.AddLayoutToCentralWidget()
	
	def CreateLayouts(self):
		self.horizontalStripLayout = QHBoxLayout()
		self.firstColumnLayout = QVBoxLayout()
		self.thirdColumnLayout = QVBoxLayout()
		self.inputLabelAndDropdownMenuPairLayout = QFormLayout()
	
	def AddElementsToLayoutAndNestLayouts(self):
		for i in range(len(inputLabels)):
			self.inputLabelAndDropdownMenuPairLayout.addRow(self.allInputLabels[i], self.allInputDropdownMenus[i])
		
		self.firstColumnLayout.addLayout(self.inputLabelAndDropdownMenuPairLayout)
		for i in range(len(checkBoxes)):
			self.firstColumnLayout.addWidget(self.allOptionCheckBoxes[i])
		
		for i in range(len(RESULTS)):
			self.thirdColumnLayout.addWidget(self.allOutputLabels[i])
		
		self.horizontalStripLayout.addLayout(self.firstColumnLayout)
		self.horizontalStripLayout.addWidget(self.valuateButton)
		self.horizontalStripLayout.addLayout(self.thirdColumnLayout)
	
	def AddLayoutToCentralWidget(self):
		widget = QWidget()
		widget.setLayout(self.horizontalStripLayout)
		self.setCentralWidget(widget)
		

def NaturalSort( l ):
	""" Sort the given list in the way that humans expect.
	"""
	convert = lambda text: int(text) if text.isdigit() else text
	alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ]
	l.sort( key=alphanum_key )

def StartPyQtGUI():
	app = QApplication([sys.argv[0]])
	window = ValuateApartment()
	sys.exit(app.exec_())

StartPyQtGUI()