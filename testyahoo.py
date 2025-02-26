import requests

url = "https://finance.yahoo.com"
try:
    response = requests.get(url, timeout=5)
    if response.status_code == 200:
        print("Connexion à Yahoo Finance réussie ! ✅")
    else:
        print(f"Erreur de connexion : Code {response.status_code}")
except requests.ConnectionError:
    print("Impossible de se connecter à Yahoo Finance ❌")