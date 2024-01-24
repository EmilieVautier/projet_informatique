class Noeud:
    """Classe representant un nœud dans un espace tridimensionnel.

    Attributes:
        
        x (float): La coordonnee x du nœud.
        
        y (float): La coordonnee y du nœud.
        
        z (float): La coordonnee z du nœud.
        
        OK (bool): Un attribut booleen indiquant l'etat du nœud (True si OK, False sinon).
    """
    def __init__(self, x, y, z):
        """Initialise un objet Noeud avec des coordonnees.

        Args:
            
            x (float): La coordonnee x du nœud.
            
            y (float): La coordonnee y du nœud.
            
            z (float): La coordonnee z du nœud.
            
            OK (bool): Un attribut booleen indiquant l'etat du nœud (True si OK, False sinon).
        """
        self.x = x
        self.y = y
        self.z = z
        self.OK = False
