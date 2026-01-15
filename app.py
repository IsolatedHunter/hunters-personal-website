import json
from flask import Flask, render_template, url_for, abort

app = Flask(__name__)

# Helper function to read your "laptop-managed" database
def get_projects_data():
    try:
        with open('projects.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/projects', strict_slashes=False)
def projects():
    # Pass the database content to the projects grid
    data = get_projects_data()
    return render_template('projects.html', projects=data)

@app.route('/projects/<project_id>', strict_slashes=False)
def project_detail(project_id):
    # This route handles EVERY individual project page automatically
    data = get_projects_data()
    project = data.get(project_id)
    
    if not project:
        abort(404) # Trigger the error handler if ID doesn't exist
        
    return render_template('project_detail.html', project=project)

@app.route('/linktree', strict_slashes=False)
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