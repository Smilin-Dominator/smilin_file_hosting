from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QLineEdit, QPushButton, QLabel
from sys import argv
from json import loads, dumps
from pathlib import Path
from connector import API
from cryptography import Crypto

# Main Variables
api = API("", "", "")
crypto = Crypto()
app = QApplication(argv)
credentials_window = uic.loadUi("credentials.ui")

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
    app.exec()
