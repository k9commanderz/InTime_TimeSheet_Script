import getpass


class User:

    def __init__(self):
        self.username = None
        self.password = None

    def requestCredential(self):
        self.username = input("Username: ")
        self.password = getpass.getpass(prompt="Password: ", stream=None)






if __name__ == "__main__":
    user = User()
    user.requestCredential()

