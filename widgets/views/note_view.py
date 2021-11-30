import json
from PyQt6.QtCore import QTimer

import PyQt6.QtWidgets as qtw

from models.note import Note
from data.note_repository import NoteRepository

class NoteView(qtw.QWidget):
    def __init__(self, connectionString, listView, settingsPath):
        super().__init__()
        self.repo = NoteRepository(connectionString)
        self.listView = listView
        self.mainLayout = qtw.QVBoxLayout()
        self.currentId = None

        with open (settingsPath, 'r') as f:
            self.settings = json.load(f)

        if self.settings['autoSave']:
            self.timer = QTimer()
            self.timer.setInterval(1000)
            self.timer.timeout.connect(self.saveNote)
            self.timer.start()

        self.build()

    def build(self):
        self.titleRow = qtw.QLineEdit()
        self.noteBody = qtw.QTextEdit()
        saveBtn = qtw.QPushButton("Save")
        saveBtn.clicked.connect(self.saveNote)

        self.mainLayout.addWidget(self.titleRow)
        self.mainLayout.addWidget(self.noteBody)
        self.mainLayout.addWidget(saveBtn)

        self.setLayout(self.mainLayout)
    
    def saveNote(self):
        print("Saving...")
        if self.currentId == None: return
        
        note = Note(self.currentId, self.titleRow.text(), self.noteBody.toPlainText())

        self.repo.updateNote(note)
        self.listView.populateScrollItems()

    def openNote(self, id):
        note = self.repo.getNoteById(id)
        self.currentId = id
        self.titleRow.setText(note.title)
        self.noteBody.setPlainText(note.content)
    
    def createNote(self):
        self.saveNote()
        self.titleRow.setText("")
        self.noteBody.setPlainText("")
        id: int = self.repo.createNote(Note(None,"", ""))
        self.openNote(id)
        