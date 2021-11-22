import sqlite3 as sql

import PyQt6.QtWidgets as qtw

from models.note import Note
from data.note_repository import NoteRepository

class NoteView(qtw.QWidget):
    def __init__(self, conStr: str, listView):
        super().__init__()
        self.repo = NoteRepository(conStr)
        self.listView = listView
        self.layout = qtw.QVBoxLayout()
        self.currentId: int = None

        self.build()

    def build(self):
        self.titleRow = qtw.QLineEdit()
        self.noteBody = qtw.QTextEdit()
        saveBtn = qtw.QPushButton("Save")
        saveBtn.clicked.connect(self.saveNote)

        self.layout.addWidget(self.titleRow)
        self.layout.addWidget(self.noteBody)
        self.layout.addWidget(saveBtn)

        self.setLayout(self.layout)
    
    def saveNote(self):
        if self.currentId == None:
            return
        note = Note(self.currentId, self.titleRow.text(), self.noteBody.toPlainText())

        self.repo.updateNote(note)
        self.listView.populateScrollItems()

    def openNote(self, id: int) -> None:
        note = self.repo.getNoteById(id)
        self.currentId = id
        self.titleRow.setText(note.title)
        self.noteBody.setPlainText(note.content)
    
    def createNote(self) -> None:
        self.saveNote()
        self.titleRow.setText("")
        self.noteBody.setPlainText("")
        self.repo.createNote(Note(None, "", ""))
        