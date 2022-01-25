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

from rsa import newkeys, PrivateKey, PublicKey, encrypt, decrypt
from binascii import hexlify, unhexlify


class Crypto:

    def __init__(self) -> None:
        self.pub = None
        self.priv = None
        self.get_keys()

    def get_keys(self) -> None:
        pubExists = Path("credentials/public.pem").exists()
        priExists = Path("credentials/private.pem").exists()
        if not (pubExists or priExists):
            self.create_new_keys()
        else:
            self.load_existing_keys()

    def create_new_keys(self) -> None:
        pub, priv = newkeys(4096)
        Path("credentials").mkdir()
        with open("./credentials/public.pem", "w+") as w:
            key_string = pub.save_pkcs1()
            w.write(key_string.decode('utf-8'))
        with open("./credentials/private.pem", "w+") as w:
            key_string = priv.save_pkcs1()
            w.write(key_string.decode('utf-8'))
        self.priv = priv
        self.pub = pub

    def load_existing_keys(self) -> None:
        with open("./credentials/private.pem", "rb") as r:
            self.priv = PrivateKey.load_pkcs1(r.read())
        with open("./credentials/public.pem", "rb") as r:
            self.pub = PublicKey.load_pkcs1(r.read())

    def decrypt_string(self, string: bytes) -> str:
        text = decrypt(unhexlify(string), self.priv)
        return text.decode('utf-8')

    def encrypt_string(self, string: str) -> bytes:
        return hexlify(encrypt(string.encode('utf-8'), self.pub))
