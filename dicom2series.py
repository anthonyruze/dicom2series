dir# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import argparse
import subprocess
import json
import os
import glob
import pandas as pd
import shutil
import pathlib



parser = argparse.ArgumentParser(description="first python version")
parser.add_argument('-i', '--infile',required=False, help='input file, in JSON format')
parser.add_argument('-o', '--outfile', required=False, help='output file, in JSON format')
parser.add_argument('-anonymise', '--anonymise',required=False,type=int, default= 0)
args = parser.parse_args()

w = args.anonymise

if args.infile :
    dir_input = args.infile
    print (dir_input)
else :
    print ('Renseignez dossier d entrée via -i path')



if args.outfile :
    dir_output = args.outfile
    print (dir_output)
else :
    print ('Renseignez dossier de sortie via -o path')

subprocess.run(['dcm2niix', '-ba', 'n','-o',dir_output, dir_input])


file_jsons = glob.glob(dir_output + "/*.json")
synonyme_dict = {}
for onefile in file_jsons:
    with open(onefile) as f:
         info = json.load(f)
         a = info['SeriesNumber']
         PatientName = info['PatientName']
         date = info['AcquisitionDateTime'][:10]
         exam_dir = f'{date}_' + PatientName + f'/S{a:2}_' + info['ProcedureStepDescription']
         final_output = dir_output + '/' + exam_dir
         exam_dir_2 = f'{date}_' + 'Sujet01' + f'/S{a:2}_' + info['ProcedureStepDescription']
         final_output_2 = dir_output + '/' + exam_dir_2
         final_nifti_2 = final_output_2 + '/v_' + 'Sujet01' + f'S{a:02}' + info['ProcedureStepDescription'] + '.nii'
         final_json_2 = final_nifti_2[:-3] + 'json'
         final_nifti = final_output + '/v_' +  PatientName + f'S{a:02}' + info['ProcedureStepDescription'] + '.nii'
         file_nifti = onefile[:-4] + 'nii'
         final_json = final_nifti[:-3] + 'json'
         file_jason = onefile
         if w == 1 :
            pathlib.Path(final_output_2).mkdir(parents=True, exist_ok=True)
            final = os.rename(file_nifti , final_nifti_2)
            final_2 = os.rename(file_jason, final_json_2)
            dir_anonyme = dir_output +  '/anonyme/' + exam_dir + '/'
            pathlib.Path(dir_anonyme).mkdir(parents=True, exist_ok=True)
            final_anonyme_nii = dir_anonyme + 'v_' + PatientName + f'S{a:02}' + info['ProcedureStepDescription'] + '.nii'
            final_ano_json = final_anonyme_nii[:-3] + 'json'
            shutil.copy(final_json_2,final_ano_json)
            shutil.copy(final_nifti_2,final_anonyme_nii)
            synonyme_dict.update({final_nifti: final_nifti_2})
            with open(final_json_2, 'r+') as g:
                json_data = json.load(g)
                json_data['PatientName'] = "Sujet01"
                json_data['PatientID'] = "Sujet01"
                g.seek(0)
                g.write(json.dumps(json_data))
                g.truncate()

         else :
            pathlib.Path(final_output).mkdir(parents=True, exist_ok=True)
            final = os.rename(file_nifti , final_nifti)
            final_2 = os.rename(file_jason, final_json)

if w == 1 :
    df = pd.DataFrame([synonyme_dict]).T
    fichier_anonyme = dir_output + '/correspondance_anonyme.csv'
    df.to_csv(fichier_anonyme, header=False)

