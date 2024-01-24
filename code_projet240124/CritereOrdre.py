import pandas as pd
import numpy as np
import Noeud
import Bibi
import Amer
import Site
import Carnet 


class CritereOrdre:
    """Classe representant un critere d'ordre pour un nœud dans un espace tridimensionnel.

    Attributes:
        
        id_carnet (int): L'identifiant unique du carnet associe au critere.
        
        bibi (Bibi): Un objet Bibi associe au critere.
        
        noeud (Noeud): Un objet Noeud auquel le critere est applique.
        
        liste_amers (list): Une liste d'objets Amer.
        
        liste_sites (list): Une liste d'objets Site.
        
        liste_carnets (list): Une liste d'objets Carnet.
        
        ordres_path (str): Le chemin du fichier contenant les ordres specifiques.
    """
 
    def __init__(self, id_carnet, bibi, noeud,liste_amers,liste_sites,liste_carnets, ordres_path):
        """Initialise un objet CritereOrdre avec les parametres specifies.

        Args:
            
            
            id_carnet (int): L'identifiant unique du carnet associe au critere.
            
            bibi (Bibi): Un objet Bibi associe au critere.
            
            noeud (Noeud): Un objet Noeud auquel le critere est applique.
            
            liste_amers (list): Une liste d'objets Amer.
            
            liste_sites (list): Une liste d'objets Site.
            
            liste_carnets (list): Une liste d'objets Carnet.
            
            ordres_path (str): Le chemin du fichier contenant les ordres specifiques.
        """
        self.id_carnet = id_carnet
        self.bibi = bibi
        self.noeud = noeud
        self.liste_amers = liste_amers
        self.liste_sites = liste_sites
        self.liste_carnets = liste_carnets
        self.ordres_path = ordres_path
       
 
    def lire_ordre(self):
        """Lire l'ordre specifie dans le carnet associe au critere.

        Returns:
            
            str: L'ordre specifie dans le carnet ("croissant" ou "decroissant").
        """
        ordres_data = pd.read_csv(self.ordres_path, delim_whitespace=True, comment='#', encoding='latin-1')

        for index, row in ordres_data.iterrows():
            if self.id_carnet == row['IdentifiantCarnet']:
                return row['Ordre']
            
    def calcule_angle(self):
        """Calculer les distances angulaires entre les amers associes aux sites de Bibi et le nœud.

        Returns:
            
            tuple: Un tuple contenant les produits scalaires pour chaque paire de sites.
        """
        site1 = self.bibi.identifiant_site1
        site2 = self.bibi.identifiant_site2
        site1_amer1 = self.caracteristique_site(site1).identifiant_amer1
        site1_amer2 = self.caracteristique_site(site1).identifiant_amer2
        site2_amer1 = self.caracteristique_site(site2).identifiant_amer1
        site2_amer2 = self.caracteristique_site(site2).identifiant_amer2
        
        x11, y11, z11 = self.caracteristique_amer(site1_amer1)
        x12, y12, z12 = self.caracteristique_amer(site1_amer2)
        x21, y21, z21 = self.caracteristique_amer(site2_amer1)
        x22, y22, z22 = self.caracteristique_amer(site2_amer2)
        
        
        #Calcule distance noeud/site1
        vecteur_site1_amer1 = np.array([x11-self.noeud.x, y11-self.noeud.y, z11-self.noeud.z])
        vecteur_site1_amer2 = np.array([x12-self.noeud.x, y12-self.noeud.y, z12-self.noeud.z])
        
        # Calculer les normes des vecteurs
        norme_vecteur_site1_amer1 = np.linalg.norm(vecteur_site1_amer1)
        norme_vecteur_site1_amer2 = np.linalg.norm(vecteur_site1_amer2)
    
        # Normaliser les vecteurs
        vecteur_normalise_site1_amer1 = vecteur_site1_amer1 / norme_vecteur_site1_amer1
        vecteur_normalise_site1_amer2 = vecteur_site1_amer2 / norme_vecteur_site1_amer2
    
        # Calculer le produit scalaire des vecteurs normalises
        produit_scalaire_site1 = np.dot(vecteur_normalise_site1_amer1, vecteur_normalise_site1_amer2)
        
        # Calcule distance noeud/site2
        vecteur_site2_amer1 = np.array([x21-self.noeud.x, y21-self.noeud.y, z21-self.noeud.z])
        vecteur_site2_amer2 = np.array([x22-self.noeud.x, y22-self.noeud.y, z22-self.noeud.z])
        
        # Calculer les normes des vecteurs
        norme_vecteur_site2_amer1 = np.linalg.norm(vecteur_site2_amer1)
        norme_vecteur_site2_amer2 = np.linalg.norm(vecteur_site2_amer2)
    
        # Normaliser les vecteurs
        vecteur_normalise_site2_amer1 = vecteur_site2_amer1 / norme_vecteur_site2_amer1
        vecteur_normalise_site2_amer2 = vecteur_site2_amer2 / norme_vecteur_site2_amer2
    
        # Calculer le produit scalaire des vecteurs normalises
        produit_scalaire_site2 = np.dot(vecteur_normalise_site2_amer1, vecteur_normalise_site2_amer2)
        
        return produit_scalaire_site1, produit_scalaire_site2 

        
        
    def caracteristique_amer(self, id_amer):
        """Obtenir les coordonnees d'un amer en fonction de son identifiant.

        Args:
            
            id_amer (int): L'identifiant unique de l'amer.

        Returns:
            
            tuple: Un tuple contenant les coordonnees (x, y, z) de l'amer.
        """
        for i, amer in enumerate(self.liste_amers):
                if amer.identifiant == id_amer:
                    return self.liste_amers[i].x, self.liste_amers[i].y, self.liste_amers[i].z
                
    def caracteristique_site(self, identifiant_site):
        """Obtenir les caracteristiques d'un site en fonction de son identifiant.

        Args:
            
            identifiant_site (int): L'identifiant unique du site.

        Returns:
            
            Site: Un objet Site correspondant a l'identifiant specifie.
        """
        for i, site in enumerate(self.liste_sites):  
            if site.identifiant == identifiant_site:
                return site

        
    def evaluer_point(self):
        """Evaluer le critere d'ordre pour le nœud considere. L'attribut OK du noeud devient True s'il valide le critere d'ordre"""
            # Recuperer l'ordre specifie dans le carnet
        ordre_carnet = self.lire_ordre()
    
        # Recuperer la liste des sites dans l'ordre specifie dans le carnet
        sites_ordre_carnet = None
        
        for carnet in self.liste_carnets:
            if carnet.identifiant[0] == self.id_carnet:
                sites_ordre_carnet = carnet.sites
                Carnet = carnet
    
        if sites_ordre_carnet is None:
            print(f"Aucun carnet trouve avec l'identifiant {self.id_carnet}.")
            return
    
        # Calculer les distances angulaires
        distance_angulaire_site1, distance_angulaire_site2 = self.calcule_angle()
        
        # Recuperer les indices des sites dans l'ordre specifie dans le carnet
        site1_index = Carnet.indice_site_par_identifiant(self.bibi.identifiant_site1)
        site2_index = Carnet.indice_site_par_identifiant(self.bibi.identifiant_site2)
    
    

        
        #Critere d'ordre pour le noeud considere 
        # calcule_angle() renvoie le cosinus de l'angle donc ordre inverse
        
        if site1_index is not None and site2_index is not None:
            
            if ordre_carnet=="croissant":
                # Comparer les distances angulaires avec l'ordre specifie dans le carnet
                if distance_angulaire_site1 > distance_angulaire_site2 and site1_index < site2_index:
                    self.noeud.OK = True
                    # if self.noeud.OK:
                    #     print("pouet")
                  
                elif distance_angulaire_site1 < distance_angulaire_site2 and site1_index > site2_index:
                    self.noeud.OK = True
                    # if self.noeud.OK:
                    #     print("pouet")
                    
                else:
                    self.noeud.OK = False

                    
            if ordre_carnet=="decroissant":
                # Comparer les distances angulaires avec l'ordre specifie dans le carnet
                if distance_angulaire_site1 > distance_angulaire_site2 and site1_index > site2_index:
                    self.noeud.OK = True       
                elif distance_angulaire_site1 < distance_angulaire_site2 and site1_index < site2_index:
                    self.noeud.OK = True
                else:
                    self.noeud.OK = False
    

     