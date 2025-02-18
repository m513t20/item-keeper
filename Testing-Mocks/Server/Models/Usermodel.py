class UserModel:
    __username: str = ""
    __password: str = ""
    __data:list = []

    def __init__(self, usr, pwd):
        self.__username = usr
        self.__password = pwd
        self.__data = []

    def get_data(self):
        return {
            "username": self.__username,
            "password": self.__password,
            "data": self.__data
        }


    @property
    def username(self):
        return self.__username


    @property
    def password(self):
        return self.__password


    @property
    def data(self):
        return self.__data