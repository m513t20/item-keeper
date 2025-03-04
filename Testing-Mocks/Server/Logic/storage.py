class storage:
    """
    storage of our users and their data
    
    Atributes:
        __data: dictionary of stored data
    """
    __data={}


    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(storage, cls).__new__(cls)
        return cls.instance


    @property
    def data(self):
        return self.__data



    #ключ хранения пользователей     
    @staticmethod
    def get_user_key():
        return "users"