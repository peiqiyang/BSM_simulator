import numpy as np

def tav(alfa, nr):
    n2 = nr**2
    np_ = n2 + 1
    nm = n2 - 1
    a = (nr + 1)**2 / 2
    k = -((n2 - 1)**2) / 4
    sin_a = np.sin(np.radians(alfa))

    if alfa != 0:
        B2 = sin_a**2 - np_ / 2
        sqrt_arg = B2**2 + k
        B1 = np.zeros_like(B2)
        valid = sqrt_arg > 0
        B1[valid] = np.sqrt(sqrt_arg[valid])
        b = B1 - B2
        b3 = b**3
        a3 = a**3

        ts = (k**2 / (6 * b3) + k / b - b / 2) - (k**2 / (6 * a3) + k / a - a / 2)
        tp1 = -2 * n2 * (b - a) / (np_**2)
        tp2 = -2 * n2 * np_ * np.log(b / a) / (nm**2)
        tp3 = n2 * (1 / b - 1 / a) / 2
        tp4 = 16 * n2**2 * (n2**2 + 1) * np.log((2 * np_ * b - nm**2) / (2 * np_ * a - nm**2)) / (np_**3 * nm**2)
        tp5 = 16 * n2**2 * n2 * (1 / (2 * np_ * b - nm**2) - 1 / (2 * np_ * a - nm**2)) / (np_**3)
        tp = tp1 + tp2 + tp3 + tp4 + tp5
        Tav = (ts + tp) / (2 * sin_a**2)
    else:
        Tav = 4 * nr / ((nr + 1)**2)
    return Tav