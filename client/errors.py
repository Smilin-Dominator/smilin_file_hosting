class SetKeyError(Exception):

    def __init__(self, key: str):
        super().__init__("Error while un-hexlifying Key '{}' of length '{}'".format(key, len(key)))


class DecryptionError(Exception):

    def __init__(self):
        super(DecryptionError, self).__init__(
            """
            Received Data but wasn't able to decrypt it.
            This is probably because the key you're using right now isn't the same key used to encrypt the files.
            """
        )
