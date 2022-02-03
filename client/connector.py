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
    """
    This class is the bridge between the Main User Interface, Cryptography and the Server.
    This handles all the server interaction, such as Uploading, Downloading and Deleting.
    """

    def __init__(self, server: str, username: str, crypto: Crypto):
        """
        The constructor accepts a Server (URL), a username and an instance of the Crypto class

        :param server: The URL to the Server
        :param username: The username/token obtained from registering
        :param crypto: An instance of the Crypto class
        """
        self.server = server
        self.username = username
        self.base_url = furl(server)
        self.base_url.path.segments = [username]
        self.crypto = crypto
        self.files = Path("files")
        self.temp = Path("temp")

    def test_connection(self) -> bool:
        """
        This tests the connection and returns False if it can't connect, and true if it can.

        :return: Whether it connected or not
        """
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
        """
        A simple setter function to set the username

        :param user: The Username/Token
        """
        self.username = user

    def set_url(self, url: str):
        """
        This takes a string URL and converts it into a 'furl' object and appends the username to it

        :param url: The link as a string
        """
        self.base_url = furl(url)
        self.base_url.path.segments = [self.username]

    def get_all_files(self) -> list[dict]:
        """
        This connects to the server '/list' and returns the list of files

        :return: Files as a list of dictionaries
        """
        url = deepcopy(self.base_url)
        url.path.segments.append("list")
        the_array = get(url.tostr()).json()
        return the_array

    def register(self, link: str) -> str:
        """
        This connects to the server and gets you a registration token

        :param link: The URL to connect to
        :return: The token obtained from registering
        """
        url = furl(link)
        url.path.segments.append("register")
        req: str = post(url.tostr()).json()
        self.set_username(req)
        self.set_url(link)
        return req

    def download_file(self, id: int, filename: str):
        """
        This accepts a filename and an id and downloads the file. It sends a request with the ID,
        saves the raw downloaded file as a GPG file (in temp), decrypts it and saves it to 'files/'

        :param id: The ID of the file
        :param filename: The decrypted filename
        """
        url = deepcopy(self.base_url)
        url.path.segments.append("download")
        if not self.files.exists():
            self.files.mkdir()
        file = get(url.tostr(), params={"id": id}, stream=True)
        if file.content != b'false':
            path_to_temp_file = Path(self.temp, "".join([filename, ".gpg"]))
            path_to_file = Path(self.files, filename)
            with open(path_to_temp_file, "wb") as d:
                d.write(file.content)
            self.crypto.decrypt_file(str(path_to_temp_file), str(path_to_file))
        else:
            print("No Such File!")

    def delete_file(self, id: int):
        """
        This launches a delete request to the server with the ID of the file

        :param id: The ID of the File to delete
        """
        url = deepcopy(self.base_url)
        url.path.segments.append("delete")
        file = delete(url.tostr(), params={"id": id})
        if not file.content == b'false':
            print("Success!")
        else:
            print("Didn't Work!")

    def upload_file(self, filename: str):
        """
        THis takes a file, encrypts it and it's filename and uploads it

        :param filename: The absolute path to the file
        """
        url = deepcopy(self.base_url)
        url.path.segments.append("upload")
        path_to_file = Path(filename)
        enc_path = self.crypto.encrypt_file(path_to_file)
        real_filename = path_to_file.name
        enc_filename = self.crypto.encrypt_string(real_filename)
        post(url.tostr(), params={"encrypted_filename": enc_filename}, files={"file": open(enc_path, "rb")})
        enc_path.unlink()
