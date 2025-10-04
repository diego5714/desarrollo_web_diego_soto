from flask import Flask, request, render_template, redirect, url_for
from markupsafe import escape

UPLOAD_FOLDER = 'static/upload'

app: Flask = Flask(__name__)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# Rutas de la aplicación ###################################################
@app.route('/')
def index() -> str:
    return render_template('index.html')

@app.route('/form')
def publication_form() -> str:
    return render_template('form.html')

@app.route('/publications')
def publication_list() -> str:
    return render_template('publication_list.html')

@app.route('/publication')
def publication() -> str:
    return render_template('publication.html')

@app.route('/image')
def image() -> str:
    return render_template('image.html')

@app.route('/statistics')
def statistics() -> str:
    return render_template('statistics.html')