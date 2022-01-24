from requests import get, post
from furl import furl
from shutil import copyfileobj


class API:

    def __init__(self, server: str, username: str):
        self.server = server
        self.username = username
        self.base_url = furl(server)
        self.base_url.path.segments = ["Devisha"]

    def get_all_files(self) -> list[dict]:
        url = self.base_url
        url.path.segments.append("list")
        url.path.segments.append("all")
        return get(url.tostr()).json()

    def download_file(self, filename: str):
        url = self.base_url
        url.path.segments.append("download")
        file = get(url.tostr(), params={"encrypted_filename": filename}, stream=True)
        with open("file.a", "wb") as d:
            d.write(file.content)

