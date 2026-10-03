import matplotlib.pyplot as plt
import numpy as np
import FindCompromisedSolution

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

marker_type = ['o', 'v', '^', '<', '>', '8', 's', 'p', '*', 'h', 'H', 'D', 'd', 'P', 'X']

IHGS_cost, IHGS_emission, length = loadData('7月21号晚上MOHGS_MOHGSwithArchive_initial_DEED_15电机_迭代1000次_N=100/MOHGSwithArchive_fitness2.txt')


findCompromised = np.zeros([len(IHGS_cost), 2])
findCompromised[:, 0] = IHGS_cost
findCompromised[:, 1] = IHGS_emission
l = FindCompromisedSolution.comprosed_solution(findCompromised)
k = findCompromised[l]

PSO_cost = [7.0613 * 10 ** 5]
PSO_emission = [3.0773 * 10 ** 5]

ITSA_cost = [7.0136 * 10 ** 5]
ITSA_emission = [2.7037 * 10 ** 5]

PSOCS_cost = [7.1074 * 10 ** 5]
PSOCS_emission = [2.6363 * 10 ** 5]

MONNDE_cost = [7.1164 * 10 ** 5]
MONNDE_emission = [2.7391 * 10 ** 5]

PPSO_cost = [7.2127 * 10 ** 5]
PPSO_emission = [2.6300 * 10 ** 5]

fig = plt.figure()
ax3 = fig.gca()  # 133
ax3.set_ylabel('Emission(lb)')
ax3.set_xlabel('Cost($)')
plt.ticklabel_format(style='sci', scilimits=(0, 0), axis='both')

ax3.scatter(IHGS_cost, IHGS_emission, s=10, marker=marker_type[0], label='Pareto front of HGSwithAL',)
# ax3.scatter(HGS_cost, HGS_emission, s=10, marker=marker_type[1], label='Pareto front of HGS',)
ax3.scatter(PSO_cost, PSO_emission, marker=marker_type[2], label='Compromised solution of PSO')
ax3.scatter(ITSA_cost, ITSA_emission, marker=marker_type[4], label='Compromised solution of ITSA')
ax3.scatter(PSOCS_cost, PSOCS_emission, marker=marker_type[5], label='Compromised solution of PS')
ax3.scatter(MONNDE_cost, MONNDE_emission, marker=marker_type[6], label='Compromised solution of MONNDE')
ax3.scatter(PPSO_cost, PPSO_emission, marker=marker_type[7], label='Compromised solution of PPSO')

plt.annotate("Compromised solution of HGSwithAL", (findCompromised[l, 0], findCompromised[l, 1]), xycoords='data',
             xytext=(findCompromised[l, 0] + 300, findCompromised[l, 1] + 20000), arrowprops=dict(arrowstyle='->'))

plt.grid()
plt.legend(loc='upper left')
plt.show()


