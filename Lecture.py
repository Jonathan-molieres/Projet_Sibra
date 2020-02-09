#!/usr/bin/python3
#-*-coding:utf-8-*-
#import 
import datetime as dt
# =============================================================================
# Ajout des donnees
# =============================================================================

# Fichier des lignes
data_file_name_1 = 'data/1_Poisy-ParcDesGlaisins.txt'
data_file_name_2 = 'data/2_Piscine-Patinoire_Campus.txt'
data_name=[]
data_name.append(data_file_name_1)
data_name.append(data_file_name_2)
nbre=len(data_name) # Nombre de bus
# =============================================================================
# Fonction
# =============================================================================
def lecture(fichier):
    try:
        with open(fichier, 'r') as f:
            content = f.read()
            #Correction des accents
            content=content.replace("Ã‰","E")
            content=content.replace("Ãˆ","E")
            content=content.replace("Ã¢","â")
            content=content.replace("Ã©","é")
    except OSError:
        # 'File not found' error message.
        print("File not found")
    return content
def recuperation_nom(fichier):
    '''recupere le numero de bus compris entre 0 et 99'''
    try: 
        return int(fichier[5:7])
    except:
        return int(fichier[5])
def dates2dic(dates):
    dic = {}
    splitted_dates = dates.split("\n")
#    print(splitted_dates)
    for stop_dates in splitted_dates:
        tmp = stop_dates.split(" ")
        dic[tmp[0]] = tmp[1:]
    return dic
def chgt_type_date(dico,Larret):
    '''change tout les horraires qui sont en str en type datetime'''
    for i_bus in range(nbre):
        for i_nom in range(len(Larret[i_bus])):
            
            noeud=Larret[i_bus][i_nom]
            for i in range(len(dico[i_bus][noeud])):
#                print(dico[noeud])
                if dico[i_bus][noeud][i]!='-':
                    dico[i_bus][noeud][i]=dt.timedelta(hours=int(dico[i_bus][noeud][i][:len(dico[i_bus][noeud][i])-3]),minutes=int(dico[i_bus][noeud][i][-2:]))  
def recuperation_arret(L):
    '''recupere les noms des arrets'''
    Larret=[]
    mot=''
    for i in  range(len(L)):
        mot+=L[i]
        if i==len(L)-1:
            # print(mot)
            Larret.append(mot)
        if L[i] ==' ':
            if  mot!=' ':
                mot=mot[:-1]
                Larret.append(mot)
            mot=''
        if L[i]=='N' and L[i-1]==' ':
            mot=''
        if L[i] =='+':
            mot=''
    return Larret
# =============================================================================
# Programme de lecture et conversion
# =============================================================================
#lecture des fichier
Lecture=[]
Lecture.append(lecture(data_file_name_1))
Lecture.append(lecture(data_file_name_2))


regular_path=[]
regular_date_go=[]
regular_date_back=[]
we_holidays_path=[]
we_holidays_date_go=[]
we_holidays_date_back=[]
nom_bus=[]
#enregistrement des donnees dans les listes
for i in range(0,nbre):
    nom_bus.append(recuperation_nom(data_name[i]))
    slited_content = Lecture[i].split("\n\n")
    regular_path.append(slited_content[0]) #correspond au chemin du bus
    regular_date_go.append(dates2dic(slited_content[1]))#correspond au heure de départ par arret
    regular_date_back.append(dates2dic(slited_content[2]))#correspond au horraire d'arrivvé par arret
    # Meme schema mais pour le week-end et vacance
    we_holidays_path.append(slited_content[3])
    we_holidays_date_go.append(dates2dic(slited_content[4]))
    we_holidays_date_back.append(dates2dic(slited_content[5]))
#print(regular_date_go[0]['GARE'])
# =============================================================================
#  format des donnees
# =============================================================================


Larret=[]#liste des arrets pour chaque bus
Larret_We=[]#liste des arrets pour chaque bus
#recuperation des chemin des bus 
for i_bus in range(0,nbre):
    Larret.append(recuperation_arret(regular_path[i_bus]))
    Larret_We.append(recuperation_arret(we_holidays_path[i_bus]))
# Conversion des str en type date   
chgt_type_date(regular_date_go,Larret)
chgt_type_date(regular_date_back,Larret)
chgt_type_date(we_holidays_date_go,Larret_We)
chgt_type_date(we_holidays_date_back,Larret_We)
# print(regular_date_go)
#print( regular_date_go[0]['GARE'])    
#print(Larret)
     
    