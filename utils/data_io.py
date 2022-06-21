'''library for reading or writing data'''

import os
import pickle
import imageio
import shutil
import pandas as pd
import numpy as np
import nibabel as nib
from skimage import morphology

#==============================================
#  read files
#==============================================
#  load *.nii.gz volume
def nib_load(file_name):
    if not os.path.exists(file_name):
        raise IOError("Cannot find file {}".format(file_name))
    return nib.load(file_name).get_data()


#==============================================
#  write files
#==============================================
#  write *.pkl files
def pkl_save(data, path):
    with open(path, "wb") as f:
        pickle.dump(data, f)

#  write *.nii.gz files
def nib_save(data, file_name):
    check_folder(file_name)
    if "seg" in file_name:
        data = data.astype(np.uint16)
    return nib.save(nib.Nifti1Image(data, np.eye(4)), file_name)

#  write MembAndNuc
def img_save(image, file_name):
    check_folder(file_name)
    imageio.imwrite(file_name, image)

#==============================================
#  data process
#==============================================
def get_bound_pad(r_len, target_x, target_y, target_z, x, y, z, r_mask):

    # lower bound
    if x - r_len <= 0:
        r_mask = r_mask[r_len - x:]
        x1 = 0
        x2 = target_x - r_mask.shape[0]
    if y - r_len <= 0:
        r_mask = r_mask[:, r_len - y:]
        y1 = 0
        y2 = target_y - r_mask.shape[1]
    if z - r_len <= 0:
        r_mask = r_mask[:, :, r_len - z:]
        z1 = 0
        z2 = target_z - r_mask.shape[2]

    # up bound
    if x - r_len >= target_x:
        r_mask = r_mask[:-(x + r_len - target_x)]
        x1 = target_x - r_mask.shape[0]
        x2 = 0
    if y - r_len >= target_y:
        r_mask = r_mask[:, :-(y + r_len - target_y)]
        y1 = target_y - r_mask.shape[1]
        y2 = 0
    if z - r_len >= target_z:
        r_mask = r_mask[:, :, :-(z + r_len - target_z)]
        z1 = target_z - r_mask.shape[2]
        z2 = 0

    # normal
    if x - r_len > 0 and x + r_len < target_x:
        x1 = int((target_x - r_len) * (x / target_x))
        x2 = target_x - r_len - x1
    if y - r_len > 0 and y + r_len < target_y:
        y1 = int((target_y - r_len) * (y / target_y))
        y2 = target_y - r_len - y1
    if z - r_len > 0 and z + r_len < target_z:
        z1 = int((target_z - r_len) * (z / target_z))
        z2 = target_z - r_len - z1

    target_mask = np.pad(r_mask, pad_width=[(x1, x2), (y1, y2), (z1, z2)], mode="constant")

    return target_mask

def generate_sphere(raw_img, x, y, z, radius):
    tem_mask = morphology.ball(radius)
    r_len = tem_mask.shape[0]
    target_x, target_y, target_z = raw_img.shape

    target_mask = get_bound_pad(r_len, target_x, target_y, target_z, x, y, z, tem_mask)

    return target_mask

def normalize3d(image, mask=None):
    assert len(image.shape) == 3, "Only support 3 D"
    assert image[0, 0, 0] == 0, "Background should be 0"
    if mask is not None:
        mask = (image > 0)
    mean = image[mask].mean()
    std = image[mask].std()
    image = image.astype(dtype=np.float32)
    image[mask] = (image[mask] - mean) / std
    return image


#===============================================
#  other utils
def check_folder(file_name):
    if "." in file_name:
        dir_name = os.path.dirname(file_name)
    else:
        dir_name = file_name
    if not os.path.isdir(dir_name):
        os.makedirs(dir_name)


# ==============
def add_dict(k, v, target):
    if k in target:
        if v not in target[k]:
            target[k] = target[k] + [v]
    else:
        target[k] = [v]

    return target

def move_file(src_file, dst_file):
    assert os.path.isfile(src_file), "src_file not exist"
    dir_name = os.path.dirname(dst_file)
    check_folder(dir_name)

    shutil.copyfile(src_file, dst_file)

def get_volume(volume_file):

    volume_pd = pd.read_csv(volume_file, header=0, index_col=0)

    return volume_pd

def get_contact(contact_file):
    contact_pd = pd.read_csv(contact_file, header=[0, 1], index_col=0)

    return contact_pd

def read_txt_cd(lineage_file, raw_size, out_size):
    nucleus_pd = pd.read_csv(lineage_file, delimiter="    ", header=0, index_col=False)
    nucleus_pd = nucleus_pd.dropna(axis=1, how='all')
    # derive the location of nucleus based on the size difference
    nucleus_pd["X"] = out_size["x_size"] / raw_size["x_size"] * nucleus_pd["X"]
    nucleus_pd["Y"] = out_size["y_size"] / raw_size["y_size"] * nucleus_pd["Y"]
    nucleus_pd["Z"] = out_size["z_size"] / raw_size["z_size"] * (raw_size["z_size"] - nucleus_pd["Z"])
    nucleus_pd = nucleus_pd.astype({"X": int, "Y": int, "Z": int})

    return nucleus_pd