from flask import Flask, request
from db import MySQL

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '1234'
app.config['MYSQL_DB'] = 'users'

mysql = MySQL(app)

@app.route('/register', methods=['POST'])
def register():
    name = request.form['name']
    password = request.form['password']
    email = request.form['email']

    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO users (name, password, email) VALUES (%s, %s, %s)", (name, password, email))
    mysql.connection.commit()
    cur.close()

    return '회원가입이 완료되었습니다.'

if __name__ == '__main__':
    app.run()
