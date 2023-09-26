from collections import UserString
from typing import re
from site import USER_BASE
from flask import Blueprint, make_response, jsonify
from flask import request
from flask_jwt_extended import (
    jwt_required, create_access_token, get_jwt_identity)
from werkzeug.exceptions import abort
import sys
sys.path.append('C:\\Users\\Dell\\Documents\\college\\semester5\\COIA\\ContainerizedPlatform\\demo-env\\config.py')
from config import Config

users_bp = Blueprint('users', __name__)

error_pwd_msg = 'password must contain at least 6 characters, including Upper/Lowercase, Special characters and numbers'

#Create new account with the user details
@users_bp.route(Config.SIGN_UP, methods=['POST'])
def sign_up():
    try:
        username = request.json['username']
        try:
            if Users.object.get(username=username):
                return make_response(jsonify({"username": username+' username already exists'}), 400)
        except UserString.DoesNotExist:
            pass

        email = request.json['email']
        if email_validation(email) is None:
            return make_request(jsonify({"email_validation": email+' is not a valid email address'}), 400)
        
        password = request.json['password']
        if password_validation(password) is None:
            return make_response(jsonify({"password_validation": password+' is not a valid password'}), 400)
        
        users = Users(username=username,
                      password=password,
                      name=request.json['name'],
                      email=email,
                      dob=request.json['dob'])
        users.save()
    except KeyError:
        abort(400)
    return make_response(jsonify({"success": 'User Created Successfully'}), 201)

@users_bp.errorhandler(400)
def invalid_request(error):
    return make_response(jsonify({'error': 'invalid Request '+error}), 400)

@users_bp.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error' : 'Sorry user not found'}), 404)

@users_bp.errorhandler(401)
def unauthorized(error):
    return make_response(jsonify({'error': 'Unauthorized Access'}), 401)

#Validate the Password
def password_validation(password):
    pwd_regex = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,20}$"
    pwd_pattern = re.compile(pwd_regex)
    passwword_regex_match = re.search(pwd_pattern, password)
    return passwword_regex_match

#Validate the email address
def email_validation(email):
    email_regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    email_pattern = re.compile(email_regex)
    email_regex_match = re.search(email_pattern, email)
    return email_regex_match