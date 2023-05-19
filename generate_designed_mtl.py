import glob
import os

working_dir=r'F:\CMap_paper\Figures\Skin Interdigitation\Skin_obj\191108plc1p1'
objs_list=glob.glob(os.path.join(working_dir,'*.obj'))
working_material_color=[[199,214,209],[78,120,118],[251,247,158],[251,247,158]]
working_cell_list=[[
'Caappd','Cpapaa','Caaapp','Caaapa','Caaaap','Caaaaa',

'ABarppaapa','ABarpaappp','ABarpaapap','ABplaaaapp','ABplaaaapa',
],
['Cpappd','Cpapap', 'Cpaapp','Cpaapa','Cpaaap','Cpaaaa',

 'ABarpppapa','ABarpaappa','ABarpapapp','ABarpaapaa',
],
['ABplaaapap',
'ABplaaappa',
'ABplaaappp',
'ABarppaaap',
'ABarppapaa',
'ABarppapap',
'ABplappapa',
'ABarppappa',
'ABplapapaap',  #misssssssssss at the begin
'ABarppappp',
'ABplappppp'],
['ABarpappap',
'ABarpapppa',
'ABarpapppp',
'ABarpppaap',
'ABarppppaa',
'ABarppppap',
'ABprappapa',
'ABarpppppa',
'ABprapapaap',  # misssssssssss at the begin
'ABarpppppp',
'ABprappppp']

]

material_List={'mat_ABarpapppa_416',
               'mat_Cpaapp_934',
               'mat_ABarppaaap_423',
               'mat_ABplaaapap_468',
               'mat_ABarpapapp_410',
               'mat_Cpaapa_933', 'mat_ABarppppaa_444', 'mat_ABarppappp_433', 'mat_Caaapp_887', 'mat_Cpapap_938',
               'mat_ABarppappa_432', 'mat_ABarpaappa_397', 'mat_ABarpaapap_395', 'mat_ABarpapppp_417',
               'mat_ABarppppap_445', 'mat_Caappd_893', 'mat_ABplaaappa_470', 'mat_Cpaaaa_930', 'mat_ABplappapa_523',
               'mat_Cpappd_940', 'mat_Caaaap_884', 'mat_ABarpppppa_447', 'mat_Caaapa_886', 'mat_ABarppaapa_425',
               'mat_ABarpppppp_448', 'mat_Cpaaap_931', 'mat_ABarpappap_414', 'mat_ABarpppapa_440', 'mat_Cpapaa_937',
               'mat_Caaaaa_883', 'mat_ABplaaappp_471', 'mat_ABprappapa_742', 'mat_ABarppapap_430', 'mat_ABarpaapaa_394',
               'mat_ABplappppp_535', 'mat_ABarpppaap_438', 'mat_ABplaaaapp_464', 'mat_ABarppapaa_429',
               'mat_ABplaaaapa_463', 'mat_ABarpaappp_398', 'mat_ABprappppp_754'}

mtl_file_list_to_save=[]
mtl_file_list_to_save.append('# MTL File')
for mat_cell_name_label in material_List:
    cell_name=mat_cell_name_label.split('_')[1]
    for tmp_idx,tmp_list in enumerate(working_cell_list):
        if cell_name in tmp_list:

            mtl_file_list_to_save.append('\n')
            mtl_file_list_to_save.append('newmtl {}'.format(mat_cell_name_label))
            mtl_file_list_to_save.append('Ns 96.078431')
            mtl_file_list_to_save.append('Ka 0.0 0.0 0.0')
            r,g,b=[x/256 for x in working_material_color[tmp_idx]]
            mtl_file_list_to_save.append('Kd {:6f} {:6f} {:6f}'.format(r,g,b))
            mtl_file_list_to_save.append('Ks 0.5 0.5 0.5')
            mtl_file_list_to_save.append('Ni 1.0')
            mtl_file_list_to_save.append('d 1.0')
            mtl_file_list_to_save.append('illum 2')
            break

mtl_save_path=os.path.join(working_dir,'designed_mat.mtl')
with open(mtl_save_path, 'w') as f:
    f.write('\n'.join(mtl_file_list_to_save))

