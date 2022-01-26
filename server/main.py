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
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
from sqlalchemy import create_engine
from formats import FileEntry, RefTable
from pathlib import Path
from shutil import copyfileobj
from hashlib import sha256
from copy import deepcopy
from datetime import datetime

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


@app.get("/{username}/list/", response_model=list[FileEntry])
async def get_all(username: str):
    table = deepcopy(RefTable)
    table.name = username.lower().replace(" ", "")
    if not table.exists:
        table.create()
        return False
    return await database.fetch_all(table.select())


@app.get("/{username}/download/")
async def get_file(username: str, id: int):
    table = deepcopy(RefTable)
    table.name = username.lower().replace(" ", "")
    homedir = Path.joinpath(files_path, username)
    if not homedir.exists():
        homedir.mkdir()
        return False
    db_result = await database.fetch_one(table.select(table.c.id == id))
    if not db_result:
        return False
    else:
        path_to_file = Path.joinpath(homedir, db_result['hash'])
        return FileResponse(path=path_to_file, media_type="application/octet-stream", filename=db_result['filename'])


@app.post("/{username}/upload/")
async def upload_file(username: str, encrypted_filename: bytes, file: UploadFile = File(...)):
    table = deepcopy(RefTable)
    table.name = username.lower().replace(" ", "")
    homedir = Path.joinpath(files_path, username)
    if not homedir.exists():
        homedir.mkdir()
    time_of_uploading = datetime.now()
    tbh = ",".join([str(encrypted_filename), time_of_uploading.ctime()]).encode()
    hashed = sha256(tbh).hexdigest()
    path_to_file = Path.joinpath(homedir, hashed)
    with open(path_to_file, "wb") as w:
        copyfileobj(file.file, w)
    query = table.insert().values(filename=encrypted_filename, hash=hashed, time=time_of_uploading)
    its_id = await database.execute(query)
    return {
        "inserted_id": its_id
    }


@app.delete("/{username}/delete")
async def delete_file(username: str, id: int):
    table = deepcopy(RefTable)
    table.name = username.lower().replace(" ", "")
    homedir = Path.joinpath(files_path, username)
    if not homedir.exists():
        homedir.mkdir()
        return False
    file = await database.fetch_one(table.select(table.c.id == id))
    if not file:
        return False
    else:
        path_to_file = Path.joinpath(homedir, file['hash'])
        path_to_file.unlink()
        await database.execute(table.delete(table.c.id == id))
        return True

