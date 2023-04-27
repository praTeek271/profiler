from flask import Flask,render_template,redirect

app = Flask(__name__, static_url_path='', 
            static_folder='static',
            template_folder='templates')
# admin panel

#-------------------------------*********----------------------------

@app.route('/admin')
def adminIndex():
    return (render_template('admin/index.html'))
#--------------------------------------------------------------------

#upload_page
@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
        return redirect(url_for('uploaded_file', filename=file.filename))
    return render_template('upload.html')

#--------------------------------------------------------------------

@app.route('/user/login')
def signup():
    return (render_template('user/signup.html',title="User1"))
#--------------------------------------------------------------------

def login():
    return(redirect('user/upload.html'))
#--------------------------------------------------------------------
@app.route('/')    
def index():
    return (render_template('index.html',title="Index1"))
#----------------------------------********------------------------

if __name__=='__main__':
    app.run(debug=True)