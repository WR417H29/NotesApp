import sqlite3 as sql

from models.note import Note

class NoteRepository:
    def __init__(self, connectionString):
        self.connectionString = connectionString

    def getAllNotes(self):
        query = "SELECT id, title, content FROM notes"

        with sql.connect(self.connectionString) as con:
            cur = con.cursor()
            notes = [Note.noteFromIterable(note) for note in cur.execute(query).fetchall()]
            con.commit()
        
        return notes

    def getNoteById(self, id):
        query = f"SELECT id, title, content FROM notes WHERE id='{id}'"

        with sql.connect(self.connectionString) as con:
            cur = con.cursor()
            note = Note.noteFromIterable(cur.execute(query).fetchone())
            con.commit()

        return note

    def updateNote(self, note):
        query = "UPDATE notes SET title = ?, content = ? WHERE id=?"

        with sql.connect(self.connectionString) as con:
            cur = con.cursor()
            cur.execute(query, [note.title, note.content, note.id])
            con.commit()

    def createNote(self, note):
        """Returns the ID of the created note"""
        query = "INSERT INTO notes (title, content) VALUES (?, ?)"

        with sql.connect(self.connectionString) as con:
            cur = con.cursor()
            cur.execute(query, [note.title, note.content])
            id = cur.execute("SELECT last_insert_rowid()").fetchone()
            con.commit()

        return id[0]

    def deleteNote(self, id = -1):
        if id == -1: return

        query = "DELETE FROM notes WHERE id=?"

        with sql.connect(self.connectionString) as con:
            cur = con.cursor()
            cur.execute(query, [id])
            con.commit()