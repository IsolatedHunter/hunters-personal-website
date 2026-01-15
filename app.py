import json
import os
from flask import Flask, render_template, abort

app = Flask(__name__)

# --- Data Management ---
# We load the data once at the global level to improve performance
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, 'data.json')

def load_static_data():
    """Helper to load the JSON file with error handling."""
    if not os.path.exists(DATA_FILE):
        return {"projects": {}, "classes": []}
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return {"projects": {}, "classes": []}

# Load data into memory when the server starts
site_data = load_static_data()

# --- Routes ---

@app.route('/')
def home():
    return render_template('index.html', title="Home")

@app.route('/projects')
def projects():
    # Access the projects dictionary from our loaded data
    project_list = site_data.get("projects", {})
    return render_template('projects.html', projects=project_list, title="Projects")

@app.route('/projects/<project_id>')
def project_detail(project_id):
    project = site_data.get("projects", {}).get(project_id)
    if not project:
        abort(404)
    return render_template('project_detail.html', project=project, title=project.get('title'))

@app.route('/academics')
def academics():
    # Pass the list of classes directly to the new template
    course_list = site_data.get("classes", [])
    return render_template('academics.html', classes=course_list, title="Academics")

@app.route('/linktree')
def linktree():
    return render_template('linktree.html', title="Links")

# --- Error Handling ---

@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html', error_code=404, error_message="Page not found."), 404

if __name__ == '__main__':
    app.run(debug=True)