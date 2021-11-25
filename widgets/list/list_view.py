from typing import Callable

import PyQt6.QtWidgets as qtw
import PyQt6.QtCore as qtc

from widgets.list.note_list_item import NoteListItem
from data.repository import Repository
from data.note_repository import NoteRepository

class ListView(qtw.QWidget):
    def __init__(self, conStr: str, openNoteFunc: Callable[[int], None], createNoteFunc: Callable[[], None]) -> None:
        super().__init__()
        self.conStr: str = conStr
        self.repo: Repository = NoteRepository(self.conStr)

        self.openNoteFunc: Callable[[int], None] = openNoteFunc
        self.createNoteFunc: Callable[[], None] = createNoteFunc

        self.layout: qtw.QLayout = qtw.QVBoxLayout()
        self.scrollWidget: qtw.QWidget = qtw.QWidget()
        self.scrollItems: qtw.QLayout = qtw.QVBoxLayout()
        self.scrollArea: qtw.QAbstractScrollArea = qtw.QScrollArea()
        
        self.build()

    def build(self) -> None:
        self.populateScrollItems()
        
        self.scrollArea.setWidgetResizable(True)
        self.scrollWidget.setLayout(self.scrollItems)
        self.scrollArea.setWidget(self.scrollWidget)

        self.scrollArea.setHorizontalScrollBarPolicy(qtc.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scrollArea.setVerticalScrollBarPolicy(qtc.Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.scrollItems.setAlignment(qtc.Qt.AlignmentFlag.AlignTop)

        self.layout.addWidget(self.scrollArea)

        newNoteButton: qtw.QAbstractButton = qtw.QPushButton("New Note")
        newNoteButton.clicked.connect(self.newNoteClicked)
        self.layout.addWidget(newNoteButton)

        self.setLayout(self.layout)
    
    def populateScrollItems(self) -> None:
        self._wipeScrollItems()
        self._repopulateScrollItems()

    def _wipeScrollItems(self) -> None:
        for i in reversed(range(self.scrollItems.count())):
            self.scrollItems.itemAt(i).widget().setParent(None)
        
    def _repopulateScrollItems(self) -> None:
        for note in self.repo.getAllNotes():
            noteWidget: qtw.QWidget = NoteListItem(note, self.conStr, self.openNoteFunc, self.populateScrollItems)
            self.scrollItems.addWidget(noteWidget)

    def newNoteClicked(self) -> None:
        self.createNoteFunc()
        self.populateScrollItems()
