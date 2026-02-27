
import json
import os
import traceback
import secrets
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv # type: ignore
from flask import Flask, render_template, abort, request, flash, redirect, url_for

load_dotenv()
app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY")

# Allow routes to be accessed with or without trailing slashes
app.url_map.strict_slashes = False

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def send_email(type, name, email, role, phone, message):
    msg = EmailMessage()
    msg["Subject"] = f'New Contact Form "{type}"'
    msg["From"] = os.getenv("EMAIL_ADDRESS")
    msg["To"] = "hunter.bradshaw@my.utsa.edu"

    msg.set_content(f"""
New contact form submission:

Name: {name}
Email: {email}
Phone: {phone}
Role: {role}
Message:
{message}

""")

    with smtplib.SMTP_SSL(
        os.getenv("EMAIL_HOST"),
        int(os.getenv("EMAIL_PORT"))
    ) as server:
        server.login(
            os.getenv("EMAIL_ADDRESS"),
            os.getenv("EMAIL_PASSWORD")
        )
        server.send_message(msg)

def load_json_data(filename):
    file_path = os.path.join(BASE_DIR, filename)
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Database file '{filename}' is missing at {file_path}")
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def title_to_slug(title):
    """Convert title to URL-friendly slug"""
    return title.lower().strip().replace(' ', '-').replace('&', 'and')

@app.route('/')
def index():
    return render_template('index.html', title="Home")

@app.route('/privacy')
def privacy():
    return render_template('privacy.html', title="Privacy & Terms")

@app.route('/portfolio')
def portfolio():
    # Load your new JSON structure
    data = load_json_data('portfolio_data.json')
    # Pass the list of entries
    return render_template('portfolio.html', entries=data['entries'])

@app.route('/.well-known/discord')
def discord_redirect():
    return 'dh=3a0dd37e7d4b5bcafb306c32b5b3ec01c39cf5fd'

@app.route('/portfolio/<slug>')
def portfolio_detail(slug):
    data = load_json_data('portfolio_data.json')
    # Find entry by matching slug to title
    for entry in data['entries']:
        if title_to_slug(entry['title']) == slug:
            return render_template('portfolio_detail.html', project=entry)
    abort(404)

@app.route('/c')
def c_redirect():
    return redirect(url_for('campaign'))

@app.route('/campaign')
def campaign():
    return render_template('campaign.html')

@app.route('/campaign/join', methods=['GET', 'POST'])
def join_campaign():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        role = request.form.get('role')
        phone = request.form.get('phone')
        type = "Join Campaign"
        message = request.form.get('message')
        send_email(type, name, email, role, phone, message)
        flash(f"We've received your information, {name}! \nThank you for joining the campaign. We'll be in touch soon.", "success")
    return render_template('join.html')

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

@app.route('/editor')
def editor():
    return render_template('description_editor.html')

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