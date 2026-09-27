import os
import requests

ODDS_KEY = os.environ.get("ODDS_API_KEY")
BASE = "https://api.the-odds-api.com/v4"

def obtener_cuotas(local, visitante, liga="soccer_spain_la_liga"):
    """Devuelve las cuotas promedio de la casa Pinnacle o similar."""
    url = f"{BASE}/sports/{liga}/odds"
    params = {
        "apiKey": ODDS_KEY,
        "regions": "eu",
        "markets": "h2h",
        "oddsFormat": "decimal",
    }
    r = requests.get(url, params=params)
    if r.status_code != 200:
        return None

    partidos = r.json()
    local_l = local.lower()
    visit_l = visitante.lower()

    for p in partidos:
        home = p.get("home_team", "").lower()
        away = p.get("away_team", "").lower()
        if local_l in home and visit_l in away:
            cuotas = {"home": [], "draw": [], "away": []}
            for book in p.get("bookmakers", []):
                for mkt in book.get("markets", []):
                    if mkt["key"] == "h2h":
                        for out in mkt["outcomes"]:
                            name = out["name"].lower()
                            if name == home:
                                cuotas["home"].append(out["price"])
                            elif name == away:
                                cuotas["away"].append(out["price"])
                            else:
                                cuotas["draw"].append(out["price"])
            return {
                "home": max(cuotas["home"]) if cuotas["home"] else None,
                "draw": max(cuotas["draw"]) if cuotas["draw"] else None,
                "away": max(cuotas["away"]) if cuotas["away"] else None,
            }
    return None
