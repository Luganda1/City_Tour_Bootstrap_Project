from flask import Flask, render_template, request, redirect, url_for, flash
import requests

import os
import datetime as dt
from selenium import webdriver
import smtplib
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import abort
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, URL
from flask_ckeditor import CKEditor, CKEditorField
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Table, Column, Integer, ForeignKey
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from form import CreatePostForm, RegisterForm, LoginForm, AddComment
from functools import wraps
from flask_gravatar import Gravatar
from pprint import pprint
import time



app = Flask(__name__)
# chrome_driver_path = r"C:\Users\tramr\OneDrive\Desktop\website\development\chromedriver.exe"
# driver = webdriver.Chrome(executable_path=chrome_driver_path)
GMAIL = os.environ.get('GMAIL')
PASSWORD = os.environ.get('GMAIL_PASSWORD')
ACCESS_KEY = os.environ.get("UNSPLASH_ACCESS_KEY")
SECRET_KEY = os.environ.get("UNSPLASH_SECRETE_KEY")
app.config['SECRET_KEY'] = os.environ.get("APP_SECRET_KEY")
ckeditor = CKEditor(app)
Bootstrap(app)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///city_posts.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
admin = "Tonny"
gravatar = Gravatar(app,
                    size=100,
                    rating='g',
                    default='retro',
                    force_default=False,
                    force_lower=False,
                    use_ssl=False,
                    base_url=None)


# Create the User Table
class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(100))
    # This will act like a List of BlogPost objects attached to each User.
    # The "author" refers to the author property in the BlogPost class.
    posts = relationship("City", back_populates="author")
    comments = relationship("Comment", back_populates="comments_author")

# Create all the tables in the database
db.create_all()


##CONFIGURE TABLE
class City(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(250), unique=True, nullable=False)
    name = db.Column(db.String(250), nullable=False)
    subtitles = db.Column(db.String(250), nullable=False)
    date = db.Column(db.String(250), nullable=False)
    info = db.Column(db.Text, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    #Create reference to the User object, the "posts" refers to the posts protperty in the User class.
    author = relationship("User", back_populates="posts")
    img = db.Column(db.String(250), nullable=False)

    comments = relationship("Comment", back_populates="parent_post")


    def __repr__(self):
        return f'<City {self.city}'

db.create_all()


class Comment(db.Model):
    __tablename__ = "comments"
    id = db.Column(db.Integer, primary_key=True)
    # *******Add child relationship*******#
    # "users.id" The users refers to the tablename of the Users class.
    # "comments" refers to the comments property in the User class.
    author_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    comments_author = relationship("User", back_populates="comments")
    #***************Child Relationship*************#
    post_id = db.Column(db.Integer, db.ForeignKey("city.id"))
    parent_post = relationship("City", back_populates="comments")
    text = db.Column(db.String(250), nullable=False)

db.create_all()


##WTForm
class CreatePostForm(FlaskForm):
    city = StringField("City", validators=[DataRequired()])
    name = StringField("Location", validators=[DataRequired()])
    subtitles = StringField("Subtitle", validators=[DataRequired()])
    author = StringField("Your Name", validators=[DataRequired()])
    img = StringField("Image", validators=[DataRequired(), URL()])
    info = CKEditorField('Story Content')
    submit = SubmitField("Submit Post")

#
# try:
#     new_city = City(
#         city="new york",
#         date="02/12/2007",
#         name="new york bridge tour",
#         author="hamid datsan",
#         subtitles=f" I fell in love with the magestic view that city gave me. To find this place I have to walk "
#                   f"Hoboken Train Station, for taking this pic I had to wait for about 2 hours,",
#         info=f"Lorem ipsum, dolor sit amet consectetur adipisicing elit. Tenetur, nam omnis error corrupti eum "
#              f"assumenda enim odit architecto corporis. Sequi     Lorem ipsum dolor sit amet, consectetur adipiscing "
#              f"elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis "
#              f"nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in "
#              f"reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat "
#              f"cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.",
#         img="https://images.unsplash.com/photo-1496442226666-8d4d0e62e6e9?ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufD
#         B8fHx8&ixlib=rb-1.2.1&auto=format&fit=crop&w=750&q=80",
#     )
#     # db.session.add(new_city)
#     # db.session.commit()
# except IntegrityError:
#     pass


# endpoint = "https://api.npoint.io/de92bcb5772f447e7202"
# all_post = requests.get(url=endpoint).json()

#Create admin-only decorator
def admin_only(function):
    @wraps(function)
    def decorated_function(*args, **kwargs):
        # If id is not 3 then return abort with 403 error
        if current_user.id != 1:
            return abort(403)
        # Otherwise continue with the route function
        return function(*args, **kwargs)
    return decorated_function


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/')
def home():
    global admin
    all_post = City.query.all()
    return render_template('index.html', post=all_post, current_user=current_user, admin=admin)


@app.route('/about')
def about():
    return render_template('about.html', current_user=current_user)



@app.route('/register', methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        email = form.email.data
        user = User.query.filter_by(email=email).first()
        if user:
            return redirect(url_for('login', id=user.id))

        hash_and_salted_password = generate_password_hash(
            form.password.data,
            method='pbkdf2:sha256',
            salt_length=8
        )

        new_user = User(
            email=form.email.data,
            name=form.name.data,
            password=hash_and_salted_password,
        )
        db.session.add(new_user)
        db.session.commit()

        login_user(new_user)
        return redirect(url_for("home"))
    return render_template("register.html", form=form, current_user=current_user)


@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    email_correct = False
    user_id = request.args.get('id')
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user = User.query.filter_by(email=email).first()
        if not user:
            flash("That email does not exist, please try again.")
            return redirect(url_for('login'))
            # Password incorrect
        elif not check_password_hash(user.password, password):
            flash('Password incorrect, please try again.')
            return redirect(url_for('login'))
        else:
            login_user(user)
            # flash('Logged in successfully.')
            return redirect(url_for('home'))
    return render_template("login.html", form=form, user=user_id, current_user=current_user)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/new_post", methods=['POST', 'GET'])
@admin_only
def new_post():
    form = CreatePostForm()
    if form.validate_on_submit():
        if request.method == "POST":
            new_city = City(
                city=form.city.data,
                date=dt.datetime.now().strftime("%b %d %Y"),
                name=form.name.data,
                # author=form.author.data,
                subtitles=form.subtitles.data,
                info=form.info.data,
                img=form.img.data,
            )
            db.session.add(new_city)
            db.session.commit()
            return redirect(url_for('home'))
    return render_template('new_post.html', form=form, current_user=current_user)


@app.route('/edit_post', methods=['POST', 'GET'])
@admin_only
def edit_post():
    blog_id = request.args.get('id')
    post_to_edit = City.query.get(blog_id)
    post_form = CreatePostForm(
        city=post_to_edit.city,
        name=post_to_edit.name,
        subtitles=post_to_edit.subtitles,
        author=current_user,
        info=post_to_edit.info,
        img=post_to_edit.img,
    )
    if post_form.validate_on_submit():
        if request.method == "POST":
            post_to_edit.city = post_form.city.data
            post_to_edit.name = post_form.name.data
            post_to_edit.subtitles = post_form.subtitles.data
            post_to_edit.info = post_form.info.data
            post_to_edit.img = post_form.img.data
            db.session.commit()
            return redirect(url_for("blog", id=post_to_edit.id))

    return render_template('edit_post.html', form=post_form, post=post_to_edit, is_edit=True, current_user=current_user)


@app.route('/contact', methods=['POST', 'GET'])
def contact():
    if request.method == "POST":
        data = request.form
        try:
            with smtplib.SMTP("smtp.gmail.com", port=587) as connection:

                connection.starttls()
                connection.login(user=GMAIL, password=PASSWORD)
                connection.sendmail(
                    from_addr=GMAIL,
                    to_addrs=data["email"],
                    msg=f"Subject: Message from {data['name']}\n\n {data['message'].encode('utf-8',errors='ignore')}"
                )
        except smtplib.SMTPAuthenticationError:
            print("Error enable less secure apps in google")
        # except UnicodeEncodeError:
        #     print("'ascii' codec can't encode character")

        return render_template('contact.html', msg_sent=True)
    return render_template('contact.html', msg_sent=False, current_user=current_user)


@app.route('/blog', methods=['GET', 'POST'])
def blog():
    global admin
    blog_id = request.args.get('id')
    city_post = City.query.get(blog_id)

    form = AddComment()

    if form.validate_on_submit():
        if not current_user.is_authenticated:
            flash("You need to login or register to comment.")
            return redirect(url_for("login"))
        new_comment = Comment(
            text=form.comment.data,
            comments_author=current_user,
            parent_post=city_post
        )
        db.session.add(new_comment)
        db.session.commit()

    comments = Comment.query.all()
    date = dt.datetime.now().strftime("%b %d %Y")
    return render_template('blog.html', post=city_post, form=form,
                           current_user=current_user, admin=admin, date=date)


@app.route('/delete_comment')
def delete_comment():
    comment_id = request.args.get('id')
    comment = Comment.query.get(comment_id)
    db.session.delete(comment)
    db.session.commit()
    return redirect(url_for('home'))


@app.route('/delete')
@admin_only
def delete():
    blog_id = request.args.get('id')
    city_post = City.query.get(blog_id)
    db.session.delete(city_post)
    db.session.commit()
    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(debug=True)

    '''

    IP address 0.0.0.0 is an invalid address: From Wikipedia: In the Internet Protocol Version 4, 
    the address 0.0.0.0 is a non-routable meta-address used to designate an invalid, unknown or 
    non-applicable target.You will have to change it to the IP address of the computer you are 
    running the server on. For most of us this will be the loop-back address 127.0.0.1 which is 
    also designated "localhost". Also FYI, the port number could be anything in the range 1 to 65535. 
    Ports 1 to 1023 are historically assigned to other processes (or reserved for future use), 
    and you all also find that some are often assigned to common protocols, such as SMTP: 465, 587 or 2525. 
    So you should be aware of possible conflicts with your chosen port number.



Form macro reference

quick_form(form, action=".", method="post", extra_classes=None, role="form", form_type="basic", 
horizontal_columns=('lg', 2, 10), enctype=None, button_map={}, id="")

    Outputs Bootstrap-markup for a complete Flask-WTF form.
    Parameters:	

        form – The form to output.
        method – <form> method attribute.
        extra_classes – The classes to add to the <form>.
        role – <form> role attribute.
        form_type – One of basic, inline or horizontal. See the Bootstrap docs for details on different form layouts.
        horizontal_columns – When using the horizontal layout, layout forms like this. Must be a 3-tuple of (column-type,
         left-column-size, right-colum-size).enctype – <form> enctype attribute. If None, will automatically be set to 
         multipart/form-data if a FileField is present in the form.button_map – A dictionary, mapping button field 
         names to names such as primary, danger or success. Buttons not found in the button_map will use the default 
         type of button.
        id 
    '''