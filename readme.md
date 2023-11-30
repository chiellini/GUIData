# The 3D Visualization Figures and GUI Data Generation

*CMap* Paper Preprint:

Quantitative cell morphology in *C. elegans* embryos reveals regulations of cell volume asymmetry

November 2023

DOI: 10.1101/2023.11.20.567849

LicenseCC BY-NC-ND 4.0


## Generation of 3D GUI Data in *ITK-SNAP-CVE* of *CMap* paper

### Cell-wise GUI Data
* generate_gui_data_cmap.py (for 8+4 uncompressed embryos in [*CMap*](https://doi.org/10.1101/2023.11.20.567849) database)
* generate_gui_data_cshaper.py (for 17 compressed embryos in [*CShaper*](https://www.nature.com/articles/s41467-020-19863-x) database)
![image](https://github.com/chiellini/GUIData/assets/26183529/247c9e43-22a0-4244-9da1-cdb0f4cb10d7)


### Fate-wise GUI Data
* generate_fate_cell_cmap.py (for 8+4 uncompressed embryos in [*CMap*](https://doi.org/10.1101/2023.11.20.567849) database)
* generate_fate_cell_cshaper.py (for 17 compressed embryos in [*CShaper*](https://www.nature.com/articles/s41467-020-19863-x) database)
![image](https://github.com/chiellini/GUIData/assets/26183529/c8a4650a-c6ee-4c5f-aa09-b782f9f84d63)


## Generation of 3D Illustration Figures in *CMap* Paper

![image](https://github.com/chiellini/GUIData/assets/26183529/451b7a20-a050-4ca3-9282-c1ec2aa7e5fb)
![image](https://github.com/chiellini/GUIData/assets/26183529/42c24ac1-3c66-4a7f-8c5d-39213e92918d)



## Generation of Rendering .obj Files for *Blender*
See the details and readme.md in [Github (biomedical-tools)](https://github.com/cao13jf/bioimage-tools).
![image](https://github.com/chiellini/GUIData/assets/26183529/c552a9fc-adb5-44c1-9c91-3cc362fef11d)


# *Useless Notes*


## CMap Visualization Code

### Steps 
1. generate segmentation
2. calculate the wrong division cells in **FILE test_post_segmentation.py** of **PROJECT CellShapeAnalysis**.
3. re-assign the label in **FILE test_post_segmentation.py** of **PROJECT CellShapeAnalysis** with  *frozen tem data*.
4. re-calculate the statistical data of CMap in *def update_wrong_dividing_cell_stat_CMap()* in **FILE test_post_segmentation.py** of **PROJECT CellShapeAnalysis**.
5. assemble them in the **FILE data_repair_stat_code.py** of **PROJECT MembraneProjectCode** with resolution 0.18.
6. generate gui in **PROJECT MembraneProjectCode** with only order gui=true in **FILE TRAIN_TEST.yaml**
7. run **FILE repair_Stat.py** in **PROJECT GUIData** to ensure the contact display in CVE software is normal.



## CShaper Visualization Code
### Steps
1. generate segmentation
2. collect materials
3. generate the volume, surface area, contact surface area in **PROJECT CellShapeAnalysis**
4. generate \*Stat.csv,\*volume.csv,\*surface.csv, in file **cshaper_data_repaircode.py** of **PROJECT MembraneProjectCode**
5. generate GUI data in this project, the 0.25**2 and **3 coefficient will applied to the data here
6. run **FILE repair_Stat.py** in **PROJECT GUIData** to ensure the contact display in CVE software is normal.

## Path
1. raw membrane data (raw_data_folder=r'D:\MembraneProjectData\GUIData\WebData_cshaper_v1'
 or D:\cell_shape_quantification\DATA\Segmentation Results\RawData)
