from flask import Flask, render_template
import sqlite3
import os

# --- IMPORT de ton script de test ---
# On importe la fonction de test depuis test_api.py
try:
    from test_api import test_aviation_api_full
except ImportError:
    test_aviation_api_full = None

app = Flask(__name__)

# Chemin absolu vers la base de données sur ton compte PythonAnywhere
DB_PATH = '/home/VALPYTHON/mysite/database.db'

def get_last_measure():
    """Récupère la dernière mesure enregistrée en base SQLite."""
    try:
        if not os.path.exists(DB_PATH):
            return None
            
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row 
        cursor = conn.cursor()
        # On prend la dernière entrée par ID
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

@app.route('/run')
def run_tests_manually():
    """Route pour déclencher le test manuellement via le navigateur."""
    if test_aviation_api_full:
        # On s'assure que la clé est bien présente pour ce run
        # Note : Ta clé est ici en dur pour garantir que le bouton 'Run' fonctionne
        os.environ["AVIATION_API_KEY"] = "867ed1bbe6e245a2531466ce59df34f5"
        
        test_aviation_api_full()
        return "<h1>Test effectué !</h1><p>Les résultats ont été enregistrés en base SQLite.</p><a href='/dashboard'>Consulter le Dashboard</a>"
    else:
        return "Erreur : Script test_api.py introuvable.", 500

@app.route('/dashboard')
def dashboard():
    """Affiche les résultats et l'historique."""
    derniere_mesure = get_last_measure()
    
    if derniere_mesure:
        stats_api = {
            "nom": "Aviation Stack",
            "status": derniere_mesure['status'],
            "latence": f"{derniere_mesure['latence']}s",
            "derniere_verif": derniere_mesure['date']
        }
    else:
        # Données par défaut si la base est encore vide
        stats_api = {
            "nom": "Aviation Stack",
            "status": "En attente de premier run",
            "latence": "N/A",
            "derniere_verif": "Aucune"
        }
        
    return render_template('dashboard.html', data=stats_api)

if __name__ == "__main__":
    # Local uniquement
    app.run(host="0.0.0.0", port=5000, debug=True)
