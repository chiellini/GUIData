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
# Get all 2D annotation file list
# =============================
# src_folder = r"D:\OneDriveBackup\OneDrive - City University of Hong Kong\paper\7_CNS\MannualAnnotations\Finished\2DAnnotation"
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
#             bug = os.path.basename(src_file).replace("_128_G", "_{}".format(str(label).zfill(4))).split(".")[0]
#             bugs.append(bug)
#
# bugs = "\n".join(bugs)
# with open("./output/2D_annotation_list.txt", "w") as f:
#     f.write(bugs)

# =============================
# get the different in 2D annotations
# =============================
# with open("./output/bug_list.txt", "r") as f:
#     seg = f.read().split("\n")
#
# with open("./output/2D_annotation_list.txt", "r") as f:
#     ann = f.read().split("\n")
#
# dif = list(set(seg) & set(ann))
# dif.sort()
#
# with open("./output/2D_annotation_dif.txt", "w") as f:
#     dif = "\n".join(dif)
#     f.write(dif)
#



    # ********************
# =============================
# Get all 2D annotation file list
# =============================
src_folder = r"D:\OneDriveBackup\OneDrive - City University of Hong Kong\paper\7_CNS\MannualAnnotations\Finished\3DAnnotation"
src_files = sorted(glob.glob(os.path.join(src_folder, "*/*_G.nii.gz")))

bugs = []
for src_file in tqdm(src_files):
    src_data = nib_load(src_file)

    all_labels = np.unique(src_data)
    for label in all_labels:
        if label != 0:
            # ====== for 2D
            bug = os.path.basename(src_file).replace("_G", "_{}".format(str(label).zfill(4))).split(".")[0]
            bugs.append(bug)

bugs = "\n".join(bugs)
with open("./output/3D_annotation_list.txt", "w") as f:
    f.write(bugs)

# =============================
# get the different in 2D annotations
# =============================
with open("./output/bug_list.txt", "r") as f:
    seg = f.read().split("\n")

with open("./output/3D_annotation_list.txt", "r") as f:
    ann = f.read().split("\n")

dif = list(set(seg) & set(ann))
dif.sort()

with open("./output/3D_annotation_dif.txt", "w") as f:
    dif = "\n".join(dif)
    f.write(dif)