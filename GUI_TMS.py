#!/usr/bin/env python3
import os
from flask import Flask, request, render_template

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ThiIsAOpenSourceProject'

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

@app.route('/')
def home():
    return render_template('upload.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    target = os.path.join(APP_ROOT)
    print(target)

    if not os.path.isdir(target):
        os.mkdir(target)
    
    for file in request.files.getlist("file"):
        print(dir(file))
        filename = file.filename
        print(filename)
        destination = "/".join([target, filename])
        print(destination)
        file.save(destination)

    return render_template('complete.html')

if __name__ == '__main__':
    app.run(debug=True)