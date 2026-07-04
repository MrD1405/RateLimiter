from functools import wraps
from flask import request , jsonify
import jwt
import os
from dotenv import load_dotenv
from database import Database , Redis
from datetime import datetime

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
        now=datetime.now()
        now=now.strftime("%Y-%m-%d %H:%M")
        username=f"username:{now}"
        userVisitCounter=r.get(username)
        userVisitCounter = int(userVisitCounter) if userVisitCounter else userVisitCounter
        if userVisitCounter == None:
            r.set(username,100,ex=60)
        elif userVisitCounter <=0 :
            return jsonify({'message':'Exceeded Rate Limit'}) , 429
        else:
            r.decr(username)
        return f(*args , **kwargs)
    return decorator
            