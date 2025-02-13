###########################################################################################################################################
'''
04/02/2025
Manal - script pour extraire les donnees de l'API, creer des dataframes 
06/02/2025
Celia - data management et exportation des dataframes en csv
'''
###########################################################################################################################################
#charger les packages/fonctions
import pandas as pd
import re 
import requests
import dash
import datetime as dt
from fonctions import mesh_dict, study_mesh, extract_year, parse_date
###########################################################################################################################################

##EXTRACTION API

#url de l'API
base_url = "https://clinicaltrials.gov/api/v2/studies"

#parametres de la requete
params = {
    "query.cond": "neoplasm* OR cancer*",
    "query.term": "France",
    "pageSize": 1000,  #maximum etudes par page
}
total_studies = 0  #compteur d'études

#listes/dictionnaire pour stocker les donnees
liste_mesh_df = []
liste_trials_df = []
liste_loc_df = []
dico_mesh_df = {"nctid": [], "neoplasm_category": [], "neoplasm": []}

#boucle pour recuperer toutes les pages
while True:
    print("Recuperation des donnees... \netudes collectees: {}".format(total_studies)) #pour voir a quel endroit ca ne fonctionne plus
    response = requests.get(base_url, params=params)

    #si la requete a reussi
    if response.status_code == 200:
        data = response.json()  
        studies = data.get('studies', []) 

        #ajouter les etudes recuperees aux listes
        for study in studies:
            #pour trials dataframe
            nctid = study.get('protocolSection', {}).get('identificationModule', {}).get('nctId')
            condition = '\n'.join(study.get('protocolSection', {}).get('conditionsModule', {}).get('conditions'))
            startDate = study.get('protocolSection', {}).get('statusModule', {}).get('startDateStruct', {}).get('date')
            endDate = study.get("protocolSection", {}).get("statusModule", {}).get("primaryCompletionDateStruct", {}).get("date")
            drug_FDA = study.get('protocolSection', {}).get('oversightModule', {}).get('isFdaRegulatedDrug')
            device_FDA = study.get('protocolSection', {}).get('oversightModule', {}).get('isFdaRegulatedDevice')
            phase = ', '.join(study.get('protocolSection', {}).get('designModule', {}).get('phases', []))
            status = study.get('protocolSection', {}).get('statusModule', {}).get('overallStatus')
            results = study.get('hasResults')
            title = study.get("protocolSection", {}).get("identificationModule", {}).get("briefTitle")
            organization = study.get("protocolSection", {}).get("identificationModule", {}).get("organization", {}).get("fullName")
            last_update = study.get("protocolSection", {}).get("statusModule", {}).get("lastUpdateSubmitDate")
            description = study.get("protocolSection", {}).get("descriptionModule", {}).get("briefSummary")
            study_type = study.get("protocolSection", {}).get("designModule", {}).get("studyType")
            if study.get('protocolSection', {}).get('contactsLocationsModule', {}).get('centralContacts'):
                contact = study.get('protocolSection', {}).get('contactsLocationsModule', {}).get('centralContacts')[0].get("name", "")+"\n"+study.get('protocolSection', {}).get('contactsLocationsModule', {}).get('centralContacts')[0].get("email", "")
            else:
                contact = "No information"
            liste_trials_df.append([nctid, condition, startDate, endDate, drug_FDA, device_FDA, phase, status, results, title, organization, last_update, description, study_type, contact])

            #pour mesh dataframe
            mesh_id = study_mesh(study)
            for key, values in mesh_dict.items():
	            #yrouver le premier element en commun entre mesh_id et values
	            common_term = next((item for item in mesh_id if item in values), None) #premier element commun
	            if common_term:  
	            	dico_mesh_df["nctid"].append(study.get('protocolSection', {}).get("identificationModule",{}).get("nctId"))
	            	dico_mesh_df["neoplasm_category"].append(key)
	            	dico_mesh_df["neoplasm"].append(common_term)  


            #pour location dataframe
            for localisation in study['protocolSection'].get('contactsLocationsModule', {}).get('locations', []):
            	if localisation.get('country') == 'France':
            		nctid = study.get('protocolSection', {}).get("identificationModule", {}).get("nctId")
            		facility = localisation.get("facility")
            		city = localisation.get("city")
            		country = localisation.get("country")
            		liste_loc_df.append([nctid, facility, city, country])

        total_studies += len(studies)  #mettre a jour le compteur

        #verifier s'il y a une page suivante
        nextPageToken = data.get('nextPageToken')
        if nextPageToken:
            params['pageToken'] = nextPageToken  #passer a la page suivante
        else:
            break  #sortir de la boucle si plus de page
    else:
        print("Erreur lors de la recupération des donnees. Code: {}".format(response.status_code)) #si la requete echoue
        break

#afficher le nombre total d'etudes extraites
print("Nombre total d'etudes extraites : {}".format(total_studies))
###########################################################################################################################################

##CREATION DATAFRAME

#convertir les listes en dataframes
df_mesh = pd.DataFrame(dico_mesh_df)
df_trials = pd.DataFrame(liste_trials_df, columns=["nctid", "condition", "startDate", "endDate", "drug_FDA", "device_FDA", "phase", "status", "results", "title", "organization", "last_update", "description", "study_type", "contact"])
df_loc = pd.DataFrame(liste_loc_df, columns=["nctid", "facility", "city", "country"])
###########################################################################################################################################

##DATA MANAGEMENT

#nettoyage de startDate dans df_mesh (extraction de l'annee)
df_trials["startYear"] = df_trials["startDate"].apply(extract_year)


#nettoyage de city dans df_loc
df_loc["city"] = df_loc["city"].str.replace(r'\s*cedex\s*\d*', '', flags=re.IGNORECASE, regex=True)
df_loc["city"] = df_loc["city"].str.title()  #standardisation (Paris, Lyon...)

#nettoyage de study type dans df_trials
df_trials["study_type"] = df_trials["study_type"].str.replace("_", " ").str.title()
df_trials["status"] = df_trials["status"].str.replace("_", " ").str.title()

#calcul de la duree d'un etude dans df_trials
df_trials["startDate"] = df_trials["startDate"].apply(parse_date)
df_trials["endDate"] = df_trials["endDate"].apply(parse_date)
df_trials["duration_days"] = (df_trials["endDate"] - df_trials["startDate"]).dt.days
df_trials["duration_year"] = df_trials["duration_days"]/365.25

#sauvegarde des resultats en csv pour moins de latence
df_trials.to_csv("trials.csv", index=False)
df_loc.to_csv("loc.csv", index=False)
df_mesh.to_csv("mesh.csv", index=False)
###########################################################################################################################################

##DASHBOARD
#voir dash_projet.py

