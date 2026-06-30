from functools import wraps
from flask import request , jsonify
import jwt
import os
from dotenv import load_dotenv
from database import Database , Redis

load_dotenv()
database = Database()
redis = Redis()
def rate_limit(f):
    @wraps(f)
    def decorator(*args , **kwargs):
        token=''
        username=kwargs['username']
        redis.make_connection()
        r=redis.conn
        userVisitCounter=int(r.get(username))
        print(f"userVisitCounter : {userVisitCounter}")
        if userVisitCounter:
            if userVisitCounter > 10:
                return jsonify({'message':'Exceeded Rate Limit'}) , 429
            r.incr(username)
        else:
            r.set(username,1)
        return f(*args , **kwargs)
    return decorator
            