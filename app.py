from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask import send_from_directory
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
import os

# simple flask app
app = Flask(__name__)
# databse connetion
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.sqlite"
# initialize the app with the extension
# app.config['SECERET_KEY']='d7fdaa6ea744c2cefd35ebfe'
db=SQLAlchemy(app)

# create table
bcrypt=Bcrypt(app)  # for password hashing
BASE_DIR=os.path.dirname(os.path.abspath(__file__))
# user class
class User(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(50))
    username=db.Column(db.String(50))
    email=db.Column(db.String(20))
    password=db.Column(db.String(20))


    def __repr__(self):
        return(f'{self.name} | {self.username} | {self.email}')

with app.app_context():
    # db.init_app(app)
    db.create_all()
#upload_page
UPLOAD_FOLDER = "UPLOAD_FOLDER"
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg'}
@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('download_file', name=filename))
    return render_template('user/upload.html')
def allowed_file(filename):
    return ('.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS)
@app.route('/uploads/<name>')
def download_file(name):
    return (send_from_directory(app.config["UPLOAD_FOLDER"], name))


@app.route('/')
def index():
    return(render_template('index.html'))
@app.route('/user/signin', methods=['POST','GET'])
def signin_data_store():
    if request.method=='POST':
        username=request.form['username']
        password=request.form['password']
        if username=="" or password=="":
            flash("Please enter the values properly")
            return redirect(url_for('signup'))
        else:
            user=User().query.filter_by(username=username).first()
            if user and bcrypt.check_password_hash(user.password,password):
                flash("Login Successful")
                return redirect(url_for('userIndex'))
            else:
                flash("Invalid Credentials")
                return redirect(url_for('signup'))
    pass
@app.route('/user/signup', methods=['POST','GET'])
def signup_data_store():
    if request.method=='POST':
        name=request.form['name']
        username=request.form['username']
        email=request.form['email']
        password=request.form['password']

        if name=="" or username=="" or email=="" or password=="":
            flash("Please enter all the fields")
            return redirect(url_for('signup'))

        else:
            data_unique=User().query.filter_by(email=email).first()
            if data_unique:
                flash("Username or Email already taken",'warning')
                print("--------------------------------->\tUsername or Email already taken")
                return redirect(url_for('signup'))
            else:
                hash_password=bcrypt.generate_password_hash(password,10)
                user=User(name=name, username=username, email=email, password=hash_password)
                db.session.add(user)
                db.session.commit()
                flash("User added successfully",'danger')
                flash("Account is Created")
                flash("Please login to continue")
                return redirect(url_for('userIndex'))
    else:
        return redirect(url_for('signup'))

@app.route('/user/login', methods=['POST','GET'])
def signup():
    return(render_template('user/user_log_signup.html',title="User1"))

@app.route('/admin')
def adminIndex():
    return (render_template('admin/index.html',title))

@app.route('/user')
def userIndex():
    return (render_template('user/dashboard.html'))

def is_unique(username,email):
    user=User().query.filter_by(username=username).first()
    email=User().query.filter_by(email=email).first()
    return(user and email)


# @app.route('/upload', methods=('POST',))
# def upload():
#     files = request.files.getlist('files')
#     for file in files:
#         fn = secure_filename(file.filename)
#         file.save(os.path.join(BASE_DIR, fn))  # replace FILES_DIR with your own directory
#     return 'false'  # change to your own logic




if __name__=="__main__":
    # with debug = True:
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.secret_key = 'd7fdaa6ea744c2cefd35ebfe'
    app.add_url_rule("/uploads/<name>", endpoint="download_file", build_only=True)
    app.run(debug=True, port=8001)

    # app.app_context()

