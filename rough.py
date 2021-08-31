import requests
import os

from flask_sqlalchemy import SQLAlchemy
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.common.keys import Keys
from pprint import pprint
import time
import datetime as dt
#
# EMAIL = ""
# PASSWORD = ""
# CITY = "New York"
# chrome_driver_path = r"C:\Users\tramr\OneDrive\Desktop\website\development\chromedriver.exe"
# driver = webdriver.Chrome(executable_path=chrome_driver_path)
#
# driver.get("https://unsplash.com/")
# time.sleep(2)
# #seacrhibg for the city
# driver.find_element_by_name('searchKeyword').send_keys(CITY)
# time.sleep(1)
# driver.find_element_by_class_name('_3d86A').click()
# time.sleep(1)
# # selecting landscape format
# driver.find_element_by_xpath('//*[@id="popover-search-orientation-filter"]/button/span').click()
# driver.find_element_by_xpath('//*[@id="popover-search-orientation-filter"]/div/div/ul/li[2]/a/div/div/div').click()
#
'''
  <form action="{{url_for('edit_post')}}" method="post" class="form" role="form" novalidate>
                  {{ form.csrf_token() }}

                  {{ wtf.form_field(form.city, placeholder=post.city) }}
                  {{ wtf.form_field(form.name, placeholder=post.name) }}
                  {{ wtf.form_field(form.author, placeholder=post.author) }}
                  {{ wtf.form_field(form.img, placeholder=post.img) }}
                  {{ wtf.form_field(form.subtitles, placeholder=post.subtitles) }}
                  {{ wtf.form_field(form.info, placeholder="Description Content") }}
                    <p><input type=submit class='btn btn-primary btn-block'>
                </form>
'''

# date = dt.datetime.now().strftime("%b %d %Y")
#
# print(date)

# Base = declarative_base()
# class User(Base):
#     """User model."""
#     id = Column(Integer, primary_key=True)
#     name = Column(Unicode, nullable=False)
#     picture = image_attachment('UserPicture')
#     __tablename__ = 'user'
# class UserPicture(Base, Image):
#     """User picture model."""
#     user_id = Column(Integer, ForeignKey('user.id'), primary_key=True)
#     user = relationship('User')
#     __tablename__ = 'user_picture'

#
# import os
# from flask import Flask, flash, request, redirect, url_for
# from werkzeug.utils import secure_filename
#
# UPLOAD_FOLDER = r'C:\Users\tramr\OneDrive\Pictures'
# ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
#
# app = Flask(__name__)
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
#
# def allowed_file(filename):
#     return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
#
# @app.route('/', methods=['GET', 'POST'])
# def upload_file():
#     if request.method == 'POST':
#         # check if the post request has the file part
#         file = request.files['file']
#         if 'file' not in request.files or file.filename == '':
#             flash('No file')
#             return redirect(request.url)
#         if file and allowed_file(file.filename):
#             filename = secure_filename(file.filename)
#             file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
#             return redirect(url_for('uploaded_file', filename=filename))
#     return '''
#       <!doctype html>
#       <title>Upload new File</title>
#       <h1>Upload new File</h1>
#       <form method=post enctype=multipart/form-data>
#         <input type=file name=file>
#         <input type=submit value=Upload>
#       </form>
#       '''
#
# if __name__ == "__main__":
#     app.run(debug=True)

#
# from flask import Flask, request, Response, render_template
# from werkzeug.utils import secure_filename
#
#
# app = Flask(__name__)
# # SQLAlchemy config. Read more: https://flask-sqlalchemy.palletsprojects.com/en/2.x/
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///img.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db = SQLAlchemy(app)
#
#
# class Img(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     img = db.Column(db.Text, unique=True, nullable=False)
#     name = db.Column(db.Text, nullable=False)
#     mimetype = db.Column(db.Text, nullable=False)
#     def __repr__(self):
#         return f'<Img {self.img}'
#
# db.create_all()
#
#
# @app.route('/')
# def hello_world():
#     return 'Hello, World!'
#
#
# @app.route('/upload', methods=['POST'])
# def upload():
#     pic = request.files['pic']
#     if pic:
#         filename = secure_filename(pic.filename)
#         mimetype = pic.mimetype
#         if not filename or not mimetype:
#             return 'Bad upload!', 400
#
#         img = Img(img=pic.read(), name=filename, mimetype=mimetype)
#         db.session.add(img)
#         db.session.commit()
#
#         # return 'Img Uploaded!', 200
#     return render_template('upload.html')
#
# @app.route('/<int:id>')
# def get_img(id):
#     img = Img.query.filter_by(id=id).first()
#     if not img:
#         return 'Img Not Found!', 404
#
#     return Response(img.img, mimetype=img.mimetype)
#
# if __name__ == "__main__":
#     app.run(debug=True)
#













