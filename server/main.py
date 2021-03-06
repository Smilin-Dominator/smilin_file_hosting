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
from uuid import uuid4, UUID
from base64 import b64encode


DATABASE_URL = "mysql+pymysql://test:123@MariaDB/app"
files_path = Path("/files/")
app = FastAPI()
database = Db(DATABASE_URL)
engine = create_engine(DATABASE_URL)


def get_table(username: str):
    table = deepcopy(RefTable)
    table.name = username.replace("-", "")
    return table


@app.on_event("startup")
async def startup():
    if not files_path.exists():
        files_path.mkdir()
    await database.connect()
    if not engine.dialect.has_table(connection=engine.connect(), table_name="users"):
        await database.execute("""
            CREATE TABLE users ( 
                uuid VARCHAR(64) PRIMARY KEY,
                time TIMESTAMP
            );
        """)


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.post("/register", response_model=UUID)
async def create_user():
    while True:
        uuid = str(uuid4())
        check = await database.fetch_one("SELECT uuid FROM users WHERE uuid = :id", {"id": uuid})
        if check is None:
            await database.execute("INSERT INTO users VALUES (:id, :time)", {"id": uuid, "time": datetime.now()})
            await database.execute(f"""
                CREATE TABLE `{uuid.replace("-", "")}` (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    filename BLOB,
                    iv BLOB,
                    hash VARCHAR(64),
                    time TIMESTAMP
                );
            """)
            print("Created Table For User '{}'!".format(uuid))
            return uuid
        else:
            continue


@app.get("/{username}")
async def confirm_user(username: str):
    table = get_table(username)
    if not engine.dialect.has_table(connection=engine.connect(), table_name=table.name):
        print("Table '{}' Does Not Exist!".format(table.name))
        return False
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
    db_result = await database.fetch_one(f"SELECT hash, filename, iv FROM {table.name} WHERE id = {id}")
    if not db_result:
        return False
    else:
        path_to_file = Path.joinpath(homedir, db_result['hash'])
        return FileResponse(
            path=path_to_file,
            media_type="application/octet-stream",
            filename=db_result['filename'],
            headers={"iv": b64encode(db_result["iv"]).decode('utf-8')}
        )


@app.post("/{username}/upload/")
async def upload_file(username: str, encrypted_filename: bytes, iv: bytes, file: UploadFile = File(...)):
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
    query = f"INSERT INTO {table.name} (filename, iv, hash, time) VALUES (:filename, :iv, :hash, :time);"
    values = {
        "filename": encrypted_filename,
        "iv": iv,
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

