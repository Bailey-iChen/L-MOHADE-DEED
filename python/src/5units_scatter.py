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

IHGS_cost, IHGS_emission, length = loadData('7月21号早上MOHGS_MOHGSwithArchive_initial_DEED_5电机_迭代1000次_N=100/MOHGSwithArchive_fitness2.txt')
HGS_cost, HGS_emission, HGS_length = loadData('7月21号早上MOHGS_MOHGSwithArchive_initial_DEED_5电机_迭代1000次_N=100/HGS_pareto_fitness2.txt')

findCompromised = np.zeros([len(IHGS_cost), 2])
findCompromised[:, 0] = IHGS_cost
findCompromised[:, 1] = IHGS_emission
l = FindCompromisedSolution.comprosed_solution(findCompromised)
k = findCompromised[l]

PSO_cost = [5.0893 * 10 ** 4]
PSO_emission = [2.0163 * 10 ** 4]

MOWOA_WM_cost = [4.6962 * 10 ** 4]
MOWOA_WM_emission = [2.0848 * 10 ** 4]

ITSA_cost = [4.5971 * 10 ** 4]
ITSA_emission = [1.8370 * 10 ** 4]

PS_cost = [4.7911 * 10 ** 4]
PS_emission = [1.8927 * 10 ** 4]

MONNDE_cost = [4.9884 * 10 ** 4]
MONNDE_emission = [1.8647 * 10 ** 4]

PPSO_cost = [4.89369 * 10 ** 4]
PPSO_emission = [2.3685 * 10 ** 4]

FBHPSO_DE_cost = [5.1118 * 10 ** 4]
FBHPSO_DE_emission = [1.9191 * 10 ** 4]

NSCSO_MH_cost = [4.7497 * 10 ** 4]
NSCSO_MH_emission = [1.8172 * 10 ** 4]

fig = plt.figure()
ax3 = fig.gca()  # 133
ax3.set_ylabel('Emission(lb)')
ax3.set_xlabel('Cost($)')
plt.ticklabel_format(style='sci', scilimits=(0, 0), axis='both')

ax3.scatter(IHGS_cost, IHGS_emission, s=10, marker=marker_type[0], label='Pareto front of MOHGS-AL',)
ax3.scatter(HGS_cost, HGS_emission, s=10, marker=marker_type[1], label='Pareto front of HGS',)
ax3.scatter(PSO_cost, PSO_emission, marker=marker_type[2], label='Compromised solution of PSO')
ax3.scatter(MOWOA_WM_cost, MOWOA_WM_emission, marker=marker_type[3], label='Compromised solution of MOWOA-WM')
ax3.scatter(ITSA_cost, ITSA_emission, marker=marker_type[4], label='Compromised solution of ITSA')
ax3.scatter(PS_cost, PS_emission, marker=marker_type[5], label='Compromised solution of PS')
ax3.scatter(MONNDE_cost, MONNDE_emission, marker=marker_type[6], label='Compromised solution of MONNDE')
ax3.scatter(PPSO_cost, PPSO_emission, marker=marker_type[7], label='Compromised solution of PPSO')
ax3.scatter(FBHPSO_DE_cost, FBHPSO_DE_emission, marker=marker_type[8], label='Compromised solution of FBHPSO-DE')
ax3.scatter(NSCSO_MH_cost, NSCSO_MH_emission, marker=marker_type[9], label='Compromised solution of NSCSO-MH')

plt.annotate("Compromised solution of MOHGS-AL", (findCompromised[l, 0], findCompromised[l, 1]), xycoords='data',
             xytext=(findCompromised[l, 0] + 300, findCompromised[l, 1] + 20000), arrowprops=dict(arrowstyle='->'))

plt.grid()
plt.legend(loc='upper left')
plt.savefig('5-units-scatter.svg', format='svg', dpi=1000)
plt.clf()
# plt.show()


