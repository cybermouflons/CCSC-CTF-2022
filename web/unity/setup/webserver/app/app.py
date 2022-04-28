#!/usr/bin/env python3

import os
from flask import Flask, flash, request, redirect, make_response, redirect, url_for, render_template
from werkzeug.utils import secure_filename
import docx

# Config app
_cwd = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = './uploads/'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'docx'}

# Initialize app
app = Flask(__name__, static_url_path='/static')
app.secret_key = "xl3];+;EbPF#H`!9CZ?*[}WHOCAR3S0{3JSxzCmp7#0>"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# Index Page
@app.route('/', methods=['GET'])
def main():
    return render_template('index.html')


# Submit CV
@app.route('/submission', methods=['POST'])
def submission():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'document' not in request.files:
            flash('Something went wrong!')
            return render_template('index.html')
        file = request.files['document']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash("Please provide a file, I don't have time for games!")
            return render_template('index.html')
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            if filename.rsplit('.', 1)[1].lower() == "docx":
                try:
                    doc = docx.Document("./uploads/" + filename)
                    title = doc.core_properties.title

                    if title == '':
                        flash("Your file (no title provided) has been uploaded successfully!")
                    else:
                        flash("Your file with title " + title + " has been uploaded successfully!")
                    return render_template('index.html')
                except:
                    flash("Corrupted document =(")
            else:
                flash("Your file has been uploaded successfully!")
                return render_template('index.html')
        else:
            flash("Invalid file type")
            return render_template('index.html')
    return render_template('index.html')

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
