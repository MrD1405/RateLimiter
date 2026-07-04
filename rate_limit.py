from functools import wraps
from flask import request , jsonify
import jwt
import os
from dotenv import load_dotenv
from database import Database , Redis
from datetime import datetime

load_dotenv()


class RateLimitError(Exception):
    pass
database = Database()
redis = Redis()
def rate_limit(f):
    @wraps(f)
    def decorator(*args , **kwargs):
        token=''
        username=kwargs['username']
        try:
            fixedWindow(username)
        except RateLimitError:
            return jsonify({'message':'Exceeded Rate Limit'}) , 429
        return f(*args , **kwargs)
    return decorator

def fixedWindow(username):
    now=datetime.now()
    now=now.strftime("%Y-%m-%d %H:%M")
    username=f"{username}:{now}"
    redis.make_connection()
    r=redis.conn
    userVisitCounter=r.get(username)
    userVisitCounter = int(userVisitCounter) if userVisitCounter else userVisitCounter
    if userVisitCounter == None:
        r.set(username,100,ex=60)
    elif userVisitCounter <=0 :
        raise RateLimitError 
    else:
        r.decr(username)
    redis.end_connection()
            