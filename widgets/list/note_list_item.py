from typing import Callable
import PyQt6.QtWidgets as qtw
import PyQt6.QtGui as qtg

from data.note_repository import NoteRepository
from data.repository import Repository
from models.note import Note

class NoteListItem(qtw.QWidget):
    def __init__(self, 
                 note: Note, 
                 conStr: str, 
                 openNote: Callable[[int], None], 
                 populateScrollItems: Callable[[], None]
                ) -> None:
        super().__init__()
        self.openNote: Callable[[int], None] = openNote
        self.note: Note = note
        self.psi: Callable[[], None] = populateScrollItems
        self.repo: Repository = NoteRepository(conStr)
        self.mainLayout: qtw.QLayout = qtw.QVBoxLayout()
        self.itemLayout: qtw.QLayout = qtw.QHBoxLayout()

        self.openNoteButton: qtw.QAbstractButton = qtw.QPushButton()
        self.openNoteButton.clicked.connect(self.openNoteFunc)
        self.build()

    def build(self) -> None:
        image: qtw.QLabel = qtw.QLabel()
        image.setPixmap(qtg.QPixmap("assets/file.png"))
        image.setMaximumWidth(18)
        image.setStyleSheet('background: white')

        title: qtw.QLabel = qtw.QLabel(self.note.title)
        title.setMinimumWidth(82)
        title.setStyleSheet('background: white')

        delete: qtw.QAbstractButton = qtw.QPushButton('X')
        delete.setFont(qtg.QFont('Fira Code', 10))
        delete.setMaximumWidth(10)
        delete.setStyleSheet('background: white')
        delete.clicked.connect(self.deleteNoteFunc)

        self.itemLayout.addWidget(image)
        self.itemLayout.addWidget(title)
        self.itemLayout.addWidget(delete)

        self.openNoteButton.setLayout(self.itemLayout)
        self.openNoteButton.setMinimumSize(140, 40)
        
        self.mainLayout.addWidget(self.openNoteButton)
        self.setLayout(self.mainLayout)
        self.setMinimumWidth(100)

        self.setStyleSheet('background: gray; border: 1px solid black')

    def openNoteFunc(self) -> None:
        self.openNote(self.note.id)

    def deleteNoteFunc(self) -> None:
        self.repo.deleteNote(self.note.id)
        self.psi()
