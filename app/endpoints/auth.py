"""Handle Authentication routes."""

from flask_restplus import Resource, Namespace, fields
from flask import request
from flask_bcrypt import Bcrypt
from app.models.user import User, users_data
from app.models.token import token_required
from app.models.blacklist import Blacklist, blacklist
import json
import re
import os

auth_namespace = Namespace(
    'auth', description='Authentication Related Operation.')

registration_model = auth_namespace.model(
    "Registration", {
        "FirstName":
        fields.String(
            required=True, description='Your First Name', example='John'),
        "LastName":
        fields.String(
            required=True, description='Your Last Name', example='Doe'),
        "Email":
        fields.String(
            required=True,
            description='your email accounts',
            example='john_doe@example.com'),
        "Password":
        fields.String(
            required=True,
            description='Your secret password',
            example='vU22f53nNp')
    })

login_model = auth_namespace.model(
    "Login", {
        "Email":
        fields.String(
            required=True,
            description='your email accounts',
            example='john_doe@example.com'),
        "Password":
        fields.String(
            required=True,
            description='Your secret password',
            example='vU22f53nNp')
    })

email_regex = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")
pattern = re.compile(r"(^[A-Za-z]+$)")


@auth_namespace.route('/signup')
class Signup(Resource):
    """Handles registration Routes."""

    @auth_namespace.doc('create new user')
    @auth_namespace.expect(registration_model)
    def post(self):
        """create a new user to database"""
        data = request.get_json()
        first_name = data['FirstName']
        last_name = data['LastName']
        email = data['Email']
        password = data['Password']

        user = User(first_name, last_name, email, password)
        user.create()

        return {
            'status': 'success',
            'message': 'Successfully registered.'
        }, 201


@auth_namespace.route('/login')
@auth_namespace.doc(
    responses={
        201: 'Successfully login',
        401: 'Invalid credential'
    },
    security=None,
    body=login_model)
class Login(Resource):
    """Handles login Routes"""

    def post(self):
        """Handle POST request for login"""
        data = request.get_json()
        user_email = data['Email']
        user_password = data['Password']

        if user_email in users_data:
            if Bcrypt().check_password_hash(users_data[user_email]["Password"],
                                            user_password):

                # # generate the auth token
                auth_token = User.encode_auth_token(user_email)

                return {
                    'status': 'success',
                    'message': 'Successfully registered.',
                    'auth_token': auth_token.decode()
                }, 200
            else:
                return {
                    "message": "Failed, Invalid password! Please try again"
                }, 401
        else:
            return {"message": "Failed, Invalid email! Please try again"}, 401


@auth_namespace.route('/logout')
@auth_namespace.doc(
    responses={
        201: 'Successfully login',
        401: 'Invalid credential'
    },
    security="apikey")
class Logout(Resource):
    """Handles logout Routes"""

    @token_required
    def post(self, current_user):
        """Handle POST request for logout"""

        # get auth token
        token = request.headers['access_token']

        # mark the token as blacklisted
        try:
            revokedToken = Blacklist(token)
            revokedToken.save_blacklist()

        except Exception as e:
            return {'status': 'Failed to logout', 'message': str(e)}, 200

        else:
            return {
                'status': 'success',
                'message': 'Successfully logged out.'
            }, 200
