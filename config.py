import sys
from presets import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
import glob

PRESETS_PATH = 'data/presets/'
MASTER_CONFIG_PATH = 'data/master_'

class Gui(QDialog):
    def __init__(self, parent=None):
        super(Gui, self).__init__(parent)
        self.setWindowTitle("Evo Art Puppetmaster")
        self.resize(540, 340)

        styleLabel = QLabel("Here you can edit the master config file.")

        self.createTopLeftGroupBox()
        self.createDictReader()

        topLayout = QHBoxLayout()
        topLayout.addWidget(styleLabel)

        mainLayout = QGridLayout()
        mainLayout.addLayout(topLayout, 0, 0, 1, 2)
        #mainLayout.addWidget(self.topLeftGroupBox, 1, 0)
        mainLayout.addLayout(self.DictEditor, 1, 0)
        self.setLayout(mainLayout)


    def CreatePresetChooser(self):
        self.presets = []


    def createDictReader(self, configPath=MASTER_CONFIG_PATH):
        widgets = {}
        self.DictEditor = QFormLayout()
        config_dict = load_config(configPath)
        for key, value in config_dict.items():
            widgets[key] = widget = {}
            widget['lineedit'] = lineedit = QLineEdit(value)
            self.DictEditor.addRow(key, lineedit)

        self.saveBtn = QPushButton("Save config")
        self.saveBtn.clicked.connect(lambda: self.saveDict(config_dict, configPath))
        self.DictEditor.addRow(self.saveBtn)


    def saveDict(self, configDict, configPath):
        print(f"saving config file as {configPath}")
        save_config(configPath, configDict)


    def createTopLeftGroupBox(self):
        self.topLeftGroupBox = QGroupBox("Group 1")

        radioButton1 = QRadioButton("Radio button 1")
        radioButton2 = QRadioButton("Radio button 2")
        radioButton3 = QRadioButton("Radio button 3")
        radioButton1.setChecked(True)

        checkBox = QCheckBox("Tri-state check box")
        checkBox.setTristate(True)
        checkBox.setCheckState(Qt.PartiallyChecked)

        layout = QVBoxLayout()
        layout.addWidget(radioButton1)
        layout.addWidget(radioButton2)
        layout.addWidget(radioButton3)
        layout.addWidget(checkBox)
        layout.addStretch(1)
        self.topLeftGroupBox.setLayout(layout)


app = QApplication(sys.argv)
gui = Gui()
gui.show()
sys.exit(app.exec_())