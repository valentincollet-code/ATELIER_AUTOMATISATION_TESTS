import requests
import time
import os
import sqlite3

# Récupération de la clé API depuis les variables d'environnement
API_KEY = os.environ.get("AVIATION_API_KEY")
URL = f"http://api.aviationstack.com/v1/flights?access_key={API_KEY}"

def sauvegarder_resultat(status, latence):
    """Enregistre le résultat du test dans la base SQLite."""
    try:
        # Connexion à la base (crée le fichier s'il n'existe pas)
        conn = sqlite3.connect('/home/VALPYTHON/mysite/database.db')
        cursor = conn.cursor()
        
        # Création de la table si elle n'existe pas
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS mesures (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                status TEXT,
                latence REAL
            )
        ''')
        
        # Insertion des données
        cursor.execute('INSERT INTO mesures (status, latence) VALUES (?, ?)', (status, latence))
        
        conn.commit()
        conn.close()
        print("Résultats sauvegardés en base de données.")
    except Exception as e:
        print(f"Erreur lors de la sauvegarde SQLite : {e}")

def test_aviation_api_full():
    print("Démarrage du test de monitoring...")
    
    start_time = time.time()
    try:
        # Tentative d'appel à l'API avec un timeout de 10s (Robustesse)
        response = requests.get(URL, timeout=10)
        end_time = time.time()
        latence = round(end_time - start_time, 2)
        
        if response.status_code == 200:
            print(f"Succès ! Latence : {latence}s")
            sauvegarder_resultat("Opérationnel", latence)
        else:
            print(f"Échec API. Code : {response.status_code}")
            sauvegarder_resultat(f"Erreur HTTP {response.status_code}", latence)
            
    except requests.exceptions.Timeout:
        print("Erreur : Timeout atteint.")
        sauvegarder_resultat("Timeout", 10.0)
    except Exception as e:
        print(f"Erreur imprévue : {e}")
        sauvegarder_resultat("Erreur Critique", 0.0)

if __name__ == "__main__":
    # Si tu veux tester manuellement sur PythonAnywhere, 
    # décommente la ligne ci-dessous et mets ta clé :
    # os.environ["AVIATION_API_KEY"] = "867ed1bbe6e245a2531466ce59df34f5"
    
    test_aviation_api_full()
