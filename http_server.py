# frontend_server.py
from flask import Flask, send_from_directory
import os

app = Flask(__name__)

# Path to your HTML file
FRONTEND_FOLDER = os.path.abspath(os.path.dirname(__file__))
HTML_FILE = os.path.join(FRONTEND_FOLDER, 'index.html')

@app.route('/')
def serve_frontend():
    return send_from_directory(FRONTEND_FOLDER, 'index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0')  # Different port from your backend