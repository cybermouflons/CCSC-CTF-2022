from flask import Flask, send_from_directory
from flask_restful import Api, Resource, reqparse
from flask_cors import CORS #comment this on deployment
from api.HelloApiHandler import HelloApiHandler
from api.postTodo import postTodo
from api.deleteTodo import deleteTodo
from api.getList import getList


app = Flask(__name__, static_url_path='', static_folder='frontend/build')
CORS(app) #comment this on deployment
api = Api(app)

@app.route("/", defaults={'path':''})
def serve(path):
    return send_from_directory(app.static_folder,'index.html')

api.add_resource(HelloApiHandler, '/hello')
api.add_resource(postTodo, '/postTodo')
api.add_resource(getList, '/getList')
api.add_resource(deleteTodo, '/deleteTodo')

