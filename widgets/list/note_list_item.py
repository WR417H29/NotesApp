import PyQt6.QtWidgets as qtw
import PyQt6.QtGui as qtg

from models.note import Note

class NoteListItem(qtw.QWidget):
    def __init__(self, note: Note, onClickFunc):
        super().__init__()
        self.function = onClickFunc
        self.note = note
        self.mainLayout = qtw.QVBoxLayout()
        self.itemLayout = qtw.QHBoxLayout()

        self.button = qtw.QPushButton()
        self.button.clicked.connect(self.onClick)
        self.build()

    def build(self):
        image = qtw.QLabel()
        image.setPixmap(qtg.QPixmap("assets/file.png"))
        image.setMaximumWidth(18)
        image.setStyleSheet('background: white')

        title = qtw.QLabel(self.note.title)
        title.setMinimumWidth(82)
        title.setStyleSheet('background: white')

        self.itemLayout.addWidget(image)
        self.itemLayout.addWidget(title)

        self.button.setLayout(self.itemLayout)
        self.button.setMinimumSize(140, 40)
        
        self.mainLayout.addWidget(self.button)
        self.setLayout(self.mainLayout)
        self.setMinimumWidth(100)

        self.setStyleSheet('background: gray; border: 1px solid black')

    def onClick(self):
        self.function(self.note.id)