import json
import os
from flask import Flask, render_template, url_for, abort

app = Flask(__name__)

def get_site_data():
    # This finds the directory where app.py is located
    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_dir, 'data.json')
    
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error: Could not load data.json. {e}")
        return {"projects": {}, "classes": []}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/projects', strict_slashes=False)
def projects():
    data = get_site_data()
    return render_template('projects.html', projects=data.get("projects", {}))

@app.route('/projects/<project_id>', strict_slashes=False)
def project_detail(project_id):
    data = get_site_data()
    project = data.get("projects", {}).get(project_id)
    if not project:
        abort(404)
    return render_template('project_detail.html', project=project)

@app.route('/academics', strict_slashes=False)
def academics():
    data = get_site_data()
    # Pass the list specifically as 'classes'
    return render_template('academics.html', classes=data.get("classes", []))

@app.route('/linktree', strict_slashes=False)
def linktree():
    return render_template('linktree.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html', error_code=404, error_message="Page not found."), 404

#@app.errorhandler(500)
#def server_error(e):
#    return render_template('error.html', error_code=500, error_message="Internal server error."), 500

if __name__ == '__main__':
    app.run(debug=True)