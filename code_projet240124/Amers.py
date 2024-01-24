import Amer
import pandas as pd

class Amers:
    """Classe representant une collection d'amers.

    Cette classe permet de lire des donnees a partir d'un fichier et de creer une liste d'objets Amer correspondants.

    """
    def lire_amers(self, file_path):
        """Lire les donnees d'amers a partir d'un fichier et creer une liste d'objets Amer.

        Args:
            
            file_path (str): Le chemin du fichier contenant les donnees d'amers.

        Returns:
            
            list: Une liste d'objets Amer crees a partir des donnees lues.
        """
        # Lire les donnees du fichier en utilisant pandas
        amers_data = pd.read_csv(file_path, delim_whitespace=True, comment='#', encoding='latin-1')

        # Creer une liste d'objets Amer a partir des donnees lues
        amers_list = []
        for index, row in amers_data.iterrows():
            amer = Amer.Amer(row['Identifiant'], row['X'], row['Y'], row['Z'])
            amers_list.append(amer)

        return amers_list


