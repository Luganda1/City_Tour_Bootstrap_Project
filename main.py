from flask import Flask, render_template
import requests
import os

app = Flask(__name__)

ACCESS_KEY = os.environ.get("UNSPLASH_ACCESS_KEY")
SECRET_KEY = os.environ.get("UNSPLASH_SECRETE_KEY")

endpoint = "https://api.npoint.io/de92bcb5772f447e7202"
response = requests.get(url=endpoint)
all_post = response.json()
# print(all_post)

@app.route('/')
def home():
    global all_post
    return render_template('index.html', post=all_post)

@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/blog/<int:item>')
def blog(item):
    global all_post
    request_post = None
    for blog_post in all_post:
        if blog_post["id"] == item:
            request_post = blog_post
    return render_template('blog.html',
                           post=request_post
                           )


if __name__ == "__main__":
    app.run(debug=True)