import os
import glob
import shutil
import json

SAVE_OTHER_CELL_AS_TRANSPARENT=True
target_cell_preix='skin_'
start_target_cells=[
    'Ealaa',
                  'Earaa',
                  'Ealpa','Earpa','Ealap','Earap','Eplaa','Epraa','Ealpp','Earpp','Eplap','Eprap','Eplpa','Eprpa',
                  'Eplpp',
                  'Eprpp']
start_target_cells.sort()
# target_cells=[
#     'Ealaa','Ealaad', 'Ealaav',
#               'Earaa','Earaad', 'Earaav',
#               'Ealpa','Earpa','Ealap','Earap','Eplaa','Epraa','Ealpp','Earpp','Eplap','Eprap','Eplpa','Eprpa',
#               'Eplpp','Eplppa','Eplppp',
#               'Eprpp','Eprppa','Eprppp']

target_cells=['ABplaaaapa',
'ABarpaapaa',
'ABplaaaapp',
'ABarpapapp',
'ABarpaapap',
'ABarpaappa',
'ABarpaappp',
'ABarppaapa',
'ABarpppapa',
'Cpaaaa',
'Caaaaa',
'Cpaaap',
'Caaaap',
'Cpaapa',
'Caaapa',
'Cpaapp',
'Caaapp',
'Cpapaa',
'Cpapap',
'Cpappd',
'Caappd',

# 'ABplaaapap',
# 'ABplaaappa',
# 'ABplaaappp',
# 'ABarppaaap',
# 'ABarppapaa',
# 'ABarppapap',
# 'ABplappapa',
# 'ABarppappa',
# 'ABplapapaap',
# 'ABarppappp',
# 'ABplappppp',
#
# 'ABarpappap',
# 'ABarpapppa',
# 'ABarpapppp',
# 'ABarpppaap',
# 'ABarppppaa',
# 'ABarppppap',
# 'ABprappapa',
# 'ABarpppppa',
# 'ABprapapaap',
# 'ABarpppppp',
# 'ABprappppp'
              ]

start_target_cells=['ABplaaaapa',
'ABarpaapaa',
'ABplaaaapp',
'ABarpapapp',
'ABarpaapap',
'ABarpaappa',
'ABarpaappp',
'ABarppaapa',
'ABarpppapa',
'Cpaaaa',
'Caaaaa',
'Cpaaap',
'Caaaap',
'Cpaapa',
'Caaapa',
'Cpaapp',
'Caaapp',
'Cpapaa',
'Cpapap',
'Cpappd',
'Caappd',

# 'ABplaaapap',
# 'ABplaaappa',
# 'ABplaaappp',
# 'ABarppaaap',
# 'ABarppapaa',
# 'ABarppapap',
# 'ABplappapa',
# 'ABarppappa',
# # 'ABplapapaap',  misssssssssss at the begin
# 'ABarppappp',
# 'ABplappppp',
#
# 'ABarpappap',
# 'ABarpapppa',
# 'ABarpapppp',
# 'ABarpppaap',
# 'ABarppppaa',
# 'ABarppppap',
# 'ABprappapa',
# 'ABarpppppa',
# # 'ABprapapaap',   misssssssssss at the begin
# 'ABarpppppp',
# 'ABprappppp'
                    ]

mtl_settt=set()
# =============resave obj ===================
source_dir=r'F:\obj_web_visulizaiton\obj_combined\200326plc1p4'
objs_list=glob.glob(os.path.join(source_dir,'*.obj'))
dst_dir=r'F:\CMap_paper\Figures\Skin Interdigitation\Skin_obj\200326plc1p4'
is_start=False
E_cell_number_dict={}

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
    found_obj=[]
    # tmp_foundobj=[]
    for line in obj_lines:
        # If the line starts with 'g' (indicating a group), check if it is the selected group
        if line.startswith('g'):
            cell_name, cell_label = line.split(' ')[1].split('\n')[0].split('_')
            # f.write(line)
            # group_name = line.split()[1]
            if cell_name in target_cells:
                reading_selected_group = True
                found_obj.append(cell_name)
                mtl_settt.add('mat_{}_{}'.format(cell_name, cell_label))
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

    found_obj.sort()
    if set(found_obj)==set(start_target_cells):
        print('found ',found_obj,len(found_obj))
        is_start=True
    # if len(found_obj)==41:
    #     is_start=True
    if is_start:

        print('saving ',found_obj)
        start_target_cells.sort()
        # print(list(set(found_obj)-set(start_target_cells)))
        E_cell_number_dict[idx]=len(found_obj)
        file_name=os.path.basename(obj_path).split('.')[0]
        obj_save_path=os.path.join(dst_dir,target_cell_preix+file_name+'.obj')
        # Write the selected group data to a new OBJ file
        with open(obj_save_path, 'w') as f:
            f.write('\n'.join(selected_cell_data))
print(mtl_settt)

# with open(r'F:\CMap_paper\Figures\Intestine Twisting\E_cell_number_dict.txt', 'w') as f:
#     f.write(json.dumps(E_cell_number_dict))