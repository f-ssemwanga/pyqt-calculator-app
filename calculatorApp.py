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
        # initialise

        self.hasDecimal = False
        self.resultGiven = True
        self.currentOperator = ""
        self.currentValue = 0

        self.Screen.setAlignment(Qt.AlignRight)  # align text to the right
        # connect button to event listener
        # self.one.clicked.connect(self.numButton)
        self.zero.clicked.connect(lambda: self.addNumber("0"))
        self.one.clicked.connect(lambda: self.addNumber("1"))
        self.two.clicked.connect(lambda: self.addNumber("2"))
        self.three.clicked.connect(lambda: self.addNumber("3"))
        self.four.clicked.connect(lambda: self.addNumber("4"))
        self.five.clicked.connect(lambda: self.addNumber("5"))
        self.clear.clicked.connect(lambda: self.reset("0"))
        # add a decimal
        self.point.clicked.connect(self.addDecimal)
        # delete characters
        self.backspace.clicked.connect(self.deleteChar)
        # handle Operators
        self.add.clicked.connect(lambda: self.setOperator("+"))

        # handle the equal sign
        self.equals.clicked.connect(lambda: self.execute(True))

    def addNumber(self, numChar):
        """handles all numeric values and adds them to the display"""
        print(f"{numChar} was pressed")
        if not self.resultGiven:
            self.Screen.setText(self.Screen.text() + numChar)
            # remove leading zeros except for decimal numbers
            if (
                self.Screen.text()[0] == "0"
                and len(self.Screen.text()) >= 2
                and self.Screen.text()[1] != "."
            ):
                self.Screen.setText(self.Screen.text()[1:])
        else:
            self.reset(numChar)

    def reset(self, value):
        """resets variables and display screens"""
        self.Screen.setText(value)
        self.valueDisplay.setText("")
        self.operatorDisplay.setText("")
        self.currentOperator = ""
        self.resultGiven = False
        self.currentValue = 0
        if value == "0.":
            self.hasDecimal = True
        else:
            self.hasDecimal = False

    def keyPressEvent(self, key):
        """binding for keyboard keys"""
        if key.key() == Qt.Key_0:
            self.addNumber("0")
        if key.key() == Qt.Key_1:
            self.addNumber("1")
        if key.key() == Qt.Key_2:
            self.addNumber("2")
        if key.key() == Qt.Key_3:
            self.addNumber("3")
        if key.key() == Qt.Key_4:
            self.addNumber("4")
        if key.key() == Qt.Key_5:
            self.addNumber("5")

    def addDecimal(self):
        # adds a decimal point
        if not self.resultGiven:
            # check if there is already a decimal point
            if not self.hasDecimal:
                self.Screen.setText(self.Screen.text() + ".")
                self.hasDecimal = True
        else:
            self.reset("0.")

    def deleteChar(self):
        """handles the backspace key"""
        if not self.resultGiven:
            if len(self.Screen.text()) > 1:
                if self.Screen.text()[-1] == ".":
                    self.hasDecimal = False
                self.Screen.setText(self.Screen.text()[:-1])
            else:
                self.Screen.setText("0")
        else:
            self.reset("0")

    def setOperator(self, operator):
        """Sets the operator for the equation"""
        if self.currentValue == "ERROR":
            self.reset("0")
            return
        self.execute(False)

        self.operatorDisplay.setText(operator)
        self.currentOperator = operator
        self.resultGiven = False

    def execute(self, isFinal):
        """Executes the equation within the calculator and handles errors"""
        hasError = False
        self.hasDecimal = False
        if self.Screen.text() == "ERROR":
            self.Screen.setText("0")
        try:
            if self.currentOperator == "+":
                self.currentValue += float(self.Screen.text())
            elif self.currentOperator == "-":
                self.currentValue -= float(self.Screen.text())
            elif self.currentOperator == "*":
                self.currentValue *= float(self.Screen.text())
            elif self.currentOperator == "/":
                self.currentValue /= float(self.Screen.text())
            elif self.currentOperator == "=":
                self.currentValue = float(self.Screen.text())
            elif self.currentOperator == "":
                self.currentValue = float(self.Screen.text())

            if type(self.currentValue) == complex:
                hasError = True
        except ZeroDivisionError:
            hasError = True
        if (
            len(str(self.currentValue)) > 2
            and str(self.currentValue)[-2] == "."
            and str(self.currentValue)[-1] == "0"
        ):
            self.currentValue = round(self.currentValue)
        if not hasError:
            if isFinal:
                if self.valueDisplay.text() != "":
                    self.Screen.setText(str(self.currentValue))
                    self.valueDisplay.setText("")
                    self.operatorDisplay.setText("=")
                    self.currentOperator = "="
                    self.resultGiven = True
            else:
                self.valueDisplay.setText(str(self.currentValue))
                self.Screen.setText("0")
        else:
            self.Screen.setText("ERROR")
            self.valueDisplay.setText("")
            self.operatorDisplay.setText("")
            self.currentOperator = ""
            self.currentValue = "ERROR"
            self.resultGiven = True


def mainApplication():
    """main application for loading the window instance"""
    app = QtWidgets.QApplication(sys.argv)
    window = CalculatorUi()
    window.show()

    app.quit()
    sys.exit(app.exec_())


mainApplication()
