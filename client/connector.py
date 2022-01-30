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
from requests import get, post, delete, ConnectionError
from cryptography import Crypto


class API:

    def __init__(self, server: str, username: str, email: str):
        self.server = server
        self.username = username
        self.base_url = furl(server)
        self.base_url.path.segments = [username]
        self.crypto = Crypto()
        self.files = Path("files")
        self.temp = Path("temp")

    def setup_crypto(self, email: str):
        self.crypto.setup_gpg(email)

    def test_connection(self) -> bool:
        try:
            req = get(self.base_url.tostr())
            if (req.status_code == 404) or (req.content == b"false"):
                print(f"[*] Connection Failed To URL: '{self.base_url.tostr()}'")
                return False
            else:
                print(f"[*] Connection Succeeded to URL: '{self.base_url.tostr()}'")
                return True
        except ConnectionError:
            print(f"[*] Connection Failed To URL: '{self.base_url.tostr()}'")
            return False

    def set_username(self, user: str):
        self.username = user

    def set_url(self, url: str):
        self.base_url = furl(url)
        self.base_url.path.segments = [self.username]

    def get_all_files(self) -> list[dict]:
        url = deepcopy(self.base_url)
        url.path.segments.append("list")
        the_files = get(url.tostr()).json()
        for file in the_files:
            file["filename"] = self.crypto.decrypt_string(file["filename"])
        return the_files

    def download_file(self, id: int):
        url = deepcopy(self.base_url)
        url.path.segments.append("download")
        if not self.files.exists():
            self.files.mkdir()
        file = get(url.tostr(), params={"id": id}, stream=True)
        if file.content != b'false':
            filename = file.headers.get("Content-Disposition")[29:]
            decrypted_filename = self.crypto.decrypt_string(filename)
            path_to_temp_file = Path(self.temp, "".join([decrypted_filename, ".gpg"]))
            path_to_file = Path(self.files, decrypted_filename)
            with open(path_to_temp_file, "wb") as d:
                d.write(file.content)
            self.crypto.decrypt_file(str(path_to_temp_file), str(path_to_file))
        else:
            print("No Such File!")

    def delete_file(self, id: int):
        url = deepcopy(self.base_url)
        url.path.segments.append("delete")
        file = delete(url.tostr(), params={"id": id})
        if not file.content == b'false':
            print("Success!")
        else:
            print("Didn't Work!")

    def upload_file(self, filename: str):
        url = deepcopy(self.base_url)
        url.path.segments.append("upload")
        path_to_file = Path(filename)
        enc_path = self.crypto.encrypt_file(path_to_file)
        real_filename = path_to_file.name
        enc_filename = self.crypto.encrypt_string(real_filename)
        post(url.tostr(), params={"encrypted_filename": enc_filename}, files={"file": open(enc_path, "rb")})
        enc_path.unlink()
