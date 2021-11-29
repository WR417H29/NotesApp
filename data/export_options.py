import json

from data.note_repository import NoteRepository

class ExportOptions:
    def __init__(self, connectionString, settingsPath):
        self.connectionString = connectionString
        self.noteRepo = NoteRepository(self.connectionString)

        with open (settingsPath, 'r') as f:
            self.settings = json.load(f)

        self.notes = self.noteRepo.getAllNotes()

    def exportFolderAsMarkdown(self):
        print("ExportFolderAsMarkdown")

    def exportFolderAsText(self):
        print("ExportFolderAsText")
    