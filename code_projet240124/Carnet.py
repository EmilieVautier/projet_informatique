class Carnet:
    """Classe representant un carnet contenant une liste de sites.

    Attributes:
        
        identifiant (int): L'identifiant unique du carnet.
        
        sites (list): Une liste d'objets Site composant le carnet.
    """
   
    def __init__(self, identifiant, sites):
        """Initialise un objet Carnet avec un identifiant et une liste de sites.

        Args:
            
            identifiant (int): L'identifiant unique du carnet.
            
            sites (list): Une liste d'objets Site composant le carnet.
        """
        self.identifiant = identifiant
        self.sites = sites
        
    def indice_site_par_identifiant(self, identifiant_site):
        """Obtenir l'indice d'un site dans le carnet en utilisant son identifiant.

        Args:
            
            identifiant_site (int): L'identifiant du site a rechercher dans le carnet.

        Returns:
            
            int or None: L'indice du site dans le carnet (commencant a 1) s'il est trouve,
                         ou None si l'identifiant du site n'est pas trouve dans le carnet.
        """
        for i, site in enumerate(self.sites):
        
            if site == identifiant_site:
                return i
        return None # Retourne None si l'identifiant du site n'est pas trouve dans le carnet

        
    