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


# ***********************************************
# functions
# ***********************************************
def test_folder(folder_name):
    if "." in folder_name[1:]:
        folder_name = os.path.dirname(folder_name)
    if not os.path.isdir(folder_name):
        os.makedirs(folder_name)

def transpose_csv(source_file, target_file):
    with open(source_file) as f, open(target_file, 'w', newline='') as fw:
        writer(fw, delimiter=',').writerows(zip(*reader(f, delimiter=',')))

DELETE_FAILED_CELLS = False
CLEAR_SURFACE = True

embryo_names = ["200113plc1p2"]
# ====================================================d==========================
# generate data for GUI
# ==============================================================================
res_embryos = {0.25: [],
               0.18: ["191108plc1p1", "200109plc1p1", "200113plc1p2", "200113plc1p3", "200322plc1p2", "200323plc1p1",
                      "200326plc1p3, ""200326plc1p4", "200122plc1lag1ip1", "200122plc1lag1ip2", "200117plc1pop1ip2", "200117plc1pop1ip3"],
               }

max_times = {"191108plc1p1":205, "200109plc1p1":205, "200323plc1p1":185, "200326plc1p3":220, "200326plc1p4":195, "200113plc1p2":255,
             "200113plc1p3": 195, "200322plc1p2":195, "200122plc1lag1ip1":195, "200122plc1lag1ip2":195, "200117plc1pop1ip2":140, "200117plc1pop1ip3":155}
max_slices = {"191108plc1p1":92, "200109plc1p1":92, "200323plc1p1":92, "200326plc1p3":92, "200326plc1p4":92, "200113plc1p2":92,
              "200113plc1p3": 92, "200322plc1p2":92, "200122plc1lag1ip1":92, "200122plc1lag1ip2":92, "200117plc1pop1ip2":92, "200117plc1pop1ip3":92}


data_folder = r"D:\OneDriveBackup\OneDrive - City University of Hong Kong\paper\7_AtlasCell\DatasetUpdated"
filtered_file = r"D:\OneDriveBackup\OneDrive - City University of Hong Kong\paper\7_AtlasCell\DatasetUpdated\QC\AllDeleted.csv"
seg_folder = r"D:\OneDriveBackup\OneDrive - City University of Hong Kong\paper\7_AtlasCell\GUIData\DeteletedCell"
save_folder = r"D:\OneDriveBackup\OneDrive - City University of Hong Kong\paper\7_AtlasCell\GUIData\DeteletedCell"
name_file = data_folder + "/number_dictionary.csv"

failed_pd = pd.read_csv(filtered_file, header=0, index_col=None)
failed_pd = failed_pd.sort_values("File Info")

pd_number = pd.read_csv(name_file, names=["name", "label"])
number_dict = pd.Series(pd_number.label.values, index=pd_number.name).to_dict()
label2name_dict = dict((v, k) for k, v in number_dict.items())


# =================== Delete Failed Cells ======================================
if DELETE_FAILED_CELLS:
    annotate_to_save = seg_folder

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
            target_file = "_".join([old_embryo_name, old_time_point, "segCell.nii.gz"])
            file_name = os.path.join(seg_folder, old_embryo_name, "SegCell", target_file)
            seg_cell = nib.load(file_name).get_fdata()
            for target_label in labels:
                seg_cell[seg_cell == target_label] = 0
            target_file_name = file_name  # os.path.join(annotate_to_save, old_embryo_name, target_file)
            nib_save(file_name=target_file_name, data=seg_cell)

            # update flags
            old_embryo_name = embryo_name
            old_time_point = time_point
            labels = [label]

        else:
            labels.append(label)
        bar.update(1)

# set surface and volume information of lost cells as zeros
if CLEAR_SURFACE:
    for embryo_name in tqdm(embryo_names, desc="Clear surface"):

        # change surface and volume
        failed_cell_strs = failed_pd[failed_pd["Embryo Name"] == embryo_name]["File Info"].tolist()
        tps = [int(failed_cell_str.split("_")[1]) for failed_cell_str in failed_cell_strs]
        cell_names = [label2name_dict[int(failed_cell_str.split("_")[-1])] for failed_cell_str in failed_cell_strs]
        # volume and surface
        surface_file = os.path.join(data_folder, embryo_name, embryo_name + "_surface.csv")
        volume_file = os.path.join(data_folder, embryo_name, embryo_name + "_volume.csv")
        contact_file = os.path.join(data_folder, embryo_name, embryo_name + "_contact.csv")

        surface_pd = pd.read_csv(surface_file, index_col=0)
        volume_pd = pd.read_csv(volume_file, index_col=0)
        contact_pd = pd.read_csv(contact_file, header=[0, 1])
        for tp, cell_name in zip(tps, cell_names):
            surface_pd.at[tp, cell_name] = np.NaN
            volume_pd.at[tp, cell_name] = np.NaN
            try:
                contact_pd.loc[tp-1, (slice(None), cell_name)] = np.NaN
                contact_pd.loc[tp-1, (cell_name, slice(None))] = np.NaN
            except:
                pass

        surface_pd = surface_pd.dropna(axis=1, how="all")
        volume_pd = volume_pd.dropna(axis=1, how="all")
        contact_pd = contact_pd.dropna(axis=1, how="all")
        # change the contact surface
        # if len(cell_names) != 0:
        #     contact_pd = contact_pd.drop(cell_names, 1, level=0)
        #     contact_pd = contact_pd.drop(cell_names, 1, level=1)

        surface_pd.to_csv(os.path.join(save_folder, embryo_name, embryo_name + "_surface.csv"), index=True)
        volume_pd.to_csv(os.path.join(save_folder, embryo_name, embryo_name + "_volume.csv"), index=True)
        contact_pd.to_csv(os.path.join(save_folder, embryo_name, embryo_name + "_contact.csv"), index=False)
        transpose_csv(os.path.join(save_folder, embryo_name, embryo_name + "_contact.csv"),
                      os.path.join(save_folder, embryo_name, embryo_name + "_Stat.csv"))
