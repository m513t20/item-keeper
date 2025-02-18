from fastapi import FastAPI
from Models.Usermodel import UserModel
from Logic.storage import storage
import uvicorn

app=FastAPI()
stor=storage()
stor.data[storage.get_user_key()]={}

@app.post("/registry")
def sign_user(username:str,password:str):
    user=UserModel(username,password)
    
    if user.username in stor.data[storage.get_user_key()].keys():
        return {"already used":"200"}
    

    stor.data[storage.get_user_key()][user.username]=user
    print(f"saved user: {user.username}")
    print(stor.data)

    return {"exit_code":"200"}

@app.get("/users")
def get_users():
    return list(stor.data[storage.get_user_key()].keys())


if __name__=='__main__':
    uvicorn.run(app,host="127.0.0.1",port=5050)