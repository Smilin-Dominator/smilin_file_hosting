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
from requests import get, post
from furl import furl
from cryptography import Crypto
from pathlib import Path
from binascii import hexlify, unhexlify


class API:

    def __init__(self, server: str, username: str):
        self.server = server
        self.username = username
        self.base_url = furl(server)
        self.base_url.path.segments = ["Devisha"]
        self.crypto = Crypto()
        self.files = Path("files")

    def get_all_files(self) -> list[dict]:
        url = self.base_url
        url.path.segments.append("list")
        url.path.segments.append("all")
        return get(url.tostr()).json()

    def download_file(self, filename: str):
        url = self.base_url
        url.path.segments.append("download")
        enc_filename = self.crypto.encrypt_string(filename)
        path_to_file = Path(self.files, filename)
        if not self.files.exists():
            self.files.mkdir()
        file = get(url.tostr(), params={"encrypted_filename": enc_filename}, stream=True)
        if file:
            with open(path_to_file, "wb") as d:
                d.write(file.content)
        else:
            print("No Such File!")

    def upload_file(self, filename: str):
        url = self.base_url
        url.path.segments.append("upload")
        enc_filename = self.crypto.encrypt_string(filename)
        post(url.tostr(), params={"encrypted_filename": enc_filename}, files={"file": open(filename, "rb")})


