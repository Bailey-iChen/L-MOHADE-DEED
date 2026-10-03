import matplotlib.pyplot as plt
import numpy as np
import warnings
from matplotlib.font_manager import FontProperties
warnings.simplefilter("ignore")

def loadData(filePath):
    fr = open(filePath, 'r+')
    lines = fr.readlines()
    length = len(lines)
    
    data_cost = []
    data_emission = []
    for line in lines:
        items = line.strip().split(' ')
        # print(items)
        data_cost.append(float(items[0]))
        data_emission.append(float(items[1]))
    return data_cost, data_emission, length

# pos: pareto-optimal solutions
def comprosed_solution(pos):
    N, M = pos.shape
    max_fitness = np.zeros(M)
    min_fitness = np.zeros(M)
    u = np.zeros([N, M])
    for m in range(M):
        max_fitness[m] = np.max(pos[:, m])
        min_fitness[m] = np.min(pos[:, m])
    for n in range(N):
        for m in range(M):
            if pos[n, m] > max_fitness[m]:
                u[n, m] = 0
            elif min_fitness[m] <= pos[n, m] <= max_fitness[m]:
                u[n, m] = (max_fitness[m] - pos[n, m]) / (max_fitness[m] - min_fitness[m])
            elif pos[n, m] <= min_fitness[m]:
                u[n, m] = 1
    u_temp = np.zeros(N)
    for n in range(N):
        u_temp[n] = np.sum(u[n, :])

    u_last = np.zeros(N)
    # for i in range(N):
    #     u_last[i] = np.sum(u[i, :]) / u_temp[i]

    for i in range(N):
        u_last[i] = np.sum(u[i, :]) / np.sum(u_temp)

    return np.argmax(u_last)
