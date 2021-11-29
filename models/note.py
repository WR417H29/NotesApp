class Note:
    def __init__(self, id = None, title = None, content = None):
        self.id = id
        self.title = title
        self.content = content

    def __repr__(self):
        return '<Note %s>' % self.id

    @staticmethod
    def noteFromIterable(data):
        return Note(data[0], data[1], data[2])