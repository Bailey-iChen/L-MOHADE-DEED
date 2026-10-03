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

IHGS_cost, IHGS_emission, length = loadData('12月14号晚上MOHGS_MOHGS-AL-PPSO_DEED_20电机_迭代20000次_N=100/MOHGSwithArchive_fitness_0001_2.txt')
HGS_cost, HGS_emission, HGS_length = loadData('12月14号晚上MOHGS_MOHGS-AL-PPSO_DEED_20电机_迭代20000次_N=100/HGS_pareto_fitness_001_3.txt')

findCompromised = np.zeros([len(IHGS_cost), 2])
findCompromised[:, 0] = IHGS_cost
findCompromised[:, 1] = IHGS_emission
l = FindCompromisedSolution.comprosed_solution(findCompromised)
k = findCompromised[l]

NSGAII_cost = [2.3113 * 10 ** 6]
NSGAII_emission = [7.4791 * 10 ** 5]
#
ABG_MOCDE_cost = [2.3031 * 10 ** 6]
ABG_MOCDE_emission = [7.5437 * 10 ** 5]
#
PSO_cost = [2.4197 * 10 ** 6]
PSO_emission = [8.0625 * 10 ** 6]
#
# MONNDE_cost = [2.4960 * 10 ** 6]
# MONNDE_emission = [7.6735 * 10 ** 5]
#
FBHPSO_DE_cost = [2.3057 * 10 ** 6]
FBHPSO_DE_emission = [8.0455 * 10 ** 5]
#
PSOCS_cost = [2.4023 * 10 ** 6]
PSOCS_emission = [8.0528 * 10 ** 5]
#
MOWOA_WM_cost = [2.3026 * 10 ** 6]
MOWOA_WM_emission = [7.8861 * 10 ** 5]
#
# NSCSO_MH_cost = [2.5010 * 10 ** 6]
# NSCSO_MH_emission = [8.7305 * 10 ** 5]

fig = plt.figure()
ax3 = fig.gca()  # 133
ax3.set_ylabel('Emission(lb)')
ax3.set_xlabel('Cost($)')
plt.ticklabel_format(style='sci', scilimits=(0, 0), axis='both')

ax3.scatter(IHGS_cost, IHGS_emission, s=10, marker=marker_type[0], label='Pareto front of MOHGS-AL',)
ax3.scatter(HGS_cost, HGS_emission, s=10, marker=marker_type[1], label='Pareto front of HGS',)
ax3.scatter(NSGAII_cost, NSGAII_emission, marker=marker_type[2], label='Compromised solution of NSGA-II')
ax3.scatter(ABG_MOCDE_cost, ABG_MOCDE_emission, marker=marker_type[3], label='Compromised solution of ABG-MOCDE')
# ax3.scatter(PSO_cost, PSO_emission, marker=marker_type[4], label='Compromised solution of PSO')
# ax3.scatter(MONNDE_cost, MONNDE_emission, marker=marker_type[5], label='Compromised solution of MONNDE')
ax3.scatter(FBHPSO_DE_cost, FBHPSO_DE_emission, marker=marker_type[6], label='Compromised solution of FBHPSO-DE')
# ax3.scatter(PSOCS_cost, PSOCS_emission, marker=marker_type[7], label='Compromised solution of PSOCS')
ax3.scatter(MOWOA_WM_cost, MOWOA_WM_emission, marker=marker_type[8], label='Compromised solution of MOWOA-WM')
# ax3.scatter(NSCSO_MH_cost, NSCSO_MH_emission, marker=marker_type[9], label='Compromised solution of NSCSO-MH')

plt.annotate("Compromised solution of MOHGS-AL", (findCompromised[l, 0], findCompromised[l, 1]), xycoords='data',
             xytext=(findCompromised[l, 0] + 1000, findCompromised[l, 1] + 35000), arrowprops=dict(arrowstyle='->'))

plt.grid()
plt.legend(loc='upper right')
# plt.show()
plt.savefig('20-units-scatter.svg', format='svg', dpi=1000)
plt.clf()
# plt.show()


