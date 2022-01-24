from pathlib import Path

from rsa import newkeys, PrivateKey, PublicKey, encrypt, decrypt


class Crypto:

    def __init__(self) -> None:
        self.pub = None
        self.priv = None

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
        text = decrypt(string, self.priv)
        return text.decode('utf-8')

    def encrypt_string(self, string: str) -> bytes:
        return encrypt(string.encode('utf-8'), self.pub)
