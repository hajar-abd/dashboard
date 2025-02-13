###########################################################################################################################################
'''
Manal - Celia
06/02/2025
fonctions pour creation dataframe/dashboard
/!/ doit etre au meme niveau que le script dataframe.py
'''
###########################################################################################################################################
#charger les packages
import pandas as pd
import re
import xml.etree.ElementTree as ET
###########################################################################################################################################

#charger le fichier XML MeSH
# tree = ET.parse("desc2024.xml") #doit etre au meme niveau que le fichier ou preciser le chemin
# root = tree.getroot()

# #code MeSH de Neoplasms
# mesh_code = "C04"
# mesh_dict = {} #utiliser dans le script dataframe

# #construire un dictionnaire des correspondances code -> nom
# mesh_categories = {}
# for descriptor in root.findall("DescriptorRecord"):
#     descriptor_name = descriptor.find("DescriptorName/String").text
#     for tree_number in descriptor.findall(".//TreeNumber"):
#         mesh_categories[tree_number.text] = descriptor_name  # Associe le code à son nom

# #construire le dictionnaire des sous-categories
# for descriptor in root.findall("DescriptorRecord"):
#     descriptor_name = descriptor.find("DescriptorName/String").text
#     categories = []

#     for tree_number in descriptor.findall(".//TreeNumber"):
#         if tree_number.text and tree_number.text.startswith(mesh_code + "."):
#             categories.append(tree_number.text)

#     if categories:
#         #extraire la categorie parent (ex: "C04.588.123" -> "C04.588")
#         first_sublevel = categories[0][:7]  #prend les 7 premiers caracteres "C04.XXX"

#         #recuperer directement le nom du parent sans boucle
#         parent_name = mesh_categories.get(first_sublevel)

#         if parent_name:
#             mesh_dict.setdefault(parent_name, []).append(descriptor_name)

mesh_dict = {
'Neoplasms by Site': ['Abdominal Neoplasms', 'Unilateral Breast Neoplasms',
'Colitis-Associated Neoplasms', 'Cardiac Papillary Fibroelastoma', 'Adrenal Cortex Neoplasms',
'Adrenal Gland Neoplasms', 'Anal Gland Neoplasms', 'Anus Neoplasms', 'Appendiceal Neoplasms',
'Bile Duct Neoplasms', 'Biliary Tract Neoplasms', 'Urinary Bladder Neoplasms', 'Bone Neoplasms', 'Brain Neoplasms',
'Breast Neoplasms', 'Bronchial Neoplasms', 'Carcinoma, Bronchogenic', 'Carcinoma, Non-Small-Cell Lung', 'Cecal Neoplasms',
'Cerebellar Neoplasms', 'Cerebral Ventricle Neoplasms', 'Uterine Cervical Neoplasms', 'Choroid Neoplasms',
'Colonic Neoplasms', 'Colorectal Neoplasms, Hereditary Nonpolyposis', 'Common Bile Duct Neoplasms', 'Conjunctival Neoplasms',
'Cranial Nerve Neoplasms', 'Digestive System Neoplasms', 'Duodenal Neoplasms', 'Ear Neoplasms', 'Endocrine Gland Neoplasms',
'Esophageal Neoplasms', 'Eye Neoplasms', 'Eyelid Neoplasms', 'Facial Neoplasms', 'Fallopian Tube Neoplasms', 'Femoral Neoplasms',
'Gallbladder Neoplasms', 'Gastrointestinal Neoplasms', 'Genital Neoplasms, Female', 'Genital Neoplasms, Male', 'Gingival Neoplasms',
'Head and Neck Neoplasms', 'Heart Neoplasms', 'Hypopharyngeal Neoplasms', 'Hypothalamic Neoplasms', 'Ileal Neoplasms', 'Intestinal Neoplasms',
'Jaw Neoplasms', 'Jejunal Neoplasms', 'Kidney Neoplasms', 'Laryngeal Neoplasms', 'Leukoplakia, Oral', 'Lip Neoplasms', 'Liver Neoplasms',
'Liver Neoplasms, Experimental', 'Lung Neoplasms', 'Mammary Neoplasms, Experimental', 'Mandibular Neoplasms', 'Maxillary Neoplasms',
'Maxillary Sinus Neoplasms', 'Mediastinal Neoplasms', 'Meigs Syndrome', 'Meningeal Neoplasms', 'Mouth Neoplasms', 'Myasthenia Gravis', 'Myelitis, Transverse',
'Nasopharyngeal Neoplasms', 'Nelson Syndrome', 'Neoplasms by Site', 'Multiple Endocrine Neoplasia', 'Paraneoplastic Endocrine Syndromes', 'Nervous System Neoplasms',
'Nose Neoplasms', 'Orbital Neoplasms', 'Oropharyngeal Neoplasms', 'Otorhinolaryngologic Neoplasms', 'Ovarian Neoplasms', 'Palatal Neoplasms', 'Pancoast Syndrome',
'Pancreatic Neoplasms', 'Paranasal Sinus Neoplasms', 'Parathyroid Neoplasms', 'Parotid Neoplasms', 'Pelvic Neoplasms', 'Penile Neoplasms',
'Peripheral Nervous System Neoplasms', 'Peritoneal Neoplasms', 'Pharyngeal Neoplasms', 'Pituitary Neoplasms', 'Pleural Neoplasms', 'Polycythemia Vera',
'Prostatic Neoplasms', 'Rectal Neoplasms', 'Respiratory Tract Neoplasms', 'Retroperitoneal Neoplasms', 'Salivary Gland Neoplasms', 'Sebaceous Gland Neoplasms',
'Sigmoid Neoplasms', 'Skin Neoplasms', 'Skull Neoplasms', 'Soft Tissue Neoplasms', 'Spinal Cord Neoplasms', 'Spinal Neoplasms', 'Splenic Neoplasms', 'Stomach Neoplasms',
'Sublingual Gland Neoplasms', 'Submandibular Gland Neoplasms', 'Sweat Gland Neoplasms', 'Testicular Neoplasms', 'Thoracic Neoplasms', 'Thymus Neoplasms',
'Thyroid Neoplasms', 'Tongue Neoplasms', 'Tonsillar Neoplasms', 'Tracheal Neoplasms', 'Ureteral Neoplasms', 'Urethral Neoplasms', 'Urogenital Neoplasms',
'Urologic Neoplasms', 'Uterine Neoplasms', 'Uveal Neoplasms', 'Vaginal Neoplasms', 'Venereal Tumors, Veterinary', 'Vulvar Neoplasms', 'Supratentorial Neoplasms',
'Epidural Neoplasms', 'Colorectal Neoplasms', 'Infratentorial Neoplasms', 'Lambert-Eaton Myasthenic Syndrome', 'Mammary Neoplasms, Animal', 'Iris Neoplasms',
'Pleural Effusion, Malignant', 'Central Nervous System Neoplasms', 'Choroid Plexus Neoplasms', 'Thyroid Nodule', 'Endometrial Neoplasms', 'Leukoplakia, Hairy',
'Adrenocortical Adenoma', 'Breast Neoplasms, Male', 'Multiple Endocrine Neoplasia Type 1', 'Multiple Endocrine Neoplasia Type 2a',
'Multiple Endocrine Neoplasia Type 2b', 'Muscle Neoplasms', 'Vascular Neoplasms', 'Bone Marrow Neoplasms', 'Skull Base Neoplasms', 'Hematologic Neoplasms',
'Retinal Neoplasms', 'Optic Nerve Neoplasms', 'Papilloma, Choroid Plexus', 'Brain Stem Neoplasms', 'Paraneoplastic Syndromes, Nervous System',
'Paraneoplastic Cerebellar Degeneration', 'Limbic Encephalitis', 'Paraneoplastic Polyneuropathy', 'Central Nervous System Cysts', 'Pulmonary Sclerosing Hemangioma',
'Adamantinoma', 'Opsoclonus-Myoclonus Syndrome', 'Multiple Pulmonary Nodules', 'Muir-Torre Syndrome', 'Small Cell Lung Carcinoma', 'Meningeal Carcinomatosis',
"Sister Mary Joseph's Nodule", 'Inflammatory Breast Neoplasms', 'Paraneoplastic Syndromes, Ocular', 'Anti-N-Methyl-D-Aspartate Receptor Encephalitis',
'Hereditary Breast and Ovarian Cancer Syndrome', 'Prostatic Neoplasms, Castration-Resistant', 'Triple Negative Breast Neoplasms'],
'Neoplasms by Histologic Type': ['Plasmablastic Lymphoma', 'Mammary Analogue Secretory Carcinoma', 'Giant Cell Tumor of Tendon Sheath',
'Fibromatosis, Plantar', 'Breast Carcinoma In Situ', 'Tubular Sweat Gland Adenomas', 'Immunoglobulin Light-chain Amyloidosis', 'Adenocarcinoma of Lung',
'Squamous Cell Carcinoma of Head and Neck', 'Chondrosarcoma, Clear Cell', 'Carcinoma, Ovarian Epithelial', 'Thyroid Cancer, Papillary', 'Nasopharyngeal Carcinoma',
'Esophageal Squamous Cell Carcinoma', 'Myopericytoma', 'Pancreatic Intraductal Neoplasms', 'Diffuse Intrinsic Pontine Glioma', 'Mesothelioma, Malignant',
'Non-Muscle Invasive Bladder Neoplasms', 'Melanoma, Cutaneous Malignant', 'Adenocarcinoma', 'Adenocarcinoma, Papillary', 'Adenofibroma', 'Adenolymphoma',
'Adenoma', 'Adenoma, Basophil', 'Adenoma, Chromophobe', 'Adenoma, Acidophil', 'Adrenal Rest Tumor', 'Ameloblastoma', 'Angiokeratoma', 'Apudoma', 'Astrocytoma',
'Avian Leukosis', 'Sarcoma, Avian', 'Blast Crisis', "Bowen's Disease", 'Brenner Tumor', 'Burkitt Lymphoma', 'Carcinoid Heart Disease', 'Carcinoid Tumor', 'Carcinoma',
'Carcinoma in Situ', 'Carcinoma 256, Walker', 'Carcinoma, Basal Cell', 'Carcinoma, Basosquamous', 'Adenocarcinoma, Bronchiolo-Alveolar',
'Carcinoma, Intraductal, Noninfiltrating', 'Carcinoma, Ehrlich Tumor', 'Carcinoma, Krebs 2', 'Adenocarcinoma, Mucinous', 'Carcinoma, Papillary',
'Carcinoma, Renal Cell', 'Adenocarcinoma, Scirrhous', 'Carcinoma, Squamous Cell', 'Carcinoma, Transitional Cell', 'Carcinosarcoma', 'Carotid Body Tumor',
'Cementoma', 'Adenoma, Bile Duct', 'Chondroblastoma', 'Chondroma', 'Chondrosarcoma', 'Chordoma', 'Hydatidiform Mole, Invasive', 'Choriocarcinoma', 'Craniopharyngioma',
'Carcinoma, Adenoid Cystic', 'Cystadenocarcinoma', 'Cystadenoma', 'Phyllodes Tumor', 'Vipoma', 'Dupuytren Contracture', 'Dysgerminoma', 'Dysplastic Nevus Syndrome',
'Ependymoma', 'Leukemia, Erythroblastic, Acute', 'Exostoses, Multiple Hereditary', 'Fibroma', 'Fibrosarcoma', 'Ganglioneuroma', 'Gardner Syndrome',
'Giant Cell Tumors', 'Glioblastoma', 'Glioma', 'Glomus Tumor', 'Glomus Jugulare Tumor', 'Glucagonoma', 'Granulosa Cell Tumor', 'Hemangioendothelioma',
'Hemangioma', 'Hemangioma, Cavernous', 'Hemangiopericytoma', 'Hemangiosarcoma', 'Carcinoma, Hepatocellular', 'Adenoma, Sweat Gland', 'Hodgkin Disease',
'Hydatidiform Mole', 'Immunoproliferative Small Intestinal Disease', 'Insulinoma', 'Adenoma, Islet Cell', 'Krukenberg Tumor', 'Leiomyoma', 'Leiomyosarcoma',
'Leukemia', 'Leukemia L1210', 'Leukemia L5178', 'Leukemia P388', 'Leukemia, Experimental', 'Leukemia, Hairy Cell', 'Leukemia, Lymphoid', 'Leukemia, Mast-Cell',
'Leukemia, Megakaryoblastic, Acute', 'Leukemia, Monocytic, Acute', 'Leukemia, Myeloid', 'Leukemia, Plasma Cell', 'Leukemia, Radiation-Induced', 'Leydig Cell Tumor',
'Linitis Plastica', 'Lipoma', 'Liposarcoma', 'Lymphangioma', 'Lymphangiomyoma', 'Lymphangiosarcoma', 'Lymphoma', 'Lymphoma, Follicular', 'Lymphoma, Non-Hodgkin',
'Lymphomatoid Granulomatosis', 'Waldenstrom Macroglobulinemia', 'Malignant Carcinoid Syndrome', 'Mastocytosis', 'Medulloblastoma', 'Melanoma', 'Melanoma, Experimental',
'Meningioma', 'Mesenchymoma', 'Mesonephroma', 'Mesothelioma', 'Adenoma, Pleomorphic', 'Multiple Myeloma', 'Mycosis Fungoides', 'Myoepithelioma', 'Myoma', 'Myosarcoma',
'Myxoma', 'Myxosarcoma', 'Neoplasms by Histologic Type', 'Neoplasms, Connective Tissue', 'Neoplasms, Germ Cell and Embryonal',
'Neoplasms, Glandular and Epithelial', 'Neoplasms, Muscle Tissue', 'Neoplasms, Nerve Tissue', 'Neoplasms, Vascular Tissue', 'Wilms Tumor', 'Neurilemmoma',
'Neuroblastoma', 'Neurofibroma', 'Neurofibromatosis 1', 'Neuroma', 'Neuroma, Acoustic', 'Nevus', 'Nevus of Ota', 'Nevus, Pigmented', 'Odontogenic Tumors', 'Odontoma',
'Oligodendroglioma', 'Osteoma', 'Osteoma, Osteoid', "Paget's Disease, Mammary", 'Paget Disease, Extramammary', 'Papilloma', 'Paraganglioma',
'Paraganglioma, Extra-Adrenal', 'Pheochromocytoma', 'Pinealoma', 'Plasmacytoma', 'Adenomatous Polyposis Coli', 'Pseudomyxoma Peritonei', 'Pulmonary Adenomatosis, Ovine',
'Retinoblastoma', 'Rhabdomyoma', 'Rhabdomyosarcoma', 'Sarcoma', 'Sarcoma 180', 'Sarcoma 37', 'Sarcoma, Ewing', 'Sarcoma, Experimental',
'Sarcoma, Kaposi', 'Mast-Cell Sarcoma', 'Osteosarcoma', 'Sarcoma, Yoshida', 'Sertoli Cell Tumor', 'Sezary Syndrome', 'Somatostatinoma', 'Struma Ovarii',
'Sturge-Weber Syndrome', 'Sarcoma, Synovial', 'Synovitis, Pigmented Villonodular', 'Teratoma', 'Thecoma', 'Thymoma', 'Trophoblastic Neoplasms', 'Urticaria Pigmentosa',
'Prolactinoma', 'Carcinoma, Merkel Cell', 'Gastrinoma', 'Leukemia, B-Cell', 'Leukemia, Lymphocytic, Chronic, B-Cell', 'Precursor B-Cell Lymphoblastic Leukemia-Lymphoma',
'Leukemia, Biphenotypic, Acute', 'Leukemia, T-Cell', 'Leukemia-Lymphoma, Adult T-Cell', 'Leukemia, Prolymphocytic, T-Cell', 'Leukemia, Prolymphocytic',
'Leukemia, Myelogenous, Chronic, BCR-ABL Positive', 'Leukemia, Myeloid, Accelerated Phase', 'Leukemia, Myeloid, Chronic-Phase', 'Leukemia, Myeloid, Acute',
'Leukemia, Basophilic, Acute', 'Leukemia, Eosinophilic, Acute', 'Leukemia, Promyelocytic, Acute', 'Leukemia, Myelomonocytic, Chronic', 'Leukemia, Myelomonocytic, Acute',
'Histiocytic Disorders, Malignant', 'Osteochondroma', 'Lymphoma, B-Cell', 'Lymphoma, T-Cell', 'Lymphoma, Large-Cell, Immunoblastic', 'Lymphoma, Large B-Cell, Diffuse',
'Lymphoma, T-Cell, Cutaneous', 'Lymphoma, T-Cell, Peripheral', 'Lymphoma, AIDS-Related', 'Neurofibromatosis 2', 'Leukemia, Feline', 'Enzootic Bovine Leukosis',
'Granular Cell Tumor', 'Neurofibromatoses', 'Neuroectodermal Tumors', 'Neuroectodermal Tumor, Melanotic', 'WAGR Syndrome', 'Lymphoma, Large-Cell, Anaplastic',
'Lymphomatoid Papulosis', 'Lymphatic Vessel Tumors', 'Lymphangioma, Cystic', 'Lymphangioleiomyomatosis', 'Neoplasms, Complex and Mixed', 'Adenomyoma', 'Adenosarcoma',
'Carcinoma, Adenosquamous', 'Hepatoblastoma', 'Mixed Tumor, Malignant', 'Mixed Tumor, Mesodermal', 'Mixed Tumor, Mullerian', 'Nephroma, Mesoblastic',
'Pulmonary Blastoma', 'Sarcoma, Endometrial Stromal', 'Neoplasms, Connective and Soft Tissue', 'Neoplasms, Adipose Tissue', 'Angiolipoma', 'Angiomyolipoma',
'Liposarcoma, Myxoid', 'Myelolipoma', 'Chondromatosis', 'Chondrosarcoma, Mesenchymal', 'Giant Cell Tumor of Bone', 'Neoplasms, Bone Tissue', 'Fibroma, Ossifying',
'Osteoblastoma', 'Osteochondromatosis', 'Osteosarcoma, Juxtacortical', 'Neoplasms, Fibrous Tissue', 'Histiocytoma, Benign Fibrous', 'Fibroma, Desmoplastic',
'Fibromatosis, Abdominal', 'Fibromatosis, Aggressive', 'Dermatofibrosarcoma', 'Myofibromatosis', 'Neoplasms, Fibroepithelial', 'Fibroadenoma', 'Sarcoma, Clear Cell',
'Sarcoma, Small Cell', 'Angiomyoma', 'Leiomyoma, Epithelioid', 'Leiomyomatosis', 'Rhabdomyosarcoma, Alveolar', 'Rhabdomyosarcoma, Embryonal',
'Sarcoma, Alveolar Soft Part', 'Smooth Muscle Tumor', 'Carcinoma, Embryonal', 'Germinoma', 'Gonadoblastoma', 'Seminoma', 'Endodermal Sinus Tumor',
'Neuroectodermal Tumors, Primitive, Peripheral', 'Neuroectodermal Tumors, Primitive', 'Teratocarcinoma', 'Trophoblastic Tumor, Placental Site', 'Adenoma, Liver Cell',
'Adenoma, Oxyphilic', 'Acrospiroma', 'Hidrocystoma', 'Syringoma', 'Adenoma, Villous', 'Adenomatoid Tumor', 'Adenomatosis, Pulmonary', 'Adenomatous Polyps',
'Mesothelioma, Cystic', 'Adenocarcinoma, Clear Cell', 'Adenocarcinoma, Follicular', 'Carcinoma, Papillary, Follicular', 'Adenocarcinoma, Sebaceous',
'Carcinoma, Acinar Cell', 'Adrenocortical Carcinoma', 'Carcinoma, Endometrioid', 'Carcinoma, Ductal, Breast', 'Carcinoma, Islet Cell', 'Carcinoma, Lobular',
'Carcinoma, Medullary', 'Carcinoma, Mucoepidermoid', 'Carcinoma, Neuroendocrine', 'Carcinoma, Signet Ring Cell', 'Carcinoma, Skin Appendage', 'Cholangiocarcinoma',
'Cystadenocarcinoma, Mucinous', 'Cystadenocarcinoma, Papillary', 'Cystadenocarcinoma, Serous', 'Klatskin Tumor', 'Carcinoma, Giant Cell', 'Carcinoma, Large Cell',
'Carcinoma, Small Cell', 'Carcinoma, Verrucous', 'Cystadenoma, Mucinous', 'Cystadenoma, Papillary', 'Cystadenoma, Serous', 'Neoplasms, Adnexal and Skin Appendage',
'Neoplasms, Basal Cell', 'Pilomatrixoma', 'Neoplasms, Cystic, Mucinous, and Serous', 'Mucoepidermoid Tumor', 'Neoplasms, Ductal, Lobular, and Medullary',
'Papilloma, Intraductal', 'Neoplasms, Mesothelial', 'Neoplasms, Neuroepithelial', 'Ganglioglioma', 'Esthesioneuroblastoma, Olfactory', 'Ganglioneuroblastoma',
'Neurocytoma', 'Neoplasms, Squamous Cell', 'Papilloma, Inverted', 'Neoplasms, Gonadal Tissue', 'Sertoli-Leydig Cell Tumor', 'Luteoma', 'Sex Cord-Gonadal Stromal Tumors',
'Glioma, Subependymal', 'Gliosarcoma', 'Nerve Sheath Neoplasms', 'Neurofibroma, Plexiform', 'Neurofibrosarcoma', 'Neurothekeoma', 'Angiofibroma',
'Hemangioendothelioma, Epithelioid', 'Hemangioma, Capillary', 'Hemangioblastoma', 'Nevi and Melanomas', "Hutchinson's Melanotic Freckle", 'Melanoma, Amelanotic',
'Nevus, Blue', 'Nevus, Intradermal', 'Nevus, Spindle Cell', 'Nevus, Epithelioid and Spindle Cell', 'Rhabdoid Tumor', 'Neuroendocrine Tumors',
'Lymphoma, B-Cell, Marginal Zone', 'Carcinoma, Lewis Lung', 'Prostatic Intraepithelial Neoplasia', 'Optic Nerve Glioma', 'Lymphoma, Mantle-Cell',
'Hemangioma, Cavernous, Central Nervous System', 'Central Nervous System Venous Angioma', 'Carcinoma, Pancreatic Ductal', 'Sarcoma, Myeloid', 'Denys-Drash Syndrome',
'Gestational Trophoblastic Disease', 'Choriocarcinoma, Non-gestational', 'Mastocytosis, Cutaneous', 'Mastocytosis, Systemic', 'Mastocytoma', 'Endometrial Stromal Tumors',
'Glomus Tympanicum Tumor', 'Carcinoma, Ductal', 'Gastrointestinal Stromal Tumors', 'Myofibroma', 'Acanthoma', 'Mongolian Spot', 'Growth Hormone-Secreting Pituitary Adenoma',
'ACTH-Secreting Pituitary Adenoma', 'Odontogenic Tumor, Squamous', 'Histiocytoma', 'Histiocytoma, Malignant Fibrous', 'Nevus, Sebaceous of Jadassohn', 'Leukemia, Large Granular Lymphocytic', 'Precursor Cell Lymphoblastic Leukemia-Lymphoma', 'Precursor T-Cell Lymphoblastic Leukemia-Lymphoma',
'Neoplasms, Plasma Cell', 'Solitary Fibrous Tumor, Pleural', 'Solitary Fibrous Tumors', 'Lymphoma, Extranodal NK-T-Cell', 'Leukemia, Prolymphocytic, B-Cell', 'Leukemia, Myelomonocytic, Juvenile', 'Leukemia, Myeloid, Chronic, Atypical, BCR-ABL Negative', 'Lymphoma, Primary Cutaneous Anaplastic Large Cell', 'Lymphoma, Primary Effusion', 'Mastocytoma, Skin', 'Dendritic Cell Sarcoma, Interdigitating', 'Dendritic Cell Sarcoma, Follicular', 'Histiocytic Sarcoma', 'Langerhans Cell Sarcoma', 'Perivascular Epithelioid Cell Neoplasms', 'Adenomyoepithelioma', 'Nevus, Halo', 'Pagetoid Reticulosis', 'Carney Complex', 'Eccrine Porocarcinoma', 'Poroma', 'Desmoplastic Small Round Cell Tumor', 'Enteropathy-Associated T-Cell Lymphoma', 'Composite Lymphoma', 'Kasabach-Merritt Syndrome', 'Cystadenofibroma', 'Buschke-Lowenstein Tumor', 'Lipoblastoma', 'Intraocular Lymphoma', 'Adenocarcinoma in Situ', 'Thyroid Carcinoma, Anaplastic'],
'Neoplastic Processes': ['Oncogene Addiction', 'Extranodal Extension', 'Warburg Effect, Oncologic',
'Anaplasia', 'Cell Transformation, Neoplastic', 'Cell Transformation, Viral', 'Cocarcinogenesis', 'Lymphatic Metastasis', 'Neoplastic Cells, Circulating', 'Neoplasm Invasiveness', 'Neoplasm Metastasis', 'Neoplasm Recurrence, Local', 'Neoplasm Regression, Spontaneous', 'Neoplasm Seeding', 'Neoplasms, Unknown Primary', 'Neoplastic Processes', 'Leukemic Infiltration', 'Neoplasm, Residual', 'Neoplasm Micrometastasis', 'Carcinogenesis'],
'Precancerous Conditions': ['Smoldering Multiple Myeloma', 'Barrett Esophagus', 'Uterine Cervical Dysplasia', 'Erythroplasia', 'Leukoplakia', 'Precancerous Conditions', 'Preleukemia', 'Xeroderma Pigmentosum', 'Keratosis, Actinic', 'Aberrant Crypt Foci', 'Atypical Squamous Cells of the Cervix', 'Squamous Intraepithelial Lesions of the Cervix'],
'Paraneoplastic Syndromes': ['ACTH Syndrome, Ectopic', 'Paraneoplastic Syndromes', 'Zollinger-Ellison Syndrome'],
'Cysts': ['Basal Cell Nevus Syndrome', 'Bone Cysts', 'Branchioma', 'Bronchogenic Cyst', 'Cysts', 'Dentigerous Cyst', 'Dermoid Cyst', 'Epidermal Cyst', 'Esophageal Cyst', 'Follicular Cyst', 'Jaw Cysts', 'Lymphocele', 'Mediastinal Cyst', 'Mesenteric Cyst', 'Mucocele', 'Nonodontogenic Cysts', 'Odontogenic Cysts', 'Ovarian Cysts', 'Pancreatic Cyst', 'Pancreatic Pseudocyst', 'Parovarian Cyst', 'Periodontal Cyst', 'Pilonidal Sinus', 'Polycystic Ovary Syndrome', 'Popliteal Cyst', 'Radicular Cyst', 'Ranula', 'Synovial Cyst', 'Thyroglossal Cyst', 'Urachal Cyst', 'Choledochal Cyst', 'Arachnoid Cysts', 'Chalazion', 'Bone Cysts, Aneurysmal', 'Odontogenic Cyst, Calcifying', 'Ganglion Cysts', 'Breast Cyst', 'Tarlov Cysts', 'Colloid Cysts'],
'Neoplasms, Experimental': ['Carcinoma, Brown-Pearce', 'Neoplasms, Experimental'],
'Hamartoma': ['Hamartoma', 'Hamartoma Syndrome, Multiple', 'Tuberous Sclerosis', 'Proteus Syndrome', 'Pallister-Hall Syndrome'],
'Neoplasms, Hormone-Dependent': ['Neoplasms, Hormone-Dependent'],
'Neoplasms, Multiple Primary': ['Neoplasms, Multiple Primary'],
'Neoplasms, Radiation-Induced': ['Neoplasms, Radiation-Induced'],
'Neoplastic Syndromes, Hereditary': ['Neoplastic Syndromes, Hereditary', 'Peutz-Jeghers Syndrome', 'Li-Fraumeni Syndrome', 'Lynch Syndrome II', 'Birt-Hogg-Dube Syndrome'],
'Pregnancy Complications, Neoplastic': ['Pregnancy Complications, Neoplastic'],
'Neoplasms, Second Primary': ['Neoplasms, Second Primary'],
'Neoplasms, Post-Traumatic': ['Neoplasms, Post-Traumatic']}

######################################

def study_mesh(study):
    #recuperer tous les mesh terms cites
    mesh = []
    ancestror = []
    if study.get("derivedSection") is not None and study["derivedSection"].get("conditionBrowseModule") is not None:
        if study["derivedSection"]["conditionBrowseModule"].get("meshes") is not None:
            mesh = [i["term"] for i in study["derivedSection"]["conditionBrowseModule"]["meshes"]]
        if study["derivedSection"]["conditionBrowseModule"].get("ancestors") is not None:
            ancestror = [i["term"] for i in study["derivedSection"]["conditionBrowseModule"]["ancestors"]]
    return mesh + ancestror

######################################

def extract_year(date_str):
    #extrait uniquement l'annee d'une date sous differents formats
    match = re.search(r'\d{4}', str(date_str))  #cherche une annee a 4 chiffres
    return int(match.group()) if match else None


def parse_date(date_str):
    try:
        # Si la date est complète (YYYY-MM-DD)
        return pd.to_datetime(date_str, format="%Y-%m-%d", errors='coerce')
    except:
        # Si la date est incomplète (YYYY-MM), on ajoute le premier jour du mois
        try:
            return pd.to_datetime(date_str + "-01", format="%Y-%m-%d", errors='coerce')
        except:
            return None
