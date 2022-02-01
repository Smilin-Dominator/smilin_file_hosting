from json import loads, dumps
from pathlib import Path
from sys import argv

from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QLineEdit, QPushButton, QLabel, QScrollArea, QVBoxLayout, QMainWindow, QWidget, QGroupBox

from connector import API
from cryptography import Crypto


class MainUI(QMainWindow):

    def __init__(self):

        # Declaration
        self.file_container: QScrollArea = None
        self.files_layout: QVBoxLayout = QVBoxLayout()
        self.files_section: QWidget = None
        self.downloading_files_status: QGroupBox = None
        self.uploading_files_status: QGroupBox = None
        self.change_credentials_button:  QPushButton = None
        self.upload_files_button: QPushButton = None

        # Initial
        super().__init__()
        uic.loadUi("main.ui", self)
        self.setWindowTitle("Smilin' File Client")

        # Post Initial
        self.change_credentials_button.clicked.connect(self.change_credentials)
        self.upload_files_button.clicked.connect(self.upload_file)

    def change_credentials(self):
        self.close()
        credentials_window.show()

    def upload_file(self):
        pass


# Main Variables

api = API("", "", "")
crypto = Crypto()
app = QApplication(argv)

credentials_window = uic.loadUi("credentials.ui")
main_window = MainUI()

# Credentials Variables (Necessary)
token_input: QLineEdit = credentials_window.token_input
link_input: QLineEdit = credentials_window.link_input
email_input: QLineEdit = credentials_window.email_input
register_button: QPushButton = credentials_window.register_button
connect_button: QPushButton = credentials_window.connect_button
credentials_status: QLabel = credentials_window.credentials_status


# ------ Credentials Functions -------------------- #

def credentials_connect():
    text = [token_input.text(), link_input.text(), email_input.text()]
    check = [i for i in text if i != ""]
    if len(check) != 3:
        credentials_status.setText("Not Enough Arguments!")
    else:
        write_file(*text)


def credentials_register():
    if link_input.text() == "":
        credentials_status.setText("Link Is Empty!")
    else:
        token = api.register(link_input.text())
        credentials_status.setText("Successfully Registered!")
        token_input.setText(token)


connect_button.clicked.connect(credentials_connect)
register_button.clicked.connect(credentials_register)


# ------------ Config File ------------------- #
def write_file(token: str, link: str, email: str) -> None:
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
        credentials_status.setText("Connection Failed!")
        credentials_window.show()
    else:
        crypto.setup_gpg(email)
        credentials_window.close()
        main_window.show()


def read_file() -> bool:
    global api
    try:
        with open("credentials/config.json", "r") as r:
            js = loads(r.read())
            api = API(server=js["link"], username=js["token"], email=js["email"])
            if not api.test_connection():
                credentials_status.setText("Connection Failed!")
                return False
            crypto.setup_gpg(js["email"])
            main_window.show()
            return True
    except FileNotFoundError:
        credentials_status.setText("File Not Found!")
        return False
    except KeyError:
        credentials_status.setText("Not Enough Options!")
        return False


if __name__ == "__main__":
    options = read_file()
    if not options:
        credentials_window.show()
    else:
        main_window.show()
    app.exec()
