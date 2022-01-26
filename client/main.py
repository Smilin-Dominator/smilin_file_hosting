# main.py -> Main Script of the Client
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
from json import loads, dumps
from tkinter import Tk, filedialog, Button, LabelFrame, Label, Entry, END, Y, LEFT, RIGHT, Frame
from connector import API
from cryptography import Crypto
from functools import partial

root = Tk()
connector = API("", "")
crypto = Crypto()


# ------------------ Functions -----------------------------------#
def set_creds(out: dict):
    connector.set_username(out["username"])
    connector.set_url(out["url"])
    link.delete(0, END)
    link.insert(0, out["url"])
    username.delete(0, END)
    username.insert(0, out["username"])


def main_package():

    status_section.pack(side=RIGHT, fill=Y)
    upload.pack()
    uploading.pack(fill=Y, expand=True)
    downloading.pack(fill=Y, expand=True)

    files_section.pack(fill="both", side="top", expand=True)


def delete_file(id: int):
    connector.delete_file(id)
    list_items()


def download_file(id: int, filename: str):
    current_file = Label(downloading, text=filename)
    current_file.pack()
    connector.download_file(id)
    current_file.destroy()


def upload_file():
    fname = filedialog.askopenfilename(title="Select A File To Upload!")
    if fname in "." or "":
        pass
    else:
        current_file = Label(uploading, text=fname)
        current_file.pack()
        connector.upload_file(fname)
        current_file.destroy()
        list_items()


def list_items():
    items = connector.get_all_files()
    [child.destroy() for child in files_section.winfo_children()]
    for file in items:
        encrypted_filename: bytes = file["filename"]
        id: int = file["id"]
        filename: str = crypto.decrypt_string(encrypted_filename)
        container: Frame = Frame(files_section)
        label: Label = Label(container, text=filename)
        download: Button = Button(container, text="Download", command=partial(download_file, id, filename))
        delete: Button = Button(container, text="Delete", command=partial(delete_file, id))
        label.pack(side="left")
        download.pack(side="right")
        delete.pack(side="right")
        container.pack(fill="x")


def read_config():
    out = {}
    try:
        with open("credentials/config.json", "r") as r:
            out = loads(r.read())
        set_creds(out)
        main_package()
        list_items()
    except FileNotFoundError:
        pass
    except KeyError:
        pass


def write_config():
    user = username.get()
    url = link.get()
    out = {
        "username": user,
        "url": url
    }
    with open("credentials/config.json", "w") as w:
        w.write(dumps(out, indent=4))
        w.flush()
        w.close()
    set_creds(out)
    main_package()
    list_items()


# ---------------------- Elements --------------------------------------------#

# The Status Section
status_section = LabelFrame(root, text="Status")
downloading = LabelFrame(status_section, text="Downloading")
uploading = LabelFrame(status_section, text="Uploading")

# The Upload Button
upload = Button(status_section, command=upload_file, text="Upload File")

# The Credentials Section
credentials_section = LabelFrame(root, text="Credentials")
username = Entry(credentials_section)
username.insert(0, "Username")
link = Entry(credentials_section)
link.insert(0, "Link")
save_creds = Button(credentials_section, text="Connect", command=write_config)

# The Files Section
files_section = LabelFrame(root, text="Files")


# --------------- Program ----------------------------#
if __name__ == "__main__":
    root.geometry("800x500")

    credentials_section.pack(side=LEFT, fill=Y)
    username.pack()
    link.pack()
    save_creds.pack()

    read_config()

    root.mainloop()
