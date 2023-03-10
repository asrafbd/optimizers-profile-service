from flask import Flask,jsonify,request
import psycopg2
from dotenv import load_dotenv
import os

app = Flask(__name__)

# set up connection to PostgreSQL database
database_name = os.getenv('DATABASE_NAME')
database_user = os.getenv('DATABASE_USER')
database_password = os.getenv('DATABASE_PASSWORD')
database_host = os.getenv('DATABASE_HOST')
database_port = os.getenv('DATABASE_PORT')

conn = psycopg2.connect(
    database=database_name,
    user=database_user,
    password=database_password,
    host=database_host,
    port=database_port
)

@app.route('/')
def hello_world():
    return 'Hello world'


# Need to refactor the route
@app.route('/reverser', methods=['POST'])
def get_user_contact():
    num = request.json['num']
    cur = conn.cursor()
    cur.execute("SELECT name FROM users WHERE number=%s", (num,))
    row = cur.fetchone()

    if row is None:
        return jsonify({'num': 'User not found'})
    else:
        return jsonify({'num': row[0]})

if __name__ == "__main__":
     app.run()