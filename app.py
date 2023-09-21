from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_user, logout_user, LoginManager
from werkzeug.utils import secure_filename
import pandas as pd
import os
from User_model.model import  db, User
from auth import check_password
from werkzeug.security import check_password_hash



UPLOAD_FOLDER = os.path.join('staticFiles', 'uploads')
ALLOWED_EXTENSIONS = {'csv'}

app = Flask(__name__)
app.config['uploads'] = UPLOAD_FOLDER
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

db.init_app(app)

app.secret_key = "5fbc9997cf8d1d040e27fe9494781d28"


@app.route('/', methods=['GET', 'POST'])
def uploadFile():
    if request.method == 'POST':
        f = request.files.get('file')
        data_filename = secure_filename(f.filename)
        f.save(os.path.join(UPLOAD_FOLDER, data_filename))
        session['uploaded_data_file_path'] = os.path.join(UPLOAD_FOLDER, data_filename)
        return render_template('index2.html')
    
    return render_template("index.html")

@app.route('/show_data')
def showData():
    data_file_path = session.get('uploaded_data_file_path', None)
    uploaded_df = pd.read_csv(data_file_path, encoding='unicode_escape')
    uploaded_df_html = uploaded_df.to_html()
    return render_template('show_csv_data.html', data_var=uploaded_df_html)

@app.route('/login', methods=['GET','POST'])
def login_sign():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        existing_user = User.query.filter_by(email=email).first()
        if existing_user and existing_user.check_password(password):
            return redirect(url_for('uploadFile'))
    return render_template('signup.html')

@app.route('/add_user', methods=['GET','POST'])
def add_user():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return  redirect(url_for('login_sign'))
        new_user = User(email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        return  redirect(url_for('login_sign'))

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
