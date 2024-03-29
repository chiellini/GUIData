import os
import pickle
import treelib
import numpy as np
from tqdm import tqdm
import pandas as pd

from utils.stat_tools import generate_name_series
from utils.cell_tree import construct_celltree

embryo_names = ["191108plc1p1","200109plc1p1", "200113plc1p2", "200113plc1p3", "200322plc1p2", "200323plc1p1",
                "200326plc1p3", "200326plc1p4"]
embryo_TPS = {"191108plc1p1":205,"200109plc1p1":205, "200113plc1p2":255, "200113plc1p3":195, "200322plc1p2":195, "200323plc1p1":185,
                "200326plc1p3":220, "200326plc1p4":195}
volume_folder = r"D:\OneDriveBackup\OneDrive - City University of Hong Kong\paper\7_AtlasCell\DatasetUpdated"
save_folder = r"D:\OneDriveBackup\OneDrive - City University of Hong Kong\paper\7_AtlasCell\DatasetUpdated\QC"

overall_threshold = 0.

# === get name dictionary
num_file = r"D:\OneDriveBackup\OneDrive - City University of Hong Kong\paper\7_AtlasCell\DatasetUpdated\number_dictionary.csv"
pd_number = pd.read_csv(num_file, names=["name", "label"])
number_dict = pd.Series(pd_number.label.values, index=pd_number.name).to_dict()
name_dict = {value: key for key, value in number_dict.items()}


# =====================================================
# Detect error based on volume consistency
# =====================================================
for embryo_name in tqdm(embryo_names, desc="QC"):
    volume_file = os.path.join(volume_folder, embryo_name, embryo_name+"_volume.csv")
    volume_pd = pd.read_csv(volume_file, index_col=0, header=0)
    volume_pd.index = list(range(1, len(volume_pd) + 1, 1))
    cell_names = list(volume_pd)

    nucleus_file = os.path.join("D:/ProjectData/AllDataPacked", embryo_name, "CD{}.csv".format(embryo_name))
    time_tree, _ = construct_celltree(nucleus_file, max_time=embryo_TPS[embryo_name], label2name_dict=num_file)

    # ==================================================
    # 1. Get the degree of cell volume diverge
    # ==================================================
    volume_pd_mean = volume_pd.mean(axis=0, skipna=True)
    volume_pd_median = volume_pd.median(axis=0, skipna=True)
    volume_pd_dif = (volume_pd - volume_pd_median).abs()
    volume_pd_diverge = volume_pd_dif.divide(volume_pd_median)

    tem = volume_pd_diverge.stack()

    outer_number = len(tem.index) # int(len(tem.index) * overall_threshold / 3)

    outer_diverge = volume_pd_diverge.stack().nlargest(outer_number, keep="first").rename("Volume Divergence of Cell")
    outer_names = generate_name_series(number_dict, outer_diverge)
    outer_diverge = pd.concat([outer_names, outer_diverge], axis=1, sort=True)
    outer_diverge.to_csv(os.path.join(save_folder, embryo_name+"_diverge.csv"), index_label=["Time Point", "Cell Name"])


    # ==================================================
    #  2. The volume of two descendents should be constrained by their parent
    # ==================================================
    child2parent_ratio_dict = [] # {"Cell Name": volume of its parent cell}
    names = []
    for cell_name in cell_names:
        if not time_tree[cell_name].is_leaf():
            children = time_tree.children(cell_name)
            children = [child.tag for child in children]
            if (children[0] in cell_names) and (children[1] in cell_names):
                children_volume = volume_pd[children[0]] + volume_pd[children[1]]
                ratio = abs(children_volume - volume_pd_median[cell_name]) / volume_pd_median[cell_name]

                child2parent_ratio_dict += [ratio, ratio]
                names += children

    child2parent_volume = pd.concat(child2parent_ratio_dict, axis=1)
    child2parent_volume.columns = names

    outer_child2parent = child2parent_volume.stack().nlargest(outer_number, keep="first").rename("Children Volume Difference")
    outer_names = generate_name_series(number_dict, outer_child2parent)
    outer_child2parent = pd.concat([outer_names, outer_child2parent], axis=1, sort=True)
    outer_child2parent.to_csv(os.path.join(save_folder, embryo_name+"_child2parent.csv"), index_label=["Time Point", "Cell Name"])


    # ==================================================
    # 3. Check whether one cell is monotonically changing
    # ==================================================
    raw_volume_diff = volume_pd.diff(axis=0).abs()
    raw_volume_diff = raw_volume_diff.drop([1])
    raw_volume_diff.index = list(range(1, len(raw_volume_diff)+1, 1))
    diff2median_ratio = raw_volume_diff.divide(volume_pd_median)

    outer_diff = diff2median_ratio.stack().nlargest(outer_number, keep="first").rename("Volume Difference to Previous TP")
    outer_names = generate_name_series(number_dict, outer_diff)
    outer_diff = pd.concat([outer_names, outer_diff], axis=1, sort=True)
    outer_diff.to_csv(os.path.join(save_folder, embryo_name+"_diff.csv"), index_label=["Time Point", "Cell Name"])

    outer_all = outer_diverge.combine_first(outer_child2parent).combine_first(outer_diff)
    label_column = outer_all.pop("Label").astype("int16")
    outer_all.insert(0, "Label", label_column)
    outer_all.to_csv(os.path.join(save_folder, embryo_name+".csv"), index_label=["Time Point", "Cell Name"])