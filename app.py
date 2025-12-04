from flask import Flask, render_template, redirect, url_for, session, flash
from models import db, User, Book
from forms import RegistrationForm, LoginForm, BookForm

""" Flask Basics 7 pts. Complete the code """

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()

""" Flask Basics 7 pts. Implement the route """ 

@app.route('/')  
def index():
    if 'user_id' not in session:
        flash('Please log in first.')
        return redirect(url_for('login'))
    user = User.query.get(session['user_id'])

    """ Flask Basics 7 pts. Complete the return Function """

    return render_template('index.html', user=user) 

@app.route('/register', methods=['GET', 'POST']) 
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        if User.query.filter_by(username=form.username.data).first():
            flash('Username already exists!')
        else:
            user = User(username=form.username.data)
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            flash('Registration successful! Please log in.')
            return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            session['user_id'] = user.id
            flash('Logged in successfully!')
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password')
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('Logged out successfully!')
    return redirect(url_for('login'))

@app.route('/add', methods=['GET', 'POST'])  
def add_book():
    if 'user_id' not in session:
        flash('Please log in first.')
        return redirect(url_for('login'))
    form = BookForm()
    if form.validate_on_submit():
        book = Book(title=form.title.data, author=form.author.data, read=form.read.data, user_id=session['user_id'])
        db.session.add(book)
        db.session.commit()
        flash('Book added successfully!')
        return redirect(url_for('index'))
    return render_template('add_book.html', form=form)