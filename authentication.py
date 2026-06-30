import jwt
from flask import request , jsonify
import os
from dotenv import load_dotenv
from functools import wraps
from datetime import datetime , timezone

from database import Database

load_dotenv()

database= Database()
class UsernameAlreadyExistsError(Exception):
    pass

def authenticate(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token =None
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.split(' ')[1]:
            token= auth_header.split(' ')[1]
        if not token:
            print('No Token')
            return jsonify({'message':'No token'}),401
        try :
            data = jwt.decode(token , os.getenv('JWT_SECRET_KEY') , algorithms =[ os.getenv('SIGNING_ALGORITHM')])
        except jwt.ExpiredSignatureError:
            print('Expired token')
            return jsonify({'message':'Token has expired'}) , 401
        except jwt.InvalidTokenError:
            print('Invalid Token')
            return jsonify({'message':'Invalid token'}) , 401
        if not doesUserExist(data['username']):
            print('User not existing')
            return jsonify({'message':'User doesnt exist'}) , 401
        return f(username=data['username'] , *args , **kwargs)
            
    return decorator
def loginUser(username , password):
    if doesUserExist(username):
        raise UsernameAlreadyExistsError
    else:
        database.make_db_connection()
        database.cursor.execute('INSERT INTO users (username , password) VALUES (%s , %s)', (username , password))
        database.conn.commit()
        database.end_db_connection()
    payload={'username':username , 'password':password , 'iat': datetime.now(timezone.utc)}
    token=jwt.encode(payload ,os.getenv('JWT_SECRET_KEY') , algorithm = os.getenv('SIGNING_ALGORITHM') )
    return jsonify({'token':token}) , 200
    
def doesUserExist(username):
    database.make_db_connection()
    database.cursor.execute('SELECT EXISTS (SELECT 1 FROM users WHERE username = %s)', (username,))
    is_user_existing = database.cursor.fetchone()[0]   
    database.end_db_connection() 
    return is_user_existing
        
        
    
