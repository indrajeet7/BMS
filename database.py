from flask_sqlalchemy import SQLAlchemy
from flask import Flask, jsonify, request, render_template, redirect, url_for
app = Flask(__name__)

"""
# Database
MYSQL_HOST = 'localhost'
MYSQL_USER = 'root'
MYSQL_PASSWORD = 'root.123'
MYSQL_DB = 'Book_Management_DB'
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+mysqlconnector://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DB}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
"""

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.secret_key = 'key'
db = SQLAlchemy(app)

class BOOk(db.Model):
    __tablename__ = 'Book_Details'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(20))
    author = db.Column(db.String(20))

with app.app_context():
    db.create_all()

@app.route('/', methods=['GET'])
def _books():
    return render_template('index.html')
@app.route('/a', methods=['GET'])
def _books1():
    return render_template('menu_bar.html')
@app.route('/get')
def get_books():
    data = []
    books = BOOk.query.all()
    for book in books:
        data.append([book.id, book.title,  book.author])
    return render_template("get.html", book_details =data)


# To add new book
@app.route('/add', methods=['POST','GET'])
def add_book():
    if request.method == "POST":
        new_book = {
            'title': request.form.get('booktitle'),
            'author': request.form.get('bookauthor')
                    }
        # If either title or author exist then don't add records and return
        books = BOOk.query.all()
        for book in books:
            if book.title == new_book['title']:
                return render_template('message.html', message='Book title exist...')
            elif book.author == new_book['author']:
                return render_template('message.html', message='Book author exist...')
        # Add new records
        book = BOOk(title=new_book['title'], author=new_book['author'])
        db.session.add(book)
        db.session.commit()
        return render_template('message.html', message='Book added successfully...')
    return render_template("add.html")

# To add new book
@app.route('/update', methods=['GET', 'POST'])
def update_book():
    book_id = request.form.get('bookid')
    if request.method == 'POST':
        if book_id:
            book = db.session.get(BOOk, int(book_id))
            if book != None:
                """
                if book.title == request.form.get('booktitle'):
                    return render_template('message.html', message='Book title exist...')

                elif book.author == request.form.get('bookauthor'):
                    return render_template('message.html', message='Book author exist...')
                """
                books = BOOk.query.all()
                for book in books:
                    if book.title == request.form.get('booktitle'):
                        return render_template('message.html', message='Book title exist...')
                    elif book.author == request.form.get('bookauthor'):
                        return render_template('message.html', message='Book author exist...')

                else:
                    book.title = request.form.get('booktitle')
                    book.author = request.form.get('bookauthor')
                    db.session.commit()
                    return render_template('message.html', message='Book updated successfully...')
            else:
                return render_template('message.html', message='Enter Valid Book_ID to update...')
    return render_template("update.html")

@app.route('/delete', methods=['GET','POST'])
def delete_book():
    if request.method == 'POST':
        book_id = request.form.get('bookid')
        book = db.session.get(BOOk, int(book_id))
        if book:
            db.session.delete(book)
            db.session.commit()
            return render_template('message.html', message='Book deleted successfully...')
        else:
            return render_template('message.html', message='Book not found...')
    return render_template("delete.html")

@app.route('/search', methods=['GET','POST'])
def search_book():
    if request.method == 'POST':
        book_id = request.form.get('bookid')
        book = db.session.get(BOOk, int(book_id))
        if book:
            return render_template("get.html", book_details =[[book.id, book.title, book.author]])
        else:
            return jsonify({'message': 'Book not found...'})
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)