import Interface
from PyQt5.QtWidgets import QApplication
import sys


# Exemple d'utilisation
if __name__ == "__main__":
    
    """Lance l'interface PyQt5. Cette fonction initialise l'application PyQt5, crée une instance de la classe Interface, et lance l'application.

    """
    
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(True)
    picker = Interface.Interface()
    picker.show()
    
    
    sys.exit(app.exec_())
