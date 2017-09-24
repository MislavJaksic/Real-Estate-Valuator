from PyQt5.QtWidgets import QComboBox, QWidget, QLabel, QComboBox, QPushButton, QCheckBox
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWidgets import QFormLayout, QHBoxLayout, QVBoxLayout

import sys
import os
sys.path.insert(0, os.path.abspath('../..'))

from RealEstateValuationSystem.DatasetSource.Database.DatabaseController import DatabaseController
from RealEstateValuationSystem.DatasetAnalysis.ApartmentForSaleCollection import DatasetConfig
from RealEstateValuationSystem.Predicting import Predictor

import re

inputLabels = ['state', 'town', 'place', 'size', 'floor', 'numberOfParkingSpaces']
checkBoxes = []
RESULTS = ["Value of property: "]

class ValuateApartment(QMainWindow):
  
  def __init__(self):
    super(ValuateApartment, self).__init__()
    self.db = DatabaseController()
    self.db.RunMongod()
    self.db.Open(DatasetConfig.conn)
    self._CreateInterface()
    
  def __exit__(self, exc_type, exc_value, traceback):
    self.db.CloseAndStop()
  
  def _CreateInterface(self):
    self._CreateGUIElements()
    self._PositionGUIElements()
    
    self.setWindowTitle("_Valuate Apartment")
    
    self.show()
    
  def _CreateGUIElements(self):
    self._CreateInputLabels()
    self._CreateInputDropdownMenus()
    self._CreateCheckBoxes()
    self._Create_ValuateButton()
    self._CreateOutputLabels()
    
  def _CreateInputLabels(self):
    self.allInputLabels = []
    for name in inputLabels:
      self.allInputLabels.append(QLabel(name))
  
  def _CreateInputDropdownMenus(self):
    self.allInputDropdownMenus = []
    for name in inputLabels:
      menu = QComboBox()
      self._AddDataToDropdownMenu(menu, name)
      self.allInputDropdownMenus.append(menu)
  
  def _AddDataToDropdownMenu(self, menu, name):
    if name == 'state':
      data = self.db.FindDistinct({}, 'state')
    if name == 'town':
      data = self.db.FindDistinct({'state':self.allInputDropdownMenus[0].currentText()}, 'town')
      self.allInputDropdownMenus[0].currentIndexChanged[str].connect(self._Change_Town_DropdownMenu)
    if name == 'place':
      data = self.db.FindDistinct({'town':self.allInputDropdownMenus[1].currentText()}, 'place')
      self.allInputDropdownMenus[1].currentIndexChanged[str].connect(self._Change_Place_DropdownMenu)
    if name == 'size':
      data = [str(number) for number in xrange(5, 449, 1)]
    if name == 'yearOfConstruction':
      data = [str(number) for number in xrange(1940, 2018, 1)]
    if name == 'yearOfLastAdaptation':
      data = [str(number) for number in xrange(1940, 2018, 1)]
    if name == 'numberOfRooms':
      data = self.db.FindDistinct({}, 'numberOfRooms')
    if name == 'floor':
      data = self.db.FindDistinct({}, 'floor')
      data.remove(0)
    if name == 'numberOfParkingSpaces':
      data = [str(number) for number in xrange(0, 7, 1)]
    
    _NaturalSort(data)
    menu.addItems(data)
    
  def _Change_Town_DropdownMenu(self, selectedState):
    data = self.db.FindDistinct({'state' : selectedState}, 'town')
    
    _NaturalSort(data)
    menu = self.allInputDropdownMenus[1] #change to a dict so you don't have to remember the position of the dropdown menu
    menu.clear()
    menu.addItems(data)
    
  def _Change_Place_DropdownMenu(self, selectedState):
    data = self.db.FindDistinct({'town' : selectedState}, 'place')
    
    _NaturalSort(data)
    menu = self.allInputDropdownMenus[2]
    menu.clear()
    menu.addItems(data)
  
  def _CreateCheckBoxes(self):
    self.allOptionCheckBoxes = []
    for name in checkBoxes:
      self.allOptionCheckBoxes.append(QCheckBox(name))
  
  def _Create_ValuateButton(self):
    self._ValuateButton = QPushButton('_Valuate apartment')
    self._ValuateButton.clicked.connect(self._Valuate)
  
  def _Valuate(self):
    customerData = {}
    for i in range(0, len(inputLabels)):
      try:
        customerData[inputLabels[i]] = [int(self.allInputDropdownMenus[i].currentText())]
      except:
        customerData[inputLabels[i]] = [self.allInputDropdownMenus[i].currentText()]
    price = Predictor.PredictApartmentValue(customerData)
    self.allOutputLabels[0].setText(RESULTS[0] + str(price) + ' euros')
  
  def _CreateOutputLabels(self):
    self.allOutputLabels = []
    for name in RESULTS:
      self.allOutputLabels.append(QLabel(name))
  
  
  #Interface design: 
  #the first column has labels and dropdown menus paired up and below them are check boxes
  # customers input data through the dropdown menus and choose additional options through the check boxes
  #the second column has a _Valuate button
  # customers will begin the valuation process by pressing it
  # the third column will display the results of the valuation
  def _PositionGUIElements(self):
    self._CreateLayouts()
    self._AddElementsToLayoutAndNestLayouts()
    self._AddLayoutToCentralWidget()
  
  def _CreateLayouts(self):
    self.horizontalStripLayout = QHBoxLayout()
    self.firstColumnLayout = QVBoxLayout()
    self.thirdColumnLayout = QVBoxLayout()
    self.inputLabelAndDropdownMenuPairLayout = QFormLayout()
  
  def _AddElementsToLayoutAndNestLayouts(self):
    for i in range(len(inputLabels)):
      self.inputLabelAndDropdownMenuPairLayout.addRow(self.allInputLabels[i], self.allInputDropdownMenus[i])
    
    self.firstColumnLayout.addLayout(self.inputLabelAndDropdownMenuPairLayout)
    for i in range(len(checkBoxes)):
      self.firstColumnLayout.addWidget(self.allOptionCheckBoxes[i])
    
    for i in range(len(RESULTS)):
      self.thirdColumnLayout.addWidget(self.allOutputLabels[i])
    
    self.horizontalStripLayout.addLayout(self.firstColumnLayout)
    self.horizontalStripLayout.addWidget(self._ValuateButton)
    self.horizontalStripLayout.addLayout(self.thirdColumnLayout)
  
  def _AddLayoutToCentralWidget(self):
    widget = QWidget()
    widget.setLayout(self.horizontalStripLayout)
    self.setCentralWidget(widget)
    

def _NaturalSort(list):
  """ Sort the given list in the way that humans expect."""
  convert = lambda text: int(text) if text.isdigit() else text
  alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ]
  list.sort( key=alphanum_key )

def StartPyQtGUI():
  app = QApplication([sys.argv[0]])
  window = ValuateApartment()
  sys.exit(app.exec_())

StartPyQtGUI()
