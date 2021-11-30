import json

from PyQt6 import (
    QtWidgets as qtw
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
        self.buildAutoSaveForm()

    def buildExportForm(self):
        exportSettingsGroupBox = qtw.QGroupBox("Export")
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

    def buildAutoSaveForm(self):
        autoSaveSettingsGroupBox = qtw.QGroupBox("Auto Save")
        autoSaveSettingsGroupBoxLayout = qtw.QVBoxLayout()
        autoSaveSettingsGroupBox.setLayout(autoSaveSettingsGroupBoxLayout)

        autoSaveWidget = qtw.QWidget()
        autoSaveLayout = qtw.QHBoxLayout()
        autoSaveWidget.setLayout(autoSaveLayout)

        self.autoSaveCurrent = qtw.QLineEdit(str(self.settings['autoSave']))
        self.autoSaveCurrent.setReadOnly(True)
        self.autoSaveSelector = qtw.QCheckBox("Auto Save")
        self.autoSaveSelector.setChecked(self.settings['autoSave'])
        self.autoSaveSelector.clicked.connect(self.getAutoSave)


        autoSaveLayout.addWidget(self.autoSaveCurrent)
        autoSaveLayout.addWidget(self.autoSaveSelector)

        autoSaveSettingsGroupBoxLayout.addWidget(autoSaveWidget)

        self.mainLayout.addWidget(autoSaveSettingsGroupBox)

    def getExportPath(self):
        fileDialog = qtw.QFileDialog()
        exportPath = fileDialog.getExistingDirectory(self, "Choose Export Path")
        self.exportPathCurrent.setText(exportPath)
        self.settings['exportPath'] = exportPath

    def getAutoSave(self):
        enabled = self.autoSaveSelector.isChecked()
        self.settings['autoSave'] = enabled
        self.autoSaveCurrent.setText(str(enabled))

    def build(self):
        saveButton = qtw.QPushButton("Save")
        saveButton.clicked.connect(self.saveChanges)

        self.mainLayout.addWidget(saveButton)
        self.setLayout(self.mainLayout)
        self.setGeometry(*self.windowSize)
        self.setWindowTitle(self.title)

    def saveChanges(self):
        with open (self.settingsPath, 'w') as f:
            json.dump(self.settings, f, indent=4)
        
        self.done(0)