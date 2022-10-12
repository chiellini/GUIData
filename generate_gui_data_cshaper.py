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

# check and rename
RENAME_FLAG = False
CHECK_DIVISION = True

# guidata needed
TP_CELLS_FLAGE = True
CELLSPAN_FLAG = True
LOST_CELL = True
NEIGHBOR_FLAG = True
GET_DIVISIONS = True
Updata_Stat=True
COPY_FILE = True

embryo_names = []
for sample_id in range(4, 21, 1):
    embryo_names.append("Sample{}".format(str(sample_id).zfill(2)))

# ==============================================================================
# generate data for GUI
# ==============================================================================
# res_embryos = {0.25: [],
#                0.18: ["191108plc1p1", "200109plc1p1", "200113plc1p2", "200113plc1p3", "200322plc1p2", "200323plc1p1",
#                       "200326plc1p3", "200326plc1p4", "200122plc1lag1ip2"],
#                }

save_folder = r"D:\MembraneProjectData\GUIData\WebData_cshaper_v2"
seg_data_folder = r"D:\project_tem\UpdatedSegmentedCell"
raw_data_folder=r'D:\MembraneProjectData\GUIData\WebData_cshaper_v1'
stat_data_path=r'D:\project_tem\Stat'
name_file_path = "./name_dictionary_cshaper.csv"

# max_times = {"191108plc1p1":205, "200109plc1p1":205, "200323plc1p1":185, "200326plc1p3":220, "200326plc1p4":195, "200113plc1p2":255,
#              "200113plc1p3": 195, "200322plc1p2":195, "200122plc1lag1ip1":195, "200122plc1lag1ip2":195}
# max_slices = {"191108plc1p1":92, "200109plc1p1":92, "200323plc1p1":92, "200326plc1p3":92, "200326plc1p4":92, "200113plc1p2":92,
#               "200113plc1p3": 92, "200322plc1p2":92, "200122plc1lag1ip1":92, "200122plc1lag1ip2":92}



pd_number = pd.read_csv(name_file_path, names=["name", "label"])
name2label_dict = pd.Series(pd_number.label.values, index=pd_number.name).to_dict()
# print(name2label_dict)

label2name_dict = dict((v, k) for k, v in name2label_dict.items())
#
# print(label2name_dict)
# print(name2label_dict)

all_lost_cells = []
if Updata_Stat:
    for embryo_name in tqdm(embryo_names, desc="Updating files from CShaper"):
        if not os.path.exists(os.path.join(save_folder, embryo_name)):
            os.makedirs(os.path.join(save_folder, embryo_name))

        volume_coefficient=(0.25)**3
        surface_coefficient=(0.25)**2

        volume_pd=pd.read_csv(os.path.join(stat_data_path, embryo_name + "_volume.csv"), header=0, index_col=0)
        volume_pd.index = list(range(1, len(volume_pd.index) + 1, 1))
        volume_pd=volume_pd*volume_coefficient
        volume_pd.to_csv(os.path.join(save_folder, embryo_name, embryo_name + "_volume.csv"))

        # move_file(os.path.join(data_folder, "VolumeAndSurface", embryo_name + "_volume.csv"),
        #                 os.path.join(save_folder, embryo_name, embryo_name + "_volume.csv"))
        # contact (with transpose)

        surface_pd = pd.read_csv(os.path.join(stat_data_path, embryo_name + "_surface.csv"), header=0,
                                 index_col=0)
        surface_pd.index = list(range(1, len(surface_pd.index) + 1, 1))
        surface_pd=surface_pd*surface_coefficient
        surface_pd.to_csv(os.path.join(save_folder, embryo_name, embryo_name + "_surface.csv"))

        # move_file(os.path.join(data_folder, "VolumeAndSurface", embryo_name + "_surface.csv"),
        #                 os.path.join(save_folder, embryo_name, embryo_name + "_surface.csv"))

        contact_pd = pd.read_csv(os.path.join(stat_data_path, embryo_name + "_Stat.csv"), header=[0, 1], index_col=0).T
        contact_pd=contact_pd*surface_coefficient
        contact_pd.to_csv(os.path.join(save_folder, embryo_name, embryo_name + "_Stat.csv"))
        # print(contact_pd*surface_coefficient)
        # transpose_csv(os.path.join(data_folder, "ContactInterface", embryo_name + "_Stat.csv"),
        #               os.path.join(save_folder, embryo_name, embryo_name + "_Stat.csv"))


# ================== copy files ==============================
if COPY_FILE:
    # volume
    for embryo_name in tqdm(embryo_names, desc="Moving files from CShaper"):

        raw_folder = os.path.join(raw_data_folder, embryo_name, "RawMemb")
        raw_files = glob.glob(os.path.join(raw_folder, "*.nii.gz"))
        seg_folder = os.path.join(seg_data_folder, embryo_name)
        seg_files = glob.glob(os.path.join(seg_folder, "*.nii.gz"))
        save_file = os.path.join(raw_folder, embryo_name, "SegCell", os.path.basename(raw_files[0]))
        check_folder(save_file)
        save_file = os.path.join(raw_folder, embryo_name, "RawMemb", os.path.basename(raw_files[0]))
        check_folder(save_file)
        for raw_file, seg_file in zip(raw_files, seg_files):
            save_file = os.path.join(save_folder, embryo_name, "RawMemb", os.path.basename(raw_file))
            move_file(raw_file, save_file)
            save_file = os.path.join(save_folder, embryo_name, "SegCell", os.path.basename(seg_file))
            move_file(seg_file, save_file)

    move_file(raw_data_folder+ "/name_dictionary.csv", save_folder + "/name_dictionary.csv")


# =================== save cell life span ======================================

for embryo_name in embryo_names:
    print("Processing {} \n".format(embryo_name))

    volume_file = os.path.join(stat_data_path, embryo_name + "_volume.csv")
    contact_file = os.path.join(stat_data_path, embryo_name + "_Stat.csv")
    ace_file = os.path.join('D:\cell_shape_quantification\DATA\Segmentation Results\RawData', embryo_name, "CD{}.txt".format(embryo_name))

    volume_pd = pd.read_csv(volume_file, header=0, index_col=0)
    volume_pd.index = list(range(1, len(volume_pd.index) + 1, 1))
    contact_pd = pd.read_csv(contact_file, header=[0, 1], index_col=0)
    ace_pd = pd.read_csv(ace_file, engine='python',  delimiter="    ", header=0, index_col=False)
    ace_pd.columns = ["cell", "time", "z", "x", "y"]
    celltree, _ = construct_celltree(ace_file, len(volume_pd.index), label2name_dict, read_old=True)

    # save cells at tp,
    if TP_CELLS_FLAGE:
        bar = tqdm(total=len(volume_pd))
        bar.set_description("saving tp cells")
        for tp, row in volume_pd.iterrows():
            row = row.dropna()
            cell_names = list(row.index)
            cell_label = [name2label_dict[x] for x in cell_names]

            write_file = os.path.join(save_folder, embryo_name, "TPCell", "{}_{}_cells.txt".format(embryo_name, str(tp).zfill(3)))
            write_string = ",".join([str(x) for x in cell_label]) + "\n"
            check_folder(write_file)

            with open(write_file, "w") as f:
                f.write(write_string)
            bar.update(1)


    # save lifecycle.csv , cell cycle
    if CELLSPAN_FLAG:
        write_file = os.path.join(save_folder, embryo_name, "{}_lifescycle.csv".format(embryo_name))
        check_folder(write_file)

        open(write_file, "w").close()
        bar = tqdm(total=len(volume_pd.columns))
        bar.set_description("saving life cycle")
        for cell_col in volume_pd:
            valid_index = volume_pd[cell_col].notnull()
            tps = list(volume_pd[valid_index].index)
            label_tps = [name2label_dict[cell_col]] + tps

            write_string = ",".join([str(x) for x in label_tps]) + "\n"

            with open(write_file, "a") as f:
                f.write(write_string)

        bar.update(1)

    # save neighbors (GuiNeighbor)
    if NEIGHBOR_FLAG:
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
                cell1 = name2label_dict[cell1]
                cell2 = name2label_dict[cell2]
                if cell1 not in neighbors:
                    neighbors[cell1] = [cell2]
                else:
                    neighbors[cell1] += [cell2]

                if cell2 not in neighbors:
                    neighbors[cell2] = [cell1]
                else:
                    neighbors[cell2] += [cell1]

            write_file = os.path.join(save_folder, embryo_name, "GuiNeighbor", "{}_{}_guiNeighbor.txt".format(embryo_name, str(tp).zfill(3)))
            check_folder(write_file)

            open(write_file, "w").close()
            with open(write_file, "a") as f:

                for k, v in neighbors.items():
                    labels = [k] + list(set(v))
                    write_string = ",".join([str(x) for x in labels]) + "\n"
                    f.write(write_string)

            bar.update(1)


    # write division cell (the cell is dividing) and LostCell
    if GET_DIVISIONS:
        bar = tqdm(total=len(volume_pd))
        bar.set_description("saving division cell")
        for tp, row in volume_pd.iterrows():
            row = row.dropna()
            # the nucleus is divided but membrane is dividing
            cur_ace_pd = ace_pd[ace_pd["time"] == tp]
            nuc_cells = list(cur_ace_pd["cell"])
            seg_cells = list(row.index)
            # use nucleus information as criteria
            dividing_cells = list(set(nuc_cells) - set(seg_cells))
            # print(nuc_cells,seg_cells,dif_cells) :
            # ['ABal', 'ABar', 'ABpl', 'ABpr', 'EMS', 'P2'] ['ABa', 'ABp', 'EMS', 'P2'] ['ABar', 'ABpl', 'ABal', 'ABpr']

            division_cells = []
            lost_cells = []

            # get average radius ? ? ?
            radii_mean = np.power(row, 1/3).mean()
            lost_radius = radii_mean * 1.3

            # if tp == 179:
            #     print("TEST")

            for dividing_cell in dividing_cells:
                parent_cell = celltree.parent(dividing_cell).tag
                sister_cells = [x.tag for x in celltree.children(parent_cell)]
                sister_cells.remove(dividing_cell)
                sister_cell = sister_cells[0]
                if parent_cell in seg_cells:
                    division_cells.append(parent_cell)
                else:
                    # seg_cell_file = os.path.join(save_folder, embryo_name, "SegCell", "{}_{}_segCell.nii.gz".format(embryo_name, str(tp).zfill(3)))
                    # seg = nib_load(seg_cell_file)
                    # sw, sh, sd = seg.shape
                    # nuc_loc = cur_ace_pd[cur_ace_pd["cell"] == dif_cell]
                    # locy, locx, locz = nuc_loc["x"].values[0] * sh / 712, nuc_loc["y"].values[0] * sw / 512, sd - nuc_loc["z"].values[0] * sd / max_slices[embryo_name]
                    # locx, locy, locz = int(locx), int(locy), int(locz)
                    # to_combine = seg[locx, locy, locz] == name2label_dict[sister_cell]
                    # # nuc_mask = np.zeros_like(seg, dtype=np.uint8)
                    # # nuc_mask = generate_sphere(seg, locx, locy, locz, lost_radius)
                    # # seg[nuc_mask != 0] = name2label_dict[dif_cell]
                    # # print(f"Add lost cells {seg_cell_file}")
                    # # nib_save(seg, seg_cell_file)
                    # # ================= add lost cell's point
                    # if to_combine:
                    #     lost_cell_name = "{}_{}_{}_{}_combine".format(embryo_name, str(tp).zfill(3), name2label_dict[dif_cell], dif_cell)
                    # else:
                    #     lost_cell_name = "{}_{}_{}_{}".format(embryo_name, str(tp).zfill(3), name2label_dict[dif_cell], dif_cell)
                    # the dividing cell (daughter nucleus)
                    all_lost_cells.append("{}_{}_{}".format(embryo_name, dividing_cell, str(tp).zfill(3)))
                    lost_cells.append(dividing_cell)

            division_cells = list(set(division_cells))
            lost_cells = list(set(lost_cells))
            division_cells_label = [name2label_dict[x] for x in division_cells]
            lost_cells = [name2label_dict[x] for x in lost_cells]

            write_file = os.path.join(save_folder, embryo_name, "LostCell", "{}_{}_lostCell.txt".format(embryo_name, str(tp).zfill(3)))
            write_string = ",".join([str(x) for x in lost_cells]) + "\n"
            check_folder(write_file)

            with open(write_file, "w") as f:
                f.write(write_string)

            write_file = os.path.join(save_folder, embryo_name, "DivisionCell", "{}_{}_division.txt".format(embryo_name, str(tp).zfill(3)))
            write_string = ",".join([str(x) for x in division_cells_label]) + "\n"
            check_folder(write_file)

            with open(write_file, "w") as f:
                f.write(write_string)

            bar.update(1)

pd_cell_lost = pd.DataFrame(all_lost_cells)
pd_cell_lost.to_csv(os.path.join(save_folder, "all_lost_cells.csv"), index=False)


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
#         print(data_file)
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
