import json
import os
import traceback
from flask import Flask, render_template, abort, request

app = Flask(__name__)

# Allow routes to be accessed with or without trailing slashes
app.url_map.strict_slashes = False

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def load_json_data(filename):
    file_path = os.path.join(BASE_DIR, filename)
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Database file '{filename}' is missing at {file_path}")
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

@app.route('/')
def home():
    return render_template('index.html', title="Home")

@app.route('/portfolio')
def portfolio():
    # Load your new JSON structure
    data = load_json_data('portfolio_data.json')
    # Pass the list of entries
    return render_template('portfolio.html', entries=data['entries'])

@app.route('/portfolio/<int:entry_id>')
def portfolio_detail(entry_id):
    data = load_json_data('portfolio_data.json')
    # Access by list index
    entry = data['entries'][entry_id]
    return render_template('portfolio_detail.html', project=entry)

@app.route('/resume')
def resume():
    return render_template('resume.html')

@app.route('/academics')
def academics():
    try:
        data = load_json_data('academics.json')
        # Ensure we are passing a list to the template
        course_list = data if isinstance(data, list) else data.get("classes", [])
        return render_template('academics.html', classes=course_list, title="Academics")
    except Exception as e:
        print(f"Error loading academics: {e}")
        abort(500)

@app.route('/linktree')
def linktree():
    return render_template('linktree.html', title="Links")

# --- Error Handlers ---

@app.errorhandler(Exception)
def handle_error(e):
    error_code = getattr(e, 'code', 500)
    
    error_messages = {
        404: "The page you're looking for has vanished into a black hole.",
        500: "Our server encountered a glitch in the simulation."
    }
    
    error_message = error_messages.get(error_code, f"Error {error_code} occurred.")
    
    tb = traceback.format_exc() if error_code == 500 else "N/A"
    
    return render_template('error.html', 
        error_code=error_code, 
        error_message=error_message,
        traceback=tb
    ), error_code

if __name__ == '__main__':
    app.run(debug=True)