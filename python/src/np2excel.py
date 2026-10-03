import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
# # --------  5-units  ---------- #

# pos = np.reshape(pos[0], (24, 5))
# data_df = pd.DataFrame(pos)
# writer = pd.ExcelWriter('pos_5units.xlsx')
# data_df.to_excel(writer, 'page_1',float_format='%.2f')
# writer.save()

# --------  6-units  ---------- #
pos = np.loadtxt('10月4号晚上MOHGSwithAL_DEED_6电机_迭代5000次_N=100/MOHGSwithArchive_position_0001_2.txt')
pos = np.reshape(pos[0], (24, 6))
data_df = pd.DataFrame(pos)
writer = pd.ExcelWriter('pos_6units.xlsx')
data_df.to_excel(writer, 'page_1',float_format='%.2f')
writer.save()

# --------  10-units  ---------- #

# pos = np.reshape(pos[0], (24, 10))
# data_df = pd.DataFrame(pos)
# writer = pd.ExcelWriter('pos_10units.xlsx')
# data_df.to_excel(writer, 'page_1',float_format='%.2f')
# writer.save()



def five_unit_bar():
        pos = np.loadtxt('7月21号早上MOHGS_MOHGSwithArchive_initial_DEED_5电机_迭代1000次_N=100/MOHGSwithArchive_position0.txt')
        pos = np.reshape(pos[0], (24, 5))

        width = 0.8
        labels = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18',
                  '19', '20',
                  '21', '22', '23', '24']
        plt.bar(labels,  
                pos[:, 0],  
                width,  
                label='P1',
                color='#a44c40')
        plt.bar(labels,  
                pos[:, 1],  
                width,  
                label='P2',
                bottom=pos[:, 0],
                color='#ffbd35')  
        plt.bar(labels,  
                pos[:, 2],  
                width,  
                label='P3',
                bottom=(pos[:, 1] + pos[:, 0]),
                color='#fcd1a1')  
        plt.bar(labels,  
                pos[:, 3],  
                width,  
                label='P4',
                bottom=(pos[:, 1] + pos[:, 0] + pos[:, 2]),
                color='#5c9eb7')  
        plt.bar(labels,  
                pos[:, 4],  
                width,  
                label='P5',
                bottom=(pos[:, 0] + pos[:, 1] + pos[:, 2] + pos[:, 3]),
                color='#68549d')  

        y_label = pos[:, 0] + pos[:, 1] + pos[:, 2] + pos[:, 3] + pos[:, 4]
        plt.plot(labels, y_label, label='Load + Loss', linestyle='--', color='#4a5e6a')

        plt.ylabel('Power(MW)')
        plt.xlabel('Hour')
        plt.legend()
        plt.savefig('5-units-bar.svg', format='svg', dpi=1000)



def six_unit_bar():
        pos = np.loadtxt('10月4号晚上MOHGSwithAL_DEED_6电机_迭代5000次_N=100/MOHGSwithArchive_position_0001_2.txt')
        pos = np.reshape(pos[0], (24, 6))

        width = 0.8
        labels = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18',
                  '19', '20',
                  '21', '22', '23', '24']
        plt.bar(labels,  
                pos[:, 0],  
                width,  
                label='P1',
                color='#a44c40')
        plt.bar(labels,  
                pos[:, 1],  
                width,  
                label='P2',
                bottom=pos[:, 0],
                color='#ffbd35')  
        plt.bar(labels,  
                pos[:, 2],  
                width,  
                label='P3',
                bottom=(pos[:, 1] + pos[:, 0]),
                color='#fcd1a1')  
        plt.bar(labels,  
                pos[:, 3],  
                width,  
                label='P4',
                bottom=(pos[:, 1] + pos[:, 0] + pos[:, 2]),
                color='#5c9eb7')  
        plt.bar(labels,  
                pos[:, 4],  
                width,  
                label='P5',
                bottom=(pos[:, 0] + pos[:, 1] + pos[:, 2] + pos[:, 3]),
                color='#6ba5a1')  

        plt.bar(labels,  
                pos[:, 5],  
                width,  
                label='P6',
                bottom=(pos[:, 0] + pos[:, 1] + pos[:, 2] + pos[:, 3] + pos[:, 4]),
                color='#68549d')  

        y_label = pos[:, 0] + pos[:, 1] + pos[:, 2] + pos[:, 3] + pos[:, 4] + pos[:, 5]
        plt.plot(labels, y_label, label='Load + Loss', linestyle='--', color='#4a5e6a')

        plt.ylabel('Power(MW)')
        plt.xlabel('Hour')
        plt.legend()
        plt.savefig('6-units-bar.svg', format='svg', dpi=1000)


def ten_unit_bar():
        pos = np.loadtxt('7月20号早上MOHGS_MOHGSwithArchive_DEED_10电机_迭代1000次_N=100/MOHGSwithArchive_position0.txt')
        pos = np.reshape(pos[0], (24, 10))

        width = 0.8
        labels = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18',
                  '19', '20',
                  '21', '22', '23', '24']
        plt.bar(labels,
                pos[:, 0],
                width,
                label='P1',
                color='#a44c40')
        plt.bar(labels,
                pos[:, 1],
                width,
                label='P2',
                bottom=pos[:, 0],
                color='#ffbd35')
        plt.bar(labels,
                pos[:, 2],
                width,
                label='P3',
                bottom=(pos[:, 1] + pos[:, 0]),
                color='#fcd1a1')
        plt.bar(labels,
                pos[:, 3],
                width,
                label='P4',
                bottom=(pos[:, 1] + pos[:, 0] + pos[:, 2]),
                color='#5c9eb7')
        plt.bar(labels,
                pos[:, 4],
                width,
                label='P5',
                bottom=(pos[:, 0] + pos[:, 1] + pos[:, 2] + pos[:, 3]),
                color='#68549d')
        plt.bar(labels,
                pos[:, 5],
                width,
                label='P6',
                bottom=(pos[:, 0] + pos[:, 1] + pos[:, 2] + pos[:, 3] + pos[:, 4]),
                color='#6ba5a1')
        plt.bar(labels,
                pos[:, 6],
                width,
                label='P7',
                bottom=(pos[:, 0] + pos[:, 1] + pos[:, 2] + pos[:, 3] + pos[:, 4] + pos[:, 5]),
                color='#68549d')
        plt.bar(labels,
                pos[:, 7],
                width,
                label='P8',
                bottom=(pos[:, 0] + pos[:, 1] + pos[:, 2] + pos[:, 3] + pos[:, 4] + pos[:, 5] + pos[:, 6]),
                color='#1c8c44')
        plt.bar(labels,
                pos[:, 8],
                width,
                label='P9',
                bottom=(pos[:, 0] + pos[:, 1] + pos[:, 2] + pos[:, 3] + pos[:, 4] + pos[:, 5] + pos[:, 6] + pos[:, 7]),
                color='#c3ffc1')
        plt.bar(labels,
                pos[:, 9],
                width,
                label='P10',
                bottom=(pos[:, 0] + pos[:, 1] + pos[:, 2] + pos[:, 3] + pos[:, 4] + pos[:, 5] + pos[:, 6] + pos[:, 7] + pos[:, 8]),
                color='#D2B48C')

        y_label = pos[:, 0] + pos[:, 1] + pos[:, 2] + pos[:, 3] + pos[:, 4] + pos[:, 5] + pos[:, 6] + pos[:, 7] +\
                  pos[:, 8] + pos[:, 9]
        plt.plot(labels, y_label, label='Load + Loss', linestyle='--', color='#4a5e6a')

        plt.ylabel('Power(MW)')
        plt.xlabel('Hour')
        plt.legend()
        plt.savefig('10-units-bar.svg', format='svg', dpi=1000)

def twenty_unit_bar():
        pos = np.loadtxt('12月14号晚上MOHGS_MOHGS-AL-PPSO_DEED_20电机_迭代20000次_N=100/MOHGSwithArchive_position_0001_2.txt')
        pos = np.reshape(pos[0], (24, 20))

        data_df = pd.DataFrame(pos)
        writer = pd.ExcelWriter('20units.xlsx')
        data_df.to_excel(writer,'page1',float_format='%.2f')
        writer.save()

        width = 0.8
        labels = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18',
                  '19', '20',
                  '21', '22', '23', '24']
        plt.bar(labels,
                pos[:, 0],
                width,
                label='P1',
                )
        plt.bar(labels,
                pos[:, 1],
                width,
                label='P2',
                bottom=pos[:, 0],
                )
        plt.bar(labels,
                pos[:, 2],
                width,
                label='P3',
                bottom=(pos[:, 1] + pos[:, 0]),
                )
        plt.bar(labels,
                pos[:, 3],
                width,
                label='P4',
                bottom=(pos[:, 1] + pos[:, 0] + pos[:, 2]),
                )
        plt.bar(labels,
                pos[:, 4],
                width,
                label='P5',
                bottom=(pos[:, 0] + pos[:, 1] + pos[:, 2] + pos[:, 3]),
                )
        plt.bar(labels,
                pos[:, 5],
                width,
                label='P6',
                bottom=(pos[:, 0] + pos[:, 1] + pos[:, 2] + pos[:, 3] + pos[:, 4]),
                )
        plt.bar(labels,
                pos[:, 6],
                width,
                label='P7',
                bottom=(pos[:, 0] + pos[:, 1] + pos[:, 2] + pos[:, 3] + pos[:, 4] + pos[:, 5]),
                )
        plt.bar(labels,
                pos[:, 7],
                width,
                label='P8',
                bottom=(pos[:, 0] + pos[:, 1] + pos[:, 2] + pos[:, 3] + pos[:, 4] + pos[:, 5] + pos[:, 6]),
                )
        plt.bar(labels,
                pos[:, 8],
                width,
                label='P9',
                bottom=(pos[:, 0] + pos[:, 1] + pos[:, 2] + pos[:, 3] + pos[:, 4] + pos[:, 5] + pos[:, 6] + pos[:, 7]),
                )
        plt.bar(labels,
                pos[:, 9],
                width,
                label='P10',
                bottom=(pos[:, 0] + pos[:, 1] + pos[:, 2] + pos[:, 3] + pos[:, 4] + pos[:, 5] + pos[:, 6] + pos[:, 7] + pos[:, 8]),
                )
        plt.bar(labels,
                pos[:, 10],
                width,
                label='P11',
                bottom=(pos[:, 0] + pos[:, 1] + pos[:, 2] + pos[:, 3] + pos[:, 4] + pos[:, 5] + pos[:, 6] + pos[:, 7] + pos[:, 8] + pos[:, 9]),
                )
        plt.bar(labels,
                pos[:, 11],
                width,
                label='P12',
                bottom=(pos[:, 0] + pos[:, 1] + pos[:, 2] + pos[:, 3] + pos[:, 4] + pos[:, 5] + pos[:, 6] + pos[:, 7] + pos[:, 8] + pos[:, 9] + pos[:, 10]),
                )
        plt.bar(labels,
                pos[:, 12],
                width,
                label='P13',
                bottom=(pos[:, 0] + pos[:, 1] + pos[:, 2] + pos[:, 3] + pos[:, 4] + pos[:, 5] + pos[:, 6] + pos[:, 7] +
                        pos[:, 8] + pos[:, 9] + pos[:, 10] + pos[:, 11]),
                )
        plt.bar(labels,
                pos[:, 13],
                width,
                label='P14',
                bottom=(pos[:, 0] + pos[:, 1] + pos[:, 2] + pos[:, 3] + pos[:, 4] + pos[:, 5] + pos[:, 6] + pos[:, 7] +
                        pos[:, 8] + pos[:, 9] + pos[:, 10] + pos[:, 11] + pos[:, 12]),
                )
        plt.bar(labels,
                pos[:, 14],
                width,
                label='P15',
                bottom=(pos[:, 0] + pos[:, 1] + pos[:, 2] + pos[:, 3] + pos[:, 4] + pos[:, 5] + pos[:, 6] + pos[:, 7] +
                        pos[:, 8] + pos[:, 9] + pos[:, 10] + pos[:, 11] + pos[:, 12] + pos[:, 13]),
                )
        plt.bar(labels,
                pos[:, 15],
                width,
                label='P16',
                bottom=(pos[:, 0] + pos[:, 1] + pos[:, 2] + pos[:, 3] + pos[:, 4] + pos[:, 5] + pos[:, 6] + pos[:, 7] +
                        pos[:, 8] + pos[:, 9] + pos[:, 10] + pos[:, 11] + pos[:, 12] + pos[:, 13] + pos[:, 14]),
                )
        plt.bar(labels,
                pos[:, 16],
                width,
                label='P17',
                bottom=(pos[:, 0] + pos[:, 1] + pos[:, 2] + pos[:, 3] + pos[:, 4] + pos[:, 5] + pos[:, 6] + pos[:, 7] +
                        pos[:, 8] + pos[:, 9] + pos[:, 10] + pos[:, 11] + pos[:, 12] + pos[:, 13] + pos[:, 14] + pos[:, 15]),
                )
        plt.bar(labels,
                pos[:, 17],
                width,
                label='P18',
                bottom=(pos[:, 0] + pos[:, 1] + pos[:, 2] + pos[:, 3] + pos[:, 4] + pos[:, 5] + pos[:, 6] + pos[:, 7] +
                        pos[:, 8] + pos[:, 9] + pos[:, 10] + pos[:, 11] + pos[:, 12] + pos[:, 13] + pos[:, 14] + pos[:, 15] + pos[:, 16]),
                )
        plt.bar(labels,
                pos[:, 18],
                width,
                label='P19',
                bottom=(pos[:, 0] + pos[:, 1] + pos[:, 2] + pos[:, 3] + pos[:, 4] + pos[:, 5] + pos[:, 6] + pos[:, 7] +
                        pos[:, 8] + pos[:, 9] + pos[:, 10] + pos[:, 11] + pos[:, 12] + pos[:, 13] + pos[:, 14] + pos[:, 15] +
                        pos[:, 16] + pos[:, 17]),
                )
        plt.bar(labels,
                pos[:, 19],
                width,
                label='P20',
                bottom=(pos[:, 0] + pos[:, 1] + pos[:, 2] + pos[:, 3] + pos[:, 4] + pos[:, 5] + pos[:, 6] + pos[:, 7] +
                        pos[:, 8] + pos[:, 9] + pos[:, 10] + pos[:, 11] + pos[:, 12] + pos[:, 13] + pos[:, 14] + pos[:, 15] +
                        pos[:, 16] + pos[:, 17] + pos[:, 18]),
                )


        y_label = pos[:, 0] + pos[:, 1] + pos[:, 2] + pos[:, 3] + pos[:, 4] + pos[:, 5] + pos[:, 6] + pos[:, 7] +\
                        pos[:, 8] + pos[:, 9] + pos[:, 10] + pos[:, 11] + pos[:, 12] + pos[:, 13] + pos[:, 14] + pos[:, 15] +\
                        pos[:, 16] + pos[:, 17] + pos[:, 18] + pos[:, 19]
        plt.plot(labels, y_label, label='Load + Loss', linestyle='--', color='#4a5e6a')

        plt.ylabel('Power(MW)')
        plt.xlabel('Hour')
        plt.legend(loc=(0.95, 0.2), prop={'size': 6})  
        # plt.show()
        plt.savefig('20-units-bar.svg', format='svg', dpi=1000)


def forty_unit_bar():
        pos = np.loadtxt('12月14号晚上MOHGS_MOHGS-AL-PPSO_DEED_40电机_迭代20000次_N=100/MOHGSwithArchive_position_0001_0.txt')
        pos = np.reshape(pos[0], (24, 40))
        data_df = pd.DataFrame(pos)
        writer = pd.ExcelWriter('40units.xlsx')
        data_df.to_excel(writer,'page1',float_format='%.2f')
        writer.save()
        width = 0.8
        labels = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18',
                  '19', '20',
                  '21', '22', '23', '24']
        plt.bar(labels,
                pos[:, 0],
                width,
                label='P1',
                )
        plt.bar(labels,
                pos[:, 1],
                width,
                label='P2',
                bottom=pos[:, 0],
                )
        plt.bar(labels,
                pos[:, 2],
                width,
                label='P3',
                bottom=(pos[:, 1] + pos[:, 0]),
                )
        plt.bar(labels,
                pos[:, 3],
                width,
                label='P4',
                bottom=(pos[:, 1] + pos[:, 0] + pos[:, 2]),
                )
        plt.bar(labels,
                pos[:, 4],
                width,
                label='P5',
                bottom=(pos[:, 0] + pos[:, 1] + pos[:, 2] + pos[:, 3]),
                )
        plt.bar(labels,
                pos[:, 5],
                width,
                label='P6',
                bottom=(pos[:, 0] + pos[:, 1] + pos[:, 2] + pos[:, 3] + pos[:, 4]),
                )
        plt.bar(labels,
                pos[:, 6],
                width,
                label='P7',
                bottom=(pos[:, 0] + pos[:, 1] + pos[:, 2] + pos[:, 3] + pos[:, 4] + pos[:, 5]),
                )
        plt.bar(labels,
                pos[:, 7],
                width,
                label='P8',
                bottom=(pos[:, 0] + pos[:, 1] + pos[:, 2] + pos[:, 3] + pos[:, 4] + pos[:, 5] + pos[:, 6]),
                )
        plt.bar(labels,
                pos[:, 8],
                width,
                label='P9',
                bottom=(pos[:, 0] + pos[:, 1] + pos[:, 2] + pos[:, 3] + pos[:, 4] + pos[:, 5] + pos[:, 6] + pos[:, 7]),
                )
        plt.bar(labels,
                pos[:, 9],
                width,
                label='P10',
                bottom=(pos[:, 0] + pos[:, 1] + pos[:, 2] + pos[:, 3] + pos[:, 4] + pos[:, 5] + pos[:, 6] + pos[:, 7] + pos[:, 8]),
                )
        plt.bar(labels,
                pos[:, 10],
                width,
                label='P11',
                bottom=(pos[:, 0] + pos[:, 1] + pos[:, 2] + pos[:, 3] + pos[:, 4] + pos[:, 5] + pos[:, 6] + pos[:, 7] + pos[:, 8] + pos[:, 9]),
                )
        plt.bar(labels,
                pos[:, 11],
                width,
                label='P12',
                bottom=(pos[:, 0] + pos[:, 1] + pos[:, 2] + pos[:, 3] + pos[:, 4] + pos[:, 5] + pos[:, 6] + pos[:, 7] + pos[:, 8] + pos[:, 9] + pos[:, 10]),
                )
        plt.bar(labels,
                pos[:, 12],
                width,
                label='P13',
                bottom=(pos[:, 0] + pos[:, 1] + pos[:, 2] + pos[:, 3] + pos[:, 4] + pos[:, 5] + pos[:, 6] + pos[:, 7] +
                        pos[:, 8] + pos[:, 9] + pos[:, 10] + pos[:, 11]),
                )
        plt.bar(labels,
                pos[:, 13],
                width,
                label='P14',
                bottom=(pos[:, 0] + pos[:, 1] + pos[:, 2] + pos[:, 3] + pos[:, 4] + pos[:, 5] + pos[:, 6] + pos[:, 7] +
                        pos[:, 8] + pos[:, 9] + pos[:, 10] + pos[:, 11] + pos[:, 12]),
                )
        plt.bar(labels,
                pos[:, 14],
                width,
                label='P15',
                bottom=(pos[:, 0] + pos[:, 1] + pos[:, 2] + pos[:, 3] + pos[:, 4] + pos[:, 5] + pos[:, 6] + pos[:, 7] +
                        pos[:, 8] + pos[:, 9] + pos[:, 10] + pos[:, 11] + pos[:, 12] + pos[:, 13]),
                )
        plt.bar(labels,
                pos[:, 15],
                width,
                label='P16',
                bottom=(pos[:, 0] + pos[:, 1] + pos[:, 2] + pos[:, 3] + pos[:, 4] + pos[:, 5] + pos[:, 6] + pos[:, 7] +
                        pos[:, 8] + pos[:, 9] + pos[:, 10] + pos[:, 11] + pos[:, 12] + pos[:, 13] + pos[:, 14]),
                )
        plt.bar(labels,
                pos[:, 16],
                width,
                label='P17',
                bottom=(pos[:, 0] + pos[:, 1] + pos[:, 2] + pos[:, 3] + pos[:, 4] + pos[:, 5] + pos[:, 6] + pos[:, 7] +
                        pos[:, 8] + pos[:, 9] + pos[:, 10] + pos[:, 11] + pos[:, 12] + pos[:, 13] + pos[:, 14] + pos[:, 15]),
                )
        plt.bar(labels,
                pos[:, 17],
                width,
                label='P18',
                bottom=(pos[:, 0] + pos[:, 1] + pos[:, 2] + pos[:, 3] + pos[:, 4] + pos[:, 5] + pos[:, 6] + pos[:, 7] +
                        pos[:, 8] + pos[:, 9] + pos[:, 10] + pos[:, 11] + pos[:, 12] + pos[:, 13] + pos[:, 14] + pos[:, 15] + pos[:, 16]),
                )
        plt.bar(labels,
                pos[:, 18],
                width,
                label='P19',
                bottom=(pos[:, 0] + pos[:, 1] + pos[:, 2] + pos[:, 3] + pos[:, 4] + pos[:, 5] + pos[:, 6] + pos[:, 7] +
                        pos[:, 8] + pos[:, 9] + pos[:, 10] + pos[:, 11] + pos[:, 12] + pos[:, 13] + pos[:, 14] + pos[:, 15] +
                        pos[:, 16] + pos[:, 17]),
                )
        plt.bar(labels,
                pos[:, 19],
                width,
                label='P20',
                bottom=(pos[:, 0] + pos[:, 1] + pos[:, 2] + pos[:, 3] + pos[:, 4] + pos[:, 5] + pos[:, 6] + pos[:, 7] +
                        pos[:, 8] + pos[:, 9] + pos[:, 10] + pos[:, 11] + pos[:, 12] + pos[:, 13] + pos[:, 14] + pos[:, 15] +
                        pos[:, 16] + pos[:, 17] + pos[:, 18]),
                )
        plt.bar(labels,
                pos[:, 20],
                width,
                label='P21',
                bottom=(pos[:, 0] + pos[:, 1] + pos[:, 2] + pos[:, 3] + pos[:, 4] + pos[:, 5] + pos[:, 6] + pos[:, 7] +
                        pos[:, 8] + pos[:, 9] + pos[:, 10] + pos[:, 11] + pos[:, 12] + pos[:, 13] + pos[:, 14] + pos[:, 15] +
                        pos[:, 16] + pos[:, 17] + pos[:, 18] + pos[:, 19]),
                )
        plt.bar(labels,
                pos[:, 21],
                width,
                label='P22',
                bottom=(pos[:, 0] + pos[:, 1] + pos[:, 2] + pos[:, 3] + pos[:, 4] + pos[:, 5] + pos[:, 6] + pos[:, 7] +
                        pos[:, 8] + pos[:, 9] + pos[:, 10] + pos[:, 11] + pos[:, 12] + pos[:, 13] + pos[:, 14] + pos[:, 15] +
                        pos[:, 16] + pos[:, 17] + pos[:, 18] + pos[:, 19] + pos[:, 20]),
                )
        plt.bar(labels,
                pos[:, 22],
                width,
                label='P23',
                bottom=(pos[:, 0] + pos[:, 1] + pos[:, 2] + pos[:, 3] + pos[:, 4] + pos[:, 5] + pos[:, 6] + pos[:, 7] +
                        pos[:, 8] + pos[:, 9] + pos[:, 10] + pos[:, 11] + pos[:, 12] + pos[:, 13] + pos[:, 14] + pos[:, 15] +
                        pos[:, 16] + pos[:, 17] + pos[:, 18] + pos[:, 19] + pos[:, 20] + pos[:, 21]),
                )
        plt.bar(labels,
                pos[:, 23],
                width,
                label='P24',
                bottom=(pos[:, 0] + pos[:, 1] + pos[:, 2] + pos[:, 3] + pos[:, 4] + pos[:, 5] + pos[:, 6] + pos[:, 7] +
                        pos[:, 8] + pos[:, 9] + pos[:, 10] + pos[:, 11] + pos[:, 12] + pos[:, 13] + pos[:, 14] + pos[:, 15] +
                        pos[:, 16] + pos[:, 17] + pos[:, 18] + pos[:, 19] + pos[:, 20] + pos[:, 21] + pos[:, 22]),
                )
        plt.bar(labels,
                pos[:, 24],
                width,
                label='P25',
                bottom=(pos[:, 0] + pos[:, 1] + pos[:, 2] + pos[:, 3] + pos[:, 4] + pos[:, 5] + pos[:, 6] + pos[:, 7] +
                        pos[:, 8] + pos[:, 9] + pos[:, 10] + pos[:, 11] + pos[:, 12] + pos[:, 13] + pos[:, 14] + pos[:, 15] +
                        pos[:, 16] + pos[:, 17] + pos[:, 18] + pos[:, 19] + pos[:, 20] + pos[:, 21] + pos[:, 22] + pos[:, 23]),
                )
        plt.bar(labels,
                pos[:, 25],
                width,
                label='P26',
                bottom=(pos[:, 0] + pos[:, 1] + pos[:, 2] + pos[:, 3] + pos[:, 4] + pos[:, 5] + pos[:, 6] + pos[:, 7] +
                        pos[:, 8] + pos[:, 9] + pos[:, 10] + pos[:, 11] + pos[:, 12] + pos[:, 13] + pos[:, 14] + pos[:, 15] +
                        pos[:, 16] + pos[:, 17] + pos[:, 18] + pos[:, 19] + pos[:, 20] + pos[:, 21] + pos[:, 22] + pos[:, 23] + pos[:, 24]),
                )
        plt.bar(labels,
                pos[:, 26],
                width,
                label='P27',
                bottom=(pos[:, 0] + pos[:, 1] + pos[:, 2] + pos[:, 3] + pos[:, 4] + pos[:, 5] + pos[:, 6] + pos[:, 7] +
                        pos[:, 8] + pos[:, 9] + pos[:, 10] + pos[:, 11] + pos[:, 12] + pos[:, 13] + pos[:, 14] + pos[:, 15] +
                        pos[:, 16] + pos[:, 17] + pos[:, 18] + pos[:, 19] + pos[:, 20] + pos[:, 21] + pos[:, 22] + pos[:, 23] +
                        pos[:, 24] + pos[:, 25]),
                )
        plt.bar(labels,
                pos[:, 27],
                width,
                label='P28',
                bottom=(pos[:, 0] + pos[:, 1] + pos[:, 2] + pos[:, 3] + pos[:, 4] + pos[:, 5] + pos[:, 6] + pos[:, 7] +
                        pos[:, 8] + pos[:, 9] + pos[:, 10] + pos[:, 11] + pos[:, 12] + pos[:, 13] + pos[:, 14] + pos[:, 15] +
                        pos[:, 16] + pos[:, 17] + pos[:, 18] + pos[:, 19] + pos[:, 20] + pos[:, 21] + pos[:, 22] + pos[:, 23] +
                        pos[:, 24] + pos[:, 25] + pos[:, 26]),
                )
        plt.bar(labels,
                pos[:, 28],
                width,
                label='P29',
                bottom=(pos[:, 0] + pos[:, 1] + pos[:, 2] + pos[:, 3] + pos[:, 4] + pos[:, 5] + pos[:, 6] + pos[:, 7] +
                        pos[:, 8] + pos[:, 9] + pos[:, 10] + pos[:, 11] + pos[:, 12] + pos[:, 13] + pos[:, 14] + pos[:, 15] +
                        pos[:, 16] + pos[:, 17] + pos[:, 18] + pos[:, 19] + pos[:, 20] + pos[:, 21] + pos[:, 22] + pos[:, 23] +
                        pos[:, 24] + pos[:, 25] + pos[:, 26] + pos[:, 27]),
                )
        plt.bar(labels,
                pos[:, 29],
                width,
                label='P30',
                bottom=(pos[:, 0] + pos[:, 1] + pos[:, 2] + pos[:, 3] + pos[:, 4] + pos[:, 5] + pos[:, 6] + pos[:, 7] +
                        pos[:, 8] + pos[:, 9] + pos[:, 10] + pos[:, 11] + pos[:, 12] + pos[:, 13] + pos[:, 14] + pos[:, 15] +
                        pos[:, 16] + pos[:, 17] + pos[:, 18] + pos[:, 19] + pos[:, 20] + pos[:, 21] + pos[:, 22] + pos[:, 23] +
                        pos[:, 24] + pos[:, 25] + pos[:, 26] + pos[:, 27] + pos[:, 28]),
                )
        plt.bar(labels,
                pos[:, 30],
                width,
                label='P31',
                bottom=(pos[:, 0] + pos[:, 1] + pos[:, 2] + pos[:, 3] + pos[:, 4] + pos[:, 5] + pos[:, 6] + pos[:, 7] +
                        pos[:, 8] + pos[:, 9] + pos[:, 10] + pos[:, 11] + pos[:, 12] + pos[:, 13] + pos[:, 14] + pos[:, 15] +
                        pos[:, 16] + pos[:, 17] + pos[:, 18] + pos[:, 19] + pos[:, 20] + pos[:, 21] + pos[:, 22] + pos[:, 23] +
                        pos[:, 24] + pos[:, 25] + pos[:, 26] + pos[:, 27] + pos[:, 28] + pos[:, 29]),
                )
        plt.bar(labels,
                pos[:, 31],
                width,
                label='P32',
                bottom=(pos[:, 0] + pos[:, 1] + pos[:, 2] + pos[:, 3] + pos[:, 4] + pos[:, 5] + pos[:, 6] + pos[:, 7] +
                        pos[:, 8] + pos[:, 9] + pos[:, 10] + pos[:, 11] + pos[:, 12] + pos[:, 13] + pos[:, 14] + pos[:, 15] +
                        pos[:, 16] + pos[:, 17] + pos[:, 18] + pos[:, 19] + pos[:, 20] + pos[:, 21] + pos[:, 22] + pos[:, 23] +
                        pos[:, 24] + pos[:, 25] + pos[:, 26] + pos[:, 27] + pos[:, 28] + pos[:, 29] + pos[:, 30]),
                )
        plt.bar(labels,
                pos[:, 32],
                width,
                label='P33',
                bottom=(pos[:, 0] + pos[:, 1] + pos[:, 2] + pos[:, 3] + pos[:, 4] + pos[:, 5] + pos[:, 6] + pos[:, 7] +
                        pos[:, 8] + pos[:, 9] + pos[:, 10] + pos[:, 11] + pos[:, 12] + pos[:, 13] + pos[:, 14] + pos[:, 15] +
                        pos[:, 16] + pos[:, 17] + pos[:, 18] + pos[:, 19] + pos[:, 20] + pos[:, 21] + pos[:, 22] + pos[:, 23] +
                        pos[:, 24] + pos[:, 25] + pos[:, 26] + pos[:, 27] + pos[:, 28] + pos[:, 29] + pos[:, 30] + pos[:, 31]),
                )
        plt.bar(labels,
                pos[:, 33],
                width,
                label='P34',
                bottom=(pos[:, 0] + pos[:, 1] + pos[:, 2] + pos[:, 3] + pos[:, 4] + pos[:, 5] + pos[:, 6] + pos[:, 7] +
                        pos[:, 8] + pos[:, 9] + pos[:, 10] + pos[:, 11] + pos[:, 12] + pos[:, 13] + pos[:, 14] + pos[:, 15] +
                        pos[:, 16] + pos[:, 17] + pos[:, 18] + pos[:, 19] + pos[:, 20] + pos[:, 21] + pos[:, 22] + pos[:, 23] +
                        pos[:, 24] + pos[:, 25] + pos[:, 26] + pos[:, 27] + pos[:, 28] + pos[:, 29] + pos[:, 30] + pos[:, 31] + pos[:, 32]),
                )
        plt.bar(labels,
                pos[:, 34],
                width,
                label='P35',
                bottom=(pos[:, 0] + pos[:, 1] + pos[:, 2] + pos[:, 3] + pos[:, 4] + pos[:, 5] + pos[:, 6] + pos[:, 7] +
                        pos[:, 8] + pos[:, 9] + pos[:, 10] + pos[:, 11] + pos[:, 12] + pos[:, 13] + pos[:, 14] + pos[:, 15] +
                        pos[:, 16] + pos[:, 17] + pos[:, 18] + pos[:, 19] + pos[:, 20] + pos[:, 21] + pos[:, 22] + pos[:, 23] +
                        pos[:, 24] + pos[:, 25] + pos[:, 26] + pos[:, 27] + pos[:, 28] + pos[:, 29] + pos[:, 30] + pos[:, 31] +
                        pos[:, 32] + pos[:, 33]),
                )
        plt.bar(labels,
                pos[:, 35],
                width,
                label='P36',
                bottom=(pos[:, 0] + pos[:, 1] + pos[:, 2] + pos[:, 3] + pos[:, 4] + pos[:, 5] + pos[:, 6] + pos[:, 7] +
                        pos[:, 8] + pos[:, 9] + pos[:, 10] + pos[:, 11] + pos[:, 12] + pos[:, 13] + pos[:, 14] + pos[:, 15] +
                        pos[:, 16] + pos[:, 17] + pos[:, 18] + pos[:, 19] + pos[:, 20] + pos[:, 21] + pos[:, 22] + pos[:, 23] +
                        pos[:, 24] + pos[:, 25] + pos[:, 26] + pos[:, 27] + pos[:, 28] + pos[:, 29] + pos[:, 30] + pos[:, 31] +
                        pos[:, 32] + pos[:, 33] + pos[:, 34]),
                )
        plt.bar(labels,
                pos[:, 36],
                width,
                label='P37',
                bottom=(pos[:, 0] + pos[:, 1] + pos[:, 2] + pos[:, 3] + pos[:, 4] + pos[:, 5] + pos[:, 6] + pos[:, 7] +
                        pos[:, 8] + pos[:, 9] + pos[:, 10] + pos[:, 11] + pos[:, 12] + pos[:, 13] + pos[:, 14] + pos[:, 15] +
                        pos[:, 16] + pos[:, 17] + pos[:, 18] + pos[:, 19] + pos[:, 20] + pos[:, 21] + pos[:, 22] + pos[:, 23] +
                        pos[:, 24] + pos[:, 25] + pos[:, 26] + pos[:, 27] + pos[:, 28] + pos[:, 29] + pos[:, 30] + pos[:, 31] +
                        pos[:, 32] + pos[:, 33] + pos[:, 34] + pos[:, 35]),
                )
        plt.bar(labels,
                pos[:, 37],
                width,
                label='P38',
                bottom=(pos[:, 0] + pos[:, 1] + pos[:, 2] + pos[:, 3] + pos[:, 4] + pos[:, 5] + pos[:, 6] + pos[:, 7] +
                        pos[:, 8] + pos[:, 9] + pos[:, 10] + pos[:, 11] + pos[:, 12] + pos[:, 13] + pos[:, 14] + pos[:, 15] +
                        pos[:, 16] + pos[:, 17] + pos[:, 18] + pos[:, 19] + pos[:, 20] + pos[:, 21] + pos[:, 22] + pos[:, 23] +
                        pos[:, 24] + pos[:, 25] + pos[:, 26] + pos[:, 27] + pos[:, 28] + pos[:, 29] + pos[:, 30] + pos[:, 31] +
                        pos[:, 32] + pos[:, 33] + pos[:, 34] + pos[:, 35] + pos[:, 36]),
                )
        plt.bar(labels,
                pos[:, 38],
                width,
                label='P39',
                bottom=(pos[:, 0] + pos[:, 1] + pos[:, 2] + pos[:, 3] + pos[:, 4] + pos[:, 5] + pos[:, 6] + pos[:, 7] +
                        pos[:, 8] + pos[:, 9] + pos[:, 10] + pos[:, 11] + pos[:, 12] + pos[:, 13] + pos[:, 14] + pos[:, 15] +
                        pos[:, 16] + pos[:, 17] + pos[:, 18] + pos[:, 19] + pos[:, 20] + pos[:, 21] + pos[:, 22] + pos[:, 23] +
                        pos[:, 24] + pos[:, 25] + pos[:, 26] + pos[:, 27] + pos[:, 28] + pos[:, 29] + pos[:, 30] + pos[:, 31] +
                        pos[:, 32] + pos[:, 33] + pos[:, 34] + pos[:, 35] + pos[:, 36] + pos[:, 37]),
                )
        plt.bar(labels,
                pos[:, 39],
                width,
                label='P40',
                bottom=(pos[:, 0] + pos[:, 1] + pos[:, 2] + pos[:, 3] + pos[:, 4] + pos[:, 5] + pos[:, 6] + pos[:, 7] +
                        pos[:, 8] + pos[:, 9] + pos[:, 10] + pos[:, 11] + pos[:, 12] + pos[:, 13] + pos[:, 14] + pos[:, 15] +
                        pos[:, 16] + pos[:, 17] + pos[:, 18] + pos[:, 19] + pos[:, 20] + pos[:, 21] + pos[:, 22] + pos[:, 23] +
                        pos[:, 24] + pos[:, 25] + pos[:, 26] + pos[:, 27] + pos[:, 28] + pos[:, 29] + pos[:, 30] + pos[:, 31] +
                        pos[:, 32] + pos[:, 33] + pos[:, 34] + pos[:, 35] + pos[:, 36] + pos[:, 37] + pos[:, 38]),
                )



        y_label = pos[:, 0] + pos[:, 1] + pos[:, 2] + pos[:, 3] + pos[:, 4] + pos[:, 5] + pos[:, 6] + pos[:, 7] +\
                        pos[:, 8] + pos[:, 9] + pos[:, 10] + pos[:, 11] + pos[:, 12] + pos[:, 13] + pos[:, 14] + pos[:, 15] +\
                        pos[:, 16] + pos[:, 17] + pos[:, 18] + pos[:, 19] + pos[:, 20] + pos[:, 21] + pos[:, 22] + pos[:, 23] +\
                        pos[:, 24] + pos[:, 25] + pos[:, 26] + pos[:, 27] + pos[:, 28] + pos[:, 29] + pos[:, 30] + pos[:, 31] +\
                        pos[:, 32] + pos[:, 33] + pos[:, 34] + pos[:, 35] + pos[:, 36] + pos[:, 37] + pos[:, 38] + pos[:, 39]
        plt.plot(labels, y_label, label='Load + Loss', linestyle='--', color='#4a5e6a')

        plt.ylabel('Power(MW)')
        plt.xlabel('Hour')
        plt.legend(loc=(0.97, -0.09), prop={'size': 5.5})  
        # plt.show()
        plt.savefig('40-units-bar.svg', format='svg', dpi=1000)

if __name__ == '__main__':
    # five_unit_bar()
    # ten_unit_bar()
    # six_unit_bar()
    # forty_unit_bar()
    twenty_unit_bar()




