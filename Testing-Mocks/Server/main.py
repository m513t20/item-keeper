from fastapi import Query, Form
from fastapi import Body
from fastapi import File, UploadFile
from fastapi import FastAPI, HTTPException
from CLI.CLI import CLI_client
from Logic.parse_csv import parse_csv
from Models.Usermodel import UserModel
from Logic.storage import storage
from Logic.parse_csv import parse_csv
import uvicorn
import time
import threading
import codecs

app = FastAPI()
stor = storage()
stor.data[storage.get_user_key()] = {}

cli=CLI_client()

@app.post("/registry")
def sign_user(username: str=Body(...,embed=True), password: str=Body(...,embed=True)):
    user = UserModel(username, password)

    if user.username in stor.data[storage.get_user_key()].keys():
        return {"already used": "200"}

    stor.data[storage.get_user_key()][user.username] = user
    print(f"saved user: {user.username}")
    print(stor.data)

    return {"exit_code": "200"}


@app.get("/users")
def get_users():
    return list(stor.data[storage.get_user_key()].keys())


@app.post("/upload")
def upload_file(username: str=Form(...,embed=True),password:str=Form(...,embed=True), file_str: UploadFile = File(...)):
    file_str=file_str.file.read().decode('ascii')
    print(file_str)
    if username not in stor.data[storage.get_user_key()] or password!=stor.data[storage.get_user_key()][username].password:
        raise HTTPException(status_code=404, detail="User not found")

    if not file_str:
        raise HTTPException(status_code=400, detail="File content is required")

    df = parse_csv(file_str)
    if df==[]:
        raise HTTPException(status_code=400, detail="bad data")
    stor.data[storage.get_user_key()][username].data.append(file_str)
    return {"succes":"200"}

@app.get("/myfiles")
def get_files_all(username:str=Body(...,embed=True),password:str=Body(...,embed=True)):
    if username not in stor.data[storage.get_user_key()] or password!=stor.data[storage.get_user_key()][username].password:
        raise HTTPException(status_code=404, detail="User not found")
    if len(stor.data[storage.get_user_key()][username].data)==0:
        raise HTTPException(status_code=404, detail="Data not found")
    return parse_csv(stor.data[storage.get_user_key()][username].data[-1])


def start_sever():
    uvicorn.run(app, host="127.0.0.1", port=8000)




if __name__ == '__main__':
    server_thread = threading.Thread(target=start_sever)
    server_thread.daemon = True 
    server_thread.start()
    time.sleep(1)
    cli.start()
"""
a,b,c
d,e,f
"""