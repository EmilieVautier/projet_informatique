import pandas as pd
import Bibi
import Amers
import Spatial3DDomaine
import Sites
import Carnets
from PyQt5.QtWidgets import QApplication
from tqdm import tqdm
import CritereOrdre
import numpy as np
import colorsys
from plyfile import PlyData, PlyElement
import matplotlib.pyplot as plt


class Analyse:
    """Classe pour effectuer une analyse 3D en utilisant des donnees de carnet, de sites et d'amers.

    Attributes:
        
        amers_path (str): Chemin vers le fichier contenant les donnees des amers.
        
        sites_path (str): Chemin vers le fichier contenant les donnees des sites.
        
        carnets_path (str): Chemin vers le fichier contenant les donnees des carnets.
        
        param_voxellisation_path (str): Chemin vers le fichier contenant les parametres de la voxellisation.
            
        ordres_path (str): Chemin vers le fichier contenant les ordres.
        
        mon_domaine_3d (Spatial3DDomaine): Objet representant le domaine 3D pour la voxellisation.
        
        liste_amers (list): Liste des objets Amer.
        
        liste_sites (list): Liste des objets Site.
        
        liste_carnets (list): Liste des objets Carnet.
    """
    def __init__(self,amers_path=None, sites_path=None, carnets_path=None, param_voxellisation_path=None, ordres_path=None):
        """Initialise une instance de la classe Analyse avec les chemins des fichiers de donnees.

        Args:
            
            amers_path (str, optional): Chemin vers le fichier des amers.
            
            sites_path (str, optional): Chemin vers le fichier des sites.
            
            carnets_path (str, optional): Chemin vers le fichier des carnets.
            
            param_voxellisation_path (str, optional): Chemin vers le fichier des parametres de la voxellisation.
            
            ordres_path (str, optional): Chemin vers le fichier des ordres.
        """
        self.mon_domaine_3d = None
        self.liste_amers = None
        self.liste_sites = None
        self.liste_carnets = None 
        self.amers_path = amers_path
        self.sites_path = sites_path
        self.carnets_path = carnets_path
        self.param_voxellisation_path = param_voxellisation_path
        self.ordres_path = ordres_path
        self.liste_amers, self.liste_sites, self.liste_carnets = None, None, None
        


    def lire_param_voxel(self):
        """Lire les parametres de la voxellisation a partir du fichier specifie.

        Returns:
            
            pd.DataFrame: Un DataFrame contenant les parametres de la voxellisation.
        """
        ParamVoxel = pd.read_csv(self.param_voxellisation_path, delim_whitespace=True, comment='#', encoding='latin-1')
        return ParamVoxel

    def creer_domaine_3d(self):
        """Cree et initialise un objet Spatial3DDomaine pour la voxellisation.

        Returns:
            
            Spatial3DDomaine: Un objet representant le domaine 3D pour la voxellisation.
        """
        param_voxel = self.lire_param_voxel()
        self.mon_domaine_3d = Spatial3DDomaine.Spatial3DDomaine()
        self.mon_domaine_3d.initToBeTested(param_voxel)
        return self.mon_domaine_3d
        
    def initialisation(self):
        """Initialise les listes d'amers, de sites et de carnets en fonction des donnees specifiees.

        Returns:
            
            tuple: Un tuple contenant les listes d'amers, de sites et de carnets.
        """
        amers_reader = Amers.Amers()
        liste_amers = amers_reader.lire_amers(self.amers_path)
  
        sites_reader = Sites.Sites()
        liste_sites = sites_reader.lire_sites(self.sites_path)
        
        carnets_reader = Carnets.Carnets()
        liste_carnets = carnets_reader.lire_carnets(self.carnets_path)
        
        
        sites_a_garder = []
        
        # On filtre les donnees pour ne garder que celle utiles
        for carnet in liste_carnets:
            for site in carnet.sites:
                sites_a_garder.append(site)
        
        liste_sites_filtree = [site for site in liste_sites if site.identifiant in sites_a_garder]
        
        amers_a_garder=[]
        for site in liste_sites_filtree:
            amers_a_garder.append(site.identifiant_amer1)
            amers_a_garder.append(site.identifiant_amer2)

        liste_amers_filtree = [amer for amer in liste_amers if amer.identifiant in amers_a_garder]
        
        
        return liste_amers_filtree, liste_sites_filtree, liste_carnets
    
    
    def analyse(self, progress, progress_label):
        """Effectue l'analyse 3D en evaluant les points OK et NONOK pour chaque carnet.

        Args:
            
            progress (QProgressBar): Barre de progression pour afficher l'avancement.
            
            progress_label (QLabel): etiquette pour afficher des informations sur l'avancement.

        Returns:
            
            tuple: Un tuple contenant les listes de points OK et NONOK pour chaque carnet.
        """
            
            
        self.liste_amers, self.liste_sites, self.liste_carnets = self.initialisation()
        points_ok_total = []
        points_non_ok_total = []

        # Initialiser un ensemble de points nomme « ToBeTested » avec l’ensemble des points de « ToBeTested0 »
        self.mon_domaine_3d = self.creer_domaine_3d()
        ToBeTested0 = self.mon_domaine_3d.ToBeTested
        
        for carnet in self.liste_carnets:
            
            ToBeTested = ToBeTested0
            points_non_ok_carnet = []
            points_ok_carnet = []
            
        

            # Lancer une boucle sur les sites du carnet, jusqu’a l’avant-dernier 
            i = 0
            for site_index in tqdm(range(len(carnet.sites) - 1), desc=f"Analyse Carnet {carnet.identifiant[0]}"):
                
                #points_non_ok_carnet = []
                points_ok_carnet = []

                
                
                
                # L’associer avec le site suivant dans un bibi
                bibi = Bibi.Bibi(identifiant_site1=carnet.sites[site_index], identifiant_site2=carnet.sites[site_index + 1])
                
                # Lancer une boucle sur les points de l’ensemble « ToBeTested »
                for noeud in ToBeTested:
                    # 1. etablir s’il est OK ou NONOK
                    critere_ordre = CritereOrdre.CritereOrdre(id_carnet=carnet.identifiant[0], bibi=bibi, noeud=noeud,
                                                 liste_amers=self.liste_amers, liste_sites=self.liste_sites, liste_carnets=self.liste_carnets, ordres_path=self.ordres_path)
                    critere_ordre.evaluer_point()

                    # S’il est OK, l’enregistrer dans un ensemble nomme « OK_(identifiantSite1_IdentifiantSite2_identifiantCarnet) »,
                    # sinon, l’enregistrer dans un ensemble nomme « NONOK_(identifiantSite1_IdentifiantSite2_identifiantCarnet) »
                    if noeud.OK:
                        points_ok_carnet.append(noeud)
                        
                    else:
                        points_non_ok_carnet.append(noeud)
                        
                    
            
                # Remplacer le contenu de « ToBeTested » par celui de « OK_(identifiantSite1_IdentifiantSite2_identifiantCarnet) »
                ToBeTested = points_ok_carnet
                #print(len(ToBeTested))
                #print("site suivant")
                
                i+=1
                
                progress.setValue(int(100*i/(len(carnet.sites)-1)))
            progress_label.setText(f"Analyse du carnet {carnet.identifiant[0]} terminee")
            QApplication.processEvents() 
            


                # Fin de la boucle sur les sites du carnet)

            # Enregistrez les points OK et NONOK pour le carnet actuel
            points_ok_total.append(points_ok_carnet)
            points_non_ok_total.append(points_non_ok_carnet)
            #print("fin boucle carnet")
            
            
        self.create_ply_file(points_ok_total)

        # Retournez les resultats
        return points_ok_total, points_non_ok_total
    
    def create_ply_file(self, points_ok_total):
        """Cree et enregistre un fichier PLY contenant les points OK.

        Args:
            
            points_ok_total (list): Liste des listes de points OK pour chaque carnet.
        """
        
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
    

                # Definition de la couleur du site avec HSV color space
                
                hue = np.random.rand()  # Valeur aleatoire de la teinte entre 0 et 1 
                saturation = np.random.uniform(0.5, 1.0)  # Valeur aleatoire de la saturation entre 0.5 et 1.0
                value = np.random.uniform(0.5, 1.0)  # Valeur aleatoire de la luminosite entre 0.5 et 1.0
    
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
                
          
                  
            # Definition de la couleur des points OK
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
            

            # Preparation des donnees pour la creation du fichier PLY
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
            

            # Ecrire le fichier PLY
            ply_filename = f'OK_{self.liste_carnets[k].identifiant[0]}.ply'
            elv = PlyElement.describe(vertex_all, 'vertex',
                                      comments=['comment1',
                                                'comment2'])
    
            elf = PlyElement.describe( points_faces, 'face',
                                    val_types={'vertex_indices': 'u1'},
                                      len_types={'vertex_indices': 'u1'})
    
            PlyData([elv,elf], text=True).write(ply_filename) # Ecriture du fichier PLY


    def create_sphere(self,radius, num_points,center,decalage):
        """Cree les vertices et faces d'une sphere.

        Args:
            
            radius (float): Rayon de la sphere.
            
            num_points (int): Nombre de points pour la creation de la sphere.
            
            center (list): Coordonnees du centre de la sphere.
            
            decalage (int): Decalage pour les indices de la sphere.

        Returns:
            
            tuple: Un tuple contenant les vertices et faces de la sphere.
        """
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
            
        
            
    def afficher_domaine_3d(self, points_ok_total, points_non_ok_total):
        """Affiche les resultats de l'analyse 3D avec des points colores en fonction des sites.
    
        Args:
            
            points_ok_total (list): Liste des points OK pour chaque carnet.
            
            points_non_ok_total (list): Liste des points NON OK pour chaque carnet.
    
        Returns:
            
            None. Affiche la visualisation 3D.
        """
        for k, points_ok in enumerate(points_ok_total):
            fig = plt.figure()
            ax = fig.add_subplot(111, projection='3d')

            x_pointsok = [point.x for point in points_ok]
            y_pointsok = [point.y for point in points_ok]
            z_pointsok = [point.z for point in points_ok]

            # Liste pour stocker les noms de sites et les couleurs correspondantes
            site_colors = []

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
                color = np.array([r, g, b]).reshape(1, 3)

                # Ajouter la couleur du site a la liste
                site_colors.append((f'Site {site}', color))

                # Afficher le point avec la couleur specifiee
                ax.scatter(x11, y11, z11, marker='o', c=color, s=100)
                ax.scatter(x12, y12, z12, marker='o', c=color, s=100)

                # Ajouter une annotation texte a côte du point
                ax.text(x11, y11, z11, f'Site {site}', color=color, fontsize=8)
                ax.text(x12, y12, z12, f'Site {site}', color=color, fontsize=8)
                
            # Afficher les positions possibles de l'utilisateur en vert
            ax.scatter(x_pointsok, y_pointsok, z_pointsok, marker='o', c='green', s=5, label='Positions Possibles')

            # Ajouter une legende avec les couleurs des sites
            legend_sites = ax.legend(handles=[plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=color, markersize=10) for _, color in site_colors],
                                     labels=[label for label, _ in site_colors], loc='upper left')

            # Ajouter une legende specifique pour les positions possibles de l'utilisateur
            legend_positions = ax.legend(handles=[plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='green', markersize=5)],
                                         labels=['Positions Possibles'], loc='upper right')

            # Ajouter la legende specifique a la figure
            ax.add_artist(legend_sites)

            ax.set_xlabel('X')
            ax.set_ylabel('Y')
            ax.set_zlabel('Z')
            ax.set_title(f'Resultats pour le carnet {self.liste_carnets[k].identifiant[0]}')
            plt.show()
            