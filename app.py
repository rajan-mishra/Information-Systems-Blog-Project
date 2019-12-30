from flask import Flask, render_template
from flask_bootstrap import Bootstrap

app = Flask(__name__)
Bootstrap(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/blogs')
def blogs():
    return render_template('blogs.html')

@app.route('/editblogs')
def editblogs():
    return render_template('editblogs.html')

@app.route('/deleteblogs')
def deleteblogs():
    return render_template('deleteblogs.html')

@app.route('/myblogs')
def myblogs():
    return render_template('myblogs.html')

@app.route('/logout')
def logout():
    return render_template('logout.html')

@app.route('/writeblog')
def writeblog():
    return render_template('writeblog.html')

if __name__ == '__main__' :
    app.run(debug = True)
