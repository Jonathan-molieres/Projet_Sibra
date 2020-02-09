# -*- coding: utf-8 -*-
"""
Created on Thu Feb  6 14:31:59 2020

@author: Jonathan Molieres
"""

import Lecture as Lc# fichier de lecture des donnees
import datetime as dt
# =============================================================================
# classe Arret
# =============================================================================
class Arret:
    
    ''' classe coorespondant aux arrets du reseau sibra'''
    def __init__(self,nom,heure_aller,heure_retour,heure_we_aller,heure_we_retour):
        self.nom=nom
        self.heure_aller=heure_aller #dictionnaire avec comme reference le nom du bus
        self.heure_retour=heure_retour
        self.heure_we_aller=heure_we_aller
        self.heure_we_retour=heure_we_retour
        self.precedent={}
        self.suivant={}
        self.nom_bus=[] #nom des bus desservit par l'arret
    #getter  
    def get_nom(self):
        return self.nom
    def get_heure_aller(self):
        return self.heure_aller  
    def get_heure_retour(self):
        return self.heure_retour
    def get_heure_we_retour(self):
        return self.heure_we_retour
    def get_heure_we_aller(self):
        return self.heure_we_aller
    def get_suivant(self):
        return self.suivant
    def get_precedent(self):
        return self.precedent
    #set
    def chgt_heure_aller(self,heure):
        self.heure_aller=heure
    def chgt_heure_retour(self,heure):
        self.heure_retour=heure
    def chgt_heure_we_aller(self,heure):
        self.heure_we_aller=heure
    def chgt_heure_we_retour(self,heure):
        self.heure_we_retour=heure
    def choix_heur(self,num):
        ''' le numero permet de choisir quelle heure on souhaite'''
        if num==0:
            return self.heure_aller
        elif num==1:
            return self.heure_retour
        elif num==2:
            return self.heure_we_aller
        elif num==3:
            return self.heure_we_retour
        else:
            print('erreur')
    def chgt_heure(self,heure_utilisateur):
        '''Convertie l'heure en format date time'''
        return dt.timedelta(hours=int(heure_utilisateur[:len(heure_utilisateur)-3]),minutes=int(heure_utilisateur[3:]))
    
    def horaire(self,heure_utilisateur,heure_arret,i_bus):
        '''fonction qui renvoie le bon horraire precedent a choisir
        avec heure_utilisateur sous la forme de time delta correspond a l'horraire entrée de l'utilisateur
        et l'heure_arret est un des attributs de type heure de arret. 
        '''
        for i in range(len(heure_arret[i_bus])):
            if heure_arret[i_bus][i]!='-' and heure_arret[i_bus][i+1]!='-':
                if  heure_arret[i_bus][i]<=heure_utilisateur and heure_arret[i_bus][i+1]>heure_utilisateur:
                    return  heure_arret[i_bus][i],i
        return -1
    
    def horaire_element(self,heure_arret,i_bus,i):
        """
        Parameters
        ----------
        heure_arret : TYPE
            DESCRIPTION.
        i_bus : TYPE
            DESCRIPTION.
        i : TYPE
            DESCRIPTION.

        Returns
        -------
        TYPE: Datetime
            DESCRIPTION.
        Utilisation:renvoie l'horaire selon l'indice i"""
        return heure_arret[i_bus][i]
    def temps_suivant(self,heure_utilisateur,num_heur,i_bus):
        '''
        Parameters
        ----------
        heure_utilisateur : TYPE: datetime
            DESCRIPTION: heure de depart de l'utilisateur
        num_heur : TYPE
            DESCRIPTION.
        i_bus : TYPE
            DESCRIPTION.

        Returns
        -------
        TYPE
            DESCRIPTION.

        Utilisation:renvoie le temps entre deux arrets qui se suivent'''
        try:
            temps_arret=self.horaire(heure_utilisateur,self.choix_heur(num_heur),i_bus)
            temps_suivant=self.suivant[i_bus].horaire_element(self.suivant[i_bus].choix_heur(num_heur),i_bus,temps_arret[1])
            
            return temps_suivant-temps_arret[0]
        except:
            #renvoie l'infini si aucun horraire est trouvé
            return dt.timedelta(seconds=86000)
    def temps_precedent(self,heure_utilisateur,num_heur,i_bus):
        '''
        Parameters
        ----------
        heure_utilisateur : TYPE: datetime
            DESCRIPTION: heure de depart de l'utilisateur
        num_heur : TYPE
            DESCRIPTION.
        i_bus : TYPE
            DESCRIPTION.

        Returns
        -------
        TYPE
            DESCRIPTION.

        Utilisation:renvoie le temps entre deux arrets qui se suivent'''
        try:
            temps_arret=self.horaire(heure_utilisateur,self.choix_heur(num_heur),i_bus)
            temps_precedent=self.precedent[i_bus].horaire_element(self.suivant[i_bus].choix_heur(num_heur),i_bus,temps_arret[1]-1)

            return temps_arret[0]-temps_precedent 
        except:
            return dt.timedelta(seconds=86000)
    
    def terminus(self):
        '''renvoie un booleen pour savoir si l'arret est un terminus ou pas'''
        return self.suivant=={}
    def terminus_precedent(self):
        '''renvoie un booleen pour savoir si l'arret est un terminus dans le sens contraire ou pas'''
        return self.precedent=={}
    def get_noeud_precedent(self):
        L_precedent=[]
        for i_bus in self.nom_bus:
            if not self.terminus_precedent():
                L_precedent.append(self.precedent[i_bus])
        return L_precedent
    def get_noeud_suivant(self):
        L_suivant=[]
        for i_bus in self.nom_bus:
            if not self.terminus_precedent():
                L_suivant.append(self.suivant[i_bus])
        return L_suivant
                
# =============================================================================
# Classe Sibra    
# =============================================================================
class Sibra:
    def __init__(self,depart):        
        self.depart=depart# Arret de départs
    def dijkstra(self,cible,heure_utilisateur,num_heur,queue):
        '''
        Parameters
        ----------
        cible : TYPE: arret 
            Arret d'arrivé.
        heure_utilisateur : TYPE: datetime
            DESCRIPTION: heure de depart de l'utilisateur

        num_heur : TYPE: int
            DESCRIPTION: Permet de determiner quelle horraire choisir.
        queue : TYPE:Liste 
            DESCRIPTION: Liste des arrets

        Returns
        -------
        path : TYPE: Liste
            DESCRIPTION: Liste du chemin
        visite : TYPE: Liste
            DESCRIPTION: Liste des noeuds visitées
        distances : TYPE: dict
            DESCRIPTION: contient les distances pour chaques arrets
        '''
        # initialisation
        
        inf=dt.timedelta(seconds=86000)# cette heure correspond à une journee d'ou l'utilisation
        # comme l'infini pour l'algorithme
        distances= { noeud: inf for noeud in queue }
        distances[self.depart]=dt.timedelta(minutes=0)
        path=[]
        visite=[]
        bus_visite=[]
        while len(queue)>0:

            noeud_mini,distances_mini = self.noeud_mini(distances, queue)

            queue.remove(noeud_mini)
            visite.append(noeud_mini)
            # Changement des distances des voisins
            for i_bus in noeud_mini.nom_bus:
                if not noeud_mini.terminus():
                    noeud2=noeud_mini.suivant[i_bus]
                    if distances[noeud2]> distances[noeud_mini]+noeud_mini.temps_suivant(heure_utilisateur,num_heur,i_bus):
                        distances[noeud2]= distances[noeud_mini]+noeud_mini.temps_suivant(heure_utilisateur,num_heur,i_bus)

                if not noeud_mini.terminus_precedent():
                    noeud2=noeud_mini.precedent[i_bus]
                    if distances[noeud2]> distances[noeud_mini]+noeud_mini.temps_precedent(heure_utilisateur,num_heur,i_bus):
                        distances[noeud2]= distances[noeud_mini]+noeud_mini.temps_precedent(heure_utilisateur,num_heur,i_bus)
        try:
            path,bus_visite=self.retour_chemin(distances, cible,inf)#effectue le chemin retour 
            #avec les distances minimum
        except:
            None
        try: 
            path,bus_visite=self.retour_chemin2(distances, cible,inf)#effectue le chemin retour 
            #avec les distances minimum
        except:
            None
        
        return path,distances[cible],bus_visite
    def noeud_mini(self,distances,queue):
        """
        Parameters
        ----------
        distances : TYPE: dict
            DESCRIPTION: contient les distances pour l'algorithme de dijkstra
        queue : TYPE : Liste
            DESCRIPTION: Liste des noeuds

        Returns
        -------
        noeud_mini : arret
            DESCRIPTION: noeud avec la distances minimum
        mini : TYPE: datetime
            DESCRIPTION: distances minimum

        retourne le noeud de distance minimal"""
        
        inf=dt.timedelta(seconds=86000)
        noeud_mini=-1
        mini=inf
        for i in queue:
            if distances[i]<mini:
                mini=distances[i]
                noeud_mini=i
        return noeud_mini,mini

    def retour_chemin(self,distances,cible,inf):
        """
        Parameters
        ----------
        distances : TYPE: dict
            DESCRIPTION: contient les distances pour l'algorithme de dijkstra
        cible : TYPE : arret
            DESCRIPTION: arret final
        inf : TYPE: datetime
            DESCRIPTION: defini l'infini pour l'algorithme de dijkstra

        Returns
        -------
        path : TYPE: Liste
            DESCRIPTION: Liste du chemin.

        """
        bus_visite=[cible.nom_bus[0]]
        path=[cible.nom]
        noeud=cible
        while noeud!= self.depart:
            predecesseur=noeud.get_noeud_precedent()
            mini=inf 
            noeud_precedent=0
            
            for noeud_preced in predecesseur:
                if distances[noeud_preced]<mini:
                    
                    mini=distances[noeud_preced]
                    noeud_precedent=noeud_preced

            noeud=noeud_precedent
            bus_visite.append(noeud_precedent.nom_bus[0])
            path.append(noeud_precedent.nom)       
        return path,bus_visite
    def retour_chemin2(self,distances,cible,inf):
        """
        Parameters
        ----------
        distances : TYPE: dict
            DESCRIPTION: contient les distances pour l'algorithme de dijkstra
        cible : TYPE : arret
            DESCRIPTION: arret final
        inf : TYPE: datetime
            DESCRIPTION: defini l'infini pour l'algorithme de dijkstra

        Returns
        -------
        path : TYPE: Liste
            DESCRIPTION: Liste du chemin.

        """
        path=[cible.nom]
        noeud=cible
        bus_visite=[cible.nom_bus[0]]
        while noeud!= self.depart:
            predecesseur=noeud.get_noeud_suivant()
            mini=inf 
            noeud_precedent=0
            
            for noeud_preced in predecesseur:
                if distances[noeud_preced]<mini:
                    
                    mini=distances[noeud_preced]
                    noeud_precedent=noeud_preced

            noeud=noeud_precedent
            bus_visite.append(noeud_precedent.nom_bus[0])
            path.append(noeud_precedent.nom)
        return path,bus_visite
    def affichage_resultat(self,cible,heure_utilisateur,num_heur,queue):
        """
        Parameters
        ----------
        cible : TYPE : arret
            DESCRIPTION: arret final
        heure_utilisateur : TYPE: datetime
            DESCRIPTION: heure de depart de l'utilisateur
        num_heur : TYPE: int
            DESCRIPTION: Permet de determiner quelle horraire choisir.
        queue : TYPE:Liste 
            DESCRIPTION: Liste des arrets

        Returns
        -------
        None: fonction d'affichage pour dijkstra
        """
        affichage='============================================================================= \n'
        affichage+='Vous avez demandé le chemin le plus court entre : '+str(self.depart.nom)
        affichage+=' et '+str(cible.nom)
        resultat=self.dijkstra(cible,heure_utilisateur,num_heur,queue)
        affichage+='\nVous devez prendre les arrets suivants : \n'
        for i in range(len(resultat[0])):
            affichage+= resultat[0][i]+' avec le bus '+str(resultat[2][i])+str(", \n")
        affichage+="\nLa durée du trajet estimée est de :"
        print(affichage,resultat[1])
        print("avec le temps d'attente de correspondances pris en compte.")
        print("L'heure de depart est : ",heure_utilisateur)
        print("L'heure d'arrivée estimée est :",heure_utilisateur+resultat[1])
        print('============================================================================= \n')
        
    def Foremost(self,cible,heure_utilisateur,num_heur,queue):
        Sibra(cible).affichage_resultat(self.depart,heure_utilisateur,num_heur+1,queue)
       # num_heur+1 correspond au horraire retour
# =============================================================================
# Verification donnee
# =============================================================================
def test(dico_arret):
    '''
    Parameters
    ----------
    dico_arret : TYPE: dict
        DESCRIPTION: contient tout les arrets avec comme clé  le nom de l'arret

    Returns
    -------
    None: C'est une fonction d'affichage.
    '''
    print('Verification du graph')
    for arret in dico_arret:
        print('\033[31marret\033[0m =',dico_arret[arret].nom)
        print('Suivant:')
        for i in dico_arret[arret].nom_bus:
            if not dico_arret[arret].terminus():
                print(dico_arret[arret].suivant[i].nom)
            else:
                print('terminus')
        print('Precedent:')
        for i in dico_arret[arret].nom_bus:
            if not dico_arret[arret].terminus_precedent():
                print(dico_arret[arret].precedent[i].nom)
            else:
                print('terminus')
def recuperation(dico_arret):
    '''
    Parameters
    ----------
    dico_arret : TYPE: Dict
        DESCRIPTION: Contient tout les arrets avec comme clé 
        le nom de l'arret

    Returns
    -------
    noeud : TYPE: Liste
        DESCRIPTION: Liste de tout les arrets

    '''
    noeud=[]
    for i in dico_arret.values():
        noeud.append(i)
    return noeud     
# =============================================================================
# # creation des instances
# =============================================================================
dico_arret={} # Dictionnaire contenant tout les arrets de sibra
# =============================================================================
# Creation des arrets
# =============================================================================
for i_bus in range(Lc.nbre):
    for i_nom in range(len(Lc.Larret[i_bus])):
        noeud=Lc.Larret[i_bus][i_nom]
        # Prendre en compte qu'il a plusieurs bus par arret 
        if not noeud in dico_arret:
            dico_arret[noeud]=Arret(noeud,
                            {Lc.nom_bus[i_bus]:Lc.regular_date_go[i_bus][noeud]},
                            {Lc.nom_bus[i_bus]:Lc.regular_date_back[i_bus][noeud]},
                            {Lc.nom_bus[i_bus]:Lc.we_holidays_date_go[i_bus][noeud]},
                            {Lc.nom_bus[i_bus]:Lc.we_holidays_date_back[i_bus][noeud]})
        
        else:
            dico_arret[noeud].get_heure_aller()[Lc.nom_bus[i_bus]]= Lc.regular_date_go[i_bus][noeud]
            dico_arret[noeud].get_heure_retour()[Lc.nom_bus[i_bus]]= Lc.regular_date_back[i_bus][noeud]
            dico_arret[noeud].get_heure_we_retour()[Lc.nom_bus[i_bus]]= Lc.we_holidays_date_go[i_bus][noeud]
            dico_arret[noeud].get_heure_we_aller()[Lc.nom_bus[i_bus]]= Lc.we_holidays_date_back[i_bus][noeud]
# =============================================================================
# Ajout des suivant et precedent arret
# =============================================================================

for i_bus in range(Lc.nbre):
    for i_nom in range(len(Lc.Larret[i_bus])):
        noeud=Lc.Larret[i_bus][i_nom]
        
        if i_nom==0:
            noeud_suivant=Lc.Larret[i_bus][i_nom+1]
            dico_arret[noeud].suivant[Lc.nom_bus[i_bus]]=dico_arret[noeud_suivant]
            if Lc.nom_bus[i_bus] not in dico_arret[noeud].nom_bus:
                dico_arret[noeud].nom_bus.append(Lc.nom_bus[i_bus])
        elif i_nom==len(Lc.Larret[i_bus])-1:
            
            noeud_precedent=Lc.Larret[i_bus][i_nom-1]
            dico_arret[noeud].precedent[Lc.nom_bus[i_bus]]=dico_arret[noeud_precedent]
            if Lc.nom_bus[i_bus] not in dico_arret[noeud].nom_bus:
                dico_arret[noeud].nom_bus.append(Lc.nom_bus[i_bus])
        else:
            noeud_precedent=Lc.Larret[i_bus][i_nom-1]
            noeud_suivant=Lc.Larret[i_bus][i_nom+1]
            dico_arret[noeud].precedent[Lc.nom_bus[i_bus]]=dico_arret[noeud_precedent]
            dico_arret[noeud].suivant[Lc.nom_bus[i_bus]]=dico_arret[noeud_suivant]
            if Lc.nom_bus[i_bus] not in dico_arret[noeud].nom_bus:
                dico_arret[noeud].nom_bus.append(Lc.nom_bus[i_bus])


# =============================================================================
# Teste
# =============================================================================
reseau=Sibra(dico_arret['GARE'])
noeud=recuperation(dico_arret)
reseau.affichage_resultat(dico_arret['Ponchy'],dt.timedelta(seconds=55260),0,noeud)
# fore=reseau.Foremost(dico_arret['Ponchy'],dt.timedelta(seconds=55260),0,noeud)
