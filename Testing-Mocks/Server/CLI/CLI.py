import requests
import questionary
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
            
                requests.post(f"http://127.0.0.1:8000/registry",json={"username":name,"password":pwd})
                self.start()
            case "upload csv":
                name=questionary.text("Username:").ask()
                pwd=questionary.password("Password:").ask()
                file_path=Path(questionary.text("Username:").ask())
                if file_path.exists():
                    with open(file_path) as file:
                        requests.post(f"http://127.0.0.1:8000/upload",json={"username":name,"password":pwd,"file_str":file.read()})
                else:
                    print('file not found')
                self.start()

            case "get users list":
                requests.get(f"http://127.0.0.1:8000/users")
                self.start()
            case "get csv":
                name=questionary.text("Username:").ask()
                pwd=questionary.password("Password:").ask()
                requests.get(f"http://127.0.0.1:8000/myfiles",json={"username":name,"password":pwd})

                self.start()





