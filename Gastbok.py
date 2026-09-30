from flask import Flask, request, render_template_string
import json, os
from datetime import datetime

app = Flask(__name__)
JSON_FILE = 'data.json'

HTML = '''
<h2>Nytt inlägg</h2>
<form method="post" action="/write-json">
    <h3>Namn</h3>
    <input name="namn">
    <h3>Meddelande</h3>
    <textarea name="meddelande" rows="6" cols="40"></textarea><br>
    <input type="submit" value="Spara">
</form>
<h2>Inlägg</h2>
{% for post in posts %}
    <div style="border: 1px solid #ccc; padding: 10px; margin-bottom: 10px;">
        <strong>{{ post.namn }}</strong>
        <small style="color: #666;"> – {{ post.tid }}</small>
        <p style="white-space: pre-wrap;">{{ post.meddelande }}</p>
    </div>
{% else %}
    <p>Inga inlägg ännu.</p>
{% endfor %}
'''


def load_posts():
    if not os.path.exists(JSON_FILE):
        return []
    try:
        with open(JSON_FILE, encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return []  
@app.route('/')
def json_demo():
    return render_template_string(HTML, posts=load_posts())

@app.route('/write-json', methods=['POST'])
def write_json():
    posts = load_posts()
    posts.append({
        'namn': request.form.get('namn', ''),
        'meddelande': request.form.get('meddelande', ''),
        'tid': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    })
    # vi kan hantera variabeln posts som en vanlig Python-lista, t.ex.
    print(posts[0]['namn'] + ' skrev följande meddelande: ' + posts[0]['meddelande'])
    # spara den uppdaterade listan som text i JSON-fil
    with open(JSON_FILE, 'w', encoding='utf-8') as f:
        json.dump(posts, f, indent=4, ensure_ascii=False)
    return render_template_string(HTML, posts=posts)

app.run(debug=True)