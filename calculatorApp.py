# import required modules
from PyQt5 import QtWidgets, uic, QtCore, QtGui
from PyQt5.QtCore import Qt
import sys


class CalculatorUi(QtWidgets.QMainWindow):
    """main calculator window"""

    def __init__(self):
        super(CalculatorUi, self).__init__()
        uic.loadUi("CalculatorUI.ui", self)
        self.show()


def mainApplication():
    """main application for loading the window instance"""
    app = QtWidgets.QApplication(sys.argv)
    window = CalculatorUi()
    window.show()

    app.quit()
    sys.exit(app.exec_())  #


mainApplication()
