#upload_page
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg'}

class Upload:
    def __init__(self,folder='/uploads'):
        self.app = app
        self.app.config['UPLOAD_FOLDER'] = BASE_DIR + os.path.join(BASE_DIR, '{0}'.format(folder))
        self.app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

    def allowed_file(filename):
        return('.' in filename and \
            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS)


    def upload_file():
        if request.method == 'POST':
            # check if the post request has the file part
            if 'file' not in request.files:
                flash('No file part')
                return(redirect(request.url))
            file = request.files['file']
            # If the user does not select a file, the browser submits an
            # empty file without a filename.
            if file.filename == '':
                flash('No selected file')
                return(redirect(request.url))
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                return(redirect(url_for('download_file', name=filename)))
        return '''
        <!doctype html>
        <title>Upload new File</title>
        <h1>Upload new File</h1>
        <form method=post enctype=multipart/form-data>
        <input type=file name=file>
        <input type=submit value=Upload>
        </form>
        '''


    def download_file(name):
        return(send_from_directory(app.config["UPLOAD_FOLDER"], name))


