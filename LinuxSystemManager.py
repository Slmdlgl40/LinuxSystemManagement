import sys
import paramiko
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QInputDialog, QMessageBox, QLineEdit, QTableWidgetItem, \
    QFileDialog
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
        self.toolButton_file_perm.clicked.connect(self.change_perm)
        self.toolButton_edit_file.clicked.connect(self.edit_file)
        self.toolButton_upload_file.clicked.connect(self.upload_file)
        self.toolButton_download_file.clicked.connect(self.download_file)


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
                stdin, stdout, stderr = self.ssh_client.exec_command(command)
                QMessageBox.information(self, "Dosya Taşıma", "Dosya başarıyla taşındı.")
                self.search_file()
            except Exception as e:
                QMessageBox.warning(self, "Dosya Taşıma", "Dosya taşınırken bir hata oluştu.")
        else:
            QMessageBox.warning(self, "Dosya Taşıma", "Lütfen bir dosya seçin.")

    def change_perm(self):
        selected_items = self.tableWidget_file.selectedItems()
        if selected_items:
            try:
                row = selected_items[0].row()
                column = selected_items[0].column()
                file_to_perm = self.tableWidget_file.item(row, column).text()
                mod, _ = QInputDialog.getText(self, "Dosya İzinleri", "Değiştirmek istediğiniz iznin mod değerini girin.")
                command = "chmod" + " " + mod + " " + file_to_perm
                stdin, stdout, stderr = self.ssh_client.exec_command(command)
                QMessageBox.information(self, "Dosya İzinleri", "Dosya izni başarıyla değiştirildi.")
            except Exception as e:
                QMessageBox.warning(self, "Dosya İzinleri", "Dosya izni değiştirilirken bir hata oluştu.")
                print(e)
        else:
            QMessageBox.warning(self, "Dosya İzinleri", "Lütfen bir dosya seçin.")

    def edit_file(self):
        selected_items = self.tableWidget_file.selectedItems()
        if selected_items:
            try:
                row = selected_items[0].row()
                column = selected_items[0].column()
                file_to_edit = self.tableWidget_file.item(row, column).text()
                command = f"cat {file_to_edit}"
                stdin, stdout, stderr = self.ssh_client.exec_command(command)
                file_content = stdout.read().decode()
                editor_window.textEdit.setPlainText(file_content)
                editor_window.ssh_client = self.ssh_client
                editor_window.file_to_edit = file_to_edit
                editor_window.show()
            except Exception as e:
                QMessageBox.warning(self, "Dosya Edit", "Dosya editlenirken bir hata oluştu.")
                print(e)
        else:
            QMessageBox.warning(self, "Dosya Edit", "Lütfen bir dosya seçin.")

    def upload_file(self):
        try:
            file_path, _ = QFileDialog.getOpenFileName(self, "Dosya Seç", ".")
            path_to_upload, _ = QInputDialog.getText(self, "Dosya Yükleme", "Dosyanın yükleneceği dizini girin.")
            file_name = file_path.split("/")[-1]
            full_path = path_to_upload + "/" +  file_name
            sftp_client = self.ssh_client.open_sftp()
            sftp_client.put(file_path, full_path)
            sftp_client.close()
            QMessageBox.information(self, "Dosya Yükleme", "Dosya başarıyla yüklendi.")
        except Exception as e:
            QMessageBox.warning(self, "Dosya Yükleme", "Dosya yüklenirken bir hata oluştu.")

    def download_file(self):
        selected_items = self.tableWidget_file.selectedItems()
        if selected_items:
            try:
                row = selected_items[0].row()
                column = selected_items[0].column()
                file_to_download = self.tableWidget_file.item(row, column).text()
                path_to_download, _ = QInputDialog.getText(self, "Dosya İndirme", "Dosyanın indirileceği dizini girin.")
                full_path = path_to_download + "/" + file_to_download.strip().split("/")[-1]
                sftp_client = self.ssh_client.open_sftp()
                sftp_client.get(file_to_download.strip(), full_path)
                sftp_client.close()
            except Exception as e:
                QMessageBox.warning(self, "Dosya İndirme", "Dosya indirilirken bir hata oluştu.")
                print(e)
        else:
            QMessageBox.warning(self, "Dosya İndirme", "Lütfen bir dosya seçin.")


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
            self.ssh_client = paramiko.SSHClient()
            self.ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.ssh_client.connect(hostname=host, port=22, username=user, password=password)

            main_window.ssh_client = self.ssh_client
            main_window.host = host
            main_window.label_user.setText(user)
            main_window.label_host.setText(host)
            main_window.ssh_client = self.ssh_client
            self.kernel_version()
            self.disk_usage()
            self.get_uptime()
            self.get_last_update()
            self.get_distro()
            self.close()
            main_window.show()

        except:
            QMessageBox.warning(self, "Bağlantı Hatası", "Lütfen girdiğiniz bilgileri kontrol edin.")

    def kernel_version(self):
        stdin, stdout, stderr = self.ssh_client.exec_command('uname -r')
        kernel_version = stdout.read().decode('utf-8').strip()
        main_window.label_kernel.setText(kernel_version)

    def disk_usage(self):
        stdin, stdout, stderr = self.ssh_client.exec_command('df -h')
        disk_usages = stdout.read().decode('utf-8').split('\n')
        for line in disk_usages:
            if line.startswith('/dev/sda'):
                main_window.label_disk.setText(line.split()[-2])

    def get_uptime(self):
        stdin, stdout, stderr = self.ssh_client.exec_command('uptime')
        uptime = stdout.read().decode('utf-8').strip().split(",")
        main_window.label_runtime.setText(uptime[0][11::])

    def get_last_update(self):
        stdin, stdout, stderr = self.ssh_client.exec_command('grep "Start-Date" /var/log/apt/history.log | tail -n 1')
        last_update_date = stdout.read().decode('utf-8').strip().split()
        main_window.label_update.setText(last_update_date[1])

    def get_distro(self):
        stdin, stdout, stderr = self.ssh_client.exec_command('cat /etc/*release')
        output = stdout.read().decode('utf-8').split('\n')
        main_window.label_distro.setText(output[0].split('=')[1])

class Editor_Window(QWidget, Editor_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.ssh_client = None
        self.file_to_edit = None

        self.pushButton_save_file.clicked.connect(self.save_file)

    def save_file(self):
        content = self.textEdit.toPlainText()
        stdin, stdout, stderr = self.ssh_client.exec_command(f"echo '{content}' > {self.file_to_edit}")
        QMessageBox.information(self, "Dosya Edit", "Dosya içeriği başarıyla değiştirildi.")
        self.close()

app = QApplication(sys.argv)
editor_window = Editor_Window()
login_window = Login_Window()
main_window = MainWindow()
login_window.show()
sys.exit(app.exec())