from typing import List
import PyQt6.QtWidgets as qtw
from data.repository import Repository

from models.note import Note
from data.note_repository import NoteRepository
from widgets.list.list_view import ListView

class NoteView(qtw.QWidget):
    def __init__(self, conStr: str, listView: ListView) -> None:
        super().__init__()
        self.repo: Repository = NoteRepository(conStr)
        self.listView: ListView = listView
        self.mainLayout: qtw.QLayout = qtw.QVBoxLayout()
        self.currentId: int = None

        self.build()

    def build(self) -> None:
        self.titleRow: qtw.QLineEdit = qtw.QLineEdit()
        self.noteBody: qtw.QTextEdit = qtw.QTextEdit()
        saveBtn: qtw.QAbstractButton = qtw.QPushButton("Save")
        saveBtn.clicked.connect(self.saveNote)

        self.mainLayout.addWidget(self.titleRow)
        self.mainLayout.addWidget(self.noteBody)
        self.mainLayout.addWidget(saveBtn)

        self.setLayout(self.mainLayout)
    
    def saveNote(self) -> None:
        if self.currentId == None:
            return
        note: Note = Note(self.currentId, self.titleRow.text(), self.noteBody.toPlainText())

        self.repo.updateNote(note)
        self.listView.populateScrollItems()

    def openNote(self, id: int) -> None:
        note: Note = self.repo.getNoteById(id)
        self.currentId = id
        self.titleRow.setText(note.title)
        self.noteBody.setPlainText(note.content)
    
    def createNote(self) -> None:
        self.saveNote()
        self.titleRow.setText("")
        self.noteBody.setPlainText("")
        id: int = self.repo.createNote(Note(None,"", ""))
        self.openNote(id)
        