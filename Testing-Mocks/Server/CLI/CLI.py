import questionary.question
import requests
import questionary
import json
from pathlib import Path

class CLI_client:
    URL=""

    def __init__(self,url=""):
        URL=url

    def _default_choice(self):
        start_question=questionary.select("Choose what do you want to do",["sign in","upload csv","get users list","get csv"]).ask()
        return start_question
    
    def start(self):
        choice=self._default_choice()
        match choice:
            case "sign in":
                name=questionary.text("Username:").ask()
                pwd=questionary.password("Password:").ask()
                print(name,pwd)
                requests.post(f"http://localhost:8000/registry",json={"username":str(name),"password":str(pwd),})
                self.start()
            case "upload csv":
                name=questionary.text("Username:").ask()
                pwd=questionary.password("Password:").ask()
                file_path=Path(questionary.text("file_path:").ask())
                if file_path.exists():
                    with open (file_path,'rb') as file_str:
                        files={"file_str":file_str}
                        requests.post(f"http://127.0.0.1:8000/upload",data={"username":name,"password":pwd},files=files)

                else:
                    print('file not found')
                self.start()

            case "get users list":
                users=requests.get(f"http://127.0.0.1:8000/users")
                print(users.json())
                self.start()

            case "get csv":
                name=questionary.text("Username:").ask()
                pwd=questionary.password("Password:").ask()
                csv=requests.get(f"http://127.0.0.1:8000/myfiles",json={"username":name,"password":pwd})
                print(csv.status_code)
                if csv.status_code==200:
                    print(csv.json())
                self.start()





