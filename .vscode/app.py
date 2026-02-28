from flask import Flask, render_template_string, request, redirect, url_for
import mysql.connector
from mysql.connector import Error
import random, time

app = Flask(__name__)


def get_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",         
            password="At25032007@",  
            database="pokemon_db"  
        )
        return connection
    except Error as e:
        print(" Database connection failed:", e)
        return None



def get_image_url(pokemon_name):
    return f"https://img.pokemondb.net/artwork/large/{pokemon_name.lower()}.jpg"



@app.route('/')
def home():
    html = '''
    <html>
    <head>
        <title>Pokémon World</title>
        <style>
            body {
                font-family: 'Trebuchet MS', sans-serif;
                background-image: url('https://wallpapercave.com/wp/wp1990544.png');
                background-size: cover;
                color: white;
                
                text-align: center;
            }
            h1 { color: #ffcb05; text-shadow: 3px 3px 6px #2a75bb; margin-top: 60px; font-size: 50px; }
            .menu {
                display: flex;
                justify-content: center;
                gap: 40px;
                margin-top: 40px;
            }
            .menu a {
                background-color: rgba(0,0,0,0.6);
                color: white;
                padding: 15px 25px;
                border-radius: 12px;
                text-decoration: none;
                font-size: 20px;
                transition: 0.3s;
                box-shadow: 0 0 15px rgba(255,255,255,0.2);
            }
            .menu a:hover {
                background-color: #ffcb05;
                color: black;
                transform: scale(1.1);
            }
            footer {
                position: fixed;
                bottom: 10px;
                width: 100%;
                color: black;
                font-size: 14px;
            }
        </style>
    </head>
    <body>
        <h1>Welcome to the Pokemon World 🌍</h1>
        <div class="menu">
            <a href="/pokedex">Pokedex</a>
            <a href="/evolution">Evolution</a>
            <a href="/battle">Battle Arena</a>
            <a href="/quiz">Pokemon Quiz</a>
            <a href="/exit">Exit</a>
        </div>
        <footer>© 2025 Pokémon Database | Built with ❤️ by Atharva</footer>
    </body>
    </html>
    '''
    return render_template_string(html)


@app.route('/pokedex')
def pokedex():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM pokedata")
    pokes = cursor.fetchall()
    cursor.close()
    conn.close()

    html = '''
    <html>
    <head>
        <title>Pokédex</title>
        <style>
            body { font-family: Arial; background: linear-gradient(to bottom,#f8f9fa,#b0e0e6); text-align: center; }
            .grid { display: flex; flex-wrap: wrap; justify-content: center; }
            .card {
                width: 180px; margin: 10px; padding: 10px; background: white;
                border-radius: 12px; box-shadow: 0 4px 8px rgba(0,0,0,0.1);
                transition: transform .2s; text-align: center;
            }
            .card:hover { transform: scale(1.1); }
            img { width: 120px; height: 120px; }
            a { text-decoration: none; color: black; }
            h1 { color: #e3350d; }
        </style>
    </head>
    <body>
        <h1>Pokedex</h1>
        <a href="/">Back</a>
        <div class="grid">
            {% for p in pokes %}
            <div class="card">
                <a href="/pokedex/{{p.sno}}">
                    <img src="{{get_image_url(p.pokemon_name)}}" alt="{{p.pokemon_name}}">
                    <div><b>{{p.pokemon_name}}</b><br>{{p.type}}</div>
                </a>
            </div>
            {% endfor %}
        </div>
    </body>
    </html>
    '''
    return render_template_string(html, pokes=pokes, get_image_url=get_image_url)


@app.route('/pokedex/<int:poke_id>')
def pokemon_detail(poke_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM pokedata WHERE sno=%s", (poke_id,))
    p = cursor.fetchone()
    cursor.close()
    conn.close()

    if not p:
        return "<h1>Pokemon not found!</h1>"

    html = '''
    <html>
    <head>
        <title>{{p.pokemon_name}} Details</title>
        <style>
            body {
                font-family: 'Segoe UI', sans-serif;
                background: linear-gradient(135deg, #c3ecb2, #7dd3fc);
                text-align: center;
                padding: 40px;
            }
            .card {
                display: inline-block;
                background: white;
                padding: 30px;
                border-radius: 20px;
                box-shadow: 0 4px 15px rgba(0,0,0,0.2);
                width: 350px;
                transition: transform 0.3s;
            }
            .card:hover { transform: scale(1.05); }
            img { width: 180px; height: 180px; border-radius: 10px; }
            h1 { color: #e63946; }
            .info { text-align: left; margin-top: 20px; font-size: 18px; color: #333; }
            a {
                display: inline-block;
                margin-top: 20px;
                text-decoration: none;
                background: #ffcb05;
                color: black;
                padding: 10px 20px;
                border-radius: 10px;
                font-weight: bold;
            }
        </style>
    </head>
    <body>
        <div class="card">
            <img src="{{get_image_url(p.pokemon_name)}}" alt="{{p.pokemon_name}}">
            <h1>{{p.pokemon_name}}</h1>
            <div class="info">
                <b>Type:</b> {{p.type}}<br>
                <b>Speciality:</b> {{p.speciality}}<br>
                <b>Level:</b> {{p.level}}<br>
                <b>Region:</b> {{p.most_prominent_region}}<br>
                 <b>Has mega evolution:</b> {{p.has_mega_evolution}}<br>
            </div>
            <a href="/pokedex">Back to Pokédex</a>
        </div>
    </body>
    </html>
    '''
    return render_template_string(html, p=p, get_image_url=get_image_url)


@app.route('/evolution')
def evolution():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM pokedata LIMIT 20")
    pokes = cursor.fetchall()
    cursor.close()
    conn.close()

    html = '''
    <html>
    <head>
        <title>Pokémon Evolution</title>
        <style>
            body { font-family: Verdana; background: #e0f7fa; text-align: center; }
            .evo {
                display: flex; flex-wrap: wrap; justify-content: center;
                gap: 40px; margin-top: 30px;
            }
            .chain {
                background: white; border-radius: 10px; padding: 15px;
                box-shadow: 0 4px 10px rgba(0,0,0,0.2);
            }
            img { width: 100px; height: 100px; margin: 0 5px; }
            h2 { color: #d32f2f; }
        </style>
    </head>
    <body>
        <h1>Pokémon Evolution</h1>
        <a href="/"> Back</a>
        <div class="evo">
            {% for p in pokes %}
            <div class="chain">
                <h2>{{p.pokemon_name}}</h2>
                <div>
                    {% if p.evolution_1 %}<img src="{{get_image_url(p.evolution_1)}}">{% endif %}
                    {% if p.evolution_2 %}<img src="{{get_image_url(p.evolution_2)}}">{% endif %}
                    {% if p.evolution_3 %}<img src="{{get_image_url(p.evolution_3)}}">{% endif %}
                </div>
            </div>
            {% endfor %}
        </div>
    </body>
    </html>
    '''
    return render_template_string(html, pokes=pokes, get_image_url=get_image_url)



@app.route('/battle', methods=['GET', 'POST'])
def battle():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM pokedata LIMIT 30")
    pokes = cursor.fetchall()
    cursor.close()
    conn.close()

    winner = None
    p1 = p2 = None

    if request.method == 'POST':
        p1_id = int(request.form['pokemon1'])
        p2_id = int(request.form['pokemon2'])
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM pokedata WHERE sno=%s", (p1_id,))
        p1 = cursor.fetchone()
        cursor.execute("SELECT * FROM pokedata WHERE sno=%s", (p2_id,))
        p2 = cursor.fetchone()
        cursor.close()
        conn.close()

        
        if p1['level'] > p2['level']:
            winner = p1
        elif p2['level'] > p1['level']:
            winner = p2
        else:
            winner = random.choice([p1, p2])

    html = '''
    <html>
    <head>
        <title>Battle Arena</title>
        <style>
            body { background: url('https://wallpapercave.com/wp/wp2757874.gif'); background-size: cover; color: white; text-align: center; font-family: Arial; }
            h1 { color: #ffcb05; text-shadow: 3px 3px 6px #2a75bb; }
            select, button { padding: 10px; margin: 10px; border-radius: 10px; font-size: 16px; }
            .arena { margin-top: 40px; }
            img { width: 150px; height: 150px; }
            .vs { font-size: 40px; color: red; font-weight: bold; animation: tilt 1s infinite alternate; }
            @keyframes tilt { from { transform: rotate(-5deg); } to { transform: rotate(5deg); } }
        </style>
    </head>
    <body>
        <h1> Online Battle Arena </h1>
        <a href="/">Back</a>
        <form method="POST">
            <select name="pokemon1">
                {% for p in pokes %}<option value="{{p.sno}}">{{p.pokemon_name}}</option>{% endfor %}
            </select>
            <select name="pokemon2">
                {% for p in pokes %}<option value="{{p.sno}}">{{p.pokemon_name}}</option>{% endfor %}
            </select>
            <button type="submit">Battle!</button>
        </form>

        {% if winner %}
        <div class="arena">
            <div>
                <img src="{{get_image_url(p1.pokemon_name)}}">
                <span class="vs">VS</span>
                <img src="{{get_image_url(p2.pokemon_name)}}">
            </div>
            <h2>Deciding Winner...</h2>
            <script>
                setTimeout(function() {
                    document.getElementById("result").style.display = "block";
                }, 3000);
            </script>
            <div id="result" style="display:none;">
                <h1>🏆 Winner: {{winner.pokemon_name}} 🏆</h1>
            </div>
        </div>
        {% endif %}
    </body>
    </html>
    '''
    return render_template_string(html, pokes=pokes, winner=winner, p1=p1, p2=p2, get_image_url=get_image_url)




@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    questions = [
        {"q": "Which Pokémon is known as the Electric Mouse?", "options": ["Pikachu", "Bulbasaur", "Charmander", "Eevee"], "answer": "Pikachu"},
        {"q": "What type is Charizard?", "options": ["Fire/Flying", "Fire/Dragon", "Fire", "Flying"], "answer": "Fire/Flying"},
        {"q": "Which Pokémon can evolve into many different 'Eeveelutions'?", "options": ["Eevee", "Ditto", "Pikachu", "Snorlax"], "answer": "Eevee"},
        {"q": "Who is the Water-type starter of Kanto?", "options": ["Squirtle", "Piplup", "Totodile", "Froakie"], "answer": "Squirtle"},
        {"q": "What is the first evolution of Bulbasaur?", "options": ["Ivysaur", "Venusaur", "Charmander", "Bulbasaur"], "answer": "Ivysaur"},
        {"q": "Which Legendary bird is Fire-type?", "options": ["Moltres", "Zapdos", "Articuno", "Ho-Oh"], "answer": "Moltres"},
        {"q": "Which Pokémon can transform into others?", "options": ["Ditto", "Mew", "Zoroark", "Smeargle"], "answer": "Ditto"},
        {"q": "Which Pokémon is Psychic-type?", "options": ["Alakazam", "Onix", "Machamp", "Scyther"], "answer": "Alakazam"},
        {"q": "What type is Gengar?", "options": ["Ghost/Poison", "Dark", "Psychic", "Fairy"], "answer": "Ghost/Poison"},
        {"q": "What was Ash's first Pokémon?", "options": ["Pikachu", "Charmander", "Squirtle", "Bulbasaur"], "answer": "Pikachu"}
    ]

    selected = random.sample(questions, 5)
    total_q = len(selected)

    if request.method == 'POST':
        posted_n = int(request.form.get("n", total_q))
        score, wrong = 0, []
        for i in range(posted_n):
            user_ans = request.form.get(f"q{i}", "")
            correct_ans = request.form.get(f"a{i}", "")
            if user_ans == correct_ans:
                score += 1
            else:
                wrong.append({"q": request.form.get(f"t{i}", ""), "yours": user_ans, "correct": correct_ans})

        pikachu_img = "https://img.pokemondb.net/artwork/large/pikachu.jpg"
        congrats_gif = "https://media.giphy.com/media/l0MYt5jPR6QX5pnqM/giphy.gif"

        return render_template_string('''
        <!doctype html>
        <html>
        <head><meta charset="utf-8"><title>Quiz Result</title></head>
        <body style="text-align:center;background:#fff7e6;font-family:Arial;">
          <h1>🎯 Quiz Result</h1>
          <h2>You scored {{score}} / {{total}}</h2>
          {% if score == total %}
            <p>🔥 Perfect Trainer! Pikachu is proud of you!</p>
            <img src="{{congrats_gif}}" width="150">
          {% elif score >= (total//2 + 1) %}
            <p>💪 Great job — you're getting stronger!</p>
            <img src="{{pikachu_img}}" width="150">
          {% else %}
            <p>🙂 Not bad — study your Pokédex and try again!</p>
            <img src="{{pikachu_img}}" width="150">
          {% endif %}
          {% if wrong %}
            <h3>Review (what you missed):</h3>
            {% for w in wrong %}
              <div><b>{{loop.index}}.</b> {{w.q}} — Yours: <i>{{w.yours}}</i> | Correct: <b>{{w.correct}}</b></div>
            {% endfor %}
          {% endif %}
          <p><a href="/">Home</a> | <a href="/quiz"> Try Again</a></p>
        </body></html>
        ''', score=score, total=posted_n, wrong=wrong, pikachu_img=pikachu_img, congrats_gif=congrats_gif)

    
    return render_template_string('''
    <!doctype html>
    <html>
    <head><meta charset="utf-8"><title>Pokémon Quiz</title></head>
    <body style="background:#bde0fe;font-family:Arial;padding:30px;">
      <div style="max-width:800px;margin:auto;background:white;padding:24px;border-radius:12px;">
        <h1 style="color:#e63946;text-align:center;">Pokémon Quiz Challenge</h1>
        <form method="post">
          <input type="hidden" name="n" value="{{total}}">
          {% for q in selected %}
            {% set qindex = loop.index0 %}
            <div class="q">
              <b>Q{{loop.index}}. {{q.q}}</b>
              {% for opt in q.options %}
                                  
                <label><input type="radio" name="q{{qindex}}" value="{{opt}}" required> {{opt}}</label><br>
              {% endfor %}
              <input type="hidden" name="a{{qindex}}" value="{{q.answer}}">
              <input type="hidden" name="t{{qindex}}" value="{{q.q}}">
            </div><br>
          {% endfor %}
          <button type="submit" style="padding:10px 20px;background:#ffcb05;border:none;border-radius:10px;">Submit</button>
        </form>
      </div>
    </body></html>
    ''', selected=selected, total=total_q)


@app.route('/exit')
def exit_app():
    html = '''
    <html><head><script>
        setTimeout(function(){ window.close(); }, 1000);
    </script></head>
    <body style="text-align:center;">
        <h1> Goodbye Trainer!</h1>
        <img src="https://wallpapercave.com/wp/wp5376668.png" width="800",height="800">
    </body></html>
    '''
    return html



if __name__ == '__main__':
    app.run(debug=True)


