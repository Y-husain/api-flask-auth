from flask_bcrypt import Bcrypt
users_data = {}


class User:
    """users class"""

    def __init__(self, first_name, last_name, email, password):
        global users_data
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password_hash = Bcrypt().generate_password_hash(password).decode(
            'UTF-8')

    def create(self):
        user = {
            self.email: {
                "FirstName": self.first_name,
                "LastName": self.last_name,
                "Password": self.password_hash
            }
        }
        return users_data.update(user)
