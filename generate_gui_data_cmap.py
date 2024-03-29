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

RENAME_FLAG = True
CHECK_DIVISION = True
TP_CELLS_FLAGE = True
CELLSPAN_FLAG = True
LOST_CELL = True
NEIGHBOR_FLAG = True
GET_DIVISIONS = True
COPY_FILE = True

embryo_names = ["191108plc1p1", "200109plc1p1", "200113plc1p2", "200113plc1p3", "200322plc1p2", "200323plc1p1",
                      "200326plc1p3", "200326plc1p4", "200122plc1lag1ip1", "200122plc1lag1ip2",'200117plc1pop1ip2','200117plc1pop1ip3']

# ==============================================================================
# generate data for GUI
# ==============================================================================
res_embryos = {0.25: [],
               0.18: ["191108plc1p1", "200109plc1p1", "200113plc1p2", "200113plc1p3", "200322plc1p2", "200323plc1p1",
                      "200326plc1p3", "200326plc1p4", "200122plc1lag1ip1", "200122plc1lag1ip2",'200117plc1pop1ip2','200117plc1pop1ip3'],
               }

save_folder = r"D:\OneDriveBackup\OneDrive - City University of Hong Kong\paper\7_AtlasCell\GUIData\DeteletedCell"
data_folder = r"D:\OneDriveBackup\OneDrive - City University of Hong Kong\paper\7_AtlasCell\DatasetUpdated"
raw_folder = r"D:\ProjectData\AllDataPacked"
name_file = data_folder + "/number_dictionary.csv"

max_times = {"191108plc1p1":205, "200109plc1p1":205, "200323plc1p1":185, "200326plc1p3":220, "200326plc1p4":195, "200113plc1p2":255,
             "200113plc1p3": 195, "200322plc1p2":195, "200122plc1lag1ip1":195, "200122plc1lag1ip2":195, "200117plc1pop1ip2":140, "200117plc1pop1ip3":155}
max_slices = {"191108plc1p1":92, "200109plc1p1":92, "200323plc1p1":92, "200326plc1p3":92, "200326plc1p4":92, "200113plc1p2":92,
              "200113plc1p3": 92, "200322plc1p2":92, "200122plc1lag1ip1":92, "200122plc1lag1ip2":92, "200117plc1pop1ip2":92, "200117plc1pop1ip3":92}



pd_number = pd.read_csv(name_file, names=["name", "label"])
number_dict = pd.Series(pd_number.label.values, index=pd_number.name).to_dict()
label2name_dict = dict((v, k) for k, v in number_dict.items())
name2label_dict = dict((k, v) for k, v in number_dict.items())


all_lost_cells = []
# ================== copy files ==============================
if COPY_FILE:
    # volume
    for embryo_name in tqdm(embryo_names, desc="Moving files from CShaper"):

        move_file(os.path.join(data_folder, embryo_name, embryo_name + "_surface.csv"),
                        os.path.join(save_folder, embryo_name, embryo_name + "_surface.csv"))

        move_file(os.path.join(data_folder, embryo_name, embryo_name + "_volume.csv"),
                        os.path.join(save_folder, embryo_name, embryo_name + "_volume.csv"))
        # contact (with transpose)
        transpose_csv(os.path.join(data_folder, embryo_name, embryo_name + "_contact.csv"),
                      os.path.join(save_folder, embryo_name, embryo_name + "_Stat.csv"))

        # raw_folder = os.path.join(data_folder, "RawData", embryo_name, "RawMemb")
        # raw_files = glob.glob(os.path.join(raw_folder, "*.nii.gz"))
        seg_folder = os.path.join(data_folder, embryo_name, "SegCellTimeCombinedLabelUnified")
        seg_files = glob.glob(os.path.join(seg_folder, "*.nii.gz"))
        save_file = os.path.join(save_folder, embryo_name, "SegCell", os.path.basename(seg_files[0]))
        check_folder(save_file)
        for seg_file in seg_files:
            save_file = os.path.join(save_folder, embryo_name, "SegCell", os.path.basename(seg_file))
            move_file(seg_file, save_file)

    move_file(name_file, save_folder + "/name_dictionary.csv")


# =================== save cell life span ======================================

for embryo_name in embryo_names:
    print("Processing {} \n".format(embryo_name))

    volume_file = os.path.join(data_folder, embryo_name, "{}_volume.csv".format(embryo_name))
    contact_file = os.path.join(data_folder, embryo_name, "{}_contact.csv".format(embryo_name))
    ace_file = os.path.join(raw_folder, embryo_name, "CD{}.csv".format(embryo_name))

    volume_pd = pd.read_csv(volume_file, header=0, index_col=0)
    volume_pd.index = list(range(1, len(volume_pd.index) + 1, 1))
    contact_pd = pd.read_csv(contact_file, header=[0, 1], index_col=0)
    celltree, _ = construct_celltree(ace_file, max_time=max_times[embryo_name], label2name_dict=name_file)

    # save cells at tp
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


        # save lifecycle.csv
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

    # save neighbors
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


        # write division
    if GET_DIVISIONS:
        bar = tqdm(total=len(volume_pd))
        bar.set_description("saving divisions")
        for tp, row in volume_pd.iterrows():
            row = row.dropna()
            ace_pd = read_new_cd(ace_file)
            cur_ace_pd = ace_pd[ace_pd["time"] == tp]
            nuc_cells = list(cur_ace_pd["cell"])
            seg_cells = list(row.index)
            dif_cells = list(set(nuc_cells) - set(seg_cells))

            division_cells = []
            lost_cells = []

            # get average radius
            radii_mean = np.power(row, 1/3).mean()
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

                    all_lost_cells.append("{}_{}_{}".format(embryo_name, dif_cell, str(tp).zfill(3)))
                    lost_cells.append(dif_cell)

            division_cells = list(set(division_cells))
            lost_cells = list(set(lost_cells))
            division_cells = [name2label_dict[x] for x in division_cells]
            lost_cells = [name2label_dict[x] for x in lost_cells]

            write_file = os.path.join(save_folder, embryo_name, "LostCell", "{}_{}_lostCell.txt".format(embryo_name, str(tp).zfill(3)))
            write_string = ",".join([str(x) for x in lost_cells]) + "\n"
            check_folder(write_file)

            with open(write_file, "w") as f:
                f.write(write_string)

            write_file = os.path.join(save_folder, embryo_name, "DivisionCell", "{}_{}_division.txt".format(embryo_name, str(tp).zfill(3)))
            write_string = ",".join([str(x) for x in division_cells]) + "\n"
            check_folder(write_file)

            with open(write_file, "w") as f:
                f.write(write_string)

            bar.update(1)

pd_cell_lost = pd.DataFrame(all_lost_cells)
pd_cell_lost.to_csv(os.path.join(save_folder, "all_lost_cells.csv"), index=False)
# =================================================
# write header (https://brainder.org/2012/09/23/the-nifti-file-format/)
# =================================================
if RENAME_FLAG:
    data_files = []
    for embryo_name in embryo_names:
        data_files += glob.glob(os.path.join(save_folder, embryo_name, "*/*.nii.gz"), recursive=True)
        # data_files += glob.glob(os.path.join(seg_folder, "*.nii.gz"))
    data_files.sort()
    for data_file in tqdm(data_files, desc="Adding header"):
        img = nib.load(data_file).get_fdata()
        img = nib.Nifti1Image(img, np.eye(4))
        img.header.set_xyzt_units(xyz=3, t=8)
        res_flag = False
        for res, embryos in res_embryos.items():
            if any([embryo in data_file for embryo in embryos]):
                res_flag = True
                img.header["pixdim"] = [1.0, res, res, res, 0., 0., 0., 0.]
                base_name = os.path.basename(data_file).split(".")[0]
                save_file = os.path.join(save_folder, base_name.split("_")[0], )
                nib.save(img, data_file)
                break
        if not res_flag:
            warnings.warn("No resolution for {}!".format(data_file.split("/")[-1]))