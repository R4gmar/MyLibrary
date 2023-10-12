from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap4
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, URL
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
db = SQLAlchemy()
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///new-books-collection.db"
db.init_app(app)
bootstrap = Bootstrap4(app)


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_name = db.Column(db.String(250), unique=True, nullable=False)
    book_author = db.Column(db.String(250), nullable=False)
    rating = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f'<Book {self.title}>'


with app.app_context():
    db.create_all()






class BookForm(FlaskForm):
    book_name = StringField('Book Name', validators=[DataRequired()])
    book_author = StringField("Book Author", validators=[DataRequired()])
    rating = StringField("Rating", validators=[DataRequired()])
    add_book = SubmitField("Add Book")





@app.route('/')
def home():
    book_form = BookForm()
    result = db.session.execute(db.select(Book).order_by(Book.book_name))
    all_books = result.scalars(result)
    return render_template("index.html", books=all_books)


@app.route("/edit", methods=["GET", "POST"])
def edit():
    if request.method == "POST":
        book_id = request.form["id"]
        book_to_update = db.get_or_404(Book, book_id)
        book_to_update.rating = request.form["rating"]
        db.session.commit()
        return redirect(url_for('home'))
    book_id = request.args.get('id')
    book_selected = db.get_or_404(Book, book_id)
    return render_template("edit.html", book=book_selected)


@app.route("/delete")
def delete():
    book_id = request.args.get('id')
    book_to_delete = db.get_or_404(Book, book_id)
    db.session.delete(book_to_delete)
    db.session.commit()
    return redirect(url_for('home'))





@app.route("/add", methods=["GET", "POST"])
def add():
    book_form = BookForm()
    if book_form.validate_on_submit():
        book_name = book_form.book_name.data
        book_author = book_form.book_author.data
        rating = book_form.rating.data
        with app.app_context():
            new_books = Book(book_name=book_name, book_author=book_author, rating=rating)
            db.session.add(new_books)
            db.session.commit()
        return redirect(url_for("home"))
    return render_template("add.html", form=book_form)


if __name__ == "__main__":
    app.run(debug=True)

