from flask_restful import Api, Resource, reqparse
from flask import Flask, request
import sqlite3

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

class deleteTodo(Resource):
  def get(self):
    return {
      'resultStatus': 'SUCCESS',
      }

  def post(self):
    print(self)
    parser = reqparse.RequestParser()
    parser.add_argument('id', type=str)

    args = parser.parse_args()

    print(args.id)

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('DELETE FROM todos WHERE id=?',(args.id))
    conn.commit()
    conn.close()
    
    final_ret = {"status": "Success","message": "You have completed one task!"}

    return final_ret