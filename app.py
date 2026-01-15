from flask import Flask, render_template, url_for

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/projects')
def projects():
    return render_template('projects.html')

@app.route('/linktree')
def linktree():
    return render_template('linktree.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html', 
                           error_code=404, 
                           error_message="We couldn't find the page you were looking for."), 404

@app.errorhandler(500)
def server_error(e):
    return render_template('error.html', 
                           error_code=500, 
                           error_message="Our server is having a moment. Please try again later."), 500

if __name__ == '__main__':
    app.run(debug=True)