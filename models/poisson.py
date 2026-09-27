import numpy as np
from scipy.stats import poisson

class PoissonModel:
    def __init__(self, lambda_local, lambda_visitante):
        self.ll = lambda_local
        self.lv = lambda_visitante

    def prob_1x2(self, max_goles=6):
        p_l = p_e = p_v = 0.0
        for i in range(max_goles + 1):
            for j in range(max_goles + 1):
                p = poisson.pmf(i, self.ll) * poisson.pmf(j, self.lv)
                if i > j:
                    p_l += p
                elif i == j:
                    p_e += p
                else:
                    p_v += p
        return p_l, p_e, p_v
