import sqlite3 as sql

from PyQt6 import (
    QtWidgets as qtw,
    QtGui as qtg
)

from data.export_options import ExportOptions
from data.note_repository import NoteRepository

from widgets.windows.import_menu import ImportMenu
from widgets.windows.settings_menu import SettingsMenu

from widgets.views.notes_list import NotesList
from widgets.views.note_view import NoteView

class MainWindow(qtw.QMainWindow):
    def __init__(self):
        super().__init__()
        self.connectionString = "assets/notes.db"
        self.settingsPath = "assets/settings.json"
        self.init_db()

        self.noteRepo = NoteRepository(self.connectionString)

        self.title = "Notes App"
        self.windowSize = [1920//6, 1080//6, 1920//1.5, 1080//1.5]
        self.mainWidget = qtw.QWidget()

        self.exportOptions = ExportOptions(self.connectionString, self.settingsPath)

        self.notesList = NotesList(self.connectionString, self.openNote, self.createNote)
        self.notesList.setMinimumWidth(200)

        self.noteView = NoteView(self.connectionString, self.notesList, self.settingsPath)
        
        self.initaliseMenuBar()

        self.setGeometry(*self.windowSize)
        self.build()

    def build(self):
        self.mainLayout = qtw.QHBoxLayout()
        self.mainLayout.addWidget(self.notesList)  
        self.mainLayout.addWidget(self.noteView, 2)
        self.mainWidget.setLayout(self.mainLayout)

        self.setMenuBar(self._menuBar)
        self.setCentralWidget(self.mainWidget)
        self.setWindowTitle(self.title)

    def initaliseMenuBar(self):
        self._menuBar = self.menuBar()

        file = self._menuBar.addMenu("File")
        settings = self._menuBar.addMenu("Settings")

        new = file.addAction("New")
        new.triggered.connect(self.createNote)
        new.setShortcut(qtg.QKeySequence("Ctrl+N"))

        save = file.addAction("Save")
        save.triggered.connect(self.noteView.saveNote)
        save.setShortcut(qtg.QKeySequence("Ctrl+S"))

        export = file.addAction("Export")
        export.triggered.connect(self.exportOptions.exportFolderAsText)
        export.setShortcut(qtg.QKeySequence("Ctrl+E"))

        userImport = file.addAction("Import")
        userImport.triggered.connect(self.importFile)

        settingsMenu = settings.addAction("Menu")
        settingsMenu.triggered.connect(self.openSettings)

        clearStorage = settings.addAction("Clear Notes")
        clearStorage.triggered.connect(self.clearDb)


    def openSettings(self):
        settingsMenu = SettingsMenu(self.settingsPath)
        settingsMenu.exec()

    def importFile(self):
        importMenu = ImportMenu(self.connectionString, self.openNote, self.notesList.populateScrollItems)
        importMenu.exec()

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

    def clearDb(self):
        for note in self.noteRepo.getAllNotes():
            self.noteRepo.deleteNote(note.id)
        self.notesList.populateScrollItems()

    def openNote(self, id):
        self.noteView.openNote(id)
    
    def createNote(self):
        self.noteView.createNote()
        self.notesList.populateScrollItems()
    