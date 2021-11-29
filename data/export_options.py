import json

from data.note_repository import NoteRepository

class ExportOptions:
    def __init__(self, connectionString, settingsPath):
        self.connectionString = connectionString
        self.noteRepo = NoteRepository(self.connectionString)

        with open (settingsPath, 'r') as f:
            self.settings = json.load(f)

    def exportFolderAsText(self):
        for note in self.noteRepo.getAllNotes():
            with open (f"{self.settings['exportPath']}/{note.title}.txt", 'w') as f:
                f.write(note.content)
