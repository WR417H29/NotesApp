import json

from PyQt6 import (
    QtWidgets as qtw,
    QtCore as qtc
)

class SettingsMenu(qtw.QDialog):
    def __init__(self, settingsPath):
        super().__init__()
        self.title = "Settings"
        self.windowSize = [1920//4, 1080//4, 1920//2, 1080//2]
        self.settingsPath = settingsPath
        with open (settingsPath, 'r') as f:
            self.settings = json.load(f)
        

        self.mainLayout = qtw.QVBoxLayout()

        self.buildForms()
        self.build()

    def buildForms(self):
        self.buildExportForm()

    def buildExportForm(self):
        exportSettingsGroupBox = qtw.QGroupBox("Export Settings")
        exportSettingsGroupBoxLayout = qtw.QVBoxLayout()
        exportSettingsGroupBox.setLayout(exportSettingsGroupBoxLayout)

        exportPathWidget = qtw.QWidget()
        exportPathLayout = qtw.QHBoxLayout()
        exportPathWidget.setLayout(exportPathLayout)

        self.exportPathCurrent = qtw.QLineEdit(self.settings['exportPath'])
        self.exportPathCurrent.setReadOnly(True)
        exportPathSelector = qtw.QPushButton("Choose Export Path")
        exportPathSelector.clicked.connect(self.getExportPath)

        exportPathLayout.addWidget(self.exportPathCurrent)
        exportPathLayout.addWidget(exportPathSelector)

        exportSettingsGroupBoxLayout.addWidget(exportPathWidget)

        self.mainLayout.addWidget(exportSettingsGroupBox)


    def getExportPath(self):
        fileDialog = qtw.QFileDialog()
        exportPath = fileDialog.getExistingDirectory(self, "Choose Export Path")
        self.exportPathCurrent.setText(exportPath)
        self.settings['exportPath'] = exportPath

    def build(self):
        saveButton = qtw.QPushButton("Save")
        saveButton.clicked.connect(self.saveChanges)

        self.mainLayout.addWidget(saveButton)
        self.setLayout(self.mainLayout)
        self.setGeometry(*self.windowSize)
        self.setWindowTitle(self.title)

    def saveChanges(self):
        with open (self.settingsPath, 'w') as f:
            json.dump(self.settings, f)
        
        self.done(0)