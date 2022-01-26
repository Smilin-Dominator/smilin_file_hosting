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
from tkinter import Tk, filedialog, Button, LabelFrame, Label, Entry, END, Y, LEFT, RIGHT
from connector import API

root = Tk()
connector = API("", "")


# ------------------ Functions -----------------------------------#
def main_package():

    status_section.pack(side=RIGHT, fill=Y)
    upload.pack()
    uploading.pack(fill=Y, expand=True)
    downloading.pack(fill=Y, expand=True)

    files_section.pack(fill="both", side="top", expand=True)


def read_config():
    out = {}
    try:
        with open("credentials/config.json", "r") as r:
            out = loads(r.read())
        connector.set_url(out["url"])
        link.delete(0, END)
        link.insert(0, out["url"])
        connector.username = out["username"]
        username.delete(0, END)
        username.insert(0, out["username"])
        main_package()
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
    main_package()


def upload_file():
    fname = filedialog.askopenfilename(title="Select A File To Upload!")
    if fname in "." or "":
        pass
    else:
        connector.upload_file(fname)


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
