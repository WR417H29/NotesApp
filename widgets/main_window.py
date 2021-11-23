import sqlite3 as sql
from typing import List

import PyQt6.QtWidgets as qtw

from widgets.list.list_view import ListView
from widgets.notes.note_view import NoteView

class MainWindow(qtw.QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.connectionString = "assets/notes.db"
        self.init_db()

        self.size = [1920//4, 1080//4, 1920//2, 1080//2]
        self.setGeometry(*self.size)
        self.title = "Notes App"
        self.mainWidget = qtw.QWidget()

        self.listView = ListView(self.connectionString, self.openNote, self.createNote)
        self.listView.setMinimumWidth(200)
        self.noteView = NoteView(self.connectionString, self.listView)

        self.build()

    def build(self) -> None:
        self.layout = qtw.QHBoxLayout()
        self.layout.addWidget(self.listView)  
        self.layout.addWidget(self.noteView, 2)
        self.mainWidget.setLayout(self.layout)

        self.setCentralWidget(self.mainWidget)
        self.setWindowTitle(self.title)


    def init_db(self) -> None:
        self.con = sql.connect(self.connectionString)
        self.cur = self.con.cursor()

        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS 'notes' (
            'id'        INTEGER NOT NULL UNIQUE,
            'title'	    TEXT NOT NULL,
            'content'	TEXT NOT NULL,
            PRIMARY KEY('id' AUTOINCREMENT) 
        );
        """)

        self.con.close()

    def openNote(self, id: int):
        self.noteView.openNote(id)
    
    def createNote(self):
        self.noteView.createNote()
    