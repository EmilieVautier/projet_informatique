from PyQt5.QtCore import Qt
import Analyse
from PyQt5.QtWidgets import QInputDialog, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QFileDialog, QMessageBox, QProgressBar, QLabel, QGridLayout
import GenParamVoxel           



class Interface(QWidget):
    def __init__(self, parent=None):
        """
        Initialisation de l'interface utilisateur.

        Args:
            
            parent: Objet parent de l'interface.
        """
        super(Interface, self).__init__(parent)
        self.analyse_instance = Analyse.Analyse(None, None, None, None, None)
        self.initUI()
        
        
        
        
    def afficher_popup(self, message):
        """
        Affiche un message dans une boîte de dialogue.

        Args:
            
            message (str): Message a afficher.

        """
        popup = QMessageBox()
        popup.setWindowTitle("Message")
        popup.setText(message)
        popup.exec_()  
         

    def initUI(self):
        """
        Initialise l'interface utilisateur avec les elements necessaires.
        
        """
        layout = QVBoxLayout()

        grid_layout = QGridLayout()

        self.amers_button = QPushButton('Selectionner le fichier des amers', self)
        self.sites_button = QPushButton('Selectionner le fichier des sites', self)
        self.carnets_button = QPushButton('Selectionner le fichier des carnets', self)
        self.parametres_button = QPushButton('Selectionner le fichier des parametres de voxellisation', self)
        self.ordres_button = QPushButton('Selectionner le fichier d ordres', self)
        self.generate_params_button = QPushButton('Generer automatiquement un fichier de parametres \nde voxellisation a partir du fichier des amers', self)
        self.process_button = QPushButton('Lancer le traitement', self)
        
        
        self.progress_label = QLabel(self)
        
        
        # Regler la taille des boutons
        button_width = 550
        button_height = 100
        self.amers_button.setFixedSize(button_width, button_height)
        self.sites_button.setFixedSize(button_width, button_height)
        self.carnets_button.setFixedSize(button_width, button_height)
        self.parametres_button.setFixedSize(button_width, button_height)
        self.ordres_button.setFixedSize(button_width, button_height)
        self.process_button.setFixedSize(button_width, button_height)

        self.amers_button.clicked.connect(lambda: self.showDialog('le fichier des amers'))
        self.sites_button.clicked.connect(lambda: self.showDialog('le fichier des sites'))
        self.carnets_button.clicked.connect(lambda: self.showDialog('le fichier des carnets'))
        self.parametres_button.clicked.connect(lambda: self.showDialog('le fichier des parametres de voxellisation'))
        self.ordres_button.clicked.connect(lambda: self.showDialog('le fichier des ordres'))
        self.process_button.clicked.connect(self.processData)
        
        # New button for generating voxelization parameters
        
        self.generate_params_button.setFixedSize(button_width, button_height)
        self.generate_params_button.clicked.connect(self.generateVoxelizationParameters)
        
        
        # Creer un bouton pour afficher les apercus
        self.preview_button = QPushButton('Afficher les apercus', self)
        self.preview_button.setFixedSize(button_width, button_height)
        self.preview_button.clicked.connect(self.showPreviews)
        self.preview_button.hide()  # Cacher le bouton initialement
        
        
        self.progress = QProgressBar(self)
        self.progress.setMaximum(100)
        


        description_amers = QLabel("Format du fichier des amers : Chaque ligne : Identifiant X Y Z", self)
        description_sites = QLabel("Format du fichier des sites : Chaque ligne : IdentifiantSite IdentifiantAmer1 IdentifiantAmer2", self)
        description_carnets = QLabel("Format du fichier des carnets : Chaque ligne : IdentifiantCarnet IdentifiantSite1 IdentifiantSite2 ...", self)
        description_ordres = QLabel("Format du fichier de l’expression de l’ordre des sites dans les carnets : Chaque ligne : IdentifiantCarnet Ordre ('croissant' ou 'decroissant')", self)
        description_parametres = QLabel("Format du fichier des parametres de voxellisation : Une ligne : xmin ymin zmin resolution nbex nbey nbez", self)

        # Style personnalise
        self.setStyleSheet("""
            QPushButton {
                background-color: #FF5252;
                color: white;
                border: none;
                padding: 10px 20px;
                text-align: center;
                text-decoration: none;
                display: inline-block;
                font-size: 20px;
                cursor: pointer;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #FF7575;
            }
            QPushButton#process_button {
                background-color: #3498DB;
            }
            QLabel {
                font-size: 20px;
                margin-bottom: 10px;
            }
            QProgressBar {
                text-align: center;
            }
        """)
        
        
        # Appliquer le style aux boutons de generation des parametres de voxellisation et de lancement de l'analyse
        self.generate_params_button.setStyleSheet("""
            QPushButton {
                background-color: #0077A8;
                color: white;
                border: none;
                padding: 10px 20px;
                text-align: center;
                text-decoration: none;
                display: inline-block;
                font-size: 20px;
                cursor: pointer;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #0096C7;
            }
        """)
        
        self.process_button.setStyleSheet("""
            QPushButton {
                background-color: #0077A8;
                color: white;
                border: none;
                padding: 10px 20px;
                text-align: center;
                text-decoration: none;
                display: inline-block;
                font-size: 20px;
                cursor: pointer;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #0096C7;
            }
        """)
        
        self.preview_button.setStyleSheet("""
            QPushButton {
                background-color: #0077A8;
                color: white;
                border: none;
                padding: 10px 20px;
                text-align: center;
                text-decoration: none;
                display: inline-block;
                font-size: 20px;
                cursor: pointer;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #0096C7;
            }
        """)
        
        # Utilisation d'une police differente pour les descriptions
        font = self.font()
        font.setPointSize(12)
        description_amers.setFont(font)
        description_sites.setFont(font)
        description_carnets.setFont(font)
        description_ordres.setFont(font)
        description_parametres.setFont(font)
        
        # Creer des layouts horizontaux pour chaque paire bouton-etiquette
        amers_layout = QHBoxLayout()
        sites_layout = QHBoxLayout()
        carnets_layout = QHBoxLayout()
        param_layout = QHBoxLayout()
        ordres_layout = QHBoxLayout()
        traitement_layout = QHBoxLayout()
        progress_layout = QHBoxLayout()
        



        # Ajouter les boutons a chaque layout horizontal
        amers_layout.addWidget(self.amers_button)
        amers_layout.addStretch()
        
        sites_layout.addWidget(self.sites_button)
       
        carnets_layout.addWidget(self.carnets_button)
     
        param_layout.addWidget(self.parametres_button)
      
        ordres_layout.addWidget(self.ordres_button)
      
        traitement_layout.addWidget(self.process_button)
        
       
    
        
        progress_layout.addWidget(self.progress)
        progress_layout.addWidget(self.progress_label)
        
       
        
        

        grid_layout.addWidget(description_amers, 0, 0, 1, 2, alignment=Qt.AlignCenter)
        grid_layout.addWidget(self.amers_button, 1, 0, 1, 2, alignment=Qt.AlignCenter)
        grid_layout.addWidget(description_sites, 2, 0, 1, 2, alignment=Qt.AlignCenter)
        grid_layout.addWidget(self.sites_button, 3, 0, 1, 2, alignment=Qt.AlignCenter)
        grid_layout.addWidget(description_carnets, 4, 0, 1, 2, alignment=Qt.AlignCenter)
        grid_layout.addWidget(self.carnets_button, 5, 0, 1, 2, alignment=Qt.AlignCenter)
        grid_layout.addWidget(description_parametres, 6, 0, 1, 2, alignment=Qt.AlignCenter)
        grid_layout.addWidget(self.parametres_button, 7, 0, 1, 1, alignment=Qt.AlignCenter)
        grid_layout.addWidget(self.generate_params_button, 7, 1, 1, 1, alignment=Qt.AlignCenter)
        grid_layout.addWidget(description_ordres, 8, 0, 1, 2, alignment=Qt.AlignCenter)
        grid_layout.addWidget(self.ordres_button, 9, 0, 1, 2, alignment=Qt.AlignCenter)
        grid_layout.addWidget(self.process_button, 10, 0, 1, 2, alignment=Qt.AlignCenter)
        grid_layout.addWidget(self.progress, 11, 0, 1, 2)
        grid_layout.addWidget(self.preview_button, 12, 0, 1, 2, alignment=Qt.AlignCenter)# Ajouter les layouts horizontaux au layout principal
        
        grid_layout.addLayout(amers_layout, 1, 0, 1, 2, alignment=Qt.AlignCenter)
        grid_layout.addLayout(sites_layout, 3, 0, 1, 2, alignment=Qt.AlignCenter)
        grid_layout.addLayout(carnets_layout, 5, 0, 1, 2, alignment=Qt.AlignCenter)
        grid_layout.addLayout(param_layout, 7, 0, 1, 2, alignment=Qt.AlignCenter)
        grid_layout.addLayout(ordres_layout, 9, 0, 1, 2, alignment=Qt.AlignCenter)
        grid_layout.addWidget(self.process_button, 11, 0, 1, 2, alignment=Qt.AlignCenter)
        grid_layout.addWidget(self.progress, 12, 0, 1, 2, alignment=Qt.AlignCenter)
        layout.addLayout(grid_layout)
        layout.addLayout(amers_layout)
        layout.addLayout(sites_layout)
        layout.addLayout(carnets_layout)
        layout.addLayout(param_layout)
        layout.addLayout(ordres_layout)
        layout.addLayout(traitement_layout)
        layout.addLayout(progress_layout)
        
        self.setLayout(layout)
    
    
    def generateVoxelizationParameters(self):
        """
        Genere automatiquement un fichier de parametres de voxellisation.

        """
        # Fenetre pour choisir la resolution
        resolution, ok = QInputDialog.getDouble(self, 'Resolution', 'Entrez la resolution:', 0.1, 0.01, 10, 2)
        
        if not ok:
            self.afficher_popup("Operation annulee.")
            return
    
        # Fenetre pour choisir le fichier des amers 
        amers_path, _ = QFileDialog.getOpenFileName(self, 'Selectionner le fichier des amers', '', 'Text files (*.txt);;All files (*)')
    
        if not amers_path:
            self.afficher_popup("Selection du fichier des amers annulee.")
            return
    
        # Fenetre pour choisir le chemin du fichier des amers
        output_directory = QFileDialog.getExistingDirectory(self, 'Selectionner le dossier de sortie', '')
    
        if not output_directory:
            self.afficher_popup("Selection du dossier de sortie annulee.")
            return
    
        # Creation du fichier des parametres de voxellisation
        generator = GenParamVoxel.VoxelizationParametersGenerator(amers_path, output_directory+"/parametres_voxellisation.txt", resolution)
        generator.generate_voxelization_parameters()
    
        self.afficher_popup(f"Le fichier de parametres de voxelisation 'parametres_voxellisation.txt' a ete genere avec succes avec la resolution {resolution}.")
            
            
    

    def showDialog(self, filename):
        """
        Affiche une boîte de dialogue pour selectionner un fichier.

        Args:
            filename (str): Nom du fichier a selectionner.

        """
        fname = QFileDialog.getOpenFileName(self, f'Selectionner {filename}', '', 'Text files (*.txt);;All files (*)')[0]
        self.verif_format(fname,filename)
            
        
    
    
    def verif_format(self, fname,filename):
        """
        Verifie la validite du format du contenu d'un fichier selon le type de fichier.
        
        Args:
            fname (str): Chemin du fichier.
            filename (str): Nom du type de fichier.

        """
        
        # Pour le fichier des carnets
        if filename=='le fichier des carnets':
            setattr(self.analyse_instance,'carnets_path', fname)
            # Verifier si un fichier a ete selectionne
            if fname:
                try:
                    # Ouvrir et lire le contenu du fichier
                    with open(fname, 'r') as file:
                        lines = file.readlines()
                        
                        # Verifier le format du contenu
                        if self.checkContent(lines,filename):
                            setattr(self.analyse_instance, 'carnets_path', fname)
                            self.carnets_button.setStyleSheet("background-color: #008000;")
                            self.carnets_button.setText(f"Fichier {filename[11:]} fourni")
                        else:
                            # Afficher un message d'erreur si le contenu n'est pas valide
                            QMessageBox.warning(self, 'Contenu incorrect', f'Le contenu du fichier {filename[11:]} n\'est pas valide')
                            
                except Exception as e:
                    # Afficher un message d'erreur en cas d'erreur lors de la lecture du fichier
                    QMessageBox.warning(self, 'Erreur de lecture', f'Erreur lors de la lecture du fichier {filename[11:]}: {str(e)}')
                    
                    
                    
        # Pour le fichier des amers        
        if filename=='le fichier des amers':
            
            # Verifier si un fichier a ete selectionne
            if fname:
                try:
                    # Ouvrir et lire le contenu du fichier
                    with open(fname, 'r') as file:
                        lines = file.readlines()
                        
                        # Verifier le format du contenu
                        if self.checkContent(lines,filename):
                            setattr(self.analyse_instance, 'amers_path', fname)
                            self.amers_button.setStyleSheet("background-color: #008000;")
                            self.amers_button.setText(f"Fichier {filename[11:]} fourni")
                        else:
                            # Afficher un message d'erreur si le contenu n'est pas valide
                            QMessageBox.warning(self, 'Contenu incorrect', f'Le contenu du fichier {filename[11:]} n\'est pas valide')
                            
                except Exception as e:
                    # Afficher un message d'erreur en cas d'erreur lors de la lecture du fichier
                    QMessageBox.warning(self, 'Erreur de lecture', f'Erreur lors de la lecture du fichier {filename[11:]}: {str(e)}')
                  
                    
                  
        # Pour le fichier des sites
        if filename=='le fichier des sites':
            
            # Verifier si un fichier a ete selectionne
            if fname:
                try:
                    # Ouvrir et lire le contenu du fichier
                    with open(fname, 'r') as file:
                        lines = file.readlines()
                        
                        # Verifier le format du contenu
                        if self.checkContent(lines,filename):
                            setattr(self.analyse_instance, 'sites_path', fname)
                            self.sites_button.setStyleSheet("background-color: #008000;")
                            self.sites_button.setText(f"Fichier {filename[11:]} fourni")
                        else:
                            # Afficher un message d'erreur si le contenu n'est pas valide
                            QMessageBox.warning(self, 'Contenu incorrect', f'Le contenu du fichier {filename[11:]} n\'est pas valide')
                            
                except Exception as e:
                    # Afficher un message d'erreur en cas d'erreur lors de la lecture du fichier
                    QMessageBox.warning(self, 'Erreur de lecture', f'Erreur lors de la lecture du fichier {filename[11:]}: {str(e)}')
                    
        
        # Pour le fichier des ordres
        if filename=='le fichier des ordres':
            
            # Verifier si un fichier a ete selectionne
            if fname:
                try:
                    # Ouvrir et lire le contenu du fichier
                    with open(fname, 'r') as file:
                        lines = file.readlines()
                        
                        # Verifier le format du contenu
                        if self.checkContent(lines,filename):
                            setattr(self.analyse_instance, 'ordres_path', fname)
                            self.ordres_button.setStyleSheet("background-color: #008000;")
                            self.ordres_button.setText(f"Fichier {filename[11:]} fourni")
                        else:
                            # Afficher un message d'erreur si le contenu n'est pas valide
                            QMessageBox.warning(self, 'Contenu incorrect', f'Le contenu du fichier {filename[11:]} n\'est pas valide')
                            
                except Exception as e:
                    # Afficher un message d'erreur en cas d'erreur lors de la lecture du fichier
                    QMessageBox.warning(self, 'Erreur de lecture', f'Erreur lors de la lecture du fichier {filename[11:]}: {str(e)}')
        
        # Pour le fichier des parametres de voxellisation
        if filename=='le fichier des parametres de voxellisation':
            
            # Verifier si un fichier a ete selectionne
            if fname:
                try:
                    # Ouvrir et lire le contenu du fichier
                    with open(fname, 'r') as file:
                        lines = file.readlines()
                        
                        # Verifier le format du contenu
                        if self.checkContent(lines,filename):
                            setattr(self.analyse_instance, 'param_voxellisation_path', fname)
                            self.parametres_button.setStyleSheet("background-color: #008000;")
                            self.parametres_button.setText(f"Fichier {filename[11:]} fourni")
                        else:
                            # Afficher un message d'erreur si le contenu n'est pas valide
                            QMessageBox.warning(self, 'Contenu incorrect', f'Le contenu du fichier {filename[11:]} n\'est pas valide')
                            
                except Exception as e:
                    # Afficher un message d'erreur en cas d'erreur lors de la lecture du fichier
                    QMessageBox.warning(self, 'Erreur de lecture', f'Erreur lors de la lecture du fichier {filename[11:]}: {str(e)}')
                    
        
        
        
        
        
    def checkContent(self, lines,filename):
        """
        Verifie si le contenu du fichier est valide en fonction du type de fichier.

        Args:
            
            lines (list): Liste des lignes du fichier.
            
            filename (str): Nom du type de fichier.

        Returns:
            
            bool: True si le contenu est valide, False sinon.
        """
        if filename=='le fichier des amers':
            # Verifier le format du contenu pour le fichier des amers
            if lines and lines[0].strip() == "Identifiant X Y Z":
                # Verifier que chaque ligne suivante contient des nombres
                for line in lines[1:]:
                    parts = line.strip().split()
                    # Verifier si la ligne a le bon nombre de parties et que ce sont des nombres
                    if len(parts) == 4 and all(part.replace('.', '').replace('-', '').isdigit() for part in parts[1:]):
                        continue
                    else:
                        return False
                return True
            return False
        
        if filename=='le fichier des carnets':
            # Verifier le format du contenu pour le fichier des carnets
            if lines and lines[0].strip() == "IdentifiantCarnet IdentifiantSite1 IdentifiantSite2 ...":
                for line in lines[1:]:
                    parts = line.strip().split()
                    # Verifier si chaque partie de la ligne est un nombre
                    if all(part.replace('-', '').isdigit() for part in parts):
                        continue
                    else:
                        return False
                return True
            
        if filename=='le fichier des sites':
            # Verifier le format du contenu pour le fichier des sites
            if lines and lines[0].strip() == "IdentifiantSite IdentifiantAmer1 IdentifiantAmer2": 
                for line in lines[1:]:
                    parts = line.strip().split()
                    # Verifier si la ligne a le bon nombre de parties et que ce sont des nombres
                    if len(parts) == 3 and all(part.replace('.', '').replace('-', '').isdigit() for part in parts[1:]):
                        continue
                    else:
                        return False
                return True
            
        if filename=='le fichier des ordres':
            # Verifier le format du contenu pour le fichier des ordres
            if lines and lines[0].strip() == "IdentifiantCarnet Ordre": 
                for line in lines[1:]:
                    parts = line.strip().split()
                    # Verifier si la ligne a le bon nombre de parties et que ce sont des nombres
                    if len(parts) == 2 and parts[0].isdigit() and parts[1].lower() in ['croissant', 'decroissant']:
                        continue
                    else:
                        return False
                return True
            
        if filename=='le fichier des parametres de voxellisation':
            # Verifier le format du contenu pour le fichier des parametres de voxellisation
            if lines and lines[0].strip() == "xmin ymin zmin resolution nbex nbey nbez": 
                for line in lines[1:]:
                    parts = line.strip().split()
                    # Verifier si la ligne a le bon nombre de parties et que ce sont des nombres
                    if len(parts) == 7 and all(part.replace('.', '').replace('-', '').isdigit() for part in parts):
                        continue
                    else:
                        return False
                return True
      
        
      
    def showPreviews(self):
        """
        Affiche les apercus des resultats de l'analyse 3D.

        """
        self.analyse_instance.afficher_domaine_3d(self.points_ok, self.points_non_ok)
     
    def processData(self):
        """
        Traite les donnees apres avoir verifie que tous les fichiers necessaires sont selectionnes.

        """
        # Verifiez si tous les attributs de l'instance de Analyse sont definis
        if all(getattr(self.analyse_instance, attr) is not None for attr in ['amers_path', 'sites_path', 'carnets_path', 'param_voxellisation_path', 'ordres_path']):
            # Desactivez le bouton de traitement pendant l'analyse
            self.sender().setEnabled(False)

            # Reactivez le bouton apres l'analyse
            self.sender().setEnabled(True)
            
            # Lancement de l'analyse
            self.points_ok, self.points_non_ok = self.analyse_instance.analyse(self.progress,self.progress_label)
            
            # Une fois l'analyse terminee, rendre le bouton visible
            self.preview_button.show()
                        

        else:
            self.afficher_popup("Veuillez selectionner tous les fichiers necessaires avant de lancer le traitement.")
           