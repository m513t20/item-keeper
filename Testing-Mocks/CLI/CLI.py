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
                pass
            case "upload csv":
                pass
            case "get users list":
                pass
            case "get csv":
                pass
            case "get csv json":
                pass


cli=CLI_client()
cli.start()

