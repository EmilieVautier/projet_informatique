class Site:
    """Classe representant un site compose de deux amers.

    Attributes:
        
        identifiant (int): L'identifiant unique du site.
        
        identifiant_amer1 (int): L'identifiant unique du premier amer composant le site.
        
        identifiant_amer2 (int): L'identifiant unique du deuxieme amer composant le site.
    """

    def __init__(self, identifiant, identifiant_amer1, identifiant_amer2):
        """Initialise un objet Site avec un identifiant et les identifiants des deux amers qui le composent.

        Args:
            
            identifiant (int): L'identifiant unique du site.
            
            identifiant_amer1 (int): L'identifiant unique du premier amer composant le site.
            
            identifiant_amer2 (int): L'identifiant unique du deuxieme amer composant le site.
        """
        # Initialisation de la classe Site avec les identifiants des amers qui le composent
        self.identifiant = identifiant
        self.identifiant_amer1 = identifiant_amer1
        self.identifiant_amer2 = identifiant_amer2

