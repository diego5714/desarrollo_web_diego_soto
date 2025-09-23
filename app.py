from flask import Flask, request, render_template, redirect, url_for
from markupsafe import escape

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/form')
def publication_form():
    return render_template('form.html')

@app.route('/publications')
def publication_list():
    return render_template('publication_list.html')

@app.route('/publication')
def publication():
    return render_template('publication.html')

@app.route('/image')
def image():
    return render_template('image.html')

@app.route('/statistics')
def statistics():
    return render_template('statistics.html')