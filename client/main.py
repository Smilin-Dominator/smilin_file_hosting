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
from tkinter import Tk, filedialog, Button, LabelFrame, Label, Entry, END, LEFT, RIGHT, Frame
from connector import API
from cryptography import Crypto
from functools import partial
from threading import Thread, RLock
from pathlib import Path
from queue import Queue
from time import sleep

root = Tk()
connector = API("", "")
crypto = Crypto()
download_queue = Queue(maxsize=5)
upload_queue = Queue(maxsize=5)
delete_queue = Queue(maxsize=20)
refresh_lock = RLock()


# ------------------ Proxies -----------------------------------#
def upload_proxy():
    fnames = filedialog.askopenfilenames(title="Select A File To Upload!")
    for filename in fnames:
        if "" or "." == filename:
            continue
        else:
            upload_queue.put(filename)
            Thread(target=upload_file, daemon=True).start()


def refresh_proxy():
    Thread(target=list_items, daemon=True).start()


def delete_proxy(id: int):
    delete_queue.put(id)
    Thread(target=delete_file).start()


def download_proxy(id: int, filename: str):
    download_queue.put((id, filename))
    Thread(target=download_file, daemon=True).start()

# ------------------ Functions -----------------------------------#


def set_creds(out: dict):
    connector.set_username(out["username"])
    connector.set_url(out["url"])
    link.delete(0, END)
    link.insert(0, out["url"])
    username.delete(0, END)
    username.insert(0, out["username"])


def main_package():

    status_section.pack(side=RIGHT, fill="y")
    refresh.pack()
    upload.pack()
    uploading.pack(fill="both", expand=True)
    downloading.pack(fill="both", expand=True)

    files_section.pack(fill="both", side="top", expand=True)


def delete_file():
    id = delete_queue.get()
    connector.delete_file(id)
    list_items()


def download_file():
    id, filename = download_queue.get()
    current_file = Label(downloading, text=filename)
    current_file.pack()
    print(f"Downloading: {filename}")
    connector.download_file(id)
    current_file.destroy()
    download_queue.task_done()


def upload_file():
    fname = upload_queue.get()
    raw_filename = Path(fname).name
    current_file = Label(uploading, text=raw_filename, justify="left")
    current_file.pack(fill="x")
    print(f"Uploading: {raw_filename}")
    connector.upload_file(fname)
    current_file.destroy()
    list_items()
    upload_queue.task_done()


def list_items():
    refresh_lock.acquire()
    items = connector.get_all_files()
    [child.destroy() for child in files_section.winfo_children()]
    for file in items:
        encrypted_filename: bytes = file["filename"]
        id: int = file["id"]
        filename: str = crypto.decrypt_string(encrypted_filename)
        container: Frame = Frame(files_section)
        label: Label = Label(container, text=filename)
        download: Button = Button(container, text="Download", command=partial(download_proxy, id, filename))
        delete: Button = Button(container, text="Delete", command=partial(delete_proxy, id))
        label.pack(side="left")
        download.pack(side="right")
        delete.pack(side="right")
        container.pack(fill="x")
    sleep(0.3499)
    refresh_lock.release()


def read_config():
    out = {}
    try:
        with open("credentials/config.json", "r") as r:
            out = loads(r.read())
        set_creds(out)
        main_package()
        refresh_proxy()
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
    refresh_proxy()


# ---------------------- Elements --------------------------------------------#

# The Status Section
status_section = LabelFrame(root, text="Status")
downloading = LabelFrame(status_section, text="Downloading")
uploading = LabelFrame(status_section, text="Uploading")

# The Control Buttons
refresh = Button(status_section, command=refresh_proxy, text="Refresh")
upload = Button(status_section, command=upload_proxy, text="Upload File")

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
    root.geometry("1000x700")

    credentials_section.pack(side=LEFT, fill="y")
    username.pack()
    link.pack()
    save_creds.pack()

    read_config()

    root.mainloop()
