from flask_restful import Api, Resource, reqparse
from flask import Flask, request
from jinja2 import Template
import sqlite3

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

class postTodo(Resource):
  def get(self):
    return {
      'resultStatus': 'SUCCESS',
      'todo': "Try a Post Request :P"
      }

  def post(self):
    print(self)
    parser = reqparse.RequestParser()
    parser.add_argument('type', type=str)
    parser.add_argument('todo', type=str)

    args = parser.parse_args()

    print(args)

    request_type = args['type']
    todo = args['todo']
    ret_msg = request_type
    ret_msg = ret_msg.replace('{{','{')
    ret_msg = ret_msg.replace('}}','}')
    ret_msg = ret_msg.replace('{%','{')
    ret_msg = ret_msg.replace('%}','}')
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO todos (descr,isDone) VALUES (?,?)",[todo,False])
    conn.commit()
    conn.close()

    if ret_msg:
      t = Template(ret_msg)
      ssti = "{}".format(t.render())
    
    message = "Your "+ssti+" "+todo+" has been added to the list!"
    final_ret = {"status": "Success", "todo": message}

    return final_ret