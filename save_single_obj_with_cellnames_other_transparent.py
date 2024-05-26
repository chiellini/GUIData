import os
import glob
import shutil

# 'CD200113plc1p2' 'WT_Sample1'
# 'CD200322plc1p2' 'WT_Sample2'
# 'CD200323plc1p1' 'WT_Sample3'
# 'CD200326plc1p3' 'WT_Sample4'
# 'CD200326plc1p4' 'WT_Sample5'
# 'CD191108plc1p1' 'WT_Sample6'
# 'CD200109plc1p1' 'WT_Sample7'
# 'CD200113plc1p3' 'WT_Sample8'


obj_path_root = r'F:\obj_web_visulizaiton\obj_combined\200113plc1p2'
obj_list_objs_tmp = ['200113plc1p2_156_segCell.obj','200113plc1p2_255_segCell.obj']
mtl_list_objs_tmp=['200113plc1p2_156_segCell.mtl','200113plc1p2_255_segCell.mtl']


# obj_path_root=r'C:\Users\zelinli6\OneDrive - City University of Hong Kong - Student\Documents\02paper cunmin segmentation\segmentation results\combined_objs\190315plc1mp1'
# obj_list_objs_tmp=sorted(glob.glob(os.path.join(obj_path_root,'*.obj')))
# mtl_list_objs_tmp=sorted(glob.glob(os.path.join(obj_path_root,'*.mtl')))
# obj_list_to_save=[]
# for obj_tmp in obj_list_objs_tmp:
#     obj_list_to_save.append(os.path.basename(obj_tmp))

obj_dst = r'C:\Users\zelinli6\OneDrive - City University of Hong Kong - Student\Documents\08paper zhaoke paper\biggest movement objs'
IS_CHANGING_CELL_MTL = True

# target_cells = ['ABa','ABp','ABar','ABal','ABpr','ABpl']
# target_cells = ['ABpl']
# target_cells = ['Ea','Ep']

target_cells = ['MSppaapp']


print(target_cells)
found_obj_list=set()

# =================modify mtl ====================================
for mtl_index,mtl_path in enumerate(mtl_list_objs_tmp):
    # print('dealing with ' + mtl_path)

    mtl_path=os.path.join(obj_path_root,mtl_path)
    mtl_save_path=os.path.join(obj_dst,os.path.basename(mtl_path))

    mtl_file_list_to_save = []
    mtl_file_list_to_save.append('# MTL File')
    with open(mtl_path) as f:
        lines = f.readlines()
    count_cell_this=0
    is_reading_selected_mtl = False
    this_mat_name=None

    for line in lines:
        if line.startswith('newmtl mat_'):
            # usemtl mat_ABp_449

            cell_name,cell_label = line.split(' ')[1].split('\n')[0].split('_')[1:]

            if cell_name in target_cells:
                # if cell_name in tmp_cell_set:
                is_reading_selected_mtl=True
                this_mat_name = 'mat_{}_{}'.format(cell_name, cell_label)
                print(os.path.basename(mtl_path),this_mat_name)
                found_obj_list.add(mtl_index)
            else:
                is_reading_selected_mtl=False
        if is_reading_selected_mtl:
            if line.startswith('Kd '):
                mtl_file_list_to_save.append('\n')
                mtl_file_list_to_save.append('newmtl {}'.format(this_mat_name))
                mtl_file_list_to_save.append('Ns 96.078431')
                mtl_file_list_to_save.append('Ka 0.0 0.0 0.0')
                mtl_file_list_to_save.append(line.split('\n')[0])
                mtl_file_list_to_save.append('Ks 0.5 0.5 0.5')
                mtl_file_list_to_save.append('Ni 1.0')
                mtl_file_list_to_save.append('d 1.0')
                mtl_file_list_to_save.append('illum 2')

    mtl_file_list_to_save.append('\n')
    mtl_file_list_to_save.append('newmtl mat_material_transparent')
    mtl_file_list_to_save.append('Ns 96.078431')
    mtl_file_list_to_save.append('Ka 0.0 0.0 0.0')
    mtl_file_list_to_save.append('Kd {:6f} {:6f} {:6f}'.format(200 / 256, 200/256, 200/256))
    mtl_file_list_to_save.append('Ks 0.5 0.5 0.5')
    mtl_file_list_to_save.append('Ni 1.0')
    mtl_file_list_to_save.append('d 0.15')
    mtl_file_list_to_save.append('illum 2')

    if mtl_index in found_obj_list:
        with open(mtl_save_path, 'w') as f:
            f.write('\n'.join(mtl_file_list_to_save))

# ======================modify the obj========================================
for obj_index,obj_path in enumerate(obj_list_objs_tmp):
    if obj_index in found_obj_list:
        # print('dealing with ' + obj_path)
        obj_path=os.path.join(obj_path_root,obj_path)
        obj_save_path=os.path.join(obj_dst,os.path.basename(obj_path))
        with open(obj_path) as f:
            lines = f.readlines()
        count_cell_this=0
        with open(obj_save_path, 'w') as f:
            for line in lines:
                if line.startswith('usemtl '):
                    # usemtl mat_ABp_449
                    cell_name,cell_label = line.split(' ')[1].split('\n')[0].split('_')[1:]
                    IS_FOUND=False
                    if cell_name in target_cells:
                        # if cell_name in tmp_cell_set:
                        f.write(line)
                        count_cell_this+=1
                        IS_FOUND=True
                    else:
                        f.write('usemtl mat_material_transparent' + '\n')
                else:
                    f.write(line)
