# formats.py -> Stores the PyDantic Base Models
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
from pydantic import BaseModel
from sqlalchemy import Table, MetaData, Column, Integer, VARCHAR, TIMESTAMP, BLOB


md = MetaData()


class FileEntry(BaseModel):
    id: int
    filename: bytes
    hash: str


class FileInput(BaseModel):
    filename: str


RefTable = Table(
    "reference",
    md,
    Column("id", Integer, primary_key=True),
    Column("filename", BLOB),
    Column("iv", BLOB),
    Column("hash", VARCHAR),
    Column("time", TIMESTAMP)
)
