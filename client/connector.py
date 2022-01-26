# connector.py -> Interacts with the API to get the files
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
from copy import deepcopy
from pathlib import Path
from furl import furl
from requests import get, post
from cryptography import Crypto


class API:

    def __init__(self, server: str, username: str):
        self.server = server
        self.username = username
        self.base_url = furl(server)
        self.base_url.path.segments = ["Devisha"]
        self.crypto = Crypto()
        self.files = Path("files")

    def get_all_files(self) -> list[dict]:
        url = deepcopy(self.base_url)
        url.path.segments.append("list")
        url.path.segments.append("all")
        return get(url.tostr()).json()

    def download_file(self, id: int):
        url = deepcopy(self.base_url)
        url.path.segments.append("download")
        if not self.files.exists():
            self.files.mkdir()
        file = get(url.tostr(), params={"id": id}, stream=True)
        if file.content == b'False':
            filename = file.headers.get("Content-Disposition")[29:]
            path_to_file = Path(self.files, self.crypto.decrypt_string(filename))
            with open(path_to_file, "wb") as d:
                d.write(file.content)
        else:
            print("No Such File!")

    def upload_file(self, filename: str):
        url = deepcopy(self.base_url)
        url.path.segments.append("upload")
        path_to_file = Path(filename)
        real_filename = path_to_file.name
        enc_filename = self.crypto.encrypt_string(real_filename)
        post(url.tostr(), params={"encrypted_filename": enc_filename}, files={"file": open(path_to_file, "rb")})
