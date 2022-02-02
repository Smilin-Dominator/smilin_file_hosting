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
from time import time_ns
from pathlib import Path
from rsa import newkeys, PrivateKey, PublicKey, encrypt, decrypt
from binascii import hexlify, unhexlify
from gnupg import GPG
from shutil import which


class Crypto:

    def __init__(self) -> None:
        self.pub = None
        self.priv = None
        self.email = None
        self.gpg = GPG
        self.files = Path("files")
        self.temp = Path("temp")

    def setup_gpg(self, email: str) -> None:
        self.gpg = GPG(gpgbinary=which("gpg"), gnupghome=str(Path(Path.home(), "AppData", "Roaming", "gnupg")))
        self.email = email

    def decrypt_string(self, string: bytes) -> str:
        return str(self.gpg.decrypt(string))

    def encrypt_string(self, string: str) -> bytes:
        return self.gpg.encrypt(string, recipients=[self.email])

    def encrypt_file(self, path: Path) -> Path:
        self.temp.mkdir() if not self.temp.exists() else None
        with open(path, "rb") as r:
            out = Path(self.temp, f"{path.name}_{str(time_ns())}")
            self.gpg.encrypt_file(file=r, recipients=[self.email], output=out)
        return out

    def decrypt_file(self, path: str, new_file: str) -> None:
        self.temp.mkdir() if not self.temp.exists() else None
        with open(path, "rb") as r:
            dec = self.gpg.decrypt_file(file=r, output=new_file, always_trust=True)
        Path(path).unlink()
