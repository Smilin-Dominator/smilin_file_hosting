from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QLineEdit, QPushButton
from sys import argv
from json import loads, dumps
from pathlib import Path

# Main Variables
app = QApplication(argv)
credentials_window = uic.loadUi("credentials.ui")

# Credentials Variables (Necessary)
token_input: QLineEdit = credentials_window.token_input
link_input: QLineEdit = credentials_window.link_input
email_input: QLineEdit = credentials_window.email_input
register_button: QPushButton = credentials_window.register_button
connect_button: QPushButton = credentials_window.connect_button


# ------------ Config File ------------------- #
def write_file(token: str, link: str, email: str) -> dict[str, str]:
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
    credentials_window.close()
    return out


def read_file() -> dict[str, str] or bool:
    try:
        with open("credentials/config.json", "r") as r:
            return loads(r.read())
    except FileNotFoundError:
        return False


if __name__ == "__main__":
    options = read_file()
    if not options:
        credentials_window.show()
    app.exec()
