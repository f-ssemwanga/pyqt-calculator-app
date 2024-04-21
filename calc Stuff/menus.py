from sympy import cos, sin, tan
from PyQt5 import QtWidgets, uic, QtCore
from PyQt5.QtCore import Qt
import sys
from sqlite3 import *

current_window = None

def connection():
    conn = connect("usersAndFilms.db")
    cur = conn.cursor()
    return conn,cur

def searchForUser(username):
    conn, cur = connection()
    cur.execute("Select userID, username, password FROM users WHERE username = ?",(username,))
    returnData = cur.fetchall()
    conn.close()
    return returnData

class Calculator(QtWidgets.QMainWindow):
    def __init__(self):
        super(Calculator, self).__init__()
        uic.loadUi("calculator.ui", self)
        self.show()

        self.hasDecimal = False
        self.resultGiven = False
        self.currentOperator = ""
        self.currentValue = 0

        self.zero     .clicked.connect(lambda: self.addNumber("0"))
        self.one      .clicked.connect(lambda: self.addNumber("1"))
        self.two      .clicked.connect(lambda: self.addNumber("2"))
        self.three    .clicked.connect(lambda: self.addNumber("3"))
        self.four     .clicked.connect(lambda: self.addNumber("4"))
        self.five     .clicked.connect(lambda: self.addNumber("5"))
        self.six      .clicked.connect(lambda: self.addNumber("6"))
        self.seven    .clicked.connect(lambda: self.addNumber("7"))
        self.eight    .clicked.connect(lambda: self.addNumber("8"))
        self.nine     .clicked.connect(lambda: self.addNumber("9"))
        self.point    .clicked.connect(self.addDecimal)
        self.plus     .clicked.connect(lambda: self.setOperator("+"))
        self.minus    .clicked.connect(lambda: self.setOperator("-"))
        self.multiply .clicked.connect(lambda: self.setOperator("*"))
        self.divide   .clicked.connect(lambda: self.setOperator("/"))
        self.equals   .clicked.connect(lambda: self.execute(True))
        self.exponent .clicked.connect(lambda: self.setOperator("^"))
        self.root     .clicked.connect(lambda: self.setOperator("n√Y"))
        self.sin      .clicked.connect(lambda: self.immediateOperator("sin"))
        self.cos      .clicked.connect(lambda: self.immediateOperator("cos"))
        self.tan      .clicked.connect(lambda: self.immediateOperator("tan"))
        self.backspace.clicked.connect(self.deleteChar)
        self.clear    .clicked.connect(lambda: self.reset("0"))
        self.pi       .clicked.connect(lambda: self.Screen.setText("3.14159265359"))

    def keyPressEvent(self, key):
        modifiers = QtWidgets.QApplication.keyboardModifiers()
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
        if key.key() == Qt.Key_6:
            self.addNumber("6")
        if key.key() == Qt.Key_7:
            self.addNumber("7")
        if key.key() == Qt.Key_8:
            self.addNumber("8")
        if key.key() == Qt.Key_9:
            self.addNumber("9")
        if key.key() == Qt.Key_Period:
            self.addDecimal()
        if key.key() == Qt.Key_Backspace:
            self.deleteChar()
        if key.key() == Qt.Key_Plus:
            self.setOperator("+")
        if key.key() == Qt.Key_Minus:
            self.setOperator("-")
        if key.key() == Qt.Key_X:
            self.setOperator("*")
        if key.key() == Qt.Key_Slash:
            self.setOperator("/")
        if key.key() == Qt.Key_AsciiCircum:
            self.setOperator("^")
        if key.key() == Qt.Key_R:
            self.setOperator("n√Y")
        if key.key() == Qt.Key_S:
            self.immediateOperator("sin")
        if key.key() == Qt.Key_C:
            self.immediateOperator("cos")
        if key.key() == Qt.Key_T:
            self.immediateOperator("tan")
        if key.key() == Qt.Key_P:
            self.Screen.setText("3.14159265359")
        if key.key() == Qt.Key_Return:
            self.execute(True)
        if key.key() == Qt.Key_Z:
            self.reset("0")

        if modifiers == QtCore.Qt.ControlModifier:
            if key.key() == Qt.Key_W:
                self.close()
        

    def addNumber(self, character):
        if not self.resultGiven:
            self.Screen.setText(self.Screen.text() + character)
            if self.Screen.text()[0] == "0" and len(self.Screen.text()) >= 2 and self.Screen.text()[1] != ".":
                self.Screen.setText(self.Screen.text()[1:])
        else:
            self.reset(character)
    
    def addDecimal(self):
        if not self.resultGiven:
            if not self.hasDecimal:
                self.Screen.setText(self.Screen.text() + ".")
                self.hasDecimal = True
        else:
            self.reset("0.")

    def deleteChar(self):
        if not self.resultGiven:
            if len(self.Screen.text()) > 1:
                if self.Screen.text()[-1] == ".":
                    self.hasDecimal = False
                self.Screen.setText(self.Screen.text()[:-1])
            else:
                self.Screen.setText("0")
        else:
            self.reset("0")
    
    def immediateOperator(self, operator):
        if self.currentValue == "ERROR":
            self.reset("0")
            return

        self.currentOperator = ""
        self.operatorDisplay.setText("")

        if operator == "sin":
            self.Screen.setText(str(sin(float(self.Screen.text()))))
            self.operatorDisplay.setText("sin")
        if operator == "cos":
            self.Screen.setText(str(cos(float(self.Screen.text()))))
            self.operatorDisplay.setText("cos")
        if operator == "tan":
            self.Screen.setText(str(tan(float(self.Screen.text()))))
            self.operatorDisplay.setText("tan")

        self.resultGiven = True

    def setOperator(self, operator):
        if self.currentValue == "ERROR":
            self.reset("0")
            return
        self.execute(False)

        self.operatorDisplay.setText(operator)
        self.currentOperator = operator
        self.resultGiven = False
    
    def execute(self, isFinal):
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
            elif self.currentOperator == "^":
                self.currentValue **= float(self.Screen.text())
            elif self.currentOperator == "n√Y":
                self.currentValue **= 1/(float(self.Screen.text()))
            elif self.currentOperator == "=":
                self.currentValue = float(self.Screen.text())
            elif self.currentOperator == "":
                self.currentValue = float(self.Screen.text())
            
            if type(self.currentValue) == complex:
                hasError = True
        except ZeroDivisionError:
            hasError = True

        if len(str(self.currentValue)) > 2 and str(self.currentValue)[-2] == "." and str(self.currentValue)[-1] == "0":
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

    def reset(self, value):
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

class Login(QtWidgets.QMainWindow): 
    def __init__(self):
        super(Login, self).__init__()
        uic.loadUi('login.ui',self)
        self.show()
        
        self.BtnSubmit.clicked.connect(self.loginButtonMethod)
        self.BtnClear.clicked.connect(self.clearInputs)
    
    def keyPressEvent(self, key):
        modifiers = QtWidgets.QApplication.keyboardModifiers()
        if key.key() == Qt.Key_Return:
            self.loginButtonMethod()

        if modifiers == QtCore.Qt.ControlModifier:
            if key.key() == Qt.Key_W:
                self.close()

    def loginButtonMethod(self):
        username = self.LnEdtUsername.text().lower()
        password = self.LnEdtPassword.text()
        if username == "" or password == "":
            self.messageBox("Blank fields", "Please enter both a username and password!", "warning")
        else:
            userData = searchForUser(username)
            if len(userData) > 0:
                if password == userData[0][2]:
                    self.messageBox("Login Successful", "You have logged in successfully!", "info")
                    self.clearInputs()
                    global current_window
                    current_window = Calculator()
                    self.close()
                else:
                    self.messageBox("Incorrect Password", "You have entered the wrong password!", "warning")
                    self.LnEdtPassword.clear()
            else:
                self.messageBox("Incorrect Username", "The username you have entered does not exist!", "warning")
                self.clearInputs()

    def clearInputs(self):
        self.LnEdtUsername.clear()
        self.LnEdtPassword.clear()

    def messageBox(self, title, content, iconType="info"):
        msgBox = QtWidgets.QMessageBox()
        if iconType == "info":
            msgBox.setIcon(QtWidgets.QMessageBox.Information)
        elif iconType == "question":
            msgBox.setIcon(QtWidgets.QMessageBox.Question)
        elif iconType == "warning":
            msgBox.setIcon(QtWidgets.QMessageBox.Warning)
        else:
            msgBox.setIcon(QtWidgets.QMessageBox.Critical)
        msgBox.setText(content)
        msgBox.setWindowTitle(title)
        msgBox.exec()

def main():
    app = QtWidgets.QApplication(sys.argv)
    global current_window
    current_window = Login()
    app.exec()
    QtWidgets.QApplication.quit()
        
main()
