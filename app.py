from datetime import datetime, timedelta
from http.client import HTTPResponse
from flask import Flask, Response, request, jsonify
import sqlite3
import jwt
from flask_cors import CORS
import uuid
from s3_wrapper import s3_wrapper
import boto3
import os

ACCESS_KEY = os.environ['ACCESS_KEY']
SECRET_ACCESS_KEY = os.environ['SECRET_ACCESS_KEY']
BUCKET_NAME = os.environ['BUCKET_NAME']

client = boto3.client('s3', aws_access_key_id = ACCESS_KEY, aws_secret_access_key = SECRET_ACCESS_KEY)

s3_client = s3_wrapper(client, BUCKET_NAME)

db_file = "db.sqlite"

def create_connection():
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Exception as e:
        print(e)
    return conn

open("db.sqlite", "w").close()

with open('schema.sql') as f:
    connection = create_connection()
    connection.executescript(f.read())

app = Flask(__name__)
cors = CORS(app, resources={r"*": {"origins": "*"}})

def login_required(func):
    def decorated(*args, **kwargs):
        headers = request.headers
        token = headers.get('Authorization')
        if not token:
            return Response(status=403)

        load = jwt.decode(token, "SECRET", algorithms=["HS256"])
        email, exp = load["email"], load["exp"]
        connection = create_connection()
        cursor = connection.cursor()
        cursor.execute(f"select * from users where email='{email}';")
        users = cursor.fetchall()
        request.user = {
            "name": users[0][1],
            "email": users[0][0]
        }
        return func(*args, **kwargs)
    
    decorated.__name__ = func.__name__
    return decorated

@app.route("/users/signup", methods=["POST"])
def signup():
    body = request.json
    email, password, name = body["email"], body["password"], body["name"]
    query = f"insert into users values ('{email}', '{name}', '{password}');"
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute(query)
    connection.commit()
    return Response(status = 200)


@app.route("/users/login", methods=["POST"])
def login():
    body = request.json
    email, password = body["email"], body["password"]
    query = f"select * from users where email='{email}';"
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute(query)
    user = list(map(lambda tup: list(tup), cursor.fetchall()))
    print("users:",user)
    if len(user)==0 or user[0][2] != password:
        return Response(status=403)
    jwt_token = jwt.encode({"email": user[0][0], 'exp': datetime.utcnow()+timedelta(days=30)}, "SECRET", algorithm="HS256")
    print(jwt_token)
    return jsonify({"jwt_token": jwt_token.decode("utf-8")})
    
 
@app.route("/files", methods=["GET"])
@login_required
def list_files():
    try:
        files = s3_client.list_files()
        files = list(map(lambda x: x["Key"], files))
        return jsonify(files)
    except Exception as e:
        return Response(status = 500)   

@app.route("/files", methods=["POST"])
@login_required
def create_file():
    body = request.json
    filename = str(uuid.uuid4())
    created_by = request.user["name"]
    created_time = str(datetime.now())
    body_object = {
        "uuid": filename,
        "created_by": created_by,
        "created_time": created_time,
        "modified_by": created_by,
        "modified_time": created_time,
        "body": body
    }

    try:
        s3_client.create(f"{filename}.json", body_object)
        return Response(status = 200)
    except Exception as e:
        return Response(status = 500)


@app.route("/files/<uuid:filename>", methods=["PUT"])
@login_required
def update_file(filename):
    body = request.json
    file_contents = None
    filename = f"{filename}.json"
    try:
        file_contents = s3_client.read(filename)
        modified_by = request.user["name"]
        modified_time = str(datetime.now())
        file_contents["body"] = body
        file_contents["modified_by"] = modified_by
        file_contents["modified_time"] = modified_time

        s3_client.update(filename, file_contents)

        return Response(status = 200)

    except Exception as e:
        return Response(status = 500)
 
@app.route("/files/<uuid:filename>", methods=["DELETE"])
@login_required
def delete_file(filename):
    filename = f"{filename}.json"
    try:
        s3_client.delete(filename)
        return Response(status = 200)
    except Exception as e:
        return Response(status = 500)
    
@app.route("/files/<uuid:filename>", methods=["GET"])
@login_required
def read_file(filename):
    filename = f"{filename}.json"
    try:
        file_contents = s3_client.read(filename)
        return jsonify(file_contents)
    except Exception as e:
        return Response(status = 500)
   



if __name__=="__main__":
    app.run(debug=True)