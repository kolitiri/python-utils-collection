"""
Book: Clean code in python.
Chapter: Properties, p38.
"""


def is_valid_email(email):
    return "@" in email


class User:
    def __init__(self, username):
        self.username = username
        self._email = None

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, email):
        if not is_valid_email(email):
            raise ValueError("The email address is not valid")
        self._email = email


user = User("username")
user.email = f"{user.username}@gmail.com"
print(user.email)
