import numpy as np
from .soil import soilwat

def BSM(soilpar, spec, emp):
    GSV = spec['GSV']
    kw = spec['Kw']
    nw = spec['nw']

    B = soilpar['B']
    lat = soilpar['lat']
    lon = soilpar['lon']
    SMp = soilpar['SMp']

    SMC = emp['SMC']
    film = emp['film']

    f1 = B * np.sin(np.radians(lat))
    f2 = B * np.cos(np.radians(lat)) * np.sin(np.radians(lon))
    f3 = B * np.cos(np.radians(lat)) * np.cos(np.radians(lon))

    rdry = f1 * GSV[:, 0] + f2 * GSV[:, 1] + f3 * GSV[:, 2]
    rwet = soilwat(rdry, nw, kw, SMp, SMC, film)
    return rdry, rwet