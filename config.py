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

        self.master_config_dict = load_config(MASTER_CONFIG_PATH)
        self.presetName = self.master_config_dict['preset_path'].split('/')[-2]

        #styleLabel = QLabel("Here you can edit the master config file.")

        self.createTopLeftGroupBox()
        self.createPresetChooser()
        self.createDictEditor(self.master_config_dict['preset_path'])

        topLayout = QHBoxLayout()
        #topLayout.addWidget(styleLabel)

        mainLayout = QGridLayout()
        #mainLayout.addLayout(topLayout, 1, 0, 1, 2)
        #mainLayout.addWidget(self.topLeftGroupBox, 1, 0)
        mainLayout.addLayout(self.PresetChooser, 0, 0)
        mainLayout.addLayout(self.DictEditor, 1, 0)


        self.setLayout(mainLayout)


    def createPresetChooser(self, masterConfigPath=MASTER_CONFIG_PATH):
        presets = glob.glob(PRESETS_PATH + '*')
        preset_names = [x.split('/')[-1] for x in presets]

        self.PresetChooser = QHBoxLayout()

        #self.master_config_dict = load_config(masterConfigPath)

        self.presetComboBox = QComboBox()
        self.presetComboBox.addItems(preset_names)
        index = self.presetComboBox.findText(self.presetName)

        if index >= 0:
            self.presetComboBox.setCurrentIndex(index)

        self.presetComboBox.activated.connect(self.updateMasterConfig)

        presetLabel = QLabel("&Active preset:")
        presetLabel.setBuddy(self.presetComboBox)

        self.saveBtn = QPushButton("Select")
        self.saveBtn.clicked.connect(lambda: self.saveDict(self.master_config_dict, masterConfigPath))

        self.PresetChooser.addWidget(presetLabel)
        self.PresetChooser.addWidget(self.presetComboBox)
        self.PresetChooser.addWidget(self.saveBtn)
        #print(preset_names)


    def updateMasterConfig(self, index):
        self.master_config_dict = load_config()
        self.presetName = self.presetComboBox.itemText(index)
        #self.master_config_dict['preset_path'].split('/')[-2]
        self.master_config_dict['preset_path'] = PRESETS_PATH + self.presetName + '/'


    def createDictEditor(self, presetPath):
        widgets = {}
        self.DictEditor = QFormLayout()
        config_dict = load_config(presetPath)
        for key, value in config_dict.items():
            widgets[key] = widget = {}
            widget['lineedit'] = lineedit = QLineEdit(str(value))
            self.DictEditor.addRow(key, lineedit)

        self.saveBtn = QPushButton("Save config")
        self.saveBtn.clicked.connect(lambda: self.saveDict(config_dict, presetPath))
        self.DictEditor.addRow(self.saveBtn)


    def saveDict(self, configDict, configPath):
        print(f"saving config file as {configPath}config.json")
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