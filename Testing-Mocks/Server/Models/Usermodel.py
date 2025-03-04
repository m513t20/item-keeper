class UserModel:
    """
        model of our user
    """
    __username: str = ""
    __password: str = ""
    __data:list = []

    def __init__(self, usr, pwd):
        """
        Args:
            username:
            password:
        """
        self.__username = usr
        self.__password = pwd
        self.__data = []

    def get_data(self):
        """
        Returns: 
            user_data in json string
        """
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