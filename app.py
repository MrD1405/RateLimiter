from flask import Flask , render_template , request , jsonify
import os
from dotenv import load_dotenv
import datetime
import redis

from authentication import authenticate , loginUser , UsernameAlreadyExistsError
from rate_limit import rate_limit

app = Flask(__name__)
load_dotenv()


@app.route('/',methods=['GET'])
def homepage():
    return render_template('index.html')

@app.route('/test',methods=['GET'])
@authenticate
@rate_limit
def test(username):
    return jsonify({'message':"This is test page"}) , 200

@app.route('/login',methods=['POST'])
def login():
    data = request.get_json()
    if not data :
        return jsonify({'message':'Invalid request'}) , 400
    username=data.get('username')
    password=data.get('password')
    if not username or not password :
        return jsonify({'message':'InValid username or password'}) , 401
    try:
        return loginUser(username , password)
    except UsernameAlreadyExistsError:
        return jsonify({'message':'Username already exists'}) , 409
    
@app.route('/loginTest',methods=['GET'])
@rate_limit
@authenticate
def test_login(username):
    global counter
    counter=counter+1
    return "Login Successful {0}".format(counter) , 200
    
if __name__ == "__main__":
    app.run(debug=True , port = "9016")