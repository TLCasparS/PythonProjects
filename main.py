from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from flask_sqlalchemy import SQLAlchemy


#db = sqlite3.connect("books-collection.db")
#cursor = db.cursor()

#cursor.execute("CREATE TABLE books (id INTEGER PRIMARY KEY, "
 #              "title varchar(250) NOT NULL UNIQUE, "
 #              "author varchar(250) NOT NULL, rating FLOAT NOT NULL)")
#cursor.execute("INSERT INTO books VALUES(1, 'Harry Potter', 'J. K. Rowling', '9.3')")
#db.commit()
db = SQLAlchemy()


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///new-books-collection.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False, )
    author = db.Column(db.String(250), unique=True, nullable=False)
    rating = db.Column(db.Float, unique = False, nullable = False)

    def __repr__(self):
        return f'<Book {self.title}>'

with app.app_context():
    db.create_all()
all_books = []

with app.app_context():

    all_books = db.session.query(Book).all()



@app.route('/', methods=['GET', 'POST', 'CLICK'])
def home():
    if request.method == "CLICK":
        pass

    with app.app_context():
        all_books = db.session.query(Book).all()
    return render_template("index.html", books=all_books)

@app.route("/delete", methods=['GET', 'POST'])
def delete():
    book_id = request.args.get('id')
    book_to_delete = db.session.execute(db.select(Book).where(Book.id == book_id)).scalar()
    db.session.delete(book_to_delete)
    db.session.commit()
    with app.app_context():
        all_books = db.session.query(Book).all()
    return render_template("index.html", books=all_books)
@app.route("/edit", methods=['GET', 'POST'])
def edit():
    if request.method == "POST":

        book_id = request.form["id"]
        book_to_update = Book.query.get(book_id)
        book_to_update.rating = request.form["rating"]



        db.session.commit()
        return redirect(url_for('home'))
    book_id = request.args.get('id')
    book_selected = Book.query.get(book_id)
    return render_template("edit.html" , book=book_selected)

@app.route("/add", methods=['GET', 'POST'])
def add():

    if request.method == "POST":
        #new_book = {
        #    "title": request.form["title"],
        #    "author": request.form["author"],
        #    "rating": request.form["rating"]
        #    }
        n_book = Book(title = request.form["title"],
                      author =request.form["author"],
                      rating = request.form["rating"])
        db.session.add(n_book)

        db.session.commit()


        #all_books.append(new_book)

        return redirect(url_for('home'))

    return render_template("add.html")
if __name__ == "__main__":
    app.run(debug=True)

