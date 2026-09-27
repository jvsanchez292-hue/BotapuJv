def detectar_value_bet(prob_modelo, cuota, margen_min=0.05):
    if cuota <= 1:
        return {"es_value": False, "edge": 0, "EV": 0, "prob_implicita": 1}

    prob_implicita = 1 / cuota
    ev = (prob_modelo * (cuota - 1)) - (1 - prob_modelo)
    edge = prob_modelo - prob_implicita

    return {
        "prob_implicita": prob_implicita,
        "edge": edge,
        "EV": ev,
        "es_value": ev > margen_min,
    }
