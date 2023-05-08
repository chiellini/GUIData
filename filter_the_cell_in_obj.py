import os
import glob
import pandas as pd
from tqdm import tqdm
import nibabel as nib

def save_target_cells_in_obj(targe_cell_name_list,ori_obj_file_path,save_obj_file_path):
    # =============resave obj ===================
    # obj_path=os.path.join(r'F:\CMap_paper\Figures\Intestine Twisting', '200113plc1p2_255_segCell.obj')
    print('dealing with ', ori_obj_file_path)
    selected_cell_data=[]
    # Read the OBJ file
    with open(ori_obj_file_path, 'r') as f:
        obj_data = f.read()

    # Split the OBJ data into lines
    obj_lines = obj_data.split('\n')

    reading_selected_group=False
    selected_cell_data.append(obj_lines[0])
    selected_cell_data.append(obj_lines[1])

    facet_offset = 0
    for line in obj_lines:
        # If the line starts with 'g' (indicating a group), check if it is the selected group
        if line.startswith('g'):
            cell_name, cell_label = line.split(' ')[1].split('\n')[0].split('_')
            # f.write(line)
            # group_name = line.split()[1]
            if cell_name in targe_cell_name_list:
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

    # obj_save_path=os.path.join(os.path.dirname(save_obj_file_path),'layer_'+str(idx)+'_'+os.path.basename(obj_path))
    # Write the selected group data to a new OBJ file
    with open(save_obj_file_path, 'w') as f:
        f.write('\n'.join(selected_cell_data))

embryo_names = ["191108plc1p1", "200109plc1p1", "200113plc1p2", "200113plc1p3", "200322plc1p2", "200323plc1p1",
                    "200326plc1p3", "200326plc1p4", "200122plc1lag1ip1", "200122plc1lag1ip2", '200117plc1pop1ip2',
                    '200117plc1pop1ip3']
max_times = {"191108plc1p1": 205, "200109plc1p1": 205, "200323plc1p1": 185, "200326plc1p3": 220,
             "200326plc1p4": 195, "200113plc1p2": 255,
             "200113plc1p3": 195, "200322plc1p2": 195, "200122plc1lag1ip1": 195, "200122plc1lag1ip2": 195,
             "200117plc1pop1ip2": 140, "200117plc1pop1ip3": 155}
raw_gui_data_folder = r"C:\Users\zelinli6\OneDrive - City University of Hong Kong - Student\MembraneProjectData\GUIData\WebData_CMap_cell_label_v3"
filtered_file = r"F:\CMap_paper\Code\AnnotationCheck\DataSource\CMapToDrop20230420.csv"

obj_combined_folder=r'F:\obj_web_visulizaiton\obj_combined'
obj_save_folder = r"F:\obj_web_visulizaiton\obj_filtered"
name_file_path = raw_gui_data_folder + "/name_dictionary.csv"
# raw_folder = r"F:\CMap_paper\AllDataPacked"


# read name dictionary
label_name_dict = pd.read_csv(name_file_path, index_col=0).to_dict()['0']
name_label_dict = {value: key for key, value in label_name_dict.items()}

failed_pd = pd.read_csv(filtered_file, header=0, index_col=None)
failed_pd["Embryo Name"] = failed_pd["Embryo Name"].map(lambda x: x[2:])
failed_pd["Time Point"] = failed_pd["Time Point"].map(lambda x: str(x).zfill(3))
failed_pd["Label"] = failed_pd["Cell Identity"].map(lambda x: str(int(name_label_dict[x])))
failed_pd["Cell Name"] = failed_pd["Cell Identity"]
failed_pd['File Info'] = failed_pd.apply(lambda row: row['Embryo Name'] + '_' + row['Time Point'] +'_'+ row['Label'],
                                         axis=1)
failed_pd = failed_pd.sort_values("File Info")


# ==== Multiple segs in the same file will be saved together
old_embryo_name = ""
old_time_point = ""
labels = []
FIRST_RUN = True
bar = tqdm(total=len(failed_pd.index), desc="Separating segs")
drop_cell_number=0
remaining_cell_number=0

for i_file, file_string in failed_pd["File Info"].items():
    embryo_name, time_point, iterative_label = file_string.split("_")
    # label = int(label)
    if FIRST_RUN:
        old_embryo_name = embryo_name
        old_time_point = time_point
        FIRST_RUN = False

    if (old_time_point != time_point or old_embryo_name != embryo_name) and len(labels) != 0:

        # generate seg
        # changed_embryos_tp.add('{}_{}'.format(old_embryo_name,old_time_point))
        target_file = "_".join([old_embryo_name, old_time_point, "segCell.obj"])
        combined_obj_file_path = os.path.join(obj_combined_folder, old_embryo_name, target_file)

        # =====================select remaining cells===
        with open(combined_obj_file_path, 'r') as f:
            combined_obj_data = f.read()
        combined_obj_lines = combined_obj_data.split('\n')
        dropped_cells=[]
        selected_cell_list=[]
        for line in combined_obj_lines:
            if line.startswith('g'):
                cell_name, cell_label = line.split(' ')[1].split('\n')[0].split('_')
                # cell_label=label_name_dict
                # f.write(line)
                # group_name = line.split()[1]
                if cell_label in labels:
                    drop_cell_number+=1
                    # print(old_embryo_name,old_time_point,cell_name,cell_label)
                    dropped_cells.append(cell_name)
                else:
                    selected_cell_list.append(cell_name)
                    remaining_cell_number+=1
        print(dropped_cells)
        filtered_obj_file_path = os.path.join(obj_save_folder, old_embryo_name, target_file)

        save_target_cells_in_obj(selected_cell_list,combined_obj_file_path,filtered_obj_file_path)
        # ===============================================

        # update flags
        old_embryo_name = embryo_name
        old_time_point = time_point
        labels = [iterative_label]

    else:
        labels.append(iterative_label)
    bar.update(1)

print('remianing cell number', remaining_cell_number)
print('deleted cell number',drop_cell_number)