from flask import Flask,render_template

app=Flask(__name__)

@app.route('/admin')
def adminIndex():
    return (render_template('admin/index.html'))



@app.route('/user')

def userIndex():
    return (render_template('user/index.html',title="User1"))

@app.route('/')    
def index():
    
    return (render_template('index.html',title="Index1"))


if __name__=='__main__':
    app.run(debug=True)