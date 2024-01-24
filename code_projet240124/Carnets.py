import Carnet 
import pandas as pd
from io import StringIO

class Carnets:
    """Classe representant une collection de carnets contenant des listes de sites. Cette classe permet de lire des donnees a partir d'un fichier et de creer une liste d'objets Carnet correspondants.

    """
    def lire_carnets(self,file_path):
        """Lire les donnees de carnets a partir d'un fichier et creer une liste d'objets Carnet.

        Args:
            
            file_path (str): Le chemin du fichier contenant les donnees de carnets.

        Returns:
            
            list: Une liste d'objets Carnet crees a partir des donnees lues.
        """
        
        carnets = []
        with open(file_path, 'r') as file:
            lines = file.readlines()[1:]  # Ignorer la premiere ligne

            for line in lines:
                # Utilisez le nom des colonnes comme IdentifiantCarnet, Site1, Site2, etc.
                col_names = ["IdentifiantCarnet"] + [f"Site{i}" for i in range(1, len(line.split()))]
                data = pd.read_csv(StringIO(line), delim_whitespace=True, names=col_names, comment='#', encoding='latin-1')
                
                identifiant = data["IdentifiantCarnet"]
                sites = [data[f"Site{i}"].iloc[0] for i in range(1, len(line.split()))]  # Utilisez iloc[0] pour obtenir la valeur
                carnet = Carnet.Carnet(identifiant, sites)
                carnets.append(carnet)
        
        return carnets
  
  