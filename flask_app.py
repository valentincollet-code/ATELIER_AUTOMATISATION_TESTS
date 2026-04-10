from flask import Flask, render_template_string, render_template, jsonify, request, redirect, url_for, session
from flask import json
from urllib.request import urlopen
from werkzeug.utils import secure_filename
import sqlite3
import os

# --- ÉTAPE A : Importer tes tests ---
# Assure-toi que test_api.py est bien dans le même dossier
try:
    from test_api import test_aviation_api
except ImportError:
    test_aviation_api = None

app = Flask(__name__)

@app.get("/")
def consignes():
     return render_template('consignes.html')

# --- ÉTAPE B : La nouvelle route Dashboard ---
@app.route('/dashboard')
def dashboard():
    # Pour l'instant on utilise des données de test
    # Plus tard, on lira la base de données SQLite (Étape 6)
    stats_api = {
        "nom": "Aviation Stack",
        "status": "Opérationnel",
        "latence": "0.78s",
        "derniere_verif": "10/04/2026"
    }
    return render_template('dashboard.html', data=stats_api)

if __name__ == "__main__":
    # utile en local uniquement
    app.run(host="0.0.0.0", port=5000, debug=True)
