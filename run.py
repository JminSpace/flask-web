from flask import Flask, send_from_directory, request, render_template, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:123456@localhost:3306/curd'
db = SQLAlchemy(app)

class Board(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    author = db.Column(db.String(50))
    content = db.Column(db.Text)
    time = db.Column(db.DateTime, default=datetime.now)

@app.route('/')
def index():
    boards = Board.query.all()
    return render_template('index.html', boards=boards)

@app.route('/create_post', methods=['POST'])
def create_post():
    title = request.form['title']
    author = request.form['author']
    content = request.form['content']
    time = datetime.now()

    post = Board(title=title, author=author, content=content, time=time)
    db.session.add(post)
    db.session.commit()

    return redirect("/")

@app.route('/edit_post/<int:post_id>')
def edit_post(post_id):
    post = Board.query.filter_by(id=post_id).first()
    if post:
        return render_template('edit.html', post=post)
    return redirect('/')

@app.route('/update_post/<int:post_id>', methods=['POST'])
def update_post(post_id):
    post = Board.query.filter_by(id=post_id).first()
    if post:
        post.title = request.form['title']
        post.author = request.form['author']
        post.content = request.form['content']
        db.session.commit()
    return redirect('/')

@app.route('/delete_post/<int:post_id>', methods=['POST'])
def delete_post(post_id):
    post = Board.query.filter_by(id=post_id).first()
    if post:
        db.session.delete(post)
        db.session.commit()
    return redirect('/')

@app.route('/search', methods=['POST'])
def search():
    search_term = request.form['search_term']
    boards = Board.query.filter(or_(Board.title.contains(search_term), Board.content.contains(search_term))).all()
    return render_template('index.html', boards=boards)

@app.route('/<path:name>')
def run(name):
    return send_from_directory('html', name)

if __name__ == '__main__':
    app.run()
