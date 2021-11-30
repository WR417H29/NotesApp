from PyQt6 import (
    QtWidgets as qtw
)

from data.note_repository import NoteRepository

from models.note import Note

class ImportMenu(qtw.QDialog):
    def __init__(self, connectionString, openNoteFunc, populateScrollItems):
        super().__init__()
        self.title = "Import File"
        self.mainLayout = qtw.QVBoxLayout()

        self.noteRepo = NoteRepository(connectionString)
        self.openNoteFunc = openNoteFunc
        self.populateScrollItems = populateScrollItems

        self.buildImportForm()
        self.build()

    def build(self):
        importBtn = qtw.QPushButton("Import")
        importBtn.clicked.connect(self.importFile)

        self.mainLayout.addWidget(importBtn)

        self.setLayout(self.mainLayout)
        self.setWindowTitle(self.title)

    def buildImportForm(self):
        importSettingsGroupBox = qtw.QGroupBox("Import File")
        importSettingsGroupBoxLayout = qtw.QVBoxLayout()
        importSettingsGroupBox.setLayout(importSettingsGroupBoxLayout)

        importPathWidget = qtw.QWidget()
        importPathLayout = qtw.QHBoxLayout()
        importPathWidget.setLayout(importPathLayout)

        self.importFileCurrent = qtw.QLineEdit("")
        self.importFileCurrent.setReadOnly(True)
        importPathSelector = qtw.QPushButton("Choose Imported File")
        importPathSelector.clicked.connect(self.getImportFile)

        importPathLayout.addWidget(self.importFileCurrent)
        importPathLayout.addWidget(importPathSelector)

        importSettingsGroupBoxLayout.addWidget(importPathWidget)

        self.mainLayout.addWidget(importSettingsGroupBox)
    
    def getImportFile(self):
        fileDialog = qtw.QFileDialog()
        importFile = fileDialog.getOpenFileName(self, "Choose Imported File", filter='Text Files (*.txt)')
        self.importFileCurrent.setText(importFile[0])

    def importFile(self):
        fp = self.importFileCurrent.text()

        splitFp = fp.split('/')
        nameWithExt = splitFp[len(splitFp)-1]
        splitName = nameWithExt.split('.')
        title = splitName[0]

        with open (fp, 'r') as f:
            content = f.read()

        id = self.noteRepo.createNote(Note(title=title, content=content))
        self.openNoteFunc(id)
        self.populateScrollItems()
        self.done(0)