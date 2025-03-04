from fastapi import Query
from fastapi import FastAPI, HTTPException
from CLI.CLI import CLI_client
from Logic.parse_csv import parse_csv
from Models.Usermodel import UserModel
from Logic.storage import storage
from Logic.parse_csv import parse_csv
import uvicorn
import time
import threading

app = FastAPI()
stor = storage()
stor.data[storage.get_user_key()] = {}

cli=CLI_client()

@app.post("/registry")
def sign_user(username: str, password: str):
    """
    Registration endpoint
    Args:
        username: name under which we will store your csv
        password: protection password for your csv
    returns:
        json: {response:code}

    """
    user = UserModel(username, password)

    if user.username in stor.data[storage.get_user_key()].keys():
        return {"already used": "200"}

    stor.data[storage.get_user_key()][user.username] = user
    print(f"saved user: {user.username}")
    print(stor.data)

    return {"exit_code": "200"}


@app.get("/users")
def get_users():
    """
        returns:
            array of users
    """
    return list(stor.data[storage.get_user_key()].keys())


@app.post("/upload")
def upload_file(username: str,password:str, file_str: str = Query(...)):
    """
    endpoint for uploading files
    Args:
        username
        password
        file_str: binary read file
    Returns:
        json {message:code}
    Raises:
        HTTPException: data havent parsed correctly or empty file
    """
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
def get_files_all(username:str,password:str):
    """
    Gets your file
    Args:
        username: your username
        password: your password
    Returns:
        your csv file as json
    Raises:
        HTTPException: if user nor found or password is incorrect
    """
    if username not in stor.data[storage.get_user_key()] or password!=stor.data[storage.get_user_key()][username].password:
        raise HTTPException(status_code=404, detail="User not found")
    return stor.data[storage.get_user_key()][username].data


def start_sever():
    """
    starts server
    """
    uvicorn.run(app, host="127.0.0.1", port=5050)


@app.get("/json/{string}")
def get_json(string:str):
    """
    parses csv as json string
    Args:
        string: your csv data
    Returns:
        json string of your csv
    """
    return parse_csv(string)


if __name__ == '__main__':
    server_thread = threading.Thread(target=start_sever)
    server_thread.daemon = True 
    server_thread.start()
    time.sleep(1)
    cli.start()
