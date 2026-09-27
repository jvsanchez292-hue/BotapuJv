LIGAS = {
    "La Liga": "soccer_spain_la_liga",
    "Premier League": "soccer_epl",
    "Champions League": "soccer_uefa_champs_league",
    "Liga 1 Perú": "soccer_peru_primera_division",
    "NBA": "basketball_nba",
}

# Nombres alternativos → nombre oficial API-Football
ALIAS_EQUIPOS = {
    "real madrid": "Real Madrid",
    "barcelona": "Barcelona",
    "bayern": "Bayern Munich",
    "bayern munich": "Bayern Munich",
    "psg": "Paris Saint Germain",
    "man city": "Manchester City",
    "man utd": "Manchester United",
    "manchester united": "Manchester United",
    "liverpool": "Liverpool",
    "chelsea": "Chelsea",
    "arsenal": "Arsenal",
    "juventus": "Juventus",
    "inter": "Inter",
    "milan": "AC Milan",
    "ac milan": "AC Milan",
    "alemanía": "Germany",
    "alemania": "Germany",
    "grecia": "Greece",
}

def normalizar_nombre(nombre):
    """Devuelve el nombre oficial de un equipo según los alias."""
    return ALIAS_EQUIPOS.get(nombre.strip().lower(), nombre.strip())
