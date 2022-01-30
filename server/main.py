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
from formats import FileEntry, RefTable
from pathlib import Path
from shutil import copyfileobj
from hashlib import sha256
from copy import deepcopy
from datetime import datetime
from sqlalchemy import create_engine

DATABASE_URL = "mysql+pymysql://test:123@MySQL/app"
files_path = Path("/files/")
app = FastAPI()
database = Db(DATABASE_URL)
engine = create_engine(DATABASE_URL)


def get_table(username: str):
    table = deepcopy(RefTable)
    table.name = username.lower().replace(" ", "")
    return table


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.get("/{username}")
async def confirm_user(username: str):
    table = get_table(username)
    if not engine.dialect.has_table(connection=engine.connect(), table_name=table.name):
        print("Table '{}' Does Not Exist!".format(table.name))
        await database.execute(f"""
            CREATE TABLE {table.name} (
                id INT AUTO_INCREMENT PRIMARY KEY,
                filename BLOB,
                hash VARCHAR(64),
                time TIMESTAMP
            );
        """)
        print("Created Table '{}' For User '{}'!".format(table.name, username))
        return True
    else:
        return True


@app.get("/{username}/list/", response_model=list[FileEntry])
async def get_all(username: str):
    table = get_table(username)
    return await database.fetch_all(f"SELECT * FROM {table.name};")


@app.get("/{username}/download/")
async def get_file(username: str, id: int):
    table = get_table(username)
    homedir = Path.joinpath(files_path, username)
    if not homedir.exists():
        homedir.mkdir()
        return False
    db_result = await database.fetch_one(f"SELECT hash, filename FROM {table.name} WHERE id = {id}")
    if not db_result:
        return False
    else:
        path_to_file = Path.joinpath(homedir, db_result['hash'])
        return FileResponse(path=path_to_file, media_type="application/octet-stream", filename=db_result['filename'])


@app.post("/{username}/upload/")
async def upload_file(username: str, encrypted_filename: bytes, file: UploadFile = File(...)):
    table = get_table(username)
    homedir = Path.joinpath(files_path, username)
    if not homedir.exists():
        homedir.mkdir()
    time_of_uploading = datetime.now()
    tbh = ",".join([str(encrypted_filename), time_of_uploading.ctime()]).encode()
    hashed = sha256(tbh).hexdigest()
    path_to_file = Path.joinpath(homedir, hashed)
    with open(path_to_file, "wb") as w:
        copyfileobj(file.file, w)
    query = f"INSERT INTO {table.name} (filename, hash, time) VALUES (:filename, :hash, :time);"
    values = {
        "filename": encrypted_filename,
        "hash": hashed,
        "time": time_of_uploading
    }
    its_id = await database.execute(query=query, values=values)
    return {
        "inserted_id": its_id
    }


@app.delete("/{username}/delete")
async def delete_file(username: str, id: int):
    table = get_table(username)
    homedir = Path.joinpath(files_path, username)
    if not homedir.exists():
        homedir.mkdir()
        return False
    file = await database.fetch_one(f"SELECT hash FROM {table.name} WHERE id = {id};")
    if not file:
        return False
    else:
        path_to_file = Path.joinpath(homedir, file['hash'])
        path_to_file.unlink()
        await database.execute(f"DELETE FROM {table.name} WHERE id = {id};")
        return True

