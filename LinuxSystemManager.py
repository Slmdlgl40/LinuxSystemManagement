import sys
import paramiko
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QInputDialog, QMessageBox, QLineEdit
from PyQt6.QtCore import QUrl
from PyQt6.QtGui import QDesktopServices
from MainGUI import Ui_MainWindow
from Login import Login_Form
from Editor import Editor_Form

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.ssh_client = None
        self.host = None


        self.toolButton_exit.clicked.connect(self.close)
        self.toolButton_chng_usr.clicked.connect(self.change_user)
        self.toolButton_disconnect.clicked.connect(self.disconnect)
        self.toolButton_github.clicked.connect(self.open_github)



    def change_user(self):
        self.ssh_client.close()
        self.username, _ = QInputDialog.getText(self, "Kullanıcı Değiştir", "Kullanıcı adını giriniz")
        self.password, _ = QInputDialog.getText(self, "Kullanıcı Değiştir", "Şifreyi giriniz")
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(hostname=self.host, port=22, username=self.username, password=self.password)
        self.label_user.setText(self.username)

    def disconnect(self):
        self.ssh_client.close()
        self.close()
        login_window.lineEdit_user.setText("")
        login_window.lineEdit_pass.setText("")
        login_window.lineEdit_host.setText("")
        login_window.show()

    def open_github(self):
        url = QUrl("https://github.com/Slmdlgl40/LinuxSystemManagement")
        QDesktopServices.openUrl(url)

class Login_Window(QWidget, Login_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.show()

        self.pushButton_conn.clicked.connect(self.connect_ssh)

    def connect_ssh(self):
        try:
            user = self.lineEdit_user.text()
            host = self.lineEdit_host.text()
            password = self.lineEdit_pass.text()
            ssh_client = paramiko.SSHClient()
            ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh_client.connect(hostname=host, port=22, username=user, password=password)

            main_window.ssh_client = ssh_client
            main_window.host = host
            main_window.label_user.setText(user)
            main_window.label_host.setText(host)
            main_window.ssh_client = ssh_client
            self.close()
            main_window.show()

        except Exception as e:
            QMessageBox.warning(self, "Bağlantı Hatası", "Lütfen girdiğiniz bilgileri kontrol edin.")
            print(e)

class Editor_Window(QWidget, Editor_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

app = QApplication(sys.argv)
editor_window = Editor_Window()
login_window = Login_Window()
main_window = MainWindow()
login_window.show()
sys.exit(app.exec())