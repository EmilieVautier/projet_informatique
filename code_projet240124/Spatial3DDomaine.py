import Noeud
import pandas as pd


class Spatial3DDomaine:
    """Classe representant un domaine spatial en 3D. Elle permet aussi de generer une liste de nœuds a tester dans le domaine spatial en fonction des parametres du voxel.

    Attributes:
        
        ToBeTested (list): Une liste de nœuds a tester dans le domaine spatial.
    """
    def __init__(self):
        """Initialise un objet Spatial3DDomaine avec une liste vide de nœuds a tester."""
        self.ToBeTested = []

    def lire_param_voxel(self, file_path):
        """Lire les parametres du voxel a partir d'un fichier.

        Args:
            
            file_path (str): Le chemin du fichier contenant les parametres du voxel.

        Returns:
            
            pd.DataFrame: Un DataFrame contenant les parametres du voxel.
        """
        ParamVoxel = pd.read_csv(file_path, delim_whitespace=True, comment='#', encoding='latin-1')
        return ParamVoxel

    def initToBeTested(self, ParamVoxel):
        """Initialise la liste de nœuds a tester dans le domaine spatial en fonction des parametres du voxel.

        Args:
            
            ParamVoxel (pd.DataFrame): Un DataFrame contenant les parametres du voxel.
        """
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

                        new_noeud = Noeud.Noeud(x_center, y_center, z_center)
                        self.ToBeTested.append(new_noeud)
                        
            
