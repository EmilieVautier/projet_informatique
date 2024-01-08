import pandas as pd
from io import StringIO
import matplotlib.pyplot as plt
import numpy as np
from tqdm import tqdm
import plyfile
from plyfile import PlyData, PlyElement
import colorsys


class Amers:
    # Définition de la classe Amers
    def lire_amers(self):
        amers_data = pd.read_csv('data/amers.txt', delim_whitespace=True, comment='#')

        # Créer une liste d'objets Amer à partir des données lues
        amers_list = []
        for index, row in amers_data.iterrows():
            amer = Amer(row['Identifiant'], row['X'], row['Y'], row['Z'])
            amers_list.append(amer)

        return amers_list

class Sites:
    # Définition de la classe Sites
    def lire_sites(self):
        sites_data = pd.read_csv('data/sites.txt', delim_whitespace=True, comment='#')

        # Créer une liste d'objets Site à partir des données lues
        sites_list = []
        for index, row in sites_data.iterrows():
            site = Site(row['IdentifiantSite'],row['IdentifiantAmer1'], row['IdentifiantAmer2'])
            sites_list.append(site)

        return sites_list

class Carnets:
    # Définition de la classe Carnets
    def lire_carnets(self):
        # Remplacez "votre_fichier.txt" par le chemin de votre fichier texte
        filename = 'data/carnets.txt'
        
        carnets = []
        with open(filename, 'r') as file:
            lines = file.readlines()[1:]  # Ignorer la première ligne

            for line in lines:
                # Utilisez le nom des colonnes comme IdentifiantCarnet, Site1, Site2, etc.
                col_names = ["IdentifiantCarnet"] + [f"Site{i}" for i in range(1, len(line.split()))]
                data = pd.read_csv(StringIO(line), delim_whitespace=True, names=col_names, comment='#')
                
                identifiant = data["IdentifiantCarnet"]
                sites = [data[f"Site{i}"].iloc[0] for i in range(1, len(line.split()))]  # Utilisez iloc[0] pour obtenir la valeur
                carnet = Carnet(identifiant, sites)
                carnets.append(carnet)
        
        return carnets
  
  
            
class Amer:
    # Définition de la classe Amer
    def __init__(self, identifiant, x, y, z):
        # Initialisation de la classe Amer avec un identifiant et des coordonnées
        self.identifiant = identifiant
        self.x = x
        self.y = y
        self.z = z

class Site:
    # Définition de la classe Site
    def __init__(self, identifiant, identifiant_amer1, identifiant_amer2):
        # Initialisation de la classe Site avec les identifiants des amers qui le composent
        self.identifiant = identifiant
        self.identifiant_amer1 = identifiant_amer1
        self.identifiant_amer2 = identifiant_amer2


class Carnet:
    # Définition de la classe Carnet
    def __init__(self, identifiant, sites):
        self.identifiant = identifiant
        self.sites = sites
        
    def indice_site_par_identifiant(self, identifiant_site):
        for i, site in enumerate(self.sites):
        
            if site == identifiant_site:
                return i  # Ajoute 1 car les indices commencent à 1 dans votre exemple
        return None  # Retourne None si l'identifiant du site n'est pas trouvé dans le carnet

        
    


class Spatial3DDomaine:
    def __init__(self):
        # Initialisation de la classe Spatial3DDomaine
        self.ToBeTested = []

    def lire_param_voxel(self, file_path):
        ParamVoxel = pd.read_csv(file_path, delim_whitespace=True, comment='#')
        return ParamVoxel

    def initToBeTested(self, ParamVoxel):
        for index, row in ParamVoxel.iterrows():
            x_min, y_min, z_min = row['xmin'], row['ymin'], row['zmin']
            resolution = row['resolution']
            nbe_x, nbe_y, nbe_z = int(row['nbex']), int(row['nbey']), int(row['nbez'])

            for i in range(nbe_x):
                for j in range(nbe_y):
                    for k in range(nbe_z):
                        x_center = x_min + i * resolution
                        y_center = y_min + j * resolution
                        z_center = z_min + k * resolution

                        new_noeud = Noeud(x_center, y_center, z_center)
                        self.ToBeTested.append(new_noeud)
                        
            

    
class Noeud:
    def __init__(self, x, y, z):
        # Initialisation de la classe Noeud avec des coordonnées
        self.x = x
        self.y = y
        self.z = z
        self.OK = False  # Ajout de l'attribut OK de type boolean


class CritereOrdre:
    # Définition de la classe CritereOrdre
    def __init__(self, id_carnet, bibi, noeud,liste_amers,liste_sites,liste_carnets):
        self.id_carnet = id_carnet
        self.bibi = bibi
        self.noeud = noeud
        self.liste_amers = liste_amers
        self.liste_sites = liste_sites
        self.liste_carnets = liste_carnets
       
 
    def lire_ordre(self):
        ordres_data = pd.read_csv('data/ordres.txt', delim_whitespace=True, comment='#')

        for index, row in ordres_data.iterrows():
            if self.id_carnet == row['IdentifiantCarnet']:
                return row['Ordre']
            
    def calcule_angle(self):
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
        
        
        """ Calcule distance noeud/site1 """
        vecteur_site1_amer1 = np.array([x11-self.noeud.x, y11-self.noeud.y, z11-self.noeud.z])
        vecteur_site1_amer2 = np.array([x12-self.noeud.x, y12-self.noeud.y, z12-self.noeud.z])
        
        # Calculer les normes des vecteurs
        norme_vecteur_site1_amer1 = np.linalg.norm(vecteur_site1_amer1)
        norme_vecteur_site1_amer2 = np.linalg.norm(vecteur_site1_amer2)
    
        # Normaliser les vecteurs
        vecteur_normalise_site1_amer1 = vecteur_site1_amer1 / norme_vecteur_site1_amer1
        vecteur_normalise_site1_amer2 = vecteur_site1_amer2 / norme_vecteur_site1_amer2
    
        # Calculer le produit scalaire des vecteurs normalisés
        produit_scalaire_site1 = np.dot(vecteur_normalise_site1_amer1, vecteur_normalise_site1_amer2)
        
        """ Calcule distance noeud/site2 """
        vecteur_site2_amer1 = np.array([x21-self.noeud.x, y21-self.noeud.y, z21-self.noeud.z])
        vecteur_site2_amer2 = np.array([x22-self.noeud.x, y22-self.noeud.y, z22-self.noeud.z])
        
        # Calculer les normes des vecteurs
        norme_vecteur_site2_amer1 = np.linalg.norm(vecteur_site2_amer1)
        norme_vecteur_site2_amer2 = np.linalg.norm(vecteur_site2_amer2)
    
        # Normaliser les vecteurs
        vecteur_normalise_site2_amer1 = vecteur_site2_amer1 / norme_vecteur_site2_amer1
        vecteur_normalise_site2_amer2 = vecteur_site2_amer2 / norme_vecteur_site2_amer2
    
        # Calculer le produit scalaire des vecteurs normalisés
        produit_scalaire_site2 = np.dot(vecteur_normalise_site2_amer1, vecteur_normalise_site2_amer2)
        
        return produit_scalaire_site1, produit_scalaire_site2 

        
        
    def caracteristique_amer(self, id_amer):
        for i, amer in enumerate(self.liste_amers):
                if amer.identifiant == id_amer:
                    return self.liste_amers[i].x, self.liste_amers[i].y, self.liste_amers[i].z
    def caracteristique_site(self, identifiant_site):
        for i, site in enumerate(self.liste_sites):  # Utiliser liste_sites au lieu de list_amers
            if site.identifiant == identifiant_site:
                return site

        
    def evaluer_point(self):
            # Récupérer l'ordre spécifié dans le carnet
        ordre_carnet = self.lire_ordre()
    
        # Récupérer la liste des sites dans l'ordre spécifié dans le carnet
        sites_ordre_carnet = None
        
        for carnet in self.liste_carnets:
            if carnet.identifiant[0] == self.id_carnet:
                sites_ordre_carnet = carnet.sites
                Carnet = carnet
    
        if sites_ordre_carnet is None:
            print(f"Aucun carnet trouvé avec l'identifiant {self.id_carnet}.")
            return
    
        # Calculer les distances angulaires
        distance_angulaire_site1, distance_angulaire_site2 = self.calcule_angle()
        
        # Récupérer les indices des sites dans l'ordre spécifié dans le carnet
        site1_index = Carnet.indice_site_par_identifiant(self.bibi.identifiant_site1)
        site2_index = Carnet.indice_site_par_identifiant(self.bibi.identifiant_site2)
    
    

        
        """ Critère d'ordre pour le noeud considéré """
        # calcule_angle() renvoie le cosinus de l'angle donc ordre inversé
        
        if site1_index is not None and site2_index is not None:
            
            if ordre_carnet=="croissant":
                # Comparer les distances angulaires avec l'ordre spécifié dans le carnet
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
                # Comparer les distances angulaires avec l'ordre spécifié dans le carnet
                if distance_angulaire_site1 > distance_angulaire_site2 and site1_index > site2_index:
                    self.noeud.OK = True       
                elif distance_angulaire_site1 < distance_angulaire_site2 and site1_index < site2_index:
                    self.noeud.OK = True
                else:
                    self.noeud.OK = False
    

        
        
        

class Bibi:
    # Définition de la classe Bibi
    def __init__(self, identifiant_site1, identifiant_site2):
        # Initialisation de la classe Site avec les identifiants des amers qui le composent
        self.identifiant_site1 = identifiant_site1
        self.identifiant_site2 = identifiant_site2

class Analyse:
    def __init__(self):
        self.mon_domaine_3d = None
        self.liste_amers = None
        self.liste_sites = None
        self.liste_carnets = None
        
        self.liste_amers, self.liste_sites, self.liste_carnets = self.initialisation()

    def lire_param_voxel(self, file_path):
        ParamVoxel = pd.read_csv(file_path, delim_whitespace=True, comment='#')
        return ParamVoxel

    def creer_domaine_3d(self, file_path):
        param_voxel = self.lire_param_voxel(file_path)
        self.mon_domaine_3d = Spatial3DDomaine()
        self.mon_domaine_3d.initToBeTested(param_voxel)
        return self.mon_domaine_3d
        
    def initialisation(self):
        amers_reader = Amers()
        liste_amers = amers_reader.lire_amers()
        
        sites_reader = Sites()
        liste_sites = sites_reader.lire_sites()
        
        carnets_reader = Carnets()
        liste_carnets = carnets_reader.lire_carnets()
        return liste_amers, liste_sites, liste_carnets
    
    
    def analyse(self):
        points_ok_total = []
        points_non_ok_total = []

        # Initialiser un ensemble de points nommé « ToBeTested » avec l’ensemble des points de « ToBeTested0 »
        self.mon_domaine_3d = self.creer_domaine_3d('data/parametres_voxellisation.txt')
        ToBeTested0 = self.mon_domaine_3d.ToBeTested
        
        for carnet in self.liste_carnets:
            
            ToBeTested = ToBeTested0
            points_non_ok_carnet = []
            points_ok_carnet = []
            

            # Lancer une boucle sur les sites du carnet, jusqu’à l’avant-dernier 
            
            for site_index in tqdm(range(len(carnet.sites) - 1), desc=f"Analyse Carnet {carnet.identifiant[0]}"):
                #points_non_ok_carnet = []
                points_ok_carnet = []

                
                
                
                # L’associer avec le site suivant dans un bibi
                bibi = Bibi(identifiant_site1=carnet.sites[site_index], identifiant_site2=carnet.sites[site_index + 1])
                
                # Lancer une boucle sur les points de l’ensemble « ToBeTested »
                for noeud in ToBeTested:
                    # 1. Établir s’il est OK ou NONOK
                    critere_ordre = CritereOrdre(id_carnet=carnet.identifiant[0], bibi=bibi, noeud=noeud,
                                                 liste_amers=self.liste_amers, liste_sites=self.liste_sites, liste_carnets=self.liste_carnets)
                    critere_ordre.evaluer_point()

                    # S’il est OK, l’enregistrer dans un ensemble nommé « OK_(identifiantSite1_IdentifiantSite2_identifiantCarnet) »,
                    # sinon, l’enregistrer dans un ensemble nommé « NONOK_(identifiantSite1_IdentifiantSite2_identifiantCarnet) »
                    if noeud.OK:
                        points_ok_carnet.append(noeud)
                        
                    else:
                        points_non_ok_carnet.append(noeud)
                        
                    
            
                # Remplacer le contenu de « ToBeTested » par celui de « OK_(identifiantSite1_IdentifiantSite2_identifiantCarnet) »
                ToBeTested = points_ok_carnet
                #print(len(ToBeTested))
                #print("site suivant")
                

                # Fin de la boucle sur les sites du carnet)

            # Enregistrez les points OK et NONOK pour le carnet actuel
            points_ok_total.append(points_ok_carnet)
            points_non_ok_total.append(points_non_ok_carnet)
            #print("fin boucle carnet")

        # Retournez les résultats
        return points_ok_total, points_non_ok_total
    
    def create_ply_file(self, filename, amers_vertices, amers_faces, points_vertices, points_faces=None):
        all_vertices = np.concatenate([amers_vertices, points_vertices])
        all_faces = np.concatenate([amers_faces, points_faces]) if points_faces is not None else None

        vertex_dtype = [('x', 'f4'), ('y', 'f4'), ('z', 'f4')]
        face_dtype = [('vertex_indices', 'i4', (3,)), ('red', 'u1'), ('green', 'u1'), ('blue', 'u1')]

        el_vertex = PlyElement.describe(all_vertices, 'vertex')
        el_face = PlyElement.describe(all_faces, 'face') if all_faces is not None else None

        PlyData([el_vertex, el_face], text=True).write(filename)


    def create_sphere(self,radius, num_points,center,decalage):
        phi = np.linspace(0, np.pi, num_points)
        theta = np.linspace(0, 2 * np.pi, num_points)
        phi, theta = np.meshgrid(phi, theta)
    
        x = radius * np.sin(phi) * np.cos(theta)
        y = radius * np.sin(phi) * np.sin(theta)
        z = radius * np.cos(phi)
    
        vertices = np.array([x.flatten(), y.flatten(), z.flatten()]).T
        
        vertices += np.array([center[0],center[1],center[2]])
    
        faces = []
       
        for i in range(0,num_points - 1):
            for j in range(0,num_points - 1):
                k1 = i * num_points + j + decalage
                k2 = k1 + 1
                k3 = (i + 1) * num_points + j + decalage
                k4 = k3 + 1
                faces.append([k1, k2, k4])
                faces.append([k1, k4, k3])
    
        return vertices, faces



    def caracteristique_amer(self, id_amer):
        for i, amer in enumerate(self.liste_amers):
            if amer.identifiant == id_amer:
                return self.liste_amers[i].x, self.liste_amers[i].y, self.liste_amers[i].z           
    
    def caracteristique_site(self, identifiant_site):
        for i, site in enumerate(self.liste_sites):  # Utiliser liste_sites au lieu de list_amers
            if site.identifiant == identifiant_site:
                return site
            
        
            
    def afficher_domaine_3d(self, points_ok_total,points_non_ok_total):
        
        for k in range (len(points_ok_total)):
            
            points_ok = points_ok_total[k]
            points_non_ok = points_non_ok_total[k]
            
            fig = plt.figure()
            ax = fig.add_subplot(111, projection='3d')
            
    
    
            x_pointsok = [point.x for point in points_ok]
            y_pointsok = [point.y for point in points_ok]
            z_pointsok = [point.z for point in points_ok]
            
            x_pointsnook = [point.x for point in points_non_ok]
            y_pointsnook = [point.y for point in points_non_ok]
            z_pointsnook = [point.z for point in points_non_ok]
            
            
            for j, site in enumerate(self.liste_carnets[k].sites):
                site_amer1 = self.caracteristique_site(site).identifiant_amer1
                site_amer2 = self.caracteristique_site(site).identifiant_amer2
                x11, y11, z11 = self.caracteristique_amer(site_amer1)
                x12, y12, z12 = self.caracteristique_amer(site_amer2)


                # Definition de la couleur du site avec HSV color space
                
                hue = np.random.rand()  # Random hue value between 0 and 1
                saturation = np.random.uniform(0.5, 1.0)  # Random saturation between 0.5 and 1.0
                value = np.random.uniform(0.5, 1.0)  # Random value (brightness) between 0.5 and 1.0
    
                # Convertir HSV en RGB
                r, g, b = colorsys.hsv_to_rgb(hue, saturation, value)
                color = np.array([r, g, b]).reshape(1,3)

                # Afficher le point avec la couleur spécifiée
                ax.scatter(x11,y11,z11, marker='o', c=color, s=100)
                ax.scatter(x12,y12,z12, marker='o', c=color, s=100)
                

                # Ajouter une annotation texte à côté du point
                ax.text(x11, y11, z11, f'Site {site}', color=color, fontsize=8)
                ax.text(x12, y12, z12, f'Site {site}', color=color, fontsize=8)
    
    
                    
            ax.scatter(x_pointsok, y_pointsok, z_pointsok, marker='o',c = 'green')
            ax.scatter(x_pointsnook, y_pointsnook, z_pointsnook, marker='o', c='red', alpha=0.2)
            ax.set_xlabel('X')
            ax.set_ylabel('Y')
            ax.set_zlabel('Z')
            ax.set_title('Domaine 3D')
    
            plt.show()
            
            

        
        
        for k in range (len(self.liste_carnets)):
            # creer les vertices et faces des spheres
            vertices_colors=[]
            spheres_vertices = []
            spheres_faces = []
            n=0

            for j, site in enumerate(self.liste_carnets[k].sites):
                site_amer1 = self.caracteristique_site(site).identifiant_amer1
                site_amer2 = self.caracteristique_site(site).identifiant_amer2
                x11, y11, z11 = self.caracteristique_amer(site_amer1)
                x12, y12, z12 = self.caracteristique_amer(site_amer2)
    
                decalage = len(spheres_vertices)
                
                # Definition de la couleur du site avec HSV color space
                
                hue = np.random.rand()  # Random hue value between 0 and 1
                saturation = np.random.uniform(0.5, 1.0)  # Random saturation between 0.5 and 1.0
                value = np.random.uniform(0.5, 1.0)  # Random value (brightness) between 0.5 and 1.0
    
                # Converti HSV en RGB
                r, v, b = colorsys.hsv_to_rgb(hue, saturation, value)
                r = int(r * 255)
                v = int(v * 255)
                b = int(b * 255)
        
                    
                            
                # Sphere du premiere amer
                center = [x11, y11, z11]
                radius = 1
                num_points = 10
                vertices1, faces1 = self.create_sphere(radius,num_points,center,len(spheres_vertices))
                for vertice in vertices1:
                    spheres_vertices.append((vertice[0],vertice[1],vertice[2]))
                    vertices_colors.append((r,v,b))
                for face in faces1:
                    spheres_faces.append((list(face),r,v,b))
                    
                
                # Sphere du deuxieme amer
                center = [x12, y12, z12]
                radius = 1
                num_points = 10
                vertices2, faces2 = self.create_sphere(radius, num_points,center,len(spheres_vertices))
                
                for vertice in vertices2:
                    spheres_vertices.append((vertice[0],vertice[1],vertice[2]))
                    vertices_colors.append((r,v,b))
                    
                for face in faces2:
                    spheres_faces.append((list(face),r,v,b))
                    
               
                n+=1
                
                
                
                
                    
                    
        
                    
                  
            #definition de la couleur des points OK
            r = 0
            v = 255
            b = 0
            
            points_ok = points_ok_total[k]
            x_pointsok = [point.x for point in points_ok]
            y_pointsok = [point.y for point in points_ok]
            z_pointsok = [point.z for point in points_ok]

            points_list=[]
            for i in range (len(x_pointsok)):
                points_list.append((x_pointsok[i],y_pointsok[i],z_pointsok[i]))
                vertices_colors.append((r,v,b))
                

        
            spheres_vertices += points_list
            

              
            vertices = spheres_vertices


            points_vertices = np.array(vertices,dtype=[('x', 'f4'), ('y', 'f4'),
                    ('z', 'f4')]).reshape(-1,)
            
            vertices_colors = np.array(vertices_colors, dtype=[('red', 'u1'), ('green', 'u1'), ('blue', 'u1')]).reshape(-1,)
            
            n = len(points_vertices)
            assert len(vertices_colors) == n
            
            vertex_all = np.empty(n, points_vertices.dtype.descr + vertices_colors.dtype.descr)
            
            for prop in points_vertices.dtype.names:
                vertex_all[prop] = points_vertices[prop]
            
            for prop in vertices_colors.dtype.names:
                vertex_all[prop] = vertices_colors[prop]
            
            
            
            
            points_faces = np.array(spheres_faces,
               dtype=[('vertex_indices', 'i4', (3,)),
                      ('red', 'u1'), ('green', 'u1'),
                      ('blue', 'u1')])
            


            # Ecrire fichier PLY
            ply_filename = f'OK_{self.liste_carnets[k].identifiant[0]}.ply'
            elv = PlyElement.describe(vertex_all, 'vertex',
                                      comments=['comment1',
                                                'comment2'])
    
            elf = PlyElement.describe( points_faces, 'face',
                                    val_types={'vertex_indices': 'u1'},
                                      len_types={'vertex_indices': 'u1'})
    
            PlyData([elv,elf], text=True).write(ply_filename)
            
         
            
    

        
class Interface:
    # Définition de la classe Interface
    pass


# Exemple d'utilisation
if __name__ == "__main__":
    # analyse_instance = Analyse()

    # # Chemin vers le fichier de paramètres de voxelisation
    # param_file_path = 'C:/Users/fredv/Desktop/projet_informatique/data/data_test/parametres_voxellisation.txt'

    # Création du domaine 3D en partant de la position fixe du centre du premier voxel
    #analyse_instance.analyse(param_file_path)

    # Affichage graphique du domaine 3D
    # analyse_instance.afficher_domaine_3d()
    
    # Exemple d'utilisation
    # carnets_reader = Carnets()
    # liste_carnets = carnets_reader.lire_carnets()
    
    # # Accès aux attributs des carnets
    # for carnet in liste_carnets:
    #     print(f"IdentifiantCarnet : {carnet.identifiant}, Sites : {carnet.sites}")
    
    
    # Exemple d'utilisation
    # amers_reader = Amers()
    # liste_amers = amers_reader.lire_amers()
    # Carnets = Carnets()
    # liste_carnets = Carnets.lire_carnets()
    # print(liste_carnets[0].identifiant)
    # print(liste_carnets[0].indice_site_par_identifiant(6622))
    # Affichage des coordonnées du premier amer dans la liste
    #print(f"Premier amer - Identifiant : {liste_amers[0].identifiant}, Coordonnées : ({liste_amers[0].x}, {liste_amers[0].y}, {liste_amers[0].z})")
    
    #Exemple d'utilisation
    # amers_reader = Amers()
    # liste_amers = amers_reader.lire_amers()
    
    # sites_reader = Sites()
    # liste_sites = sites_reader.lire_sites()
    
    # carnets_reader = Carnets()
    # liste_carnets = carnets_reader.lire_carnets()
    
    # # Exemple de création d'un Bibi
    # bibi_exemple = Bibi(identifiant_site1=6622, identifiant_site2=2993)
    
    # # Exemple de création d'un Noeud (vous devez remplacer les valeurs appropriées)
    # noeud_exemple = Noeud(92.5412356785003, 88.6182356785003, 98.2712356785003)
    
    # # Exemple de création d'une instance de la classe CritereOrdre
    # critere_ordre = CritereOrdre(id_carnet=1, bibi=bibi_exemple, noeud=noeud_exemple, liste_amers=liste_amers, liste_sites=liste_sites, liste_carnets=liste_carnets)
    
    # # Exemple d'évaluation du point
    # critere_ordre.evaluer_point()
    
    # spatial_domain = Spatial3DDomaine()

    # # Lire le fichier des paramètres de voxelisation
    # param_file_path = 'C:/Users/fredv/Desktop/projet_informatique/data/data_test/parametres_voxellisation.txt'
    # param_voxel = spatial_domain.lire_param_voxel(param_file_path)

    # # Initialiser le domaine 3D
    # spatial_domain.initToBeTested(param_voxel)
    
    # print(spatial_domain.ToBeTested[10].x)
    
    
    analyse_instance = Analyse()

    # ... (initialisez le domaine 3D et autres données nécessaires)

    # Appelez la fonction d'analyse
    points_ok, points_non_ok = analyse_instance.analyse()
    
    analyse_instance.afficher_domaine_3d(points_ok,points_non_ok)

    # # Affichez ou utilisez les résultats comme nécessaire
    # print("Points OK:")
    # for points_ok_carnet in points_ok:
    #     print(points_ok_carnet)

    # print("Points NON OK:")
    # for points_non_ok_carnet in points_non_ok:
    #     print(points_non_ok_carnet)
    
