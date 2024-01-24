class Bibi:
    """Classe representant un objet Bibi compose de deux sites.

    Attributes:
        
        identifiant_site1 (int): L'identifiant unique du premier site.
        
        identifiant_site2 (int): L'identifiant unique du deuxieme site.
    """
    def __init__(self, identifiant_site1, identifiant_site2):
        """Initialise un objet Bibi avec les identifiants des deux sites qui le composent.

        Args:
            
            identifiant_site1 (int): L'identifiant unique du premier site.
            
            identifiant_site2 (int): L'identifiant unique du deuxieme site.
        """
        self.identifiant_site1 = identifiant_site1
        self.identifiant_site2 = identifiant_site2

