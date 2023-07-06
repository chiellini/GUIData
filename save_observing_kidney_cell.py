import os
import glob
import shutil
import json
import pandas as pd
# 200109plc1p1 200113plc1p2,200326plc1p4
embryo_name_this_using='200109plc1p1'

cell_fate_dict={}
cell_fate_pd=pd.read_csv(os.path.join(r'F:\CMap_paper\Figures\Movie Fate','cell_fate_dictionary.csv'),index_col=0,names=['Fate'])
for index in cell_fate_pd.index:
    cell_fate_dict[index[:-1]]=cell_fate_pd.loc[index]['Fate'][:-1]
# print(cell_fate_dict)
# quit(0)
predecent_len=4
kiney_cells=['ABplpappaap']
first_set=['AB','ABp','ABpl']
non_apoptotic_set=['P1','ABa','ABpr']
apoptotic_set=['ABplpappap']

target_cells_set=[set(first_set),set(non_apoptotic_set),set(apoptotic_set)]
for item_this in kiney_cells:
    target_cells_set[0].add(item_this)
    sister_last_syntnax='a' if item_this[-1] == 'p' else 'p'
    sister_cell_name_tmp=item_this[:-1]+sister_last_syntnax

    if cell_fate_dict[sister_cell_name_tmp] == 'Death':
        target_cells_set[2].add(sister_cell_name_tmp)
    else:
        target_cells_set[1].add(sister_cell_name_tmp)

    if len(item_this) > predecent_len:
        for predescent_len in range(predecent_len, len(item_this)):
            target_cells_set[0].add(item_this[:predescent_len])
            sister_last_syntnax = 'a' if item_this[predescent_len] == 'p' else 'p'
            sister_cell_name_tmp = item_this[:predescent_len] + sister_last_syntnax
            print(cell_fate_dict[sister_cell_name_tmp])
            if cell_fate_dict[sister_cell_name_tmp] == 'Death':
                target_cells_set[2].add(sister_cell_name_tmp)
            else:
                target_cells_set[1].add(sister_cell_name_tmp)
print(target_cells_set)

target_mtl_color_list=[
    [218,55,56],
    [55,220,57],
[189,183,107]
]
target_mtl_name_list=['mat_kiney_cells','mat_kiney_sister_cells','mat_apoptotic_sister_cells']
# =============resave obj ===================
source_dir=r'F:\obj_web_visulizaiton\obj_combined\{}'.format(embryo_name_this_using)
objs_list=glob.glob(os.path.join(source_dir,'*.obj'))
dst_dir=r'F:\CMap_paper\Figures\KidneyCell\{}'.format(embryo_name_this_using)

output_found_cells=[{},{},{}]

for idx,obj_path in enumerate(objs_list):
# for idx, targe_cell_name_list in enumerate(target_cells):
#     print('dealing with ', obj_path)
    file_name = os.path.basename(obj_path).split('.')[0]

    selected_cell_data=[]
    # Read the OBJ file
    with open(obj_path, 'r') as f:
        obj_data = f.read()

    # Split the OBJ data into lines
    obj_lines = obj_data.split('\n')

    reading_selected_group=False
    selected_cell_data.append('# OBJ File')
    selected_cell_data.append('mtllib designed_mat.mtl')

    facet_offset = 0
    found_obj=[]
    # tmp_foundobj=[]
    for line in obj_lines:
        # If the line starts with 'g' (indicating a group), check if it is the selected group
        if line.startswith('g'):
            cell_name, cell_label = line.split(' ')[1].split('\n')[0].split('_')
            # f.write(line)
            # group_name = line.split()[1]
            if cell_name in target_cells_set[0] or cell_name in target_cells_set[1] or cell_name in target_cells_set[2]:
                reading_selected_group = True
                found_obj.append(cell_name)
            else:
                reading_selected_group = False

                # If we are currently reading the selected group, add the line to the selected group data
        if reading_selected_group:
            # If the line starts with 'f' (indicating a face), update the vertex indices to account for the facet offset
            if line.startswith('f'):
                face_data = line.split()[1:]
                updated_face_data = []
                for vertex in face_data:
                    vertex_index = int(vertex.split('/')[0])
                    updated_vertex_index = vertex_index - facet_offset
                    updated_vertex = str(updated_vertex_index) + vertex[len(str(vertex_index)):]
                    updated_face_data.append(updated_vertex)
                updated_line = 'f ' + ' '.join(updated_face_data)
                selected_cell_data.append(updated_line)
            elif line.startswith('usemtl '):
                _,cell_name, cell_label = line.split(' ')[1].split('\n')[0].split('_')
                if cell_name in  target_cells_set[0]:
                    selected_cell_data.append('usemtl mat_kiney_cells')
                    if not output_found_cells[0].get(file_name,False):
                        output_found_cells[0][file_name]=[cell_name]
                    else:
                        output_found_cells[0][file_name].append(cell_name)
                elif cell_name in target_cells_set[1]:
                    selected_cell_data.append('usemtl mat_kiney_sister_cells')
                    if not output_found_cells[1].get(file_name, False):
                        output_found_cells[1][file_name] = [cell_name]
                    else:
                        output_found_cells[1][file_name].append(cell_name)
                elif cell_name in target_cells_set[2]:
                    selected_cell_data.append('usemtl mat_apoptotic_sister_cells')
                    if not output_found_cells[2].get(file_name, False):
                        output_found_cells[2][file_name] = [cell_name]
                    else:
                        output_found_cells[2][file_name].append(cell_name)

                else:
                    raise Exception('unexpected cell name in seleting mtl of  cell data')
            else:
                selected_cell_data.append(line)

                # If the line starts with 'v' (indicating a vertex), increment the facet offset
        elif line.startswith('v'):
            facet_offset += 1

    if len(found_obj)>0:
        print('saving ',found_obj,file_name)
        obj_save_path=os.path.join(dst_dir,file_name+'.obj')
        # Write the selected group data to a new OBJ file
        with open(obj_save_path, 'w') as f:
            f.write('\n'.join(selected_cell_data))

with open(os.path.join(dst_dir,embryo_name_this_using+'_appearance.txt'), 'w') as f:
    f.write(json.dumps(output_found_cells))

mtl_file_list_to_save=[]
mtl_file_list_to_save.append('# MTL File')
for tmp_color_idx,tmp_color_list in enumerate(target_mtl_color_list):

    mtl_file_list_to_save.append('\n')
    mtl_file_list_to_save.append('newmtl '+target_mtl_name_list[tmp_color_idx])
    mtl_file_list_to_save.append('Ns 96.078431')
    mtl_file_list_to_save.append('Ka 0.0 0.0 0.0')
    r,g,b=[x/256 for x in tmp_color_list]
    mtl_file_list_to_save.append('Kd {:6f} {:6f} {:6f}'.format(r,g,b))
    mtl_file_list_to_save.append('Ks 0.5 0.5 0.5')
    mtl_file_list_to_save.append('Ni 1.0')
    mtl_file_list_to_save.append('d 1.0')
    mtl_file_list_to_save.append('illum 2')

mtl_save_path=os.path.join(dst_dir,'designed_mat.mtl')
with open(mtl_save_path, 'w') as f:
    f.write('\n'.join(mtl_file_list_to_save))