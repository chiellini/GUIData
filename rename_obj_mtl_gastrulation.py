import os
import glob


target_obj_cell_set_list=[
    {
'ABalaap',
'ABalapp',
'ABalpaaap',
'ABalpaapp',
'ABalpaaaaa',
'ABalpaaaap',
'ABalpaapaa',
'ABalpaapap',
'ABalpappaa',
'ABalpapppa',
'ABalpapppp',
'ABalpppa',
'ABalpppp',
'ABaraaapaa',
'ABaraaapap',
'ABaraapaa',
'ABaraapap',
'ABaraappa',
'ABaraappp',
'ABarapaaaa',
'ABarapaaap',
'ABarapaap',
'ABarapapaa',
'ABarapappa',
'ABarapappp',
'ABarappp',
'ABplppap',
'ABprpaap',
'ABprpapppa',
'ABprpapppp',

},
    {
'MS',
        'MSa',
        'MSp',
        'MSaa',
        'MSap',
        'MSpa',
        'MSpp',
'MSaaaa',
'MSaaap',
'MSaapaa',
'MSaapap',
'MSaappa',
'MSaappp',
'MSapaa',
'MSapap',
'MSappa',
'MSappp',
'MSpaaa',
'MSpaap',
'MSpapaa',
'MSpapap',
'MSpappa',
'MSpappp',
'MSppaa',
'MSppap',
'MSpppa',
'MSpppp',

    },{'EMS',
        'E',
'Ea',
'Ep',
       'Eal',
       'Ear',
       'Epl',
       'Epr',
'Eala',
'Ealp',
       'Eara',
'Earp',

'Epla',
'Eplp',

       'Epra',
'Eprp',



    },
    {
        'C',
        'Ca',
        'Cp'
        'Cap',
        'Cpp',
        'Capa',
        'Capp',
        'Cppa',
        'Cppp',

'Capaa',
'Capap',
'Cappa',
'Cappp',
'Cppaa',
'Cppap',
'Cpppa',
'Cpppp'

    },
    {'D',
        'Da',
        'Dp',
'Daa',
'Dap',
'Dpa',
'Dpp',

    },
    {'P2',
     'P3',
     'P4'},
    {'Z2',
'Z3'
}
]
predecent_len=5
new_target_obj_cell_set_list=[set(),set(),set(),set(),set(),set(),set()]
for lineage_idx, lineage_set in enumerate(target_obj_cell_set_list):
    print(lineage_idx,len(lineage_set),lineage_set)
    for item_this in lineage_set:
        new_target_obj_cell_set_list[lineage_idx].add(item_this)
        if len(item_this)>predecent_len:
            for predescent_len in range(predecent_len,len(item_this)):
                new_target_obj_cell_set_list[lineage_idx].add(item_this[:predescent_len])
    print(len(new_target_obj_cell_set_list[lineage_idx]),new_target_obj_cell_set_list[lineage_idx])


other_cell_color=[200, 200, 200]
# AB, MS, E, C, D, P, Z
target_mtl_color_list=[
    # [6,0,237],
    [200, 200, 200],
    [0,100,100],
    [0,240,0],
    [247,2,245],
    [240,0,0],
[242,244,0],
    [1,1,1]
    # others
]
target_mtl_name_list=[
    'AB',
    'MS', 'E', 'C', 'D', 'P' ,'Z']

# =============rename  obj ===================
obj_list=glob.glob(os.path.join(r'F:\obj_web_visulizaiton\obj_combined\200113plc1p2', '*.obj'))
dst_folder=r'F:\CMap_paper\Figures\Gastrulation\objs'
count_cell_list=[]
for obj_path in obj_list:
    print('dealing with ' + obj_path)
    obj_save_path=os.path.join(dst_folder,'gastrulation_'+os.path.basename(obj_path))
    with open(obj_path) as f:
        lines = f.readlines()
    count_cell_this=0
    with open(obj_save_path, 'w') as f:
        for line in lines:
            if line.startswith('mtllib '):
                # print(cell_name_cell_label)
                f.write('mtllib designed_mat.mtl' + '\n')
            elif line.startswith('usemtl '):
                # usemtl mat_ABp_449
                cell_name,cell_label = line.split(' ')[1].split('\n')[0].split('_')[1:]
                IS_FOUND=False
                for tmp_color_idx,tmp_cell_set in enumerate(new_target_obj_cell_set_list):
                    if cell_name in tmp_cell_set:
                        f.write('usemtl mat_gastrulation_'+target_mtl_name_list[tmp_color_idx] + '\n')
                        count_cell_this+=1
                        IS_FOUND=True
                        break
                if not IS_FOUND:
                    f.write('usemtl mat_gastrulation_OTHER' + '\n')
            else:
                f.write(line)
    count_cell_list.append(count_cell_this)

# Save the list to a text file
with open(os.path.join(dst_folder,'cell_count_list.txt'), 'w') as f:
    for item in count_cell_list:
        f.write(f'{item}\n')



mtl_file_list_to_save=[]
mtl_file_list_to_save.append('# MTL File')
for tmp_color_idx,tmp_color_list in enumerate(target_mtl_color_list):

    mtl_file_list_to_save.append('\n')
    mtl_file_list_to_save.append('newmtl mat_gastrulation_'+target_mtl_name_list[tmp_color_idx])
    mtl_file_list_to_save.append('Ns 96.078431')
    mtl_file_list_to_save.append('Ka 0.0 0.0 0.0')
    r,g,b=[x/256 for x in tmp_color_list]
    mtl_file_list_to_save.append('Kd {:6f} {:6f} {:6f}'.format(r,g,b))
    mtl_file_list_to_save.append('Ks 0.5 0.5 0.5')
    mtl_file_list_to_save.append('Ni 1.0')
    mtl_file_list_to_save.append('d 1.0')
    mtl_file_list_to_save.append('illum 2')

mtl_file_list_to_save.append('\n')
mtl_file_list_to_save.append('newmtl mat_gastrulation_OTHER')
mtl_file_list_to_save.append('Ns 96.078431')
mtl_file_list_to_save.append('Ka 0.0 0.0 0.0')
r,g,b=[x / 256 for x in other_cell_color]
mtl_file_list_to_save.append('Kd {:6f} {:6f} {:6f}'.format(r,g,b))
mtl_file_list_to_save.append('Ks 0.5 0.5 0.5')
mtl_file_list_to_save.append('Ni 1.0')
mtl_file_list_to_save.append('d 1.0')
mtl_file_list_to_save.append('illum 2')

mtl_save_path=os.path.join(dst_folder,'designed_mat.mtl')
with open(mtl_save_path, 'w') as f:
    f.write('\n'.join(mtl_file_list_to_save))