class UserModel:
    __username:str=""
    __password:str=""
    

    def __init__(self,usr,pwd):
        self.__username=usr
        self.__password=pwd


    def get_data(self):
        return {self.__username:self.__password}
    
    @property
    def username(self):
        return self.__username
    
    @property
    def password(self):
        return self.__password
    