import os
import glob
import shutil

import pandas as pd
from tqdm import tqdm
import numpy as np
from PIL import Image
from skimage.transform import resize
from skimage.exposure import rescale_intensity
from utils.utils import nib_load, nib_save, P
from scipy.ndimage.morphology import grey_closing

# ################# Draw videos
label_number_first = True

src_folder = r'F:\CMap_paper\Figures\NotchDiagram\3Dniigz'
dst_folder = r"F:\CMap_paper\Figures\NotchDiagram\tiff"  # need to change to generate complete or half

# embryo_name_this='191108plc1p1_012_segCell_1'
# embryo_name_this='200109plc1p1_016_segCell_2'
# embryo_name_this='200109plc1p1_016_segCell_3'
# embryo_name_this='200109plc1p1_055_segCell_4'
# embryo_name_this='200109plc1p1_071_segCell_5'
embryo_name_this='200109plc1p1_083_segCell_6'

# not_transparent_cells = ['P2', 'ABp', 'ABa']
# not_transparent_cells = ['MS', 'ABalp', 'ABala']
# not_transparent_cells = ['MS', 'ABara', 'ABarp']
# not_transparent_cells = ['ABalapa', 'ABalapp', 'ABplaaa', 'ABplaap']
# not_transparent_cells = ['MSapp', 'ABplpapp', 'ABplpapa']
not_transparent_cells = ['MSappp', 'ABplpppp', 'ABplpppa']

seg_file_reading = os.path.join(src_folder, "{}.nii.gz".format(embryo_name_this))
# base_name = os.path.basename(seg_file_reading).split(".")[0]

name_file_path = os.path.join(os.path.dirname(src_folder), 'name_dictionary.csv')
label_name_dict = pd.read_csv(name_file_path, index_col=0).to_dict()['0']
name_label_dict = {value: key for key, value in label_name_dict.items()}

seg_original = nib_load(seg_file_reading)
cell_labels_list=np.unique(seg_original).tolist()[1:]
seg_original_normalized=np.zeros(seg_original.shape)
seg_original_normalized[seg_original!=0]=255
for cell_name in not_transparent_cells:
    this_cell_label=name_label_dict[cell_name]
    reduce_this=this_cell_label%255
    print(cell_name,this_cell_label,reduce_this)
    assert this_cell_label in cell_labels_list
    seg_original_normalized[seg_original==this_cell_label]=reduce_this

print(np.unique(seg_original_normalized,return_counts=True))
seg_original_normalized=grey_closing(seg_original_normalized,size=(2,2,2)).astype(np.uint8)
print(np.unique(seg_original_normalized,return_counts=True))

tif_imgs = []
num_slices = seg_original_normalized.shape[-1]
for i_slice in range(num_slices):
    tif_img = Image.fromarray(seg_original_normalized[..., i_slice], mode="P")
    tif_img.putpalette(P)
    tif_imgs.append(tif_img)
save_file = os.path.join(dst_folder, "_".join([embryo_name_this, "render.tif"]))
if os.path.isfile(save_file):
    os.remove(save_file)

# label_num = np.unique(seg_original_normalized).tolist()[-1]
# if label_number_first:
#     label_number_first=False
#     with open(label_file, "w") as f:
#         f.write("{}\n".format(label_num))
# else:
#     with open(label_file, "a") as f:
#         f.write("{}\n".format(label_num))

tif_imgs[0].save(save_file, save_all=True, append_images=tif_imgs[1:])
