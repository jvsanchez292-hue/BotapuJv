import os
import requests
from services.ligas import normalizar_nombre

API_KEY = os.environ.get("RAPIDAPI_KEY")
HOST = "v3.football.api-sports.io"
BASE = f"https://{HOST}"

HEADERS = {
    "X-RapidAPI-Key": API_KEY,
    "X-RapidAPI-Host": HOST,
}

def buscar_fixture(local, visitante, fecha=None):
    """Busca un partido por nombres de equipos en los próximos 20 fixtures."""
    local = normalizar_nombre(local).lower()
    visitante = normalizar_nombre(visitante).lower()

    url = f"{BASE}/fixtures"
    params = {"next": 30}
    r = requests.get(url, headers=HEADERS, params=params)
    if r.status_code != 200:
        return None

    data = r.json().get("response", [])
    for fx in data:
        home = fx["teams"]["home"]["name"].lower()
        away = fx["teams"]["away"]["name"].lower()
        if (local in home or home in local) and (visitante in away or away in visitante):
            return {
                "id": fx["fixture"]["id"],
                "liga": fx["league"]["name"],
                "raw": fx,
            }
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
