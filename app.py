from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask import send_from_directory
from werkzeug.utils import secure_filename
import os

# simple flask app 
app = Flask(__name__)
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

@app.route('/user/login')
def signup():
    return (render_template('user/user_log_signup.html',title="User1"))

@app.route('/admin')
def adminIndex():
    return (render_template('admin/index.html',title))

if __name__=="__main__":
    # with debug = True:
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.add_url_rule("/uploads/<name>", endpoint="download_file", build_only=True)
    app.run(debug=True, port=8001)

