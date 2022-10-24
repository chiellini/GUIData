import numpy as np
import pandas as pd
import os
import shutil

def moveStatFile():
    max_times = {"191108plc1p1": 205, "200109plc1p1": 205, "200323plc1p1": 185, "200326plc1p3": 220,
                 "200326plc1p4": 195, "200113plc1p2": 255,
                 "200113plc1p3": 195, "200322plc1p2": 195, "200122plc1lag1ip1": 195, "200122plc1lag1ip2": 195,
                 "200117plc1pop1ip2": 140, "200117plc1pop1ip3": 155}
    for embryo_name in max_times.keys():
        shutil.copy(os.path.join(
            r'C:\Users\zelinli6\OneDrive - City University of Hong Kong - Student\MembraneProjectData\GUIData\WebData_CMap_cell_label_v0.1\\',
            embryo_name, embryo_name + '_Stat.csv'),
                    os.path.join(r'C:\Users\zelinli6\OneDrive - City University of Hong Kong - Student\Desktop\tem',
                                 embryo_name + '_Stat.csv'))

    embryo_names = []
    for sample_id in range(4, 21, 1):
        embryo_names.append("Sample{}".format(str(sample_id).zfill(2)))
    for embryo_name in embryo_names:
        shutil.copy(os.path.join(
            r'C:\Users\zelinli6\OneDrive - City University of Hong Kong - Student\MembraneProjectData\GUIData\WebData_cshaper_v1.1\\',
            embryo_name, embryo_name + '_Stat.csv'),
                    os.path.join(r'C:\Users\zelinli6\OneDrive - City University of Hong Kong - Student\Desktop\tem',
                                 embryo_name + '_Stat.csv'))

def CShaperAddZeroToUnresonableBlank():
    current_folder = r'C:\Users\zelinli6\OneDrive - City University of Hong Kong - Student\MembraneProjectData\GUIData\WebData_cshaper_v2\\'
    data_folder = r'C:\Users\zelinli6\OneDrive - City University of Hong Kong - Student\MembraneProjectData\GUIData\WebData_cshaper_v2\\'

    embryo_names = []
    for sample_id in range(4, 21, 1):
        embryo_names.append("Sample{}".format(str(sample_id).zfill(2)))

    # max_times = {"200117plc1pop1ip3":155}
    for embryo_name in embryo_names:
        contact_file = pd.read_csv(os.path.join(current_folder, embryo_name, embryo_name + '_Stat.csv'), header=0,
                                   index_col=[0, 1])
        # for column_num,column_value in enumerate(contact_file.columns):
        #     print(column_num,column_value)
        # print(not contact_file.at[('Dap','Daaa'),str(144)]>=0)
        # print(not contact_file.loc[('Dap','Daaa')][143]>=0)
        # # Earap
        # # Earpp
        # print(not contact_file.at[('Earap','Earpp'),str(144)]>=0)
        #
        # input()
        for tp_index in contact_file.index:
            # print(embryo_name,'  contact pairs  ',tp_index)
            start_column = 0
            stop_column = 0
            first_flag = False
            # notNullIndex=contact_file.loc[tp_index].notna()
            for column_num, column_value in enumerate(contact_file.columns):
                # print(notNullIndex.loc[idx])
                if contact_file.at[tp_index, column_value] >= 0 and not first_flag:
                    start_column = column_num
                    first_flag = True
                if contact_file.at[tp_index, column_value] >= 0:
                    stop_column = column_num

            # print(start_column,stop_column)
            for col in range(start_column, stop_column + 1):
                # if tp_index == ('Dap', 'Daaa'):
                #     # print(start_column, stop_column)
                #     print(col,not contact_file.loc[tp_index][col]>=0)
                # if contact_file.loc[tp_index][col]<0:
                #     print('gagagaga')
                if not contact_file.loc[tp_index][col] >= 0:
                    # print(tp_index,col)
                    contact_file.loc[tp_index][col] = 0
            # print(notNullIndex)
        contact_file.to_csv(os.path.join(data_folder, embryo_name, embryo_name + '_Stat.csv'))

def CMapAddZeroToUnresonableBlank():
    current_folder=r'C:\Users\zelinli6\OneDrive - City University of Hong Kong - Student\MembraneProjectData\GUIData\WebData_CMap_cell_label_v3'
    data_folder=r'C:\Users\zelinli6\OneDrive - City University of Hong Kong - Student\MembraneProjectData\GUIData\WebData_CMap_cell_label_v3'

    max_times = {"191108plc1p1":205, "200109plc1p1":205, "200323plc1p1":185, "200326plc1p3":220, "200326plc1p4":195, "200113plc1p2":255,
                 "200113plc1p3": 195, "200322plc1p2":195, "200122plc1lag1ip1":195, "200122plc1lag1ip2":195, "200117plc1pop1ip2":140, "200117plc1pop1ip3":155}

    # max_times = {"200117plc1pop1ip3":155}
    for embryo_name in max_times.keys():
        contact_file=pd.read_csv(os.path.join(current_folder,embryo_name,embryo_name+'_Stat.csv'),header=0,index_col=[0,1])
        # for column_num,column_value in enumerate(contact_file.columns):
        #     print(column_num,column_value)
        # print(not contact_file.at[('Dap','Daaa'),str(144)]>=0)
        # print(not contact_file.loc[('Dap','Daaa')][143]>=0)
        # # Earap
        # # Earpp
        # print(not contact_file.at[('Earap','Earpp'),str(144)]>=0)
        #
        # input()
        for tp_index in contact_file.index:
            # print(embryo_name,'  contact pairs  ',tp_index)
            start_column=0
            stop_column=0
            first_flag=False
            # notNullIndex=contact_file.loc[tp_index].notna()
            for column_num,column_value in enumerate(contact_file.columns):
                # print(notNullIndex.loc[idx])
                if contact_file.at[tp_index,column_value]>=0 and not first_flag:
                    start_column=column_num
                    first_flag=True
                if contact_file.at[tp_index,column_value]>=0:
                    stop_column=column_num

            # print(start_column,stop_column)
            for col in range(start_column,stop_column+1):
                # if tp_index == ('Dap', 'Daaa'):
                #     # print(start_column, stop_column)
                #     print(col,not contact_file.loc[tp_index][col]>=0)
                # if contact_file.loc[tp_index][col]<0:
                #     print('gagagaga')
                if not contact_file.loc[tp_index][col] >=0:
                    print(tp_index,col)
                    contact_file.loc[tp_index][col]=0
            # print(notNullIndex)
        contact_file.to_csv(os.path.join(data_folder,embryo_name,embryo_name+'_Stat.csv'))

if __name__=="__main__":
    # CShaperAddZeroToUnresonableBlank()
    CMapAddZeroToUnresonableBlank()