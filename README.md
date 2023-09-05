# dicom2series
Fonctionne comme suit : python3 dicom2series.py -i path/folder_input -o path/folder_output (-anonymise 1 si tu veux anonymiser sinon -anonymise 0 ou rien mettre tout court)
Permet de convertir fichier dicom en niftii/jason avec une nouvelle nomenclature et un chemin spécifique selon le modèle suivant :
/folder_output/DateAcquisition_NomPatient/NuméroSérie_ProcédureImagerie/v_NomPatient_NuméroSérie_ProcédureImagerie.nii/json
Anonymisation faite en remplacant Nompatient par Sujet01 dans tout le chemion et créant aussi des fichiers folder_output/**anonyme**/DateAcquisition_NomPatient/NuméroSérie_ProcédureImagerie/v_NomPatient_NuméroSérie_ProcédureImagerie.nii/json
Crée un dictionnaire avec chemin anonyme : chemin non anonymisé 
