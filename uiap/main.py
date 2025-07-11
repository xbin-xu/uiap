import sys
from PySide6 import QtWidgets
from gui.gui_uiap import UiapWindow


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = UiapWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
