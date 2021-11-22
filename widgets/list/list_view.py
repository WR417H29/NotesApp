import sqlite3 as sql

import PyQt6.QtWidgets as qtw
import PyQt6.QtCore as qtc

from widgets.list.note_list_item import NoteListItem
from data.note_repository import NoteRepository

class ListView(qtw.QWidget):
    def __init__(self, conStr: str, openNoteFunc, createNoteFunc):
        super().__init__()
        self.repo = NoteRepository(conStr)
        self.conStr = conStr
        self.openNoteFunc = openNoteFunc
        self.createNoteFunc = createNoteFunc
        self.layout = qtw.QVBoxLayout()
        self.scrollArea = qtw.QScrollArea()
        self.scrollItems = qtw.QVBoxLayout()
        self.scrollWidget = qtw.QWidget()
        
        self.build()

    def build(self):
        self.populateScrollItems()
        
        self.scrollArea.setWidgetResizable(True)
        self.scrollWidget.setLayout(self.scrollItems)
        self.scrollArea.setWidget(self.scrollWidget)

        self.scrollArea.setHorizontalScrollBarPolicy(qtc.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self.layout.addWidget(self.scrollArea)

        newNoteButton = qtw.QPushButton("New Note")
        newNoteButton.clicked.connect(self.newNoteClicked)
        self.layout.addWidget(newNoteButton)

        self.setLayout(self.layout)
    
    def populateScrollItems(self):
        self._wipeScrollItems()
        self._repopulateScrollItems()

    def _wipeScrollItems(self):
        for i in reversed(range(self.scrollItems.count())):
            self.scrollItems.itemAt(i).widget().setParent(None)
        
    def _repopulateScrollItems(self):
        for note in self.repo.getAllNotes():
            noteWidget = NoteListItem(note, self.conStr, self.openNoteFunc, self.populateScrollItems)
            self.scrollItems.addWidget(noteWidget)

    def newNoteClicked(self):
        self.createNoteFunc()
        self.populateScrollItems()
