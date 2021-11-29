import sqlite3 as sql

from PyQt6 import (
    QtWidgets as qtw,
    QtGui as qtg
)

from data.export_options import ExportOptions
from widgets.settings_menu import SettingsMenu

from widgets.views.notes_list import NotesList
from widgets.views.note_view import NoteView

class MainWindow(qtw.QMainWindow):
    def __init__(self):
        super().__init__()
        self.connectionString = "assets/notes.db"
        self.settingsPath = "assets/settings.json"
        self.init_db()

        self.title = "Notes App"
        self.windowSize = [1920//6, 1080//6, 1920//1.5, 1080//1.5]
        self.mainWidget = qtw.QWidget()

        self.exportOptions = ExportOptions(self.connectionString, self.settingsPath)

        self.listView = NotesList(self.connectionString, self.openNote, self.createNote)
        self.listView.setMinimumWidth(200)

        self.noteView = NoteView(self.connectionString, self.listView)
        
        self.initaliseMenuBar()

        self.setGeometry(*self.windowSize)
        self.build()

    def build(self):
        self.mainLayout = qtw.QHBoxLayout()
        self.mainLayout.addWidget(self.listView)  
        self.mainLayout.addWidget(self.noteView, 2)
        self.mainWidget.setLayout(self.mainLayout)

        self.setMenuBar(self._menuBar)
        self.setCentralWidget(self.mainWidget)
        self.setWindowTitle(self.title)

    def initaliseMenuBar(self):
        self._menuBar = self.menuBar()

        file = self._menuBar.addMenu("File")
        settings = self._menuBar.addMenu("Settings")

        export = file.addMenu("Export")

        settingsMenu = settings.addAction("Menu")
        settingsMenu.triggered.connect(self.openSettings)

        exportFolderMarkdown = export.addAction("Markdown")
        exportFolderMarkdown.triggered.connect(self.exportOptions.exportFolderAsMarkdown)
        
        exportFolderText = export.addAction("Text")
        exportFolderText.triggered.connect(self.exportOptions.exportFolderAsText)

    def openSettings(self):
        settingsMenu = SettingsMenu(self.settingsPath)
        settingsMenu.exec()

    def init_db(self):
        con = sql.connect(self.connectionString)
        cur = con.cursor()

        queries = [
            """
            CREATE TABLE IF NOT EXISTS 'notes' (
                'id'        INTEGER NOT NULL UNIQUE,
                'title'     TEXT NOT NULL,
                'content'   TEXT NOT NULL,
                PRIMARY KEY('id' AUTOINCREMENT)
            );
            """
        ]

        for query in queries:
            cur.execute(query)

        con.commit()
        con.close()

    def openNote(self, id):
        self.noteView.openNote(id)
    
    def createNote(self):
        self.noteView.createNote()
    