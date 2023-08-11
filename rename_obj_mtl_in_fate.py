import os
import glob

import pandas as pd


cell_fate_dict={}
cell_fate_pd=pd.read_csv(os.path.join(r'F:\CMap_paper\Figures\Movie Fate','cell_fate_dictionary.csv'),index_col=0,names=['Fate'])
for index in cell_fate_pd.index:
    cell_fate_dict[index[:-1]]=cell_fate_pd.loc[index]['Fate'][:-1]
print(cell_fate_dict)
# quit(0)
# =============rename  obj ===================
embryo_name_this='200109plc1p1'
obj_list=glob.glob(os.path.join(r'F:\obj_web_visulizaiton\obj_combined\{}'.format(embryo_name_this), '*.obj'))
dst_folder=r'F:\CMap_paper\Figures\Movie Fate\{}'.format(embryo_name_this)
for obj_path in obj_list:
    print('dealing with ' + obj_path)
    obj_save_path=os.path.join(dst_folder,'fate_'+os.path.basename(obj_path))
    with open(obj_path) as f:
        lines = f.readlines()
    with open(obj_save_path, 'w') as f:
        for line in lines:
            if line.startswith('mtllib '):
                # print(cell_name_cell_label)
                f.write('mtllib designed_mat.mtl' + '\n')
            elif line.startswith('usemtl '):
                # usemtl mat_ABp_449
                cell_name,cell_label = line.split(' ')[1].split('\n')[0].split('_')[1:]
                cell_fate_this=cell_fate_dict[cell_name]
                f.write('usemtl mat_' +cell_fate_this+ '\n')

            else:
                f.write(line)