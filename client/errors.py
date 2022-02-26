class SetKeyError(Exception):

    def __init__(self, key: str):
        super().__init__("Error while un-hexlifying Key '{}' of length '{}'".format(key, len(key)))
