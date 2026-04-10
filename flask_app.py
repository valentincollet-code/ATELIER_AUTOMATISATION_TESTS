from flask import Flask, render_template
import sqlite3
import os

app = Flask(__name__)

# Chemin vers la base de données (sur PythonAnywhere)
DB_PATH = '/home/VALPYTHON/mysite/database.db'

def get_last_measure():
    """Récupère la dernière ligne enregistrée dans la base de données."""
    try:
        conn = sqlite3.connect(DB_PATH)
        # On demande les résultats sous forme de dictionnaire
        conn.row_factory = sqlite3.Row 
        cursor = conn.cursor()
        
        # On récupère la toute dernière mesure (id le plus grand)
        cursor.execute('SELECT date, status, latence FROM mesures ORDER BY id DESC LIMIT 1')
        row = cursor.fetchone()
        conn.close()
        return row
    except Exception as e:
        print(f"Erreur lecture SQLite : {e}")
        return None

@app.route('/')
def consignes():
    return render_template('consignes.html')

@app.route('/dashboard')
def dashboard():
    derniere_mesure = get_last_measure()
    
    if derniere_mesure:
        stats_api = {
            "nom": "Aviation Stack",
            "status": derniere_mesure['status'],
            "latence": f"{derniere_mesure['latence']}s",
            "derniere_verif": derniere_mesure['date']
        }
    else:
        # Données par défaut si la base est vide
        stats_api = {
            "nom": "Aviation Stack",
            "status": "Aucune donnée",
            "latence": "N/A",
            "derniere_verif": "Jamais"
        }
        
    return render_template('dashboard.html', data=stats_api)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
