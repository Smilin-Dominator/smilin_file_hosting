# main.py -> The main user interface!
"""
    Smilin' File Hosting - Hosting Files With A Smile
    Copyright (C) 2022 Devisha Padmaperuma

    Smilin' File Hosting is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as
    published by the Free Software Foundation, either version 3 of the
    License, or (at your option) any later version.

    Smilin' File Hosting is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
from time import time
from json import loads, dumps
from pathlib import Path
from sys import argv
from threading import Thread, Lock
from concurrent.futures import ThreadPoolExecutor
from binascii import unhexlify

from PyQt6 import uic
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication, QLineEdit, QPushButton, QLabel, QMainWindow, QListWidgetItem, QFileDialog,
    QListWidget, QTreeWidget, QTreeWidgetItem, QTreeWidgetItemIterator, QSpinBox
)

from connector import API
from cryptography import Crypto


class CredentialsUI(QMainWindow):
    """
    This class is used to check the Validity of your credentials. If they're valid, you'll go straight
    to the main UI. If the file doesn't exist or there's a missing field or the connection fails, it'll
    display this window.
    """

    def __init__(self):
        """
        This loads a .ui file called "credentials.ui" (Which was designed with QtCreator) and expands it. I've
        pre-declared the Variables before loading the file for convenience.
        """

        # Declaration
        self.token_input: QLineEdit = None
        self.link_input: QLineEdit = None
        self.key_input: QLineEdit = None
        self.register_button: QPushButton = None
        self.connect_button: QPushButton = None
        self.credentials_status: QLabel = None
        self.concurrent_downloads: QSpinBox = None
        self.concurrent_uploads: QSpinBox = None
        self.downloaded_files_folder: QLineEdit = None
        self.temp_folder: QLineEdit = None
        self.file_chooser = QFileDialog()

        # Initial
        super(CredentialsUI, self).__init__()
        uic.loadUi("credentials.ui", self)
        self.setWindowTitle("Smilin' File Client - Credentials")

        # Post Initial
        self.connect_button.clicked.connect(self.credentials_connect)
        self.register_button.clicked.connect(self.import_options)

    def safe_show(self, path: Path = None):
        """
        This parses the credential file and looks for the options. If the file doens't exist, this does
        not happen, but if it does exist, it'll write the values in the config file to the respective
        input in this window.
        """
        if path is None:
            config_file = Path("credentials/config.json")
        else:
            config_file = path
        if config_file.exists():
            js: dict = loads(open(config_file, "r").read())
            self.token_input.setText(js.get("token"))
            self.link_input.setText(js.get("link"))
            self.key_input.setText(js.get("key"))
            if js.get("advanced") is not None:
                self.concurrent_downloads.setValue(js.get("advanced").get("concurrent_downloads"))
                self.concurrent_uploads.setValue(js.get("advanced").get("concurrent_uploads"))
            if js.get("directories") is not None:
                self.downloaded_files_folder.setText(js.get("directories").get("downloaded_files_folder"))
                self.temp_folder.setText(js.get("directories").get("temp_folder"))
        self.show()

    def import_options(self):
        """
        This imports all the options from a file and displays it
        """
        fn = self.file_chooser.getOpenFileName(self, "Import File", "config", "JSON Files (*.json)")[0]
        self.safe_show(Path(fn))

    def export_options(self):
        """
        This gets all the current options and exports it to a filename of your choice
        """
        filename = self.file_chooser.getSaveFileName(self, "Save File", "config", "JSON Files (*.json)")[0]
        with open(filename, "w+") as w:
            w.write(dumps(self.get_options(), indent=4))
            w.close()

    def get_options(self) -> dict:
        """
        This parses the entry fields and returns a dictionary object

        :return: The credentials in a JSON format
        """
        return {
            "token": self.token_input.text(),
            "link": self.link_input.text(),
            "key": self.key_input.text(),
            "advanced": {
                "concurrent_downloads": self.concurrent_downloads.value(),
                "concurrent_uploads": self.concurrent_uploads.value()
            },
            "directories": {
                "downloaded_files_folder": self.downloaded_files_folder.text(),
                "temp_folder": self.temp_folder.text()
            }
        }

    def credentials_connect(self) -> None:
        """
        This checks if all 3 Input Fields are filled;

        - If they are, it writes to the file ('credentials/config.json').
        - If they aren't, it sets the status to "Not Enough Arguments!"
        """
        get = self.get_options()
        text = [get["token"], get["link"], get["key"], get["directories"]["downloaded_files_folder"], get["directories"]["temp_folder"]]
        check = [i for i in text if i != ""]
        if len(check) != 5:
            self.credentials_status.setText("Not Enough Arguments!")
        else:
            self.write_file(get)

    def credentials_register(self) -> None:
        """
        This checks if the link entry is filled and registers you.
        By registering, I mean, it sends a GET request to 'url/register', which
        returns a unique UUID token, which you will use to connect. Note that if you
        lose this token, you won't be able to get your files!
        """
        global crypto
        if self.link_input.text() == "":
            self.credentials_status.setText("Link Is Empty!")
        else:
            token = api.register(self.link_input.text())
            self.key_input.setText(crypto.generate_key())
            self.credentials_status.setText("Successfully Registered!")
            self.token_input.setText(token)

    def write_file(self, options: dict) -> None:
        """
        This accepts the credential parameters and writes to the file

        :param options: A dictionary in the format returned by `self.get_options()`

        If the connection fails, it'll re-display the credentials dialog. Otherwise, it'll setup the API and launch
        the main user interface.
        """
        global main_window, api
        creds = Path("credentials")
        creds.mkdir() if not creds.exists() else None
        with open("credentials/config.json", "w") as w:
            w.write(dumps(options, indent=4))
            w.flush()
            w.close()
        download_dir = Path(options["directories"]["temp_folder"])
        temp_dir = Path(options["directories"]["temp_folder"])
        api = API(server=options["link"], username=options["token"], crypto=crypto, download_dir=download_dir, temp_dir=temp_dir)
        if not api.test_connection():
            self.credentials_status.setText("Connection Failed!")
            self.show()
        else:
            crypto.files = download_dir
            crypto.temp = temp_dir
            crypto.set_key(options["key"])
            self.close()
            main_window.show()
            main_window.list_items()

    def read_file(self) -> bool:
        """
        This reads the options of the config.json file. If the connection succeeds, it'll setup the API and take
        you to the Main User Interface. Otherwise, it'll redisplay the credentials dialog.

        :returns: True if the credentials are valid and the connection Succeeds. False if; The Connection Fails,
            The file doesn't exist or there's a missing option
        """
        global api, main_window
        try:
            with open("credentials/config.json", "r") as r:
                js = loads(r.read())
                download_dir = Path(js["directories"]["downloaded_files_folder"])
                temp_dir = Path(js["directories"]["temp_folder"])
                api = API(server=js["link"], username=js["token"], crypto=crypto, download_dir=download_dir, temp_dir=temp_dir)
                if not api.test_connection():
                    self.credentials_status.setText("Connection Failed!")
                    return False
                crypto.set_key(js["key"])
                crypto.files = download_dir
                crypto.temp = temp_dir
                main_window.MAX_CONCURRENT_UPLOADS = js["advanced"]["concurrent_uploads"]
                main_window.MAX_CONCURRENT_DOWNLOADS = js["advanced"]["concurrent_downloads"]
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
    """
    This is the main user interface of the program. All the operations are done here.
    """

    def __init__(self):
        """
        It loads a UI file called 'main.ui' which was designed in QtCreator. I've pre-declared
        the variables for convenience.
        """

        # Declaration
        self.MAX_CONCURRENT_DOWNLOADS = 1
        self.MAX_CONCURRENT_UPLOADS = 1

        self.files: QTreeWidget = None
        self.files_ar: list[dict] = None
        self.refresh_lock = Lock()

        self.status_bar: QLabel = None
        self.downloading_files_status: QListWidget = QListWidget()
        self.uploading_files_status: QListWidget = QListWidget()

        self.download_selected: QPushButton = None
        self.delete_selected: QPushButton = None
        self.change_credentials_button: QPushButton = None
        self.upload_files_button: QPushButton = None
        self.refresh_button: QPushButton = None

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
        self.delete_selected.clicked.connect(self.delete_files)
        self.refresh_button.clicked.connect(self.list_items)

    def list_items(self) -> None:
        """
        Checks if the refresh queue is full. If it's not, it starts a new thread to start refreshing
        """

        def refresh():
            self.refresh_lock.acquire()
            t = Thread(target=self.ops.get_files)
            t.start()
            t.join()
            self.refresh_lock.release()

        if not self.refresh_lock.locked():
            Thread(target=refresh).start()

    def change_credentials(self) -> None:
        """
        This closes the current window and opens the credentials window. There's no need to re-open this
        window as it gets re-opened when you write the credentials.
        """
        self.close()
        credentials_window.safe_show()

    def upload_file(self) -> None:
        """
        This gets filenames from the file-opening dialog, adds them to the upload queue and starts new Threads to
         upload each file.
        """
        def do_upload():
            with ThreadPoolExecutor(max_workers=self.MAX_CONCURRENT_UPLOADS) as exe:
                exe.map(self.ops.upload_file, files)

        files = self.file_opener.getOpenFileNames()[0]
        Thread(name="Feed_Upload", target=do_upload).start()

    def download_files(self):
        """
        This gets all the Checked Items, adds them to the download queue and starts new Threads to download
        each file.
        """
        def do_download():
            it = QTreeWidgetItemIterator(self.files, QTreeWidgetItemIterator.IteratorFlag.Checked)
            fs: list[tuple[int, str]] = []
            while it.value():
                item = it.value()
                filename = item.text(0)
                id = self.ops.get_id(filename)
                fs.append((id, filename))
                it += 1
            with ThreadPoolExecutor(max_workers=self.MAX_CONCURRENT_DOWNLOADS) as exe:
                exe.map(self.ops.download_file, fs)

        Thread(name="Feed_Download", target=do_download).start()

    def delete_files(self):
        """
        This gets all the checked items, adds them to the delete queue and starts new Threads to delete each file.
        """
        def do_delete():
            it = QTreeWidgetItemIterator(self.files, QTreeWidgetItemIterator.IteratorFlag.Checked)
            ids = []
            while it.value():
                item = it.value()
                ids.append(self.ops.get_id(item.text(0)))
                it += 1
            with ThreadPoolExecutor(max_workers=4) as exe:
                exe.map(self.ops.delete_file, ids)

        Thread(name="Feed_Delete", target=do_delete).start()

    class ConnectorFunctions(object):
        """
        This Class was built to support its parent class (MainUI). All the functions in the parent class are the
        plural version of the functions in this class. That's because this is the class that does all the operations
        and the parent class launches a Thread(s) when performing any of the below functions. There's alot of
        interaction between this class and the parent class.
        """

        def __init__(self, meta_class) -> None:
            """
            This is the constructor of the operations class. It contains the parent class instance along with
            queues for downloading, uploading, deleting and refreshing.

            :param meta_class: The instance of the parent class
            """
            self.meta_class = meta_class

        def get_id(self, filename: str) -> int:
            """
            Iterates through the file array until it finds the ID that matches the filename

            :param filename: The filename you're looking for
            :return: The ID of the Filename
            """
            for el in self.meta_class.files_ar:
                if el.get("filename") == filename:
                    return el.get("id")

        def get_filename(self, path: str) -> str:
            """
            This accepts a path and returns the filename

            :param path: The Absolute / Relative Path
            :return: The Filename
            """
            return Path(path).name

        def delete_file(self, id: int) -> None:
            """
            This gets an ID of a File from the queue and deletes it

             :param id: The ID of the File
             """
            api.delete_file(id)
            self.meta_class.list_items()

        def upload_file(self, filename: str) -> None:
            """
            This gets a path to a file from the queue, adds the filename to the uploading_files status,
            uploads it and refreshes the file list.

            :param filename: The absolute path to the file
            """
            file_widget = QListWidgetItem(self.get_filename(filename))
            self.meta_class.uploading_files_status.addItem(file_widget)
            print("Uploading File '{}' !".format(filename))
            api.upload_file(filename)
            print("Finished Uploading File '{}' !".format(filename))
            self.meta_class.list_items()
            self.meta_class.uploading_files_status.takeItem(self.meta_class.uploading_files_status.row(file_widget))

        def download_file(self, container: tuple[int, str]) -> None:
            """
            This gets an ID and a Filename from the queue, adds the filename to the download_files status and
            downloads the file

            :param container: A Tuple that contains an ID and a Filename
            """
            file_id, filename = container
            file_widget = QListWidgetItem(self.get_filename(filename))
            self.meta_class.downloading_files_status.addItem(file_widget)
            print("Downloading File '{}' !".format(filename))
            api.download_file(file_id, filename)
            print("Finished Downloading File '{}' !".format(filename))
            self.meta_class.downloading_files_status.takeItem(self.meta_class.downloading_files_status.row(file_widget))

        def get_files(self) -> None:
            """ This clears all the entries in the files section and refreshes the list """

            def insert_element(file: dict):
                wid = QTreeWidgetItem()
                decrypted_name = crypto.decrypt_string(unhexlify(file["filename"]), unhexlify(file["iv"]))
                file["filename"] = decrypted_name
                wid.setText(0, decrypted_name)
                wid.setCheckState(0, Qt.CheckState.Unchecked)
                self.meta_class.files.addTopLevelItem(wid)

            self.meta_class.files_ar.clear() if not (self.meta_class.files_ar is None) else None
            self.meta_class.files_ar = api.get_all_files()
            self.meta_class.files.clear()

            t = time()
            with ThreadPoolExecutor(max_workers=4) as exe:
                exe.map(insert_element, self.meta_class.files_ar)
            print("Took '{}' Seconds To Decrypt All Elements!".format(time() - t))


# Main Variables

crypto = Crypto(None, None)
api = API("", "", crypto, None, None)
app = QApplication(argv)

credentials_window = CredentialsUI()
main_window = MainUI()

if __name__ == "__main__":
    options = credentials_window.read_file()
    if not options:
        credentials_window.safe_show()
    app.exec()
