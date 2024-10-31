from flask import Flask, request, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager, create_access_token
from models import db
from config import Config
from resources.blacklist import AddToBlacklist, CheckBlacklist
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
jwt = JWTManager(app)
api = Api(app)

@app.route('/login', methods=['POST'])
def login():
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    
    if username == "admin" and password == "password":
        access_token = create_access_token(identity=username)
        return jsonify(access_token=access_token)
    else:
        return jsonify({"msg": "Bad credentials"}), 401

api.add_resource(AddToBlacklist, '/blacklists')
api.add_resource(CheckBlacklist, '/blacklists/<string:email>')

migrate = Migrate(app, db)

if __name__ == '__main__':
    app.run()
