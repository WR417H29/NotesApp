import PyQt6.QtWidgets as qtw

from models.note import Note
from data.note_repository import NoteRepository

class NoteView(qtw.QWidget):
    def __init__(self, connectionString, listView):
        super().__init__()
        self.repo = NoteRepository(connectionString)
        self.listView = listView
        self.mainLayout = qtw.QVBoxLayout()
        self.currentId = None

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
        