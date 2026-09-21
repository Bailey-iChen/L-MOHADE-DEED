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

IHGS_cost, IHGS_emission, length = loadData('10月4号晚上MOHGSwithAL_DEED_6电机_迭代5000次_N=100/MOHGSwithArchive_fitness_0001_2.txt')
HGS_cost, HGS_emission, HGS_length = loadData('10月4号晚上MOHGS_DEED_6电机_迭代5000次_N=100/HGS_pareto_fitness_01_0.txt')

findCompromised = np.zeros([len(IHGS_cost), 2])
findCompromised[:, 0] = IHGS_cost
findCompromised[:, 1] = IHGS_emission
l = FindCompromisedSolution.comprosed_solution(findCompromised)
k = findCompromised[l]

# HGS_cost = [29319.4]
# HGS_emission = [7.37745]

GSOMP_cost = [25924.45557]
GSOMP_emission = [6.004125]

MAMODE_cost = [25912.89419]
MAMODE_emission = [5.979548]

HS_NPSA_cost = [26751.55730]
HS_NPSA_emission = [6.12362]

DHS_cost = [26530.57997]
DHS_emission = [5.92523]

MHS_cost = [26764.70886]
MHS_emission = [5.93908]

NEHS_cost = [26295.93182]
NEHS_emission = [5.72755]

FBHPSO_DE_cost = [27196.3581]
FBHPSO_DE_emission = [6.0982]

MOWOA_WM_cost = [29330.23444]
MOWOA_WM_emission = [7.3099]

fig = plt.figure()
ax3 = fig.gca()  # 133
ax3.set_ylabel('Emission(lb)')
ax3.set_xlabel('Cost($)')
plt.ticklabel_format(style='sci', scilimits=(0, 0), axis='both')

ax3.scatter(IHGS_cost, IHGS_emission, s=10, marker=marker_type[0], label='Pareto front of MOHGS-AL',)
ax3.scatter(HGS_cost, HGS_emission, s=10, marker=marker_type[10], label='Pareto front of HGS',)
ax3.scatter(GSOMP_cost, GSOMP_emission, marker=marker_type[2], label='Compromised solution of GSOMP')
ax3.scatter(MAMODE_cost, MAMODE_emission, marker=marker_type[3], label='Compromised solution of MAMODE')
ax3.scatter(HS_NPSA_cost, HS_NPSA_emission, marker=marker_type[4], label='Compromised solution of HS-NPSA')
ax3.scatter(DHS_cost, DHS_emission, marker=marker_type[5], label='Compromised solution of DHS')
ax3.scatter(MHS_cost, MHS_emission, marker=marker_type[6], label='Compromised solution of MHS')
ax3.scatter(NEHS_cost, NEHS_emission, marker=marker_type[7], label='Compromised solution of NEHS')
# ax3.scatter(SA_cost, SA_emission, marker=marker_type[8], label='Compromised solution of SA')
ax3.scatter(MOWOA_WM_cost, MOWOA_WM_emission, marker=marker_type[1], label='Compromised solution of MOWOA-WM')
ax3.scatter(FBHPSO_DE_cost, FBHPSO_DE_emission, marker=marker_type[8], label='Compromised solution of FBHPSO-DE')
# ax3.scatter(NSCSO_MH_cost, NSCSO_MH_emission, marker=marker_type[9], label='Compromised solution of NSCSO-MH')

# plt.annotate("Compromised solution of MOHGS-AL", (findCompromised[l, 0], findCompromised[l, 1]), xycoords='data',
#              xytext=(findCompromised[l, 0] - 100, findCompromised[l, 1] - 0.2), arrowprops=dict(arrowstyle='->'))

plt.grid()
plt.legend(loc='upper right')
plt.savefig('6-units-scatter.svg', format='svg', dpi=1000)
plt.clf()
# plt.show()


