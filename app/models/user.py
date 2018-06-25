from flask_bcrypt import Bcrypt
import datetime
import jwt
import os
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
                "Email": self.email,
                "Password": self.password_hash
            }
        }
        return users_data.update(user)

    @classmethod
    def encode_auth_token(cls, user_id):
        """
        Generates the Auth Token
        :return: string
        """

        try:
            payload = {
                'exp':
                datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
                'iat':
                datetime.datetime.utcnow(),
                'sub':
                user_id
            }
            return jwt.encode(
                payload, os.getenv('SECRET'), algorithm='HS256')
        except Exception as e:
            return e

    @staticmethod
    def decode_auth_token(auth_token):
        """
        Decodes the auth token
        :param auth_token:
        :return: integer|string
        """
        try:
            payload = jwt.decode(auth_token, os.getenv('SECRET_KEY'))
            return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'
