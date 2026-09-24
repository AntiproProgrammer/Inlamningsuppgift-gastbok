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
<pre>{{ posts }}</pre>
'''

# läs text från JSON-filen och returnera innehållet som en lista
def load_posts():
    if not os.path.exists(JSON_FILE):
        return []
    try:
        with open(JSON_FILE, encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return []   # fel bör egentligen hanteras/meddelas ordentligt, men vi bryr oss inte om detta här

@app.route('/')
def json_demo():
    return render_template_string(HTML, posts=json.dumps(load_posts(), indent=4, ensure_ascii=False))

@app.route('/write-json', methods=['POST'])
def write_json():
    # ta emot listan från load_posts-funktionen och lägg till nytt innehåll
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
    return render_template_string(HTML, posts=json.dumps(posts, indent=4, ensure_ascii=False))

app.run(debug=True)