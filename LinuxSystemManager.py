import sys
import paramiko
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QInputDialog, QMessageBox, QLineEdit, QTableWidgetItem
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
        self.toolButton_disconnect.clicked.connect(self.disconn)
        self.toolButton_github.clicked.connect(self.open_github)
        self.toolButton_new_file.clicked.connect(self.new_file)
        self.lineEdit_search_file.returnPressed.connect(self.search_file)
        self.toolButton_delete_file.clicked.connect(self.delete_file)
        self.toolButton_copy_file.clicked.connect(self.copy_file)
        self.toolButton_move_file.clicked.connect(self.move_file)



    def change_user(self):
        self.ssh_client.close()
        self.username, _ = QInputDialog.getText(self, "Kullanıcı Değiştir", "Kullanıcı adını giriniz")
        self.password, _ = QInputDialog.getText(self, "Kullanıcı Değiştir", "Şifreyi giriniz")
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(hostname=self.host, port=22, username=self.username, password=self.password)
        self.label_user.setText(self.username)

    def disconn(self):
        self.ssh_client.close()
        self.close()
        login_window.lineEdit_user.setText("")
        login_window.lineEdit_pass.setText("")
        login_window.lineEdit_host.setText("")
        login_window.show()

    def open_github(self):
        url = QUrl("https://github.com/Slmdlgl40/LinuxSystemManagement")
        QDesktopServices.openUrl(url)

    def new_file(self):
        self.new_filename, _ = QInputDialog.getText(self, "Yeni Dosya", "Dosya adını yolu ile birlikte giriniz.")
        command = f'touch {self.new_filename}'
        self.ssh_client.exec_command(command)

    def search_file(self):
        try:
            self.tableWidget_file.clearContents()
            self.tableWidget_file.setRowCount(0)
            self.file_to_search = self.lineEdit_search_file.text()
            command = f'find / -name {self.file_to_search} 2> /dev/null'
            stdin, stdout, stderr = self.ssh_client.exec_command(command)
            file_result = stdout.readlines()
            for i in file_result:
                command2 = f'ls -la {i}'
                stdin, stdout, stderr = self.ssh_client.exec_command(command2)
                file_result2 = stdout.readlines()
                splited_result = file_result2[0].split(' ')
                filename_searched = splited_result[-1]
                file_owner = splited_result[2]
                file_perms = splited_result[0]
                row_position = self.tableWidget_file.rowCount()
                self.tableWidget_file.insertRow(row_position)
                self.tableWidget_file.setItem(row_position, 0, QTableWidgetItem(file_perms))
                self.tableWidget_file.setItem(row_position, 1, QTableWidgetItem(file_owner))
                self.tableWidget_file.setItem(row_position, 2, QTableWidgetItem(filename_searched))
        except Exception as e:
            QMessageBox.warning(self, "Dosya Arama", "Dosya bulunamadı")

    def delete_file(self):
        selected_items = self.tableWidget_file.selectedItems()
        if selected_items:
            try:
                row = selected_items[0].row()
                column = selected_items[0].column()
                file_to_delete = self.tableWidget_file.item(row, column).text()
                command = f'rm {file_to_delete}'
                stdin, stdout, stderr = self.ssh_client.exec_command(command)
                QMessageBox.information(self, "Dosya Silme", "Dosya başarıyla silindi.")
                self.search_file()
            except Exception as e:
                QMessageBox.warning(self, "Dosya Silme", "Dosya silinirken bir hata oluştu.")
                print(e)
        else:
            QMessageBox.warning(self, "Dosya Silme", "Lütfen bir dosya seçin.")

    def copy_file(self):
        selected_items = self.tableWidget_file.selectedItems()
        if selected_items:
            try:
                row = selected_items[0].row()
                column = selected_items[0].column()
                file_to_copy = self.tableWidget_file.item(row, column).text()
                copy_dir, _ = QInputDialog.getText(self, "Dosya Kopyalama", "Dosyanın kopyalanacağı dizini girin.")
                command = "cp" + " " + file_to_copy.strip() + " " + copy_dir
                print(command)
                stdin, stdout, stderr = self.ssh_client.exec_command(command)
                QMessageBox.information(self, "Dosya Kopyalama", "Dosya başarıyla kopyalandı.")
                self.search_file()
            except Exception as e:
                QMessageBox.warning(self, "Dosya Kopyalama", "Dosya kopyalanırken bir hata oluştu.")
                print(e)
        else:
            QMessageBox.warning(self, "Dosya Kopyalama", "Lütfen bir dosya seçin.")

    def move_file(self):
        selected_items = self.tableWidget_file.selectedItems()
        if selected_items:
            try:
                row = selected_items[0].row()
                column = selected_items[0].column()
                file_to_copy = self.tableWidget_file.item(row, column).text()
                copy_dir, _ = QInputDialog.getText(self, "Dosya Taşıma", "Dosyanın taşınacağı dizini girin.")
                command = "mv" + " " + file_to_copy.strip() + " " + copy_dir
                print(command)
                stdin, stdout, stderr = self.ssh_client.exec_command(command)
                QMessageBox.information(self, "Dosya Taşıma", "Dosya başarıyla taşındı.")
                self.search_file()
            except Exception as e:
                QMessageBox.warning(self, "Dosya Taşıma", "Dosya taşınırken bir hata oluştu.")
                print(e)
        else:
            QMessageBox.warning(self, "Dosya Taşıma", "Lütfen bir dosya seçin.")


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

        except:
            QMessageBox.warning(self, "Bağlantı Hatası", "Lütfen girdiğiniz bilgileri kontrol edin.")

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