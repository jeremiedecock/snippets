import sys
from PySide6.QtWidgets import QApplication
from bookwindow import BookWindow
import rc_books

if __name__ == "__main__":
    app = QApplication([])

    window = BookWindow()
    window.resize(800, 600)
    window.show()

    sys.exit(app.exec())
