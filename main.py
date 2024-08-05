from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import random
import string

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///urls.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Urls(db.Model):
    id_ = db.Column("id_", db.Integer, primary_key=True)
    long = db.Column("long", db.String(), unique=True)
    short = db.Column("short", db.String(3), unique=True)

    def __init__(self, long, short):
        self.long = long
        self.short = short

tables_created = False

@app.before_request
def create_tables():
    global tables_created
    if not tables_created:
        db.create_all()
        tables_created = True

def shortern_url(length=3):
    """Generate a random string of fixed length for the short URL."""
    letters_and_digits = string.ascii_letters + string.digits
    while True:
        rand_letters = ''.join(random.choices(letters_and_digits, k=length))
        if not Urls.query.filter_by(short=rand_letters).first():
            return rand_letters

@app.route('/', methods=['POST', 'GET'])
def home():
    if request.method == "POST":
        url_received = request.form['nm']
        found_url = Urls.query.filter_by(long=url_received).first()
        if found_url:
            return redirect(url_for("display_short_url", url=found_url.short))
        else:
            short_url = shortern_url()
            new_url = Urls(url_received, short_url)
            db.session.add(new_url)
            db.session.commit()
            return redirect(url_for("display_short_url", url=short_url))
    else:
        return render_template("home.html")

@app.route('/display/<url>')
def display_short_url(url):
       return render_template('shorturl.html', short_url_display=url)  # Corrected variable name

@app.route('/<short_url>')
def redirection(short_url):
    long_url = Urls.query.filter_by(short=short_url).first()
    if long_url:
         return redirect(long_url.long)
    else:
         return f'<h1'>'Url doesnt exist</h1>'

if __name__ == "__main__":
    app.run(port=5000, debug=True)
