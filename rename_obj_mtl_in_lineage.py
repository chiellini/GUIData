import os
import glob

# =============rename  obj ===================
obj_list=glob.glob(os.path.join(r'F:\obj_web_visulizaiton\obj_combined\200113plc1p2', '*.obj'))
dst_folder=r'F:\CMap_paper\Figures\Movie Lineage\lineageColoredObjs'
for obj_path in obj_list:
    print('dealing with ' + obj_path)
    obj_save_path=os.path.join(dst_folder,'lineage_'+os.path.basename(obj_path))
    with open(obj_path) as f:
        lines = f.readlines()
    with open(obj_save_path, 'w') as f:
        for line in lines:
            if line.startswith('mtllib '):
                # print(cell_name_cell_label)
                f.write('mtllib designed_mat.mtl' + '\n')
            elif line.startswith('usemtl '):
                # usemtl mat_ABp_449
                cell_name,cell_label = line.split(' ')[1].split('\n')[0].split('_')[1:]
                if cell_name.startswith('AB'):
                    f.write('usemtl mat_AB' + '\n')
                elif cell_name.startswith('C'):
                    f.write('usemtl mat_C' + '\n')
                elif cell_name.startswith('D'):
                    f.write('usemtl mat_D' + '\n')
                elif cell_name.startswith('E'):
                    f.write('usemtl mat_E' + '\n')
                elif cell_name.startswith('MS'):
                    f.write('usemtl mat_MS' + '\n')
                elif cell_name.startswith('P') or cell_name.startswith('Z'):
                    f.write('usemtl mat_P' + '\n')
                else:
                    print('IMPOSSIBLE THINGS: ',cell_name,cell_label)
                    quit(100)
            else:
                f.write(line)