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
from skimage.transform import resize

# ***********************************************
# functions
# ***********************************************
def test_folder(folder_name):
    if "." in folder_name[1:]:
        folder_name = os.path.dirname(folder_name)
    if not os.path.isdir(folder_name):
        os.makedirs(folder_name)

def transpose_csv(source_file, target_file):
    with open(source_file) as f, open(target_file, 'w') as fw:
        writer(fw, delimiter=',').writerows(zip(*reader(f, delimiter=',')))

RENAME_FLAG = True
CELLSPAN_FLAG = False
TP_CELLS_FLAGE = False
LOST_CELL = False
NEIGHBOR_FLAG = False
COPY_FILE = False

embryo_names = ["200113plc1p2", "200113plc1p3"]
volume_ratio = 1.0

# =================================================
# write header (https://brainder.org/2012/09/23/the-nifti-file-format/)
# =================================================
if RENAME_FLAG:
    res_embryos = {0.25: [],
           0.18: ["191108plc1p1", "200109plc1p1", "200113plc1p2", "200113plc1p3", "200322plc1p2", "200323plc1p1",
                  "200326plc1p3", "200326plc1p4"],
    }

    data_folder = r"D:\OneDriveBackup\OneDrive - City University of Hong Kong\paper\5_NMethodPaper\GUIWeb\WebData_V5\GUIData"
    data_files = []
    for embryo_name in embryo_names:
        data_files += glob.glob(os.path.join(data_folder, embryo_name, "*/*.nii.gz"), recursive=True)
    data_files.sort()
    for data_file in tqdm(data_files, desc="Adding header"):
        img = nib.load(data_file)
        img_data = img.get_fdata()
        # out_shape = [int(x*volume_ratio) for x in img_data.shape]
        # img_data = resize(img_data, output_shape=out_shape, order=0, preserve_range=True, anti_aliasing=False).astype(np.int16)
        if "raw" in data_file:
            img_data = img_data.astype(np.uint8)
        elif "seg" in data_file:
            img_data = img_data.astype(np.uint16)
        else:
            raise Exception("Please specific the kind of image")
        img = nib.Nifti1Image(img_data, np.eye(4))
        img.header.set_xyzt_units(xyz=3, t=8)
        res_flag = False
        for res, embryos in res_embryos.items():
            if any([embryo in data_file for embryo in embryos]):
                res_flag = True
                res = res / volume_ratio
                img.header["pixdim"] = [1.0, res, res, res, 0., 0., 0., 0.]
                nib.save(img, data_file, )
                break
        if not res_flag:
            warnings.warn("No resolution for {}!".format(data_file.split("/")[-1]))