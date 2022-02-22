# cryptography.py -> Manages all the encryption and decryption
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
from pathlib import Path
from shutil import which
from time import time_ns
from gnupg import GPG
from platform import system
from Crypto.Cipher import AES


class Crypto:
    """ This class performs all the cryptographic operations. """

    def __init__(self) -> None:
        """ This initiates the paths 'files' and 'temp' """
        self.email = None
        self.gpg = GPG
        self.files = Path("files")
        self.temp = Path("temp")
        self.key: bytes = b""

    def setup_gpg(self, email: str) -> None:
        """
        This accepts the GPG User's Email and sets up the GPG instance with the GPG Home Directory

        :param email: The Email attached to the user's key
        """
        gpg_home = ""
        match system():
            case "Windows":
                gpg_home = str(Path(Path.home(), "AppData", "Roaming", "gnupg"))
            case _:
                gpg_home = str(Path(Path.home(), ".gnupg"))
        self.gpg = GPG(gpgbinary=which("gpg"), gnupghome=gpg_home)
        self.email = email

    def decrypt_string(self, string: bytes, iv: bytes) -> str:
        """
        This accepts a binary and returns a decrypted string

        :param iv: The initialization vector
        :param string: The bytes
        :return: The decrypted output
        """
        cipher = AES.new(self.key, AES.MODE_CFB, iv=iv)
        return cipher.decrypt(string).decode('utf-8')

    def encrypt_string(self, string: str, iv: bytes = None) -> bytes | tuple[bytes, bytes]:
        """
        This accepts a string and returns an encrypted binary

        :param string: The string to encrypt
        :param iv: The Initialization Vector
        :return: The encrypted output and the initialization vector
        """
        encoded = string.encode('utf-8')
        if iv is not None:
            cipher = AES.new(self.key, AES.MODE_CFB, iv=iv)
            return cipher.encrypt(encoded)
        else:
            cipher = AES.new(self.key, AES.MODE_CFB)
            return cipher.encrypt(encoded), cipher.iv

    def encrypt_file(self, path: Path) -> Path:
        """
        This accepts an absolute path to a file, encrypts it and returns the Patg of the encrypted
        file stored in 'temp'

        :param path: The path to the file to encrypt
        :return: The path to the encrypted file in 'temp'
        """
        self.temp.mkdir() if not self.temp.exists() else None
        with open(path, "rb") as r:
            out = Path(self.temp, f"{path.name}_{str(time_ns())}")
            self.gpg.encrypt_file(file=r, recipients=[self.email], output=out)
        return out

    def decrypt_file(self, path: str, new_file: str) -> None:
        """
        This decrypts the file, writes it to the specified path and deletes the encrypted file.

        :param path: Absolute path to the file that should be decrypted
        :param new_file: The output filename
        """
        self.temp.mkdir() if not self.temp.exists() else None
        with open(path, "rb") as r:
            dec = self.gpg.decrypt_file(file=r, output=new_file, always_trust=True)
        Path(path).unlink()
