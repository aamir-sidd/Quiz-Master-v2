from flask import request
from flask_restful import Resource
from flask_jwt_extended import create_access_token
from .models import db, User

class UserRegistrationAPI(Resource):
    def post(self):
        data = request.get_json()
        
        existing_user = User.query.filter_by(email=data['email']).first()
        if existing_user:
            return {'message': 'User with this email already exists'}, 409
        
        new_user = User(
            email=data['email'],
            password=data['password'],
            full_name=data['full_name'],
            role='student'
        )
        
        db.session.add(new_user)
        db.session.commit()
        
        return {
            'message': 'User registered successfully',
            'user': {
                'id': new_user.id,
                'email': new_user.email,
                'full_name': new_user.full_name,
                'role': new_user.role
            }
        }, 201
        

class UserLoginAPI(Resource):
    def post(self):
        data = request.get_json()
        
        if 'email' not in data or 'password' not in data:
            return {'message': 'Email and password are required'}, 400
        
        user = User.query.filter_by(email=data['email']).first()
        
        if not user or not user.password == data['password']:
            return {'message': 'Invalid email or password'}, 401
        
        access_token = create_access_token(identity={'id': user.id, 'role': user.role})
        
        return {
            'access_token': access_token,
            'user': {
                'id': user.id,
                'email': user.email,
                'full_name': user.full_name,
                'role': user.role
            }
        }, 200
        
