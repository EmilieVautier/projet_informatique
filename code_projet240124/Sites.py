import Site
import pandas as pd 


class Sites:
    """Classe representant une collection de sites composes de deux amers. Cette classe permet de lire des donnees a partir d'un fichier et de creer une liste d'objets Site correspondants.

    """

    def lire_sites(self,file_path):
        """Lire les donnees de sites a partir d'un fichier et creer une liste d'objets Site.

        Args:
            
            file_path (str): Le chemin du fichier contenant les donnees de sites.

        Returns:
            
            list: Une liste d'objets Site crees a partir des donnees lues.
        """
        # Lire les donnees du fichier en utilisant pandas
        sites_data = pd.read_csv(file_path, delim_whitespace=True, comment='#', encoding='latin-1')

        # Creer une liste d'objets Site a partir des donnees lues
        sites_list = []
        for index, row in sites_data.iterrows():
            site = Site.Site(row['IdentifiantSite'],row['IdentifiantAmer1'], row['IdentifiantAmer2'])
            sites_list.append(site)

        return sites_list
