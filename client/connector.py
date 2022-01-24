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
from requests import get, post
from furl import furl
from shutil import copyfileobj
from pathlib import Path


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

