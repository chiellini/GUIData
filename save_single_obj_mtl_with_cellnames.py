import os
import glob
import shutil

# 'CD200113plc1p2' 'WT_Sample1'
# 'CD200322plc1p2' 'WT_Sample2'
# 'CD200323plc1p1' 'WT_Sample3'
# 'CD200326plc1p3' 'WT_Sample4'
# 'CD200326plc1p4' 'WT_Sample5'
# 'CD191108plc1p1' 'WT_Sample6'
# 'CD200109plc1p1' 'WT_Sample7'
# 'CD200113plc1p3' 'WT_Sample8'


obj_path_root = r'C:\Users\zelinli6\OneDrive - City University of Hong Kong - Student\Documents\02paper cunmin segmentation\segmentation results\combined_objs\190311plc1mp1'
obj_list_to_save = ['190311plc1mp1_057_merged.obj']


# obj_path_root=r'C:\Users\zelinli6\OneDrive - City University of Hong Kong - Student\Documents\02paper cunmin segmentation\segmentation results\combined_objs\190311plc1mp1'
# obj_list_objs_tmp=glob.glob(os.path.join(obj_path_root,'*.obj'))
# obj_list_to_save=[]
# for obj_tmp in obj_list_objs_tmp:
#     obj_list_to_save.append(os.path.basename(obj_tmp))

obj_dst = r'C:\Users\zelinli6\OneDrive - City University of Hong Kong - Student\Documents\02paper cunmin segmentation\figure_single_cells\Ea'
IS_CHANGING_CELL_MTL = False

target_cells = [['Ea','Ear', 'Eal']]

print(target_cells)
for obj_basename in obj_list_to_save:
    obj_path = os.path.join(obj_path_root, obj_basename)
    # =============resave obj ===================
    for idx, targe_cell_name_list in enumerate(target_cells):
        print('dealing with ', targe_cell_name_list)
        selected_cell_data = []
        # Read the OBJ file
        with open(obj_path, 'r') as f:
            obj_data = f.read()

        # Split the OBJ data into lines
        obj_lines = obj_data.split('\n')

        reading_selected_group = False
        selected_cell_data.append(obj_lines[0])
        if IS_CHANGING_CELL_MTL:
            selected_cell_data.append('mtllib designed_mat.mtl\n')
        else:
            selected_cell_data.append(obj_lines[1])

        facet_offset = 0
        found_obj = []
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
                # elif line.startswith('usemtl ') and IS_CHANGING_CELL_MTL:
                #     selected_cell_data.append('usemtl mat_'+cell_fate_dict[cell_name]+'\n')
                else:
                    selected_cell_data.append(line)

                    # If the line starts with 'v' (indicating a vertex), increment the facet offset
            elif line.startswith('v'):
                facet_offset += 1
        print('found ', found_obj)
        if len(found_obj)>0:
            # obj_save_path=os.path.join(os.path.dirname(obj_path),'layer_'+str(idx)+'_'+os.path.basename(obj_path))
            obj_save_path = os.path.join(obj_dst, os.path.basename(obj_path))
            # Write the selected group data to a new OBJ file
            with open(obj_save_path, 'w') as f:
                f.write('\n'.join(selected_cell_data))
    if not IS_CHANGING_CELL_MTL and len(found_obj)>0:
        mtl_file_path = obj_path.replace('.obj', '.mtl')
        shutil.copy2(mtl_file_path, obj_dst)  # target filename is /dst/dir/file.ext
