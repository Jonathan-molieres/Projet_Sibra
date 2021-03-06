# -*- coding: utf-8 -*-
"""
Created on Tue Feb  4 11:52:20 2020

@author: moliereJ
"""
import classe as Cl
import datetime as dt
from jours_feries_france.compute import JoursFeries
noeud=Cl.recuperation(Cl.dico_arret)
# =============================================================================
# Programme pritsncipal de Sibra
# =============================================================================
if __name__ == '__main__':
    print('=============================================================================')
    print('                                  Sibra                                  ')
    print('=============================================================================')
    Menu = True
    while Menu:
        # Affichage du Menu du jeux
        print('=============================================================================')
        print("                                 Menu                                        ")
        print('=============================================================================')
        print("Pour quitter, entrez \033[31mexit\033[0m. Pour ajouter un fichier à la base de donnée."
            +"\nEntrer \033[31mteste\033[0m, pour verifier le graph."
            +"\nEntrer \033[31msibra\033[0m, pour faire une recherche d'iterinaire"
            +"\nVoici la liste des arrets possibles: ")
        L_arret=[arret for arret in Cl.dico_arret.keys()]
        print(L_arret)
        choix=input('choix : ')
        
        if choix == 'exit':
                #sorti de la boucle 
                Menu = False
        elif choix=='teste':
            Cl.test(Cl.dico_arret)
            print('=============================================================================')
            print('                         Fin du teste')
            print('=============================================================================')
        elif  choix=='sibra':
            try:
                print("Fonction de recherche pour le chemin le plus court en terme de temps")
                date=input("Quelle est la date du depart(format: 01/10/2018) : ")
                dates=dt.date(int(date[-4:]), int(date[3:5]),int( date[:2]))
                jours=input("Quelle est le jour du depart : ")
                horraire=input("Entrer l'heure de depart : ")
                arret_depart=input("Entrer l'arret de depart : ")
                arret_arrive=input("Entrer l'arret d'arrivé : ")
                reseau=Cl.Sibra(Cl.dico_arret[arret_depart])
                dict_ferie=JoursFeries.for_year(int(date[-4:]))
                if jours=='dimanche' or jours=='samedi':
                    jour=3
                else:
                    jour=0
    
                for values in dict_ferie.values():
                    if values==dates:
                        jour=3
        
                resultat=reseau.affichage_resultat(Cl.dico_arret[arret_arrive],dt.timedelta(hours=int(horraire[:len(horraire)-3]),minutes=int(horraire[-2:])),jour,noeud)
            except:
                print('\033[31m=============================================================================\033[0m')
                print("\033[31mIl y a eu une erreur. Verifier les données entrées \033[0m")
                print('\033[31m=============================================================================\033[0m')
