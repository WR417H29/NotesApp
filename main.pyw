#!C:\Users\iacna\..Programming\Desktop\NotesApp\.env\Scripts\pythonw.exe

import sys

from PyQt6 import (
    QtWidgets as qtw
)

from widgets.windows.main_window import MainWindow

if __name__ == "__main__":
    app = qtw.QApplication(sys.argv)
    mw = MainWindow()
    mw.show()
    app.exec()