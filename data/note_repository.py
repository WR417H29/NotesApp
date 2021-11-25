import sqlite3 as sql

from sqlite3 import Cursor

from typing import List, Tuple

from data.repository import Repository
from models.note import Note

class NoteRepository(Repository):
    def __init__(self, connectionString: str) -> None:
        super().__init__(connectionString)

    def getAllNotes(self) -> List[Note]:
        query: str = "SELECT id, title, content FROM notes"

        with sql.connect(self.conStr) as con:
            cur: Cursor = con.cursor()
            notes: List[Note] = [Note.noteFromTuple(note) for note in cur.execute(query).fetchall()]
            con.commit()
        
        return notes

    def getNoteById(self, id: int) -> Note:
        query: str = f"SELECT id, title, content FROM notes WHERE id='{id}'"

        with sql.connect(self.conStr) as con:
            cur: Cursor = con.cursor()
            note: Note = Note.noteFromTuple(cur.execute(query).fetchone())
            con.commit()

        return note

    def updateNote(self, note: Note) -> None:
        query: str = "UPDATE notes SET title = ?, content = ? WHERE id=?"

        with sql.connect(self.conStr) as con:
            cur: Cursor = con.cursor()
            cur.execute(query, [note.title, note.content, note.id])
            con.commit()

    def createNote(self, note: Note) -> int:
        """Returns the ID of the created note"""
        query: str = "INSERT INTO notes (title, content) VALUES (?, ?)"

        with sql.connect(self.conStr) as con:
            cur: Cursor = con.cursor()
            cur.execute(query, [note.title, note.content])
            id: Tuple = cur.execute("SELECT last_insert_rowid()").fetchone()
            con.commit()

        return id[0]

    def deleteNote(self, id: int) -> None:
        query: str = "DELETE FROM notes WHERE id=?"

        with sql.connect(self.conStr) as con:
            cur: Cursor = con.cursor()
            cur.execute(query, [id])
            con.commit()