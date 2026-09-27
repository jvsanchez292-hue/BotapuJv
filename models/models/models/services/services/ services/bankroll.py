def kelly_stake(prob, cuota, bankroll, fraccion=0.25):
    """Kelly fraccionado. fraccion=0.25 → 1/4 Kelly (recomendado)."""
    b = cuota - 1
    p = prob
    q = 1 - p
    if b <= 0:
        return 0.0
    f = (b * p - q) / b
    f = max(0.0, f) * fraccion
    return round(bankroll * f, 2)
