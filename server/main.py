# main.py -> The main script that defines the API route
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
from databases import Database as Db
from fastapi import FastAPI
from sqlalchemy import create_engine

from server.formats import FileEntry, RefTable

DATABASE_URL = "mariadb+mariadbconnector://thedevi:testpw!@127.0.0.1:3306/app"
app = FastAPI()

database = Db(DATABASE_URL)
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.get("/{username}/get/all", response_model=list[FileEntry])
async def get_all(username: str):
    table = RefTable
    table.name = username.lower().replace(" ", "")
    if not table.exists:
        table.create()
    q = table.select()
    return await database.fetch_all(q)
