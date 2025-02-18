from fastapi import Query

from fastapi import FastAPI, HTTPException
import pandas as pd
from Models.Usermodel import UserModel
from Logic.storage import storage
from Logic.parse_csv import parse_csv
import uvicorn

app = FastAPI()
stor = storage()
stor.data[storage.get_user_key()] = {}


@app.post("/registry")
def sign_user(username: str, password: str):
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
def upload_file(username: str, file_str: str = Query(...)):
    if username not in stor.data[storage.get_user_key()]:
        raise HTTPException(status_code=404, detail="User not found")

    if not file_str:
        raise HTTPException(status_code=400, detail="File content is required")

    df = pd.read_csv(file_str)
    if df:
        stor.data[storage.get_user_key()][username].data.append(df)
    raise HTTPException(status_code=400, detail = "File is empty")


@app.get("/json/{string}")
def get_json(string:str):
    return parse_csv(string)


if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=5050)