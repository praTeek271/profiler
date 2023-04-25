from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import os

# simple flask app 
app = Flask(__name__, static_url_path='', 
            static_folder='static',
            template_folder='templates')
#upload_page
@app.route('/upload', methods=['GET', 'POST'])

def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
        return redirect(url_for('uploaded_file', filename=file.filename))
    return render_template('upload.html')
def login():
    
    pass
@app.route('/')
def index():
    return render_template('index.html')



if __name__=="__main__":
    # with debug = True:
    app.debug = True
    app.run()