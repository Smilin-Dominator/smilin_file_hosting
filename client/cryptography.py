from rsa import newkeys, PrivateKey, PublicKey
from pathlib import Path


def create_new_keys():
    pub, priv = newkeys(4096)
    Path("credetials").mkdir()
    with open("./credentials/public.pem", "w") as w:
        key_string = pub.save_pkcs1()
        w.write(key_string.decode('utf-8'))
    with open("./credentials/private.pem", "w") as w:
        key_string = priv.save_pkcs1()
        w.write(key_string.decode('utf-8'))
