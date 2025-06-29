import numpy as np
from scipy.stats import poisson
from .tav import tav

def soilwat(rdry, nw, kw, SMp, SMC, deleff):
    k_vals = np.arange(7)
    mu = (SMp - 5) / SMC
    if mu <= 0:
        return rdry

    tav_2 = tav(90, 2.0)
    tav_n = tav(90, 2.0 / nw)
    rbac = 1 - (1 - rdry) * (rdry * tav_n / tav_2 + 1 - rdry)

    p = 1 - tav(90, nw) / nw**2
    Rw = 1 - tav(40, nw)

    fmul = poisson.pmf(k_vals, mu)
    tw = np.exp(-2 * kw[:, None] * deleff * k_vals)
    Rwet_k = Rw[:, None] + (1 - Rw[:, None]) * (1 - p[:, None]) * tw * rbac[:, None] / (1 - p[:, None] * tw * rbac[:, None])
    rwet = rdry * fmul[0] + Rwet_k[:, 1:] @ fmul[1:]
    return rwet