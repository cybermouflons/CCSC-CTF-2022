from flask_restful import Api, Resource, reqparse
from flask import Flask, request
from jinja2 import Template
import sqlite3
import json

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


class getList(Resource):
  def get(self):
    conn = get_db_connection()
    todos = conn.execute('SELECT * FROM todos').fetchall()
    json_output = json.dumps([dict(ix) for ix in todos])
    conn.close()
    return {
      'resultStatus': 'SUCCESS',
      'todos': json_output
      }