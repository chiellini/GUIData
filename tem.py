import numpy as np
import os
import shutil
from tqdm import tqdm
from glob import glob
import pandas as pd

from utils.cell_tree import construct_celltree, read_new_cd


cd_file = r"D:\ProjectData\AllRawData\200109plc1p1\aceNuc\CD200109plc1p1.csv"
# name_file = r'D:\OneDriveBackup\OneDrive - City University of Hong Kong\paper\7_AtlasCell\Dataset\number_dictionary.csv'
#
# lost_folder = r"D:\OneDriveBackup\OneDrive - City University of Hong Kong\paper\5_GUIer\GUIWeb\WebData_v7\200109plc1p1\LostCell"
#
# lost_files = glob(os.path.join(lost_folder, "*.txt"))
# pd_ace = read_new_cd(cd_file)
# pd_number = pd.read_csv(name_file, names=["name", "label"])
# number_dict = pd.Series(pd_number.label.values, index=pd_number.name).to_dict()
# label2name_dict = dict((v, k) for k, v in number_dict.items())
#
# tps = []
# cells = []
# for lost_file in lost_files:
#     tp = int(os.path.basename(lost_file).split("_")[1])
#     with open(lost_file, "r") as f:
#         cells0 = f.readline().split(",")[:-1]
#     if len(cells0) == 0:
#         continue
#     names = [label2name_dict[int(cell)] for cell in cells0]
#     tps = tps + [tp] * len(names)
#     cells = cells + names
#
# df = pd.DataFrame(data={"Time": tps, "Cell": cells})
# df.to_csv("./200109plc1p1_failed.csv", index=False)


# =================
# get number of  cells
# =================
# embryo_names = ["191108plc1p1", "200109plc1p1", "200113plc1p2", "200113plc1p3", "200322plc1p2", "200323plc1p1", "200326plc1p3", "200326plc1p4"]
# outs = []
# for idx, embryo_name in enumerate(embryo_names):
#     surface_file = r"D:\OneDriveBackup\OneDrive - City University of Hong Kong\paper\7_AtlasCell\DatasetUpdated\{}\{}_volume.csv".format(embryo_name, embryo_name)
#     pd_ace = pd.read_csv(surface_file, header=0)
#     pd_ace = pd_ace.replace(np.nan, 0)
#     num_cells = pd_ace.astype(bool).sum(axis=1)
#     outs.append(num_cells.astype(np.int16))
#
# out = pd.concat(outs, axis=1)
# out.columns = embryo_names
# out.index = list(range(1, 256))
# out.index.name = "Time Point"
# out.to_csv(r"D:\OneDriveBackup\OneDrive - City University of Hong Kong\paper\7_AtlasCell\DatasetUpdated\cell_numbers.csv", )
#
#

# ========================
# Check lost sisters
# ========================
# save_folder = r"D:\OneDriveBackup\OneDrive - City University of Hong Kong\paper\5_GUIer\GUIWeb\WebData_v7"
# name_file = r'D:\OneDriveBackup\OneDrive - City University of Hong Kong\paper\7_AtlasCell\DatasetUpdated\number_dictionary.csv'
# pd_number = pd.read_csv(name_file, names=["name", "label"])
# number_dict = pd.Series(pd_number.label.values, index=pd_number.name).to_dict()
# label2name_dict = dict((v, k) for k, v in number_dict.items())
# name2label_dict = dict((k, v) for k, v in number_dict.items())
#
# lost_file = os.path.join(save_folder, "all_lost_cells.csv")
# lost_files = pd.read_csv(lost_file, names=["lost_file"])["lost_file"].tolist()
#
# for lost_file in lost_files:
#     str_splits = lost_file.split("_")
#     base_name = "{}_{}_segCell.nii.gz".format(str_splits[0], str_splits[1])
#     cell_label = int(str_splits[2])
#     cell_name = str_splits[-1]
#     embryo_name = str_splits[0]
#     ace_file = os.path.join(r"D:\ProjectData\AllRawData", embryo_name, "aceNuc", "CD{}.csv".format(embryo_name))
#     celltree, _ = construct_celltree(ace_file, len(volume_pd.index), name_file)


# ============= test
from utils.data_io import read_txt_cd

# lineage_file = r"D:\OneDriveBackup\OneDrive - City University of Hong Kong\paper\6_NCommunication\Submission\CShaper Supplementary Data\Segmentation Results\RawData\Sample08\CDSample08.txt"
# name_file = r'D:\OneDriveBackup\OneDrive - City University of Hong Kong\paper\6_NCommunication\Submission\CShaper Supplementary Data\Segmentation Results\number_dictionary.csv'
#
# nucleus_pd = pd.read_csv(lineage_file, delimiter="    ", header=0, index_col=False)
# celltree, _ = construct_celltree(lineage_file, len(nucleus_pd.index), name_file)


# =====================================
# Rename CShaper dataset
# =====================================
# pre_names = []
# for sample_id in range(4, 21, 1):
#     pre_names.append("Sample{}".format(str(sample_id).zfill(2)))
#
# after_names = []
# for sample_id in range(1, 18, 1):
#     after_names.append("Sample{}".format(str(sample_id).zfill(2)))
#
# data_folder = r"D:\OneDriveBackup\OneDrive - City University of Hong Kong\paper\5_GUIer\GUIWeb\WebData_cshaper"

# === change names of folder
# all_files = glob(os.path.join(data_folder, "*"), recursive=False)
# all_files = [file for file in all_files if os.path.isdir(file)]
# all_files.sort()
# for idx, file in enumerate(all_files):  # if folder?
#     pre_name = pre_names[idx]
#     target_name = after_names[idx]
#     assert pre_name in file, "wrong file names"
#     if os.path.isdir(file):
#         dir_name = os.path.dirname(file)
#         base_name = os.path.basename(file)
#         target_base_name = base_name.replace(pre_name, target_name)
#         target_file = os.path.join(dir_name, target_base_name)
#         os.rename(file, target_file)

#===================================================
# pre_csv = pd.read_csv(r"D:\OneDriveBackup\OneDrive - City University of Hong Kong\paper\6_NCommunication\Submission\CShaper Supplementary Data\Segmentation Results\VolumeAndSurface\Sample06_volume.csv", header=[0])
# new_csv =  pd.read_csv(r"D:\tem\updated\181210plc1p2_volume.csv", header=[0])
# pre_csv = pre_csv.append(new_csv[200:], sort=False)
# cols = list(pre_csv.columns)
# pre_csv = pre_csv[cols[1:]]
# pre_csv.to_csv(r"D:\tem\updated\Sample06_volume.csv", index=True)

# ==========================================
# Resave cells to be deleted in mutant cells
# ==========================================
src_file = r"D:\OneDriveBackup\OneDrive - City University of Hong Kong\paper\7_AtlasCell\DatasetUpdated\QC\DeletedCellsRaw\RECORD.csv"
name_dictionary = r"D:\OneDriveBackup\OneDrive - City University of Hong Kong\paper\7_AtlasCell\DatasetUpdated\number_dictionary.csv"

pd_number = pd.read_csv(name_dictionary, names=["name", "label"])
name_dict = dict(zip(pd_number.name, pd_number.label))
pd_data1 = pd.read_csv(src_file, header=0)
pd_data1["Embryo Name"] = pd_data1.apply(lambda row: row["Embryo Name"][2:], axis=1)

pd_data1["Label"] = pd_data1.apply(lambda row: name_dict[row["Cell Name"]], axis=1)
pd_data1["File Info"] = pd_data1.apply(lambda row: "_".join([row["Embryo Name"], str(row["Time Point"]).zfill(3), str(row["Label"])]), axis=1)



src_file = r"D:\OneDriveBackup\OneDrive - City University of Hong Kong\paper\7_AtlasCell\DatasetUpdated\QC\DeletedCellsRaw\RecordNew.csv"
pd_data2 = pd.read_csv(src_file, header=0)
pd_data2["Embryo Name"] = pd_data2.apply(lambda row: row["Embryo Name"][2:], axis=1)

pd_data2["Label"] = pd_data2.apply(lambda row: name_dict[row["Cell Name"]], axis=1)
pd_data2["File Info"] = pd_data2.apply(lambda row: "_".join([row["Embryo Name"], str(row["Time Point"]).zfill(3), str(row["Label"])]), axis=1)


pd_data = pd.concat([pd_data1, pd_data2], ignore_index=True)
pd_data = pd_data.sort_values(by=["File Info"])

dst_file = r"D:\OneDriveBackup\OneDrive - City University of Hong Kong\paper\7_AtlasCell\DatasetUpdated\QC\AllDeleted.csv"
pd_data.to_csv(dst_file, index=False)
