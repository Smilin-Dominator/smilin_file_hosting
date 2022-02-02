from json import loads, dumps
from pathlib import Path
from queue import Queue
from sys import argv
from threading import Thread

from PyQt6 import uic
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication, QLineEdit, QPushButton, QLabel, QMainWindow, QListWidgetItem, QFileDialog,
    QListWidget, QTreeWidget, QTreeWidgetItem, QTreeWidgetItemIterator
)

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
        global main_window, api
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
            api.setup_crypto(email)
            self.close()
            main_window.show()
            main_window.list_items()

    def read_file(self) -> bool:
        global api, main_window
        try:
            with open("credentials/config.json", "r") as r:
                js = loads(r.read())
                api = API(server=js["link"], username=js["token"], email=js["email"])
                if not api.test_connection():
                    self.credentials_status.setText("Connection Failed!")
                    return False
                api.setup_crypto(js["email"])
                main_window.show()
                main_window.list_items()
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
        self.files: QTreeWidget = None
        self.files_ar: list[dict] = None

        self.status_bar: QLabel = None
        self.downloading_files_status: QListWidget = QListWidget()
        self.uploading_files_status: QListWidget = QListWidget()

        self.download_selected: QPushButton = None
        self.delete_selected: QPushButton = None
        self.change_credentials_button: QPushButton = None
        self.upload_files_button: QPushButton = None

        self.file_opener: QFileDialog = QFileDialog()

        # Initial
        super().__init__()
        uic.loadUi("main.ui", self)
        self.setWindowTitle("Smilin' File Client")

        # Post Initial
        self.ops = self.ConnectorFunctions(self)
        self.change_credentials_button.clicked.connect(self.change_credentials)
        self.upload_files_button.clicked.connect(self.upload_file)
        self.download_selected.clicked.connect(self.download_files)

    def list_items(self):
        Thread(target=self.ops.get_files).start()

    def change_credentials(self):
        self.close()
        credentials_window.show()

    def upload_file(self):
        files = self.file_opener.getOpenFileNames()[0]
        for file in files:
            self.ops.upload_queue.put(file)
            Thread(target=self.ops.upload_file).start()

    def download_files(self):
        id_and_files: list[tuple[str, int]] = []
        it = QTreeWidgetItemIterator(self.files, QTreeWidgetItemIterator.IteratorFlag.Checked)
        while it.value():
            item = it.value()
            filename = item.text(0)
            id = 0
            for el in self.files_ar:
                if el.get("filename") == filename:
                    id = el.get("id")
                    break
            self.ops.download_queue.put((id, filename))
            Thread(target=self.ops.download_file).start()
            it += 1

    class ConnectorFunctions(object):

        def __init__(self, meta_class) -> None:
            self.meta_class = meta_class
            self.upload_queue = Queue(maxsize=5)
            self.download_queue = Queue(maxsize=5)

        def get_filename(self, path: str):
            return Path(path).name

        def upload_file(self) -> None:
            filename: str = self.upload_queue.get()
            file_widget = QListWidgetItem(self.get_filename(filename))
            self.meta_class.uploading_files_status.addItem(file_widget)
            print("Uploading File '{}' !".format(filename))
            api.upload_file(filename)
            print("Finished Uploading File '{}' !".format(filename))
            self.upload_queue.task_done()
            self.meta_class.uploading_files_status.takeItem(self.meta_class.uploading_files_status.row(file_widget))

        def download_file(self) -> None:
            file_id, filename = self.download_queue.get()
            file_widget = QListWidgetItem(self.get_filename(filename))
            self.meta_class.downloading_files_status.addItem(file_widget)
            print("Downloading File '{}' !".format(filename))
            api.download_file(file_id)
            print("Finished Downloading File '{}' !".format(filename))
            self.download_queue.task_done()
            self.meta_class.downloading_files_status.takeItem(self.meta_class.downloading_files_status.row(file_widget))

        def get_files(self) -> None:
            self.meta_class.files_ar.clear() if not (self.meta_class.files_ar is None) else None
            self.meta_class.files_ar = api.get_all_files()
            self.meta_class.files.clear()
            items = []
            for file in self.meta_class.files_ar:
                wid = QTreeWidgetItem()
                wid.setText(0, file["filename"])
                wid.setCheckState(0, Qt.CheckState.Unchecked)
                items.append(wid)
            self.meta_class.files.addTopLevelItems(items)


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
        main_window.list_items()
    app.exec()
