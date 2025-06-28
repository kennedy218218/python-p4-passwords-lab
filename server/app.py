#!/usr/bin/env python3

from flask import request, session
from flask_restful import Resource

from config import app, db, api
from models import User

class ClearSession(Resource):
    def delete(self):
        session.pop('page_views', None)
        session.pop('user_id', None)
        return {}, 204

class Signup(Resource):
    def post(self):
        json_data = request.get_json()
        user = User(username=json_data['username'])
        user.password_hash = json_data['password']
        db.session.add(user)
        db.session.commit()
        return user.to_dict(), 201

class Login(Resource):
    def post(self):
        data = request.get_json()
        user = User.query.filter_by(username=data.get('username')).first()
        if not user or not user.authenticate(data.get('password')):
            return {'error': 'Invalid credentials'}, 401
        session['user_id'] = user.id
        return user.to_dict(), 200

class Logout(Resource):
    def delete(self):                
        session.pop('user_id', None) 
        return {}, 204

class CheckSession(Resource):
    def get(self):
        user_id = session.get('user_id')
        if not user_id:
            return {}, 204          
        user = db.session.get(User, user_id)

        if not user:
            return {}, 204           
        return user.to_dict(), 200

api.add_resource(ClearSession, '/clear', endpoint='clear')
api.add_resource(Signup, '/signup', endpoint='signup')
api.add_resource(Login, '/login', endpoint='login')
api.add_resource(Logout, '/logout', endpoint='logout')
api.add_resource(CheckSession, '/check_session', endpoint='check_session')

if __name__ == '__main__':
    app.run(port=5555, debug=True)
