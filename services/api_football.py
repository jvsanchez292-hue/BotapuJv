import os
import requests

API_KEY = os.environ.get("RAPIDAPI_KEY")
HOST = "v3.football.api-sports.io"
BASE = f"https://{HOST}"

HEADERS = {
    "X-RapidAPI-Key": API_KEY,
    "X-RapidAPI-Host": HOST,
}

def buscar_fixture(local, visitante, fecha=None):
    """Busca un partido por nombres de equipos."""
    url = f"{BASE}/fixtures"
    params = {"next": 20}
    r = requests.get(url, headers=HEADERS, params=params)
    if r.status_code != 200:
        return None

    data = r.json().get("response", [])
    local_l = local.lower()
    visit_l = visitante.lower()

    for fx in data:
        home = fx["teams"]["home"]["name"].lower()
        away = fx["teams"]["away"]["name"].lower()
        if local_l in home and visit_l in away:
            return {"id": fx["fixture"]["id"], "raw": fx}
    return None

def obtener_prediccion(fixture_id):
    """Obtiene la predicción de API-Football."""
    url = f"{BASE}/predictions"
    params = {"fixture": fixture_id}
    r = requests.get(url, headers=HEADERS, params=params)
    if r.status_code != 200:
        return None
    data = r.json().get("response", [])
    return data[0] if data else None
