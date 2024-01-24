class Amer:
    """Classe representant un amer, avec un identifiant et des coordonnees tridimensionnelles.

    Attributes:
        
        identifiant (int): L'identifiant unique de l'amer.
        
        x (float): Coordonnee x de l'amer.
        
        y (float): Coordonnee y de l'amer.
        
        z (float): Coordonnee z de l'amer.
    """

    def __init__(self, identifiant, x, y, z):
        """Initialise un objet Amer avec un identifiant et des coordonnees.

        Args:
            
            identifiant (int): L'identifiant unique de l'amer.
            
            x (float): Coordonnee x de l'amer.
            
            y (float): Coordonnee y de l'amer.
            
            z (float): Coordonnee z de l'amer.
        """
        self.identifiant = identifiant
        self.x = x
        self.y = y
        self.z = z