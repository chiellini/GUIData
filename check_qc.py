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

from utils.data_io import nib_load, nib_save

# =============================
# Get all annotation files in dataset and datasetupdated
# =============================
# src_folder = r"D:\OneDriveBackup\OneDrive - City University of Hong Kong\paper\7_CNS\Dataset"
# dst_folder = r"D:\OneDriveBackup\OneDrive - City University of Hong Kong\paper\7_CNS\DatasetUpdated"
#
# src_files = sorted(glob.glob(os.path.join(src_folder, "*/SegCellTimeCombinedLabelUnified/*nii.gz")))
# dst_files = sorted(glob.glob(os.path.join(dst_folder, "*/SegCellTimeCombinedLabelUnified/*nii.gz")))
#
# bugs = []
# for src_file, dst_file in tqdm(zip(src_files, dst_files)):
#     src_data = nib_load(src_file)
#     dst_data = nib_load(dst_file)
#
#     dif_mask = src_data != dst_data
#     all_labels, all_counts = np.unique(src_data, return_counts=True)
#     all_dict = dict(zip(all_labels, all_counts))
#     dif_labels, dif_counts = np.unique(src_data[dif_mask], return_counts=True)
#     for label, count in zip(dif_labels, dif_counts):
#         if label != 0 and count / all_dict[label] > 0.2:
#             bug = os.path.basename(src_file).split(".")[0] + "_{}".format(str(label).zfill(3))
#             bugs.append(bug)
#
# bugs = "\n".join(bugs)
# with open("./output/bug_list.txt", "w") as f:
#     f.write(bugs)



# =============================
# Get all QC annotation file list
# =============================
# src_folder = r"D:\OneDriveBackup\OneDrive - City University of Hong Kong\paper\7_CNS\MannualAnnotations\Finished\QCAnnotation"
#
# src_files = sorted(glob.glob(os.path.join(src_folder, "*/*_G.nii.gz")))
#
# bugs = []
# for src_file in tqdm(src_files):
#     src_data = nib_load(src_file)
#
#     all_labels = np.unique(src_data)
#     for label in all_labels:
#         if label != 0:
#             # ====== for 2D
#             bug = os.path.basename(src_file).replace("_G", "_{}".format(str(label).zfill(4))).split(".")[0]
#             bugs.append(bug)
#
# bugs = "\n".join(bugs)
# with open("./output/QC_annotation_list.txt", "w") as f:
#     f.write(bugs)

# =============================
# get the different in 2D annotations
# =============================
# with open("./output/bug_list.txt", "r") as f:
#     seg = f.read().split("\n")
#
# with open("./output/QC_annotation_list.txt", "r") as f:
#     ann = f.read().split("\n")
#
# dif = list(set(seg) & set(ann))
# dif.sort()
#
# with open("./output/QC_annotation_dif.txt", "w") as f:
#     dif = "\n".join(dif)
#     f.write(dif)
#


# ==================================
# check large difference
# ==================================
# with open("./output/QC_annotation_dif.txt", "r") as f:
#     anns = f.read().split("\n")
#
# src_folder = r"D:\OneDriveBackup\OneDrive - City University of Hong Kong\paper\7_CNS\Dataset"
# dst_folder = r"D:\OneDriveBackup\OneDrive - City University of Hong Kong\paper\7_CNS\MannualAnnotations\Finished\QCAnnotation"
#
# for ann in tqdm(anns):
#     label = int(ann.split("_")[-1])
#     base_name = "_".join(ann.split("_")[:3])
#     embryo_name = ann.split("_")[0]
#
#     src_file = os.path.join(src_folder, embryo_name, "SegCellTimeCombinedLabelUnified", base_name + ".nii.gz")
#     dst_file =

# =========================
# Format the statistics
# =========================
# volume_files = glob.glob(r"D:\OneDriveBackup\OneDrive - City University of Hong Kong\paper\7_AtlasCell\DatasetUpdated\**\*_volume.csv", recursive=True)
# surface_files = glob.glob(r"D:\OneDriveBackup\OneDrive - City University of Hong Kong\paper\7_AtlasCell\DatasetUpdated\**\*_surface.csv", recursive=True)
# for volume_file, surface_file in zip(volume_files, surface_files):
#     volume = pd.read_csv(volume_file, header=0, index_col=0)
#     surface = pd.read_csv(surface_file, header=0, index_col=0)
#     volume.index = list(range(1, len(volume)+1, 1))
#     surface.index = list(range(1, len(volume)+1, 1))
#     volume.index.name = "Time point"
#     surface.index.name = "Time point"
#     volume.to_csv(volume_file)
#     surface.to_csv(surface_file)

# qc_files = glob.glob(r"D:\OneDriveBackup\OneDrive - City University of Hong Kong\paper\7_AtlasCell\DatasetUpdated\QC\*.csv", recursive=True)
# for qc_file in qc_files:
#     qc = pd.read_csv(qc_file)
#     qc["Time Point"] = qc["Time Point"] + 1

