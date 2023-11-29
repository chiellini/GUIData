import os
import glob

IS_DELETE_OTHER_CELL=True
target_obj_cell_set_list=[


    {'ABprpppppaa',
'ABprpppppap',

    },
    {

'ABprppppppa',
'ABprppppppp',},
{
    'EMS',
'MSapappp',
'MSapaaap',
'MSappppa',
'MSapappa',
'MSappppp',
'MSapppap',
'MSapapap',
'MSapppaa',
'MSappapp',
'MSaapppaa',
'MSaapppap',
'MSaappppa',
'MSaappppp',
'MSpappaa',
'MSpppapp',
'MSpapppaa',
'MSpapppap',
'MSpappppa',
'MSpappppp',
'MSpappap',
'MSppapap',
'MSppppaa',
'MSppaaap',
'MSppappa',
'MSppppap',
'MSppappp',
'MSpppppa',
'MSpppppp'
    },
    {'C',
'Cappaap',
'Capppaa',
'Capppap',
'Cappppd',
'Cappaaa',
'Capapaa',
'Capapap',
'Cappapa',
'Cappapp',
'Capaaaa',
'Capaaap',
'Capaapa',
'Capaapp',
'Capappp',
'Cappppv',
'Capappa',
'Cppappp',
'Cppaaaa',
'Cppaaap',
'Cppaapa',
'Cppaapp',
'Cppappa',
'Cpppppv',
'Cpppaaa',
'Cppapaa',
'Cppapap',
'Cpppapa',
'Cpppapp',
'Cpppaap',
'Cppppaa',
'Cppppap',
'Cpppppd'
},
    {'D',
'Dappaa',
'Dappap',
'Dapppa',
'Dapppp',
'Daaap',
'Dapap',
'Dapaa',
'Daapa',
'Daapp',
'Dpapa',
'Dpapp',
'Dpaaa',
'Dppaa',
'Dpaap',
'Dppap',
'Dpppaa',
'Dpppap',
'Dppppa',
'Dppppp'
    },{'P1','P2','P3','P4'}
]

predecent_len=2
new_target_obj_cell_set_list=[set(),set(),set(),set(),set(),set()]
for lineage_idx, lineage_set in enumerate(target_obj_cell_set_list):
    print(lineage_idx,len(lineage_set),lineage_set)
    for item_this in lineage_set:
        new_target_obj_cell_set_list[lineage_idx].add(item_this)
        if len(item_this)>predecent_len:
            for predescent_len in range(predecent_len,len(item_this)):
                new_target_obj_cell_set_list[lineage_idx].add(item_this[:predescent_len])
    print(len(new_target_obj_cell_set_list[lineage_idx]),new_target_obj_cell_set_list[lineage_idx])


other_cell_color=[200, 200, 200]
# AB, MS, C, D, P
target_mtl_color_list=[

    [6,0,237],
[50,50,255],
    [0,100,100],
    [247,2,245],
    [240,0,0],
[170, 170, 170]
]
target_mtl_name_list=['AB','AB_sister','MS', 'C', 'D','P']

# =============rename and save muscle obj  other cells as transparent===================
obj_list=glob.glob(os.path.join(r'F:\obj_web_visulizaiton\obj_combined\200113plc1p2', '*.obj'))
transparent_dst_folder= r'F:\CMap_paper\Figures\Body wall muscle with AB sister\transparent_objs'
count_cell_list=[]
for obj_path in obj_list:
    print('dealing with ' + obj_path)
    obj_save_path=os.path.join(transparent_dst_folder, 'muscle_' + os.path.basename(obj_path))
    with open(obj_path) as f:
        lines = f.readlines()
    count_cell_this=0
    with open(obj_save_path, 'w') as f:
        for line in lines:
            if line.startswith('mtllib '):
                # print(cell_name_cell_label)
                f.write('mtllib designed_mat.mtl' + '\n')
            elif line.startswith('usemtl '):
                # usemtl mat_ABp_449
                cell_name,cell_label = line.split(' ')[1].split('\n')[0].split('_')[1:]
                IS_FOUND=False
                for tmp_color_idx,tmp_cell_set in enumerate(new_target_obj_cell_set_list):
                    if cell_name in tmp_cell_set:
                        f.write('usemtl mat_muscle_'+target_mtl_name_list[tmp_color_idx] + '\n')
                        count_cell_this+=1
                        IS_FOUND=True
                        break
                if not IS_FOUND:
                    f.write('usemtl mat_muscle_OTHER' + '\n')
            else:
                f.write(line)
    count_cell_list.append(count_cell_this)

# Save the list to a text file
with open(os.path.join(transparent_dst_folder, 'cell_count_list.txt'), 'w') as f:
    for item in count_cell_list:
        f.write(f'{item}\n')



mtl_file_list_to_save=[]
mtl_file_list_to_save.append('# MTL File')
for tmp_color_idx,tmp_color_list in enumerate(target_mtl_color_list):

    mtl_file_list_to_save.append('\n')
    mtl_file_list_to_save.append('newmtl mat_muscle_'+target_mtl_name_list[tmp_color_idx])
    mtl_file_list_to_save.append('Ns 96.078431')
    mtl_file_list_to_save.append('Ka 0.0 0.0 0.0')
    r,g,b=[x/256 for x in tmp_color_list]
    mtl_file_list_to_save.append('Kd {:6f} {:6f} {:6f}'.format(r,g,b))
    mtl_file_list_to_save.append('Ks 0.5 0.5 0.5')
    mtl_file_list_to_save.append('Ni 1.0')
    mtl_file_list_to_save.append('d 1.0')
    mtl_file_list_to_save.append('illum 2')

mtl_file_list_to_save.append('\n')
mtl_file_list_to_save.append('newmtl mat_muscle_OTHER')
mtl_file_list_to_save.append('Ns 96.078431')
mtl_file_list_to_save.append('Ka 0.0 0.0 0.0')
r,g,b=[x / 256 for x in other_cell_color]
mtl_file_list_to_save.append('Kd {:6f} {:6f} {:6f}'.format(r,g,b))
mtl_file_list_to_save.append('Ks 0.5 0.5 0.5')
mtl_file_list_to_save.append('Ni 1.0')
mtl_file_list_to_save.append('d 0.15')
mtl_file_list_to_save.append('illum 2')

mtl_save_path=os.path.join(transparent_dst_folder, 'designed_mat.mtl')
with open(mtl_save_path, 'w') as f:
    f.write('\n'.join(mtl_file_list_to_save))



# ===========save obj with other cell deleted===================
source_dir=transparent_dst_folder
objs_list=glob.glob(os.path.join(source_dir,'*.obj'))
no_transparent_dst_folder= r'F:\CMap_paper\Figures\Body wall muscle with AB sister\objs'
target_cells=set()
for tmp_set in new_target_obj_cell_set_list:
    target_cells=target_cells.union(tmp_set)
print(target_cells)
for idx,obj_path in enumerate(objs_list):
# for idx, targe_cell_name_list in enumerate(target_cells):
    print('dealing with ', obj_path)
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
    # tmp_foundobj=[]
    for line in obj_lines:
        # If the line starts with 'g' (indicating a group), check if it is the selected group
        if line.startswith('g'):
            cell_name, cell_label = line.split(' ')[1].split('\n')[0].split('_')
            # f.write(line)
            # group_name = line.split()[1]
            if cell_name in target_cells:
                reading_selected_group = True
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
            else:
                selected_cell_data.append(line)

                # If the line starts with 'v' (indicating a vertex), increment the facet offset
        elif line.startswith('v'):
            facet_offset += 1

    obj_save_path=os.path.join(no_transparent_dst_folder, os.path.basename(obj_path))
    # Write the selected group data to a new OBJ file
    with open(obj_save_path, 'w') as f:
        f.write('\n'.join(selected_cell_data))
