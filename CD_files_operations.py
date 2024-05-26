import os
import zipfile
import pandas as pd
import glob
import shutil

from utils.data_io import check_folder


def rename_12_cd_files():
    original_cdfiles_path=r'C:\Users\zelinli6\OneDrive - City University of Hong Kong - Student\Documents\04paper CMap coroperation\document\12 morphology CD File'
    renaming_files_path=r'C:\Users\zelinli6\OneDrive - City University of Hong Kong - Student\Documents\04paper CMap coroperation\document\wt_mt_renaming.csv'
    renaming_dict=pd.read_csv(renaming_files_path,index_col=0).to_dict()['0']
    print(renaming_dict)

    cd_files=glob.glob(os.path.join(original_cdfiles_path,'*.csv'))
    renamed_cd_files_to_archive=[]
    for cd_file in cd_files:
        reading_this=pd.read_csv(cd_file)
        file_structure=os.path.join(renaming_dict[os.path.basename(cd_file).split('.')[0][2:]],'Tracing_'+renaming_dict[os.path.basename(cd_file).split('.')[0][2:]]+'.csv')
        # renamed_cd_file=os.path.join(original_cdfiles_path,file_structure)

        renamed_cd_files_to_archive.append(file_structure)
        check_folder(file_structure)
        reading_this.to_csv(file_structure,index=False)

    zipped_file = r'C:\Users\zelinli6\OneDrive - City University of Hong Kong - Student\MembraneProjectData\CMapSubmission\Dataset Access\Dataset B\Dataset B.zip'
    add_files_with_structure_to_zip(zipped_file,renamed_cd_files_to_archive)

    for path in renamed_cd_files_to_archive:
        shutil.rmtree(os.path.dirname(path))
    # ============add the file to the zip with structure===================



def add_files_with_structure_to_zip(zip_file_path,files_to_add):
    with zipfile.ZipFile(zip_file_path, 'a') as zip_ref:
        for file in files_to_add:
            # archive_path = os.path.join('.', file)
            zip_ref.write(file, arcname=file)


def rename_reconstruct_97_cd_files():
    zipped_files_path=r'C:\Users\zelinli6\OneDrive - City University of Hong Kong - Student\Documents\04paper CMap coroperation\Dataset raw images'


    embryo_list_path1=r'C:\Users\zelinli6\OneDrive - City University of Hong Kong - Student\Documents\04paper CMap coroperation\document\expression Table S13.xlsx'
    embryo_list_in_list1=pd.read_excel(embryo_list_path1)
    embryo_list_in_list1=embryo_list_in_list1[embryo_list_in_list1['Data source']=='This paper\'']
    embryo_list_in_list1['purename']=embryo_list_in_list1['Embryo file name'].apply(lambda x:x[2:-5]).to_list()
    # print(embryo_list_in_list1.columns)
    edited_tp_dict=dict(zip(embryo_list_in_list1['purename'].tolist(),embryo_list_in_list1['Edited time point\nfor a complete embryo'].tolist()))
    print(edited_tp_dict)

    renaming_files_path = r'C:\Users\zelinli6\OneDrive - City University of Hong Kong - Student\Documents\04paper CMap coroperation\document\EXP_embryo_renaming.csv'
    renaming_dict = pd.read_csv(renaming_files_path, index_col=0).to_dict()['0']
    print(renaming_dict)

    cd_files=r'C:\Users\zelinli6\OneDrive - City University of Hong Kong - Student\Documents\04paper CMap coroperation\document\97 gene expression CDFiles'
    for cd_file_path in glob.glob(os.path.join(cd_files,'*.csv')):
        embryo_name_this=os.path.basename(cd_file_path).split('.')[0][2:]
        renamed_embryo_name=renaming_dict[embryo_name_this]

        original_cd_df=pd.read_csv(cd_file_path)
        original_cd_df=original_cd_df.loc[original_cd_df['time']<=edited_tp_dict[embryo_name_this]]
        original_cd_df=original_cd_df[['cellTime','blot']]

        multi_index = pd.MultiIndex.from_tuples((('Data1','Cell & Time'), ('Data2','Expression')), names=['column1', 'column2'])
        new_cd_df=pd.DataFrame(columns=multi_index,data=original_cd_df.values)
        new_cd_df[('Data2','Expression')][new_cd_df[('Data2','Expression')]<0]=0
        # print(new_cd_df)
        saving_zipping_csv_path='Tracing_'+renamed_embryo_name+'.csv'
        new_cd_df.to_csv(saving_zipping_csv_path,index=False)

        zipped_file=os.path.join(zipped_files_path,renamed_embryo_name+'.zip')
        assert os.path.exists(zipped_file)
        add_files_with_structure_to_zip(zipped_file,[saving_zipping_csv_path])
        print(zipped_file)

        os.remove(saving_zipping_csv_path)





if __name__ == '__main__':
    rename_reconstruct_97_cd_files()