import glob
import os

naming_dict={'190311plc1mp1':'Emb1','190311plc1mp3':'Emb2','190311plc1mp2':'Emb3','Membrane':'Emb4','190315plc1mp1':'Emb5',
             'emb1':'Emb1','emb2':'Emb2','emb3':'Emb3','emb4':'Emb4','emb5':'Emb5'}
# naming_dict={}

data_source=r'C:\Users\zelinli6\OneDrive - City University of Hong Kong - Student\Documents\02paper cunmin segmentation\EmbSAM\seg_result\seg_cell'

for folder_name in os.listdir(data_source):
    files=glob.glob(os.path.join(data_source,folder_name,'*.nii.gz'))
    embryo_name_this_orin=os.path.basename(files[0]).split('.')[0].split('_')[0]
    for file_name in files:
        target_name=file_name.replace(embryo_name_this_orin,naming_dict[embryo_name_this_orin])
        os.rename(file_name,target_name)