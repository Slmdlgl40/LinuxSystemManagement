# Form implementation generated from reading ui file '.\Login.ui'
#
# Created by: PyQt6 UI code generator 6.4.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(282, 391)
        Form.setStyleSheet("QWidget\n"
"{\n"
"background-color: yellow;\n"
"}\n"
"\n"
"QPushButton\n"
"{\n"
"background-color:white;\n"
"border-radius:10px;\n"
"}\n"
"\n"
"QPushButton:hover\n"
"{\n"
"background-color:#dddddd;\n"
"border-radius:10px;\n"
"}\n"
"\n"
"QLineEdit\n"
"{\n"
"background-color:white;\n"
"border-radius:10px;\n"
"}\n"
"")
        self.pushButton_conn = QtWidgets.QPushButton(parent=Form)
        self.pushButton_conn.setGeometry(QtCore.QRect(10, 340, 261, 40))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.pushButton_conn.setFont(font)
        self.pushButton_conn.setObjectName("pushButton_conn")
        self.lineEdit_user = QtWidgets.QLineEdit(parent=Form)
        self.lineEdit_user.setGeometry(QtCore.QRect(10, 160, 261, 41))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.lineEdit_user.setFont(font)
        self.lineEdit_user.setStyleSheet("")
        self.lineEdit_user.setObjectName("lineEdit_user")
        self.lineEdit_pass = QtWidgets.QLineEdit(parent=Form)
        self.lineEdit_pass.setGeometry(QtCore.QRect(10, 220, 211, 41))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.lineEdit_pass.setFont(font)
        self.lineEdit_pass.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self.lineEdit_pass.setObjectName("lineEdit_pass")
        self.lineEdit_host = QtWidgets.QLineEdit(parent=Form)
        self.lineEdit_host.setGeometry(QtCore.QRect(10, 280, 261, 41))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.lineEdit_host.setFont(font)
        self.lineEdit_host.setObjectName("lineEdit_host")
        self.pushButton_rsa = QtWidgets.QPushButton(parent=Form)
        self.pushButton_rsa.setGeometry(QtCore.QRect(230, 220, 41, 41))
        self.pushButton_rsa.setObjectName("pushButton_rsa")
        self.label = QtWidgets.QLabel(parent=Form)
        self.label.setGeometry(QtCore.QRect(40, 20, 201, 121))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.label.setFont(font)
        self.label.setObjectName("label")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Bağlan"))
        self.pushButton_conn.setText(_translate("Form", "Bağlan"))
        self.lineEdit_user.setPlaceholderText(_translate("Form", "Kullanıcı Adı"))
        self.lineEdit_pass.setPlaceholderText(_translate("Form", "Şifre"))
        self.lineEdit_host.setPlaceholderText(_translate("Form", "Host"))
        self.pushButton_rsa.setText(_translate("Form", "RSA"))
        self.label.setText(_translate("Form", "Bağlantı Bilgileri"))