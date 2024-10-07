from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import Qt, QUrl, QFileInfo, Signal
from PySide6.QtGui import QDesktopServices
from PySide6.QtWidgets import QLabel
import os
from PySide6.QtWebEngineWidgets import QWebEngineView

class ClickableLabel(QLabel):
    clicked = Signal()

    def __init__(self, text='', parent=None):
        super().__init__(text, parent)
        self.setCursor(Qt.PointingHandCursor)
        self.setStyleSheet("color: blue; text-decoration: underline;")

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.clicked.emit()


class Ui_MainWindow(object):
    email = ""
    password = ""

    email = None
    password = None

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(900, 600)
        MainWindow.setMinimumSize(QtCore.QSize(900, 600))
        MainWindow.setMaximumSize(QtCore.QSize(900, 600))
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.widget = QtWidgets.QWidget(parent=self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(0, 0, 680, 600))
        self.widget.setMaximumSize(QtCore.QSize(680, 16777215))
        self.widget.setObjectName("widget")
        self.label = QtWidgets.QLabel(parent=self.widget)
        self.label.setEnabled(True)
        self.label.setGeometry(QtCore.QRect(0, 0, 680, 600))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap("views/graphics/background2.jpg"))
        self.label.setScaledContents(True)
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeading|QtCore.Qt.AlignmentFlag.AlignLeft|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.label.setObjectName("label")
        self.widget_2 = QtWidgets.QWidget(parent=self.centralwidget)
        self.widget_2.setGeometry(QtCore.QRect(680, 0, 220, 600))
        self.widget_2.setStyleSheet("")
        self.widget_2.setObjectName("widget_2")
        self.widget_3 = QtWidgets.QWidget(parent=self.widget_2)
        self.widget_3.setGeometry(QtCore.QRect(0, 30, 220, 80))
        self.widget_3.setObjectName("widget_3")
        self.label_2 = QtWidgets.QLabel(parent=self.widget_3)
        self.label_2.setGeometry(QtCore.QRect(0, 0, 220, 80))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(25)
        font.setBold(False)
        font.setItalic(False)
        font.setStrikeOut(False)
        font.setKerning(True)
        self.label_2.setFont(font)
        self.label_2.setStyleSheet("color: #FFFFFF\n"
"")
        self.label_2.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.widget_4 = QtWidgets.QWidget(parent=self.widget_2)
        self.widget_4.setGeometry(QtCore.QRect(0, 110, 220, 490))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(15)
        self.widget_4.setFont(font)
        self.widget_4.setObjectName("widget_4")
        self.widget_5 = QtWidgets.QWidget(parent=self.widget_4)
        self.widget_5.setGeometry(QtCore.QRect(0, 80, 220, 30))
        self.widget_5.setObjectName("widget_5")
        self.txt_email = QtWidgets.QLineEdit(parent=self.widget_5)
        self.txt_email.setGeometry(QtCore.QRect(20, 0, 180, 30))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(10)
        self.txt_email.setFont(font)
        self.txt_email.setStyleSheet("border-radius: 10px; padding-left: 5px\n"
"")
        self.txt_email.setObjectName("txt_email")
        global email
        email = self.txt_email
        self.widget_6 = QtWidgets.QWidget(parent=self.widget_4)
        self.widget_6.setGeometry(QtCore.QRect(0, 130, 220, 30))
        self.widget_6.setObjectName("widget_6")
        self.txt_password = QtWidgets.QLineEdit(parent=self.widget_6)
        self.txt_password.setGeometry(QtCore.QRect(20, 0, 180, 30))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(10)
        self.txt_password.setFont(font)
        self.txt_password.setStyleSheet("border-radius: 10px; padding-left: 5px\n"
"")
        self.txt_password.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self.txt_password.setObjectName("txt_password")
        global password
        password = self.txt_password
        self.widget_7 = QtWidgets.QWidget(parent=self.widget_4)
        self.widget_7.setGeometry(QtCore.QRect(0, 200, 220, 30))
        self.widget_7.setObjectName("widget_7")
        self.btn_login = QtWidgets.QPushButton(parent=self.widget_7)
        self.btn_login.setGeometry(QtCore.QRect(75, 0, 70, 30))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        self.btn_login.setFont(font)
        self.btn_login.setStyleSheet("QPushButton { background-color: white; border-radius: 15px; }")
        self.btn_login.setAutoDefault(False)
        self.btn_login.setFlat(False)
        self.btn_login.setObjectName("btn_login")
        self.btn_login.clicked.connect(self.retrieve_credentials)
        self.widget_8 = QtWidgets.QWidget(parent=self.widget_4)
        self.widget_8.setGeometry(QtCore.QRect(0, 320, 220, 30))
        self.widget_8.setObjectName("widget_8")
        self.lbl_signin = ClickableLabel("Sign In", parent=self.widget_4)
        self.lbl_signin.setGeometry(QtCore.QRect(0, 250, 220, 30))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(10)
        self.lbl_signin.setFont(font)
        self.lbl_signin.setStyleSheet("color: #ffffff\n"
"")
        self.lbl_signin.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.lbl_signin.setObjectName("lbl_signin")
        self.label_3 = QtWidgets.QLabel(parent=self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(0, 0, 900, 600))
        self.label_3.setText("")
        self.label_3.setPixmap(QtGui.QPixmap("views/graphics/background1.png"))
        self.label_3.setObjectName("label_3")
        self.label_3.raise_()
        self.widget.raise_()
        self.widget_2.raise_()
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retrieve_credentials (self):
        self.email = self.txt_email.text()
        self.password = self.txt_password.text()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "DAMA IT"))
        self.label_2.setText(_translate("MainWindow", "DAMA IT"))
        self.txt_email.setPlaceholderText(_translate("MainWindow", "email"))
        self.txt_password.setPlaceholderText(_translate("MainWindow", "password"))
        self.btn_login.setText(_translate("MainWindow", "Login"))
        self.lbl_signin.setText(_translate("MainWindow", "Are you not registered yet? Sign up"))
