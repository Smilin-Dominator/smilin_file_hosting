from rsa import newkeys, PrivateKey, PublicKey
from pathlib import Path


class Crypto:

    def __init__(self):
        self.pub = PublicKey
        self.priv = PrivateKey

    def create_new_keys(self):
        pub, priv = newkeys(4096)
        Path("credetials").mkdir()
        with open("./credentials/public.pem", "w") as w:
            key_string = pub.save_pkcs1()
            w.write(key_string.decode('utf-8'))
        with open("./credentials/private.pem", "w") as w:
            key_string = priv.save_pkcs1()
            w.write(key_string.decode('utf-8'))
        self.priv = priv
        self.pub = pub

    def load_existing_keys(self):
        with open("./credentials/public.pem", "wb") as r:
            self.priv = PrivateKey.load_pkcs1(r.read())
        with open("./credentials/private.pem", "wb") as r:
            self.pub = PublicKey.load_pkcs1(r.read())
