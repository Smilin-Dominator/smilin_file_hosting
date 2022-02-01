from json import loads, dumps
from pathlib import Path
from sys import argv
from threading import Thread
from queue import Queue

from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QLineEdit, QPushButton, QLabel, QScrollArea, QVBoxLayout, QMainWindow, QWidget, QGroupBox, QFileDialog

from connector import API
from cryptography import Crypto


class CredentialsUI(QMainWindow):

    def __init__(self):

        # Declaration
        self.token_input: QLineEdit = None
        self.link_input: QLineEdit = None
        self.email_input: QLineEdit = None
        self.register_button: QPushButton = None
        self.connect_button: QPushButton = None
        self.credentials_status: QLabel = None

        # Initial
        super(CredentialsUI, self).__init__()
        uic.loadUi("credentials.ui", self)
        self.setWindowTitle("Smilin' File Client - Credentials")

        # Post Initial
        self.connect_button.clicked.connect(self.credentials_connect)
        self.register_button.clicked.connect(self.credentials_register)

    def credentials_connect(self):
        text = [self.token_input.text(), self.link_input.text(), self.email_input.text()]
        check = [i for i in text if i != ""]
        if len(check) != 3:
            self.credentials_status.setText("Not Enough Arguments!")
        else:
            self.write_file(*text)

    def credentials_register(self):
        if self.link_input.text() == "":
            self.credentials_status.setText("Link Is Empty!")
        else:
            token = api.register(self.link_input.text())
            self.credentials_status.setText("Successfully Registered!")
            self.token_input.setText(token)

    def write_file(self, token: str, link: str, email: str) -> None:
        global crypto, main_window
        out = {
            "token": token,
            "link": link,
            "email": email
        }
        creds = Path("credentials")
        creds.mkdir() if not creds.exists() else None
        with open("credentials/config.json", "w") as w:
            w.write(dumps(out, indent=4))
            w.flush()
            w.close()
        api = API(server=link, username=token, email=email)
        if not api.test_connection():
            self.credentials_status.setText("Connection Failed!")
            self.show()
        else:
            crypto.setup_gpg(email)
            self.close()
            main_window.show()

    def read_file(self) -> bool:
        global api
        try:
            with open("credentials/config.json", "r") as r:
                js = loads(r.read())
                api = API(server=js["link"], username=js["token"], email=js["email"])
                if not api.test_connection():
                    self.credentials_status.setText("Connection Failed!")
                    return False
                crypto.setup_gpg(js["email"])
                main_window.show()
                return True
        except FileNotFoundError:
            self.credentials_status.setText("File Not Found!")
            return False
        except KeyError:
            self.credentials_status.setText("Not Enough Options!")
            return False


class MainUI(QMainWindow):

    def __init__(self):

        # Declaration
        self.file_container: QScrollArea = None
        self.files_layout: QVBoxLayout = QVBoxLayout()
        self.files_section: QWidget = None

        self.downloading_files_status: QGroupBox = None
        self.downloading_files_layout: QVBoxLayout = QVBoxLayout()

        self.uploading_files_status: QGroupBox = None
        self.uploading_files_layout: QVBoxLayout = QVBoxLayout()

        self.change_credentials_button:  QPushButton = None
        self.upload_files_button: QPushButton = None

        self.file_opener: QFileDialog = QFileDialog()

        # Initial
        super().__init__()
        uic.loadUi("main.ui", self)
        self.setWindowTitle("Smilin' File Client")

        # Post Initial
        self.downloading_files_status.setLayout(self.downloading_files_layout)
        self.uploading_files_status.setLayout(self.uploading_files_layout)

        self.ops = self.ConnectorFunctions(self.uploading_files_layout, self.downloading_files_layout)

        self.change_credentials_button.clicked.connect(self.change_credentials)
        self.upload_files_button.clicked.connect(self.upload_file)

    def change_credentials(self):
        self.close()
        credentials_window.show()

    def upload_file(self):
        files = self.file_opener.getOpenFileNames()
        for file in files:
            self.ops.upload_queue.put(file)
            Thread(target=self.ops.upload_file).start()

    def download_file(self, filename: str, id: int):
        self.ops.download_queue.put((id, filename))
        Thread(target=self.ops.download_file).start()

    class ConnectorFunctions(object):

        def __init__(self, upload_status: QVBoxLayout, download_status: QVBoxLayout) -> None:
            self.connector = api
            self.upload_status = upload_status
            self.download_status = download_status
            self.upload_queue = Queue(maxsize=5)
            self.download_queue = Queue(maxsize=5)

        def upload_file(self) -> None:
            filename: str = self.upload_queue.get()
            file_widget = QLabel(filename)
            self.upload_status.addWidget(file_widget)
            self.connector.upload_file(filename)
            self.upload_status.removeWidget(file_widget)

        def download_file(self) -> None:
            file_id, filename = self.download_queue.get()
            file_widget = QLabel(filename)
            self.download_status.addWidget(file_widget)
            self.connector.download_file(file_id)
            self.download_status.removeWidget(file_widget)

        def get_files(self) -> list[dict]:
            return self.connector.get_all_files()


# Main Variables

api = API("", "", "")
crypto = Crypto()
app = QApplication(argv)

credentials_window = CredentialsUI()
main_window = MainUI()

if __name__ == "__main__":
    options = credentials_window.read_file()
    if not options:
        credentials_window.show()
    else:
        main_window.show()
    app.exec()
