import os
import glob


# target_cells=[['Z2','Z3'],
#     ['Ealaad', 'Ealaav', 'Earaad', 'Earaav'],
#
#               ['Ealpa','Earpa'],
#                 ['Ealap','Earap'],
#
#
#               ['Eplaa','Epraa'],
#                 ['Ealpp','Earpp'],
#
#               ['Eplap','Eprap'],
#               ['Eplpa','Eprpa'],
#               ['Eplppa','Eplppp','Eprppa','Eprppp']
#               ]

target_cells=[['Z2','Z3','Ealaad', 'Ealaav', 'Earaad', 'Earaav','Ealpa','Earpa','Ealap','Earap','Eplaa','Epraa','Ealpp','Earpp','Eplap','Eprap','Eplpa','Eprpa','Eplppa','Eplppp','Eprppa','Eprppp'],
    ['Ealaad', 'Ealaav', 'Earaad', 'Earaav','Ealpa','Earpa','Ealap','Earap','Eplaa','Epraa','Ealpp','Earpp','Eplap','Eprap','Eplpa','Eprpa','Eplppa','Eplppp','Eprppa','Eprppp']]
# =============resave obj ===================
obj_path=os.path.join(r'F:\CMap_paper\Figures\Intestine Twisting', '200113plc1p2_255_segCell.obj')
for idx, targe_cell_name_list in enumerate(target_cells):
    print('dealing with ', targe_cell_name_list)
    selected_cell_data=[]
    # Read the OBJ file
    with open(obj_path, 'r') as f:
        obj_data = f.read()

    # Split the OBJ data into lines
    obj_lines = obj_data.split('\n')

    reading_selected_group=False
    selected_cell_data.append(obj_lines[0])
    selected_cell_data.append(obj_lines[1])

    facet_offset = 0
    found_obj=[]
    for line in obj_lines:
        # If the line starts with 'g' (indicating a group), check if it is the selected group
        if line.startswith('g'):
            cell_name, cell_label = line.split(' ')[1].split('\n')[0].split('_')
            # f.write(line)
            # group_name = line.split()[1]
            if cell_name in targe_cell_name_list:
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
            else:
                selected_cell_data.append(line)

                # If the line starts with 'v' (indicating a vertex), increment the facet offset
        elif line.startswith('v'):
            facet_offset += 1
    print('found ',found_obj)
    obj_save_path=os.path.join(os.path.dirname(obj_path),'layer_'+str(idx)+'_'+os.path.basename(obj_path))
    # Write the selected group data to a new OBJ file
    with open(obj_save_path, 'w') as f:
        f.write('\n'.join(selected_cell_data))

