from flask import Flask,render_template,flash,redirect,url_for,session,request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import UserMixin
from wtforms import Form,StringField,TextAreaField,PasswordField,validators
from passlib.hash import sha256_crypt
from flask_login import login_required, current_user

class RegisterForm(Form):
    name=StringField("Name Surname:",validators=[validators.Length(min=6, max=30)])
    email = StringField("E-mail Address:",validators=[validators.Email(message="Please enter a valid e-mail address!")])
    password = PasswordField("Password:",validators=[
        validators.DataRequired("Please Set A Password."),
        validators.length(min=8)
        #validators.EqualTo(fieldname="Confirm your password.",message="Passwords are not same.")        
    ])
    confirm=PasswordField("Password Validation:")

class LoginForm(Form):
    email=StringField("Email")
    password=PasswordField("Password")

class BookForm(Form):
    book_name=StringField("Title:",validators=[validators.Length(min=1, max=150)])
    author=StringField("Author:",validators=[validators.Length(min=6, max=150)])
    content=TextAreaField("Content:",validators=[validators.Length(min=8)])

app=Flask(__name__)

app.config['SECRET_KEY']= 'elif is here'  #encrypt or secure the cookies and session data related to our website
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Eyh23894@localhost:5432/Bookworm_DB'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db=SQLAlchemy()
db.init_app(app)

migrate = Migrate(app, db)

class Users(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password

    def __repr__(self):
        return '<id {}>'.format(self.id)

class Books(db.Model, UserMixin):
    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    book_name = db.Column(db.String(150), nullable=False)
    author = db.Column(db.String(150), nullable=False)
    content = db.Column(db.String(400), nullable=False)

    def __init__(self, book_name, author, content):
        self.book_name = book_name
        self.author = author
        self.content = content

    def __repr__(self):
        return '<id {}>'.format(self.id)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/book/<string:id>")
def book(id):
    book = Books.query.filter_by(id=id).one()
    return render_template("book.html",book=book)

@app.route("/books")
def books():
    books=Books.query.order_by(Books.id.asc()).all()
    return render_template("books.html",books=books)

@app.route("/register",methods=["GET","POST"])
def register():
    form = RegisterForm(request.form)
    if(request.method=="POST" and form.validate()):
        name=form.name.data
        email=form.email.data
        password = sha256_crypt.encrypt(form.password.data)

        user = Users.query.filter_by(email=email).first()
        if user:
            flash('E-mail already exist!')
            return redirect(url_for("register"))

        new_user = Users(name=name,email=email,password=password)
        db.session.add(new_user)
        db.session.commit()
        flash('You have successfully signed in!',"success")
        return redirect(url_for("login"))
    else:
        return render_template("register.html",form=form)


@app.route("/login",methods=["GET","POST"])
def login():
    form = LoginForm(request.form)
    if(request.method=="POST"):
        email=form.email.data
        password = form.password.data

        user = Users.query.filter_by(email=email).first()
        if user:
            if sha256_crypt.verify(password,user.password):
                session["logged_in"] = True
                session["email"] = email
                flash("You have successfully logged in!","success")
                #session["id"] = id
                #print(session.get("id"))
                return redirect(url_for("index"))
            else:
                flash("Wrong password!","danger")
                return redirect(url_for("login"))

    return render_template("login.html", user=current_user,form=form)

@login_required
@app.route("/dashboard")
def dashboard():
    books=Books.query.order_by(Books.id.asc()).all()
    return render_template("dashboard.html",books=books)

@login_required
@app.route("/addbook",methods=["GET","POST"])
def addbook():
    form=BookForm(request.form)
    if request.method=="POST" and form.validate:
        book_name = form.book_name.data
        author=form.author.data
        content = form.content.data

        book = Books.query.filter_by(book_name=book_name).first()
        if book:
            flash('Book already exist!')
            return redirect(url_for("addbook"))

        new_book = Books(book_name=book_name,author=author,content=content)
        db.session.add(new_book)
        db.session.commit()
        flash("The book successfully saved!","success")
        return redirect(url_for("dashboard"))
    return render_template("addbook.html",form=form)

@login_required
@app.route("/delete/<string:id>")
def delete(id):
    book = Books.query.filter_by(id=id).one()
    db.session.delete(book)
    db.session.commit()
    flash("The book deleted!","success")
    return redirect(url_for("dashboard"))

@login_required
@app.route("/logout")
def logout():
    session.clear()
    flash("You logged out!","success")
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)


"""
@login_required
@app.route("/myprofile/<string:id>")
def myprofile(id):
    user = Users.query.filter_by(id=current_user.id).one()
    return render_template("myprofile.html",user=user)

@login_required
@app.route("/edit/<string:id>",methods=["GET","POST"])
def edit(id):
    if request.method == "GET":
        book = Books.query.filter_by(id=id).one()
        form =BookForm()
        form.book_name.data = book["book_name"]
        form.author.data = book["author"]
        form.content.data = book["content"]
        return render_template("update.html",form = form)
    else:
    
        book = Books.query.filter_by(id=id).one()
        form = BookForm(request.form)
        editedbook_name=form.book_name.data
        editedauthor = form.author.data
        editedcontent=form.content.data
        book = Books(book_name=editedbook_name,author=editedauthor,content=editedcontent)
        db.session.add(book)
        db.session.commit()
        flash("Kitap başarılı bir şekilde güncellendi","success")
        return redirect(url_for("dashboard"))
"""






