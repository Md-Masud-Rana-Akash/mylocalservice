from flask import Flask, jsonify
from flaskext.mysql import MySQL
app = Flask(__name__)

mysql = MySQL()

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'found'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)


@app.route('/')
def hello_world():
    return '<h1>Hello World</h1>'


@app.route('/greetings/<name>/<address>/<date>', methods=['GET'])
def greetings(name, address, date):
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute('Select * from posts Limit 10')
    info = cursor.fetchall()
    print(info)

    info = {}
    info['name'] = name
    info['address'] = address
    info['date'] = date

    response = jsonify(info)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response
