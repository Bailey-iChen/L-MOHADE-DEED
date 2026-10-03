from pathlib import Path
import numpy as np

aaa = np.loadtxt(Path(__file__).resolve().parent / '15_24_G.txt')
GENERATORS_MIN_POWER = np.array([150, 150, 20, 20, 150, 135, 135, 60, 25, 25, 20, 20, 25, 15, 15])
m = aaa[:, 1]
print(aaa[:, 0] - GENERATORS_MIN_POWER)
print('aaaa')