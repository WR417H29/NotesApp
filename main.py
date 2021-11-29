import sys

import PyQt6.QtWidgets as qtw

from widgets.main_window import MainWindow

if __name__ == "__main__":
    app = qtw.QApplication(sys.argv)
    mw = MainWindow()
    mw.show()
    app.exec()