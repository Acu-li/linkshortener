# File: app.py
from flask import Flask, request, redirect, render_template_string
import os
import pyperclip

# --- Config ---
DOMAIN = '343.im'
TXT_PATH = 'urls.txt'

# Load existing links from TXT_PATH
links = {}
if os.path.exists(TXT_PATH):
    with open(TXT_PATH, 'r', encoding='utf-8') as f:
        for line in f:
            alias, url = line.strip().split(' ', 1)
            links[alias] = url

app = Flask(__name__)

# HTML Template as string with pastel styling and English text
INDEX_HTML = '''
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>343.im</title>
  <style>
    /* Dark background and pastel accents */
    body { background: #111; color: #ffb6c1; font-family: sans-serif; text-align: center; padding-top: 50px; }
    h1 { font-size: 4rem; margin: 0; }
    p.subtitle { color: #ffb6c1; margin: 10px 0 40px; }
    p.subtitle2 {  color: #add8e6; margin: 10px 0 40px; }
    input, button { padding: 10px; margin: 5px; font-size: 1rem; border-radius: 5px; border: 2px solid #add8e6; }
    input { width: 60%; background: #222; color: #ffb6c1; }
    button { background: #add8e6; color: #111; cursor: pointer; }
    a { color: #add8e6; margin: 0 10px; text-decoration: none; }
    .message { margin-top:20px; color: #ffb6c1; }
  </style>
</head>
<body>
  <h1>343.im</h1>
  <p class="subtitle">The link shortener nobody asked for. UwU</p>
  <form method="POST">
    <input name="original_url" placeholder="Paste your URL here" required><br>
    <input name="alias" placeholder="Custom alias" required><br>
    <button type="submit">Shorten</button>
  </form>
  {% if message %}
    <div class="message">{{ message }}</div>
  {% endif %}
  <br>
  <br>
  <br>
  <br>
    <p class="subtitle2">I don’t know how long the links will stay active before they reset, but they should last at least a few minutes, lol.</p>
  <footer style="position:fixed; bottom:20px; width:100%;">
    <a href="mailto:admin@acu.li">contact</a>
    <a href="https://rechtliches.acu.li/impressum.html" target="_blank">Imprint</a>
    <a href="https://rechtliches.acu.li/dsgvo.html" target="_blank">Privacy</a>
  </footer>
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def index():
    message = None

    if request.method == 'POST':
        original = request.form.get('original_url', '').strip()
        alias = request.form.get('alias', '').strip()
        if not original or not alias:
            message = 'Please fill out both fields.'
        elif alias in links:
            message = 'Alias already exists.'
        else:
            # persist to file and memory
            links[alias] = original
            with open(TXT_PATH, 'a', encoding='utf-8') as f:
                f.write(f"{alias} {original}\n")
            short_url = f"https://{DOMAIN}/{alias}"
            try:
                pyperclip.copy(short_url)
            except Exception:
                pass
            message = 'Copied :)'

    return render_template_string(INDEX_HTML, message=message)

@app.route('/<alias>')
def redirect_short(alias):
    url = links.get(alias)
    if url:
        return redirect(url)
    return '404 Not Found', 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
