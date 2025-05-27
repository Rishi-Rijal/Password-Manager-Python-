import sys
from PyQt5.QtWidgets import QApplication
import ui
import db

if __name__ == "__main__":
    db.connect()
    app = QApplication(sys.argv)
    window = ui.PasswordManager()
    window.show()
    sys.exit(app.exec_())
