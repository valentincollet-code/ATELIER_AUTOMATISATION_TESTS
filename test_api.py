import requests
import os

# ⚠️ TRÈS IMPORTANT : Ne mets jamais ta vraie clé en clair dans le code !
# On utilise une variable d'environnement (qu'on configurera dans GitHub Secrets plus tard)
API_KEY = os.environ.get("AVIATION_API_KEY") 
URL = f"http://api.aviationstack.com/v1/flights?access_key={API_KEY}"

def test_aviation_api():
    # On lance la requête
    response = requests.get(URL)
    
    # 1. Assertion sur le statut HTTP (doit être 200 OK)
    assert response.status_code == 200, f"Erreur de statut HTTP: {response.status_code}"
    
    # On convertit la réponse en JSON
    data = response.json()
    
    # 2. Assertions sur le format JSON et les champs attendus
    # On vérifie que la clé "data" existe bien dans la réponse
    assert "data" in data, "Le champ 'data' est manquant dans la réponse JSON"
    
    # On vérifie que 'data' est bien une liste (tableau) de vols
    assert isinstance(data["data"], list), "Le champ 'data' n'est pas une liste"
    
    print("Tous les tests de base sont passés avec succès !")

if __name__ == "__main__":
    # Pour tester en local, tu peux temporairement forcer ta clé ici 
    # mais n'oublie pas de l'effacer avant de faire ton commit !
    # os.environ["AVIATION_API_KEY"] = "ta_vraie_cle_ici" 
    test_aviation_api()
