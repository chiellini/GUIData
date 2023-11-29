
from utils.obj_visulization import combine_objs, rename_objs

if __name__ == "__main__":
    # resize_the_segcell_niigz()
    embryo_names = ['200122plc1lag1ip1', '200122plc1lag1ip2','200117plc1pop1ip2','200117plc1pop1ip3']
    tps = [195, 195, 140, 155]

    # '191108plc1p1'，'200109plc1p1', '200113plc1p2', '200113plc1p3', '200322plc1p2', '200323plc1p1',
    # '200326plc1p3', '200326plc1p4', '200122plc1lag1ip1', '200122plc1lag1ip2', '200117plc1pop1ip2',
    # '200117plc1pop1ip3']
    # tps = [205, 205, 255, 195, 195, 185, 220, 195, 195, 195, 140, 155]
    max_middle_num = 6
    root = r'F:\obj_web_visulizaiton\obj_seperated'
    tiff_map_txt_path = r'F:\obj_web_visulizaiton\tiff\tiffmaptxt'
    rename_objs(embryo_names,tps,max_middle_num,root,tiff_map_txt_path)

    target_root = r'F:\obj_web_visulizaiton\obj_combined'
    combine_objs(embryo_names,tps,max_middle_num,root,target_root)
