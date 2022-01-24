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
from fastapi.responses import FileResponse
from sqlalchemy import create_engine
from formats import FileEntry, RefTable
from pathlib import Path

DATABASE_URL = "postgresql://test:123@Postgres/app"
files_path = Path("/files/")
app = FastAPI()

database = Db(DATABASE_URL)
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.get("/{username}/get/list/all", response_model=list[FileEntry])
async def get_all(username: str):
    table = RefTable
    table.name = username.lower().replace(" ", "")
    if not table.exists:
        table.create()
    q = table.select()
    return await database.fetch_all(q)


@app.get("/{username}/get/download/{encrypted_filename}")
async def get_file(username: str, encrypted_filename: str):
    table = RefTable
    table.name = username.lower().replace(" ", "")
    homedir = Path.joinpath(files_path, username)
    if not homedir.exists():
        homedir.mkdir()
    path_to_file = Path.joinpath(homedir, encrypted_filename)
    return FileResponse(path=path_to_file, media_type="application/octet-stream", filename=path_to_file.name)
