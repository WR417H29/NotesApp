from typing import Tuple

class Note:
    def __init__(self, id: int = None, title: str = None, content: str = None) -> None:
        self.id = id
        self.title = title
        self.content = content

    def __repr__(self) -> str:
        return '<Note %s>' % self.id

    @staticmethod
    def noteFromTuple(data: Tuple) -> 'Note':
        return Note(data[0], data[1], data[2])