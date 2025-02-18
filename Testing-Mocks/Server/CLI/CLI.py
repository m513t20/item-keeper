import requests
import questionary

class CLI_client:
    URL=""

    def __init__(self,url=""):
        URL=url

    def _default_choice(self):
        start_question=questionary.select("Choose what do you want to do",["sign in","upload csv","get users list","get csv","get csv json"]).ask()
        return start_question
    
    def start(self):
        choice=self._default_choice()
    
        match choice:
            case "sign in":
                name=questionary.text("Username:").ask()
                pwd=questionary.password("Password:").ask()
                requests.post(f"http://127.0.0.1:8000",json={"username":name,"password":pwd})
                self.start()
            case "upload csv":
                self.start()
            case "get users list":
                self.start()
            case "get csv":
                self.start()
            case "get csv json":
                self.start()




