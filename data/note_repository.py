import sqlite3 as sql

from sqlite3 import Cursor

from typing import List, Tuple

from models.note import Note

class NoteRepository:
    def __init__(self, connectionString: str) -> None:
        self.conStr = connectionString

    def getAllNotes(self) -> List[Note]:
        query = "SELECT id, title, content FROM notes"

        with sql.connect(self.conStr) as con:
            cur = con.cursor()
            notes = [Note.noteFromTuple(note) for note in cur.execute(query).fetchall()]
            con.commit()
        
        return notes

    def getNoteById(self, id: int) -> Note:
        query = f"SELECT id, title, content FROM notes WHERE id='{id}'"

        with sql.connect(self.conStr) as con:
            cur = con.cursor()
            note = Note.noteFromTuple(cur.execute(query).fetchone())
            con.commit()

        return note

    def updateNote(self, note: Note) -> None:
        query = "UPDATE notes SET title = ?, content = ? WHERE id=?"

        with sql.connect(self.conStr) as con:
            cur = con.cursor()
            cur.execute(query, [note.title, note.content, note.id])
            con.commit()

    def createNote(self, note: Note) -> int:
        """Returns the ID of the created note"""
        query = "INSERT INTO notes (title, content) VALUES (?, ?)"

        with sql.connect(self.conStr) as con:
            cur = con.cursor()
            cur.execute(query, [note.title, note.content])
            id = cur.execute("SELECT last_insert_rowid()").fetchone()
            con.commit()

        return id[0]

    def deleteNote(self, id: int = -1) -> None:
        if id == -1: return

        query = "DELETE FROM notes WHERE id=?"

        with sql.connect(self.conStr) as con:
            cur = con.cursor()
            cur.execute(query, [id])
            con.commit()