import os
import glob
import pickle
import warnings
import shutil
import numpy as np
import nibabel as nib
from tqdm import tqdm
import pandas as pd
from csv import reader, writer

# import user defined library
from utils.data_io import nib_load, nib_save
from utils.cell_tree import construct_celltree, read_new_cd

# ***********************************************
# functions
# ***********************************************
def move_the_files_for_delete():
    embryo_names = ['191108plc1p1', '200109plc1p1', '200113plc1p2', '200113plc1p3', '200322plc1p2', '200323plc1p1',
                    '200326plc1p3', '200326plc1p4', '200122plc1lag1ip1', '200122plc1lag1ip2', '200117plc1pop1ip2',
                    '200117plc1pop1ip3']


    src_dir = r'C:\Users\zelinli6\OneDrive - City University of Hong Kong - Student\MembraneProjectData\GUIData\WebData_CMap_cell_label_v3'
    dst_dir = r'C:\Users\zelinli6\OneDrive - City University of Hong Kong - Student\MembraneProjectData\GUIData\WebData_CMap_cell_label_deleted'
    exclude_dir = 'RawMemb'

    for idx, embryo_name in enumerate(embryo_names):
        src_path = os.path.join(src_dir, embryo_name)
        dst_path = os.path.join(dst_dir, embryo_name)
        if not os.path.exists(dst_path):
            os.makedirs(dst_path)
        for item in os.listdir(src_path):
            src_path_this = os.path.join(src_path, item)
            dst_path_this = os.path.join(dst_path, item)

            if os.path.isdir(src_path_this) and item != exclude_dir:
                shutil.copytree(src_path_this, dst_path_this)
            elif os.path.isfile(src_path_this):
                shutil.copy2(src_path_this, dst_path_this)


def test_folder(folder_name):
    if "." in folder_name[1:]:
        folder_name = os.path.dirname(folder_name)
    if not os.path.isdir(folder_name):
        os.makedirs(folder_name)


def transpose_csv(source_file, target_file):
    with open(source_file) as f, open(target_file, 'w', newline='') as fw:
        writer(fw, delimiter=',').writerows(zip(*reader(f, delimiter=',')))


def delete_and_combine_annotated_gui():
    DELETE_FAILED_CELLS = False
    REGENERATE_OTHER_GUI_FILES = True

    COMBINE_ANNOTATED_GUI_FROM_DELETED_GUI=False

    embryo_names = ["191108plc1p1", "200109plc1p1", "200113plc1p2", "200113plc1p3", "200322plc1p2", "200323plc1p1",
                    "200326plc1p3", "200326plc1p4", "200122plc1lag1ip1", "200122plc1lag1ip2", '200117plc1pop1ip2',
                    '200117plc1pop1ip3']
    max_times = {"191108plc1p1": 205, "200109plc1p1": 205, "200323plc1p1": 185, "200326plc1p3": 220,
                 "200326plc1p4": 195, "200113plc1p2": 255,
                 "200113plc1p3": 195, "200322plc1p2": 195, "200122plc1lag1ip1": 195, "200122plc1lag1ip2": 195,
                 "200117plc1pop1ip2": 140, "200117plc1pop1ip3": 155}
    data_folder = r"C:\Users\zelinli6\OneDrive - City University of Hong Kong - Student\MembraneProjectData\GUIData\WebData_CMap_cell_label_v3"
    filtered_file = r"F:\CMap_paper\Code\AnnotationCheck\DataSource\CMapToDrop20230420.csv"
    # seg_folder = r"D:\OneDriveBackup\OneDrive - City University of Hong Kong\paper\7_AtlasCell\GUIData\DeteletedCell"
    save_folder = r"C:\Users\zelinli6\OneDrive - City University of Hong Kong - Student\MembraneProjectData\GUIData\WebData_CMap_cell_label_deleted"
    name_file_path = data_folder + "/name_dictionary.csv"
    raw_folder = r"F:\CMap_paper\AllDataPacked"


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

    print(failed_pd)

    changed_embryos_tp=set()
    # =================== Delete Failed Cells ======================================
    if DELETE_FAILED_CELLS:
        # annotate_to_save = seg_folder

        # ==== Multiple segs in the same file will be saved together
        old_embryo_name = ""
        old_time_point = ""
        labels = []
        FIRST_RUN = True
        bar = tqdm(total=len(failed_pd.index), desc="Separating segs")
        for i_file, file_string in failed_pd["File Info"].items():
            embryo_name, time_point, label = file_string.split("_")
            label = int(label)
            if FIRST_RUN:
                old_embryo_name = embryo_name
                old_time_point = time_point
                FIRST_RUN = False

            if (old_time_point != time_point or old_embryo_name != embryo_name) and len(labels) != 0:

                # generate seg
                changed_embryos_tp.add('{}_{}'.format(old_embryo_name,old_time_point))
                target_file = "_".join([old_embryo_name, old_time_point, "segCell.nii.gz"])
                file_name = os.path.join(data_folder, old_embryo_name, "SegCell", target_file)
                seg_cell = nib.load(file_name).get_fdata()
                for target_label in labels:
                    seg_cell[seg_cell == target_label] = 0
                target_file_name = os.path.join(save_folder, old_embryo_name, "SegCell", target_file)
                nib_save(file_name=target_file_name, data=seg_cell)
                # update flags
                old_embryo_name = embryo_name
                old_time_point = time_point
                labels = [label]
            else:
                labels.append(label)
            bar.update(1)

    # set surface and volume information of lost cells as zeros
    if REGENERATE_OTHER_GUI_FILES:
        for embryo_name in tqdm(embryo_names, desc="Clear surface"):

            # change surface and volume
            failed_cell_strs = failed_pd[failed_pd["Embryo Name"] == embryo_name]["File Info"].tolist()
            tps = [int(failed_cell_str.split("_")[1]) for failed_cell_str in failed_cell_strs]
            cell_names = [label_name_dict[int(failed_cell_str.split("_")[-1])] for failed_cell_str in failed_cell_strs]
            # volume and surface
            surface_file = os.path.join(data_folder, embryo_name, embryo_name + "_surface.csv")
            volume_file = os.path.join(data_folder, embryo_name, embryo_name + "_volume.csv")
            contact_file = os.path.join(data_folder, embryo_name, embryo_name + "_Stat.csv")

            surface_pd = pd.read_csv(surface_file, index_col=0)
            volume_pd = pd.read_csv(volume_file, index_col=0)
            contact_pd = pd.read_csv(contact_file, index_col=[0, 1],header=0)
            # print(contact_pd)
            contact_pd=contact_pd.transpose()
            # print(volume_pd.index, volume_pd.columns)
            # print(surface_pd.index, surface_pd.columns)
            # print(contact_pd.index, contact_pd.columns)

            # quit(0)
            for tp, cell_name in zip(tps, cell_names):
                surface_pd.at[tp, cell_name] = np.NaN
                volume_pd.at[tp, cell_name] = np.NaN

                try:
                    contact_pd.loc[str(tp),(slice(None), cell_name)] = np.NaN
                    contact_pd.loc[str(tp),(cell_name, slice(None))] = np.NaN
                except:
                    print(cell_name, 'have no contact at ', tp)


            surface_pd = surface_pd.dropna(axis=1, how="all")
            volume_pd = volume_pd.dropna(axis=1, how="all")
            contact_pd = contact_pd.dropna(axis=0, how="all")

            # print(volume_pd.index,volume_pd.columns)
            # print(surface_pd.index,surface_pd.columns)
            # print(contact_pd.index,contact_pd.columns)

            # change the contact surface
            # if len(cell_names) != 0:
            #     contact_pd = contact_pd.drop(cell_names, 1, level=0)
            #     contact_pd = contact_pd.drop(cell_names, 1, level=1)

            surface_pd.to_csv(os.path.join(save_folder, embryo_name, embryo_name + "_surface.csv"), index=True)
            volume_pd.to_csv(os.path.join(save_folder, embryo_name, embryo_name + "_volume.csv"), index=True)
            contact_pd.to_csv(os.path.join(save_folder, embryo_name, embryo_name + "_contact.csv"), index=True)
            transpose_csv(os.path.join(save_folder, embryo_name, embryo_name + "_contact.csv"),
                          os.path.join(save_folder, embryo_name, embryo_name + "_Stat.csv"))
            os.remove(os.path.join(save_folder, embryo_name, embryo_name + "_contact.csv"))


            # ====================save cells at tp==========================
            bar = tqdm(total=len(volume_pd))
            bar.set_description("saving tp cells")
            for tp, row in volume_pd.iterrows():
                row = row.dropna()
                cell_names = list(row.index)
                cell_label = [name_label_dict[x] for x in cell_names]

                write_file = os.path.join(save_folder, embryo_name, "TPCell",
                                          "{}_{}_cells.txt".format(embryo_name, str(tp).zfill(3)))
                write_string = ",".join([str(x) for x in cell_label]) + "\n"
                # check_folder(write_file)

                with open(write_file, "w") as f:
                    f.write(write_string)
                bar.update(1)

            # ======================save lifecycle.csv========================
            write_file = os.path.join(save_folder, embryo_name, "{}_lifescycle.csv".format(embryo_name))
            # check_folder(write_file)
            open(write_file, "w").close()
            bar = tqdm(total=len(volume_pd.columns))
            bar.set_description("saving life cycle")
            for cell_col in volume_pd:
                valid_index = volume_pd[cell_col].notnull()
                tps = list(volume_pd[valid_index].index)
                label_tps = [name_label_dict[cell_col]] + tps

                write_string = ",".join([str(x) for x in label_tps]) + "\n"

                with open(write_file, "a") as f:
                    f.write(write_string)

            bar.update(1)

            # contact_pd=contact_pd.transpose()
            contact_pd = contact_pd.replace(0, np.nan)
            bar = tqdm(total=len(contact_pd))
            bar.set_description("saving neighbors")
            for tp, row in contact_pd.iterrows():
                row = row.dropna()
                neighbors = {}
                pairs = sorted(list(row.index))
                if len(pairs) == 0:
                    continue
                for cell1, cell2 in pairs:
                    cell1 = name_label_dict[cell1]
                    cell2 = name_label_dict[cell2]
                    if cell1 not in neighbors:
                        neighbors[cell1] = [cell2]
                    else:
                        neighbors[cell1] += [cell2]

                    if cell2 not in neighbors:
                        neighbors[cell2] = [cell1]
                    else:
                        neighbors[cell2] += [cell1]

                write_file = os.path.join(save_folder, embryo_name, "GuiNeighbor",
                                          "{}_{}_guiNeighbor.txt".format(embryo_name, str(tp).zfill(3)))
                # check_folder(write_file)

                open(write_file, "w").close()
                with open(write_file, "a") as f:

                    for k, v in neighbors.items():
                        labels = [k] + list(set(v))
                        write_string = ",".join([str(x) for x in labels]) + "\n"
                        f.write(write_string)

                bar.update(1)

            # ==================generatatatetwea lost and dividing celssssssssss====================
            ace_file_path = os.path.join(raw_folder, embryo_name, "CD{}.csv".format(embryo_name))
            celltree, _ = construct_celltree(ace_file_path, max_time=max_times[embryo_name], label2name_dict=label_name_dict)

            all_lost_cells=[]
            bar = tqdm(total=len(volume_pd))
            bar.set_description("saving divisions")
            for tp, row in volume_pd.iterrows():
                row = row.dropna()
                ace_pd = read_new_cd(ace_file_path)
                cur_ace_pd = ace_pd[ace_pd["time"] == tp]
                nuc_cells = list(cur_ace_pd["cell"])
                seg_cells = list(row.index)
                dif_cells = list(set(nuc_cells) - set(seg_cells))

                division_cells = []
                lost_cells = []

                # get average radius
                radii_mean = np.power(row, 1 / 3).mean()
                lost_radius = radii_mean * 1.3

                # if tp == 179:
                #     print("TEST")

                for dif_cell in dif_cells:
                    parent_cell = celltree.parent(dif_cell).tag
                    sister_cells = [x.tag for x in celltree.children(parent_cell)]
                    sister_cells.remove(dif_cell)
                    sister_cell = sister_cells[0]
                    if parent_cell in seg_cells:
                        division_cells.append(parent_cell)
                    else:

                        all_lost_cells.append("{}_{}_{}".format(embryo_name, dif_cell, str(tp).zfill(3)))
                        lost_cells.append(dif_cell)

                division_cells = list(set(division_cells))
                lost_cells = list(set(lost_cells))
                division_cells = [name_label_dict[x] for x in division_cells]
                lost_cells = [name_label_dict[x] for x in lost_cells]

                write_file = os.path.join(save_folder, embryo_name, "LostCell",
                                          "{}_{}_lostCell.txt".format(embryo_name, str(tp).zfill(3)))
                write_string = ",".join([str(x) for x in lost_cells]) + "\n"
                # check_folder(write_file)

                with open(write_file, "w") as f:
                    f.write(write_string)

                write_file = os.path.join(save_folder, embryo_name, "DivisionCell",
                                          "{}_{}_division.txt".format(embryo_name, str(tp).zfill(3)))
                write_string = ",".join([str(x) for x in division_cells]) + "\n"
                # check_folder(write_file)

                with open(write_file, "w") as f:
                    f.write(write_string)

                bar.update(1)

    if COMBINE_ANNOTATED_GUI_FROM_DELETED_GUI:
        # ===============================================
        # combine annotated gui datatatatatatatatatat into data
        # =================================================
        # read name dictionary
        label_name_dict = pd.read_csv(os.path.join(save_folder,'name_dictionary.csv'), index_col=0).to_dict()['0']
        name_label_dict = {value: key for key, value in label_name_dict.items()}

        checked_dead_data_subfolder=['QCAnnotation','QCAnnotation3','QCAnnotation20230425']
        finished_dead_root_folder=r'F:\CMap_paper\MannualAnnotations\Finished'
        # labelled_csv=pd.DataFrame(columns=['Embryo Name','Time Point','Cell Name'])
        for sub_folder in checked_dead_data_subfolder:
            labbelled_embryo_csv_path=os.path.join(finished_dead_root_folder,sub_folder,'all_annotated.csv')
            labbelled_embryo_csv=pd.read_csv(labbelled_embryo_csv_path)
            old_embryo_name = ""
            old_time_point = ""
            labels = []
            FIRST_RUN = True
            bar = tqdm(total=len(labbelled_embryo_csv.index), desc="Separating segs {}".format(sub_folder))
            for idx_this in labbelled_embryo_csv.index:
                embryo_name, time_point, _,label,_,_,_,_ = labbelled_embryo_csv.loc[idx_this]
                label = int(label)
                if FIRST_RUN:
                    old_embryo_name = embryo_name
                    old_time_point = time_point
                    FIRST_RUN = False

                if (old_time_point != time_point or old_embryo_name != embryo_name) and len(labels) != 0:
                    changed_embryos_tp.add("_".join([old_embryo_name, str(int(old_time_point)).zfill(3)]))
                    # generate seg
                    seg_GROUD_embryo_name="_".join([old_embryo_name, str(int(old_time_point)).zfill(3), "segCell_G.nii.gz"])
                    seg_RAW_embryo_name="_".join([old_embryo_name, str(int(old_time_point)).zfill(3), "segCell.nii.gz"])
                    labelled_file_path = os.path.join(finished_dead_root_folder,sub_folder,old_embryo_name,seg_GROUD_embryo_name)
                    if os.path.exists(labelled_file_path):
                        labelled_cell_data = nib.load(labelled_file_path).get_fdata().astype(int)
                    else:
                        labelled_cell_data = nib.load(
                            os.path.join(finished_dead_root_folder, sub_folder, old_embryo_name,
                                         seg_RAW_embryo_name)).get_fdata().astype(int)

                    deleted_file_path = os.path.join(save_folder, old_embryo_name, "SegCell", seg_RAW_embryo_name)
                    deleted_seg_cell = nib.load(deleted_file_path).get_fdata()

                    for labelled_label in labels:
                        deleted_seg_cell[labelled_cell_data == labelled_label] = labelled_label

                    # target_file_name = file_name  # os.path.join(annotate_to_save, old_embryo_name, target_file)
                    nib.save(nib.Nifti1Image(deleted_seg_cell, np.eye(4)), deleted_file_path)

                    # update flags
                    old_embryo_name = embryo_name
                    old_time_point = time_point
                    labels = [label]

                else:
                    labels.append(label)
                bar.update(1)

        # Save the list to a text file
        with open(os.path.join(save_folder,'changed_embryos_tp_20230429.txt'), 'w') as f:
            for item in changed_embryos_tp:
                f.write(f'{item}\n')

    # # Read the list from the text file
    # with open('my_list.txt', 'r') as f:
    #     my_list = [line.strip() for line in f]

if __name__ == '__main__':
    delete_and_combine_annotated_gui()