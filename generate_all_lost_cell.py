import pandas as pd
import os

cshaper_embryo_names = ['Sample' + str(i).zfill(2) for i in range(4, 21)]
cshaper_max_times=[150, 170, 210, 165, 160, 160, 160, 170, 165, 150, 155, 170, 160, 160, 160, 160, 170]

cmap_embryo_names = ['191108plc1p1', '200109plc1p1', '200113plc1p2', '200113plc1p3', '200322plc1p2', '200323plc1p1',
                    '200326plc1p3', '200326plc1p4', '200122plc1lag1ip1', '200122plc1lag1ip2', '200117plc1pop1ip2',
                    '200117plc1pop1ip3']
cmap_max_times = [205, 205, 255, 195, 195, 185, 220, 195, 195, 195, 140, 155]

# embryo_names=cshaper_embryo_names+cmap_embryo_names
# max_times=cshaper_max_times+cmap_max_times

nucLocFilePath=r'D:\project_tem\UpdatedNucleusLoc'

# -----------------cmap------------------------
all_lost_cell_pd=pd.DataFrame(columns=['embryo_name','time_point','nucleus_label','nucleus_name',	'x_256',	'y_356',	'z_214'	])
for idx,embryo_name in enumerate(cmap_embryo_names):
    for tp in range(1,cmap_max_times[idx]+1):
        nucLoc=pd.read_csv(os.path.join(nucLocFilePath,embryo_name,'{}_{}_nucLoc.csv'.format(embryo_name,str(tp).zfill(3))))
        lost_series=nucLoc[nucLoc['note']=='lost']
        if len(lost_series)>0:
            for tem_i in lost_series.index:
                tem_list=lost_series.loc[tem_i]
                all_lost_cell_pd.loc[len(all_lost_cell_pd)]=[embryo_name,tp,tem_list['nucleus_label'],tem_list['nucleus_name'],tem_list['x_256'],tem_list['y_356'],tem_list['z_214']]

print(all_lost_cell_pd)
all_lost_cell_pd.to_csv(os.path.join(nucLocFilePath,'cmap_all_lost_cells.csv'),index=False)
# ---------------------------------------------

# -----------------cshaper------------------------
all_lost_cell_pd=pd.DataFrame(columns=['embryo_name','time_point','nucleus_label',	'nucleus_name',	'x_184',	'y_256',	'z_114'])
for idx,embryo_name in enumerate(cshaper_embryo_names):
    for tp in range(1,cshaper_max_times[idx]+1):
        nucLoc=pd.read_csv(os.path.join(nucLocFilePath,embryo_name,'{}_{}_nucLoc.csv'.format(embryo_name,str(tp).zfill(3))))
        lost_series=nucLoc[nucLoc['note']=='lost']
        if len(lost_series)>0:
            for tem_i in lost_series.index:
                tem_list=lost_series.loc[tem_i]
                all_lost_cell_pd.loc[len(all_lost_cell_pd)]=[embryo_name,tp,tem_list['nucleus_label'],tem_list['nucleus_name'],tem_list['x_184'],tem_list['y_256'],tem_list['z_114']]

print(all_lost_cell_pd)
all_lost_cell_pd.to_csv(os.path.join(nucLocFilePath,'cshaper_all_lost_cells.csv'),index=False)
# ---------------------------------------------