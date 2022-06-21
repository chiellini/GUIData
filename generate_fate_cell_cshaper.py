import os
import glob
import pickle
import warnings
import shutil
import numpy as np
import nibabel as nib
from tqdm import tqdm
import pandas as pd
from scipy import ndimage, stats
from csv import reader, writer
from skimage.morphology import ball


# import user defined library
from utils.data_io import generate_sphere, read_txt_cd
from utils.data_io import nib_load, nib_save, add_dict, get_volume, check_folder, move_file
from utils.cell_tree import construct_celltree, read_new_cd


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

RENAME_FLAG = False
CHECK_DIVISION = True
TP_CELLS_FLAGE = True
CELLSPAN_FLAG = True
LOST_CELL = True
NEIGHBOR_FLAG = True
GET_DIVISIONS = True
COPY_FILE = False
Update_stat=False


embryo_names = []
for sample_id in range(4, 21, 1):
    embryo_names.append("Sample{}".format(str(sample_id).zfill(2)))
samplename_realname=[]


# ==============================================================================
# generate cshaper data for GUI----cell fate
# ==============================================================================


save_folder = r"D:\BaiduNetdiskWorkspace\GUIData\WebData_cshaper_cell_fate"
data_folder = r"D:\OneDriveBackup\OneDrive - City University of Hong Kong\paper\6_NCommunication\Submission\CShaper Supplementary Data\Segmentation Results"
name_file = data_folder + "/name_dictionary.csv"



# =========================
# read cell fate
# =========================
fate_file = r"D:\OneDriveBackup\OneDrive - City University of Hong Kong\paper\7_AtlasCell\DatasetUpdated\CellFate.xls"
cell_fate = pd.read_excel(fate_file, names=["Cell", "Fate"], converters={"Cell": str, "Fate": str}, header=None)
cell_fate = cell_fate.applymap(lambda x: x[:-1])
cell2fate = dict(zip(cell_fate.Cell, cell_fate.Fate))
all_fates = sorted(list(set(sorted(list(cell_fate.Fate)))))
fate2label = dict(zip(all_fates, list(range(1, len(all_fates) + 1, 1))))
pd.DataFrame.from_dict(dict(zip( list(range(1, len(all_fates) + 1, 1)),all_fates)),orient='index').to_csv(save_folder + "/name_dictionary.csv")

pd_number = pd.read_csv(name_file, names=["name", "label"],header=0)
number_dict = pd.Series(pd_number.label.values, index=pd_number.name).to_dict()

print(number_dict)

label2name_dict = dict((k, v) for k, v in number_dict.items())
name2label_dict = dict((v, k) for k, v in number_dict.items())
print(name2label_dict)

log_file = r"D:\BaiduNetdiskWorkspace\AdditionFiles\CshaperPairedFate.csv"
cell_fate["Cell label"] = cell_fate.apply(lambda x: name2label_dict[x["Cell"]], axis=1)
cell_fate["Fate label"] = cell_fate.apply(lambda x: fate2label[x["Fate"]], axis=1)
cell_fate.to_csv(log_file, index=False)
# =========================
# change to fate-wise labels
# =========================
def change_labels(seg, label2name_dict, cell2fate, fate2label):
    new_seg = np.zeros_like(seg)
    labels = list(np.unique(seg))[1:]
    for label in labels:
        tissue_label = fate2label[cell2fate.get(label2name_dict[label],'Unspecified')]
        new_seg[seg==label] = tissue_label

    return new_seg

all_lost_cells = []

if Update_stat:
    for embryo_name in tqdm(embryo_names, desc="Moving files from CShaper {} Segmentation Result"):
        file_name = os.path.join(data_folder, 'VolumeAndSurface', embryo_name + "_surface.csv")
        pd_data = pd.read_csv(file_name, index_col=0, header=0)
        pd_data = pd_data.applymap(lambda x: "")
        file_name = os.path.join(save_folder, embryo_name, embryo_name + "_surface.csv")
        check_folder(file_name)
        pd_data.to_csv(file_name)

        file_name = os.path.join(data_folder, 'VolumeAndSurface', embryo_name + "_volume.csv")
        pd_data = pd.read_csv(file_name, index_col=0, header=0)
        pd_data = pd_data.applymap(lambda x: "")
        file_name = os.path.join(save_folder, embryo_name, embryo_name + "_volume.csv")
        pd_data.to_csv(file_name)

        # contact (with transpose)


        save_name = os.path.join(save_folder, embryo_name, embryo_name + "_Stat.csv")
        transpose_csv(os.path.join(data_folder, "ContactInterface", embryo_name + "_Stat.csv"),
                      os.path.join(save_folder, embryo_name, embryo_name + "_Stat.csv"))
        pd_data = pd.read_csv(save_name, index_col=None, header=0)
        pd_data = pd_data.applymap(lambda x: "")
        pd_data.to_csv(save_name, index=False)

# ================== copy files ==============================
if COPY_FILE:
    # volume
    for embryo_name in tqdm(embryo_names, desc="Moving files from CShaper {} Segmentation Result"):
        file_name = os.path.join(data_folder, 'VolumeAndSurface', embryo_name + "_surface.csv")

        raw_folder = os.path.join(data_folder, 'RawData',embryo_name, "RawMemb")
        raw_files = sorted(glob.glob(os.path.join(raw_folder, "*.nii.gz")))

        seg_folder = os.path.join(data_folder, 'SegmentedCell',embryo_name+'LabelUnified')
        seg_files = sorted(glob.glob(os.path.join(seg_folder, "*.nii.gz")))
        save_file = os.path.join(save_folder, embryo_name, "SegCell", os.path.basename(seg_files[0]))
        check_folder(save_file)
        save_file = os.path.join(save_folder, embryo_name, "RawMemb", os.path.basename(raw_files[0]))
        check_folder(save_file)
        for raw_file, seg_file in zip(raw_files, seg_files):
            save_file = os.path.join(save_folder, embryo_name, "SegCell", os.path.basename(seg_file))
            seg = nib_load(seg_file)
            seg = change_labels(seg, label2name_dict, cell2fate, fate2label)
            nib_save(seg, save_file)

            save_file = os.path.join(save_folder, embryo_name, "RawMemb", os.path.basename(raw_file))
            move_file(raw_file, save_file)


# =================== save cell life span ======================================

for embryo_name in embryo_names:
    print("Processing {} \n".format(embryo_name))

    seg_folder = os.path.join(save_folder, embryo_name, "SegCell")
    seg_files = sorted(glob.glob(os.path.join(seg_folder, "*.nii.gz")))

    volume_file = os.path.join(save_folder, embryo_name, "{}_volume.csv".format(embryo_name))
    ace_file = os.path.join(data_folder, "RawData", embryo_name, "CD{}.txt".format(embryo_name))


    volume_pd = pd.read_csv(volume_file, header=0, index_col=0)
    volume_pd.index = list(range(1, len(volume_pd.index) + 1, 1))
    ace_pd = pd.read_csv(ace_file, engine='python', delimiter="    ", header=0, index_col=False)
    ace_pd.columns = ["cell", "time", "z", "x", "y"]
    celltree, _ = construct_celltree(ace_file, len(volume_pd.index), name_file, read_old=True)
    # save cells at tp
    if TP_CELLS_FLAGE:
        bar = tqdm(total=len(seg_files))
        bar.set_description("saving tp cells")
        for tp in range(1, len(seg_files)+1, 1):

            write_file = os.path.join(save_folder, embryo_name, "TPCell", "{}_{}_cells.txt".format(embryo_name, str(tp).zfill(3)))
            cell_label =list(fate2label.values())
            write_string = ",".join([str(x) for x in cell_label]) + "\n"
            check_folder(write_file)

            with open(write_file, "w") as f:
                f.write(write_string)
            bar.update(1)


        # save lifecycle.csv
    if CELLSPAN_FLAG:
        write_file = os.path.join(save_folder, embryo_name, "{}_lifescycle.csv".format(embryo_name))
        check_folder(write_file)

        open(write_file, "w").close()
        bar = tqdm(total=len(volume_pd.columns))
        bar.set_description("saving life cycle")
        for cell_col in list(fate2label.values()):
            label_tps = [str(cell_col)] + list(range(1, len(volume_pd.index)+1, 1))

            write_string = ",".join([str(x) for x in label_tps]) + "\n"

            with open(write_file, "a") as f:
                f.write(write_string)

        bar.update(1)

    # save neighbors
    if NEIGHBOR_FLAG:
        bar = tqdm(total=len(seg_files))
        bar.set_description("saving neighbors")
        for tp in range(1, len(seg_files)+1, 1):

            write_file = os.path.join(save_folder, embryo_name, "GuiNeighbor", "{}_{}_guiNeighbor.txt".format(embryo_name, str(tp).zfill(3)))
            check_folder(write_file)

            neighbors = {1: [2], 2:[1]}
            with open(write_file, "a") as f:

                for k, v in neighbors.items():
                    labels = [k] + list(set(v))
                    write_string = ",".join([str(x) for x in labels]) + "\n"
                    f.write(write_string)

            bar.update(1)

        # write division
    if GET_DIVISIONS:
        bar = tqdm(total=len(volume_pd))
        bar.set_description("saving divisions")
        for tp, row in volume_pd.iterrows():


            write_file = os.path.join(save_folder, embryo_name, "LostCell", "{}_{}_lostCell.txt".format(embryo_name, str(tp).zfill(3)))
            write_string = "\n"
            check_folder(write_file)

            with open(write_file, "w") as f:
                f.write(write_string)

            write_file = os.path.join(save_folder, embryo_name, "DivisionCell", "{}_{}_division.txt".format(embryo_name, str(tp).zfill(3)))
            write_string = "\n"
            check_folder(write_file)

            with open(write_file, "w") as f:
                f.write(write_string)

            bar.update(1)
#
# pd_cell_lost = pd.DataFrame(all_lost_cells)
# pd_cell_lost.to_csv(os.path.join(save_folder, "all_lost_cells.csv"), index=False)
# =================================================
# write header (https://brainder.org/2012/09/23/the-nifti-file-format/)
# =================================================
# if RENAME_FLAG:
#     data_files = []
#     for embryo_name in embryo_names:
#         data_files += glob.glob(os.path.join(data_folder, embryo_name, "*/*.nii.gz"), recursive=True)
#         # data_files += glob.glob(os.path.join(seg_folder, "*.nii.gz"))
#     data_files.sort()
#     for data_file in tqdm(data_files, desc="Adding header"):
#         img = nib.load(data_file).get_fdata()
#         img = nib.Nifti1Image(img, np.eye(4))
#         img.header.set_xyzt_units(xyz=3, t=8)
#         res_flag = False
#         for res, embryos in res_embryos.items():
#             if any([embryo in data_file for embryo in embryos]):
#                 res_flag = True
#                 img.header["pixdim"] = [1.0, res, res, res, 0., 0., 0., 0.]
#                 base_name = os.path.basename(data_file).split(".")[0]
#                 save_file = os.path.join(save_folder, base_name.split("_")[0], )
#                 nib.save(img, data_file)
#                 break
#         if not res_flag:
#             warnings.warn("No resolution for {}!".format(data_file.split("/")[-1]))
#
# if CHECK_DIVISION:
#     lost_file = os.path.join(save_folder, "all_lost_cells.csv")
#     pd_lost = pd.read_csv(lost_file)

