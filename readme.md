
# CMap Code
## step
1. generate segmentation
2. calculate the wrong division cells in **FILE test_post_segmentation.py** of **PROJECT CellShapeAnalysis**.
3. re-assign the label in **FILE test_post_segmentation.py**.
4. re-calculate the statistical data of CMap.
5. assemble them in the **FILE data_repair_stat_code.py** of **PROJECT MembraneProjectCode**.
6. generate gui in **PROJECT MembraneProjectCode** with order gui=true in **FILE TRAIN_TEST.yaml**




# CShaper Code
## step
1. generate segmentation
2. collect materials
3. generate the volume, surface area, contact surface area in **PROJECT CellShapeAnalysis**
4. generate \*Stat.csv,\*volume.csv,\*surface.csv, in file **cshaper_data_repaircode.py** of **PROJECT MembraneProjectCode**
5. generate GUI data in this project, the 0.25**2 and **3 coefficient will applied to the data here
6. run repair_Stat.py to ensure the contact display in CVE software is normal.

## material (path)
1. raw membrane data (raw_data_folder=r'D:\MembraneProjectData\GUIData\WebData_cshaper_v1'
 or D:\cell_shape_quantification\DATA\Segmentation Results\RawData)
2. 
