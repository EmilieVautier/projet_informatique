import numpy as np

class VoxelizationParametersGenerator:
    """
    Initialise le generateur de parametres de voxellisation.

    Args:
        
        file_path (str): Chemin du fichier d'amers.
        
        output_file_path (str): Chemin du fichier de sortie des parametres de voxellisation.
        
        resolution (float): Resolution pour la voxellisation.

    """
    def __init__(self, file_path, output_file_path, resolution):
        self.file_path = file_path
        self.output_file_path = output_file_path
        self.coordinates = None
        self.resolution = resolution
        self.num_voxels = None

    def calculate_num_voxels(self):
        """
        Calcule le nombre de voxels necessaires en fonction des coordonnees des amers.

        """
        with open(self.file_path, 'r') as file:
            lines = file.readlines()[1:]  # Ignore the first line

        self.coordinates = [(float(line.split()[1]), float(line.split()[2]), float(line.split()[3])) for line in lines]

        size_x = max(x for x, y, z in self.coordinates) - min(x for x, y, z in self.coordinates)
        size_y = max(y for x, y, z in self.coordinates) - min(y for x, y, z in self.coordinates)
        size_z = max(z for x, y, z in self.coordinates) - min(z for x, y, z in self.coordinates)

        self.num_voxels = (
            int(np.ceil(size_x / self.resolution)),
            int(np.ceil(size_y / self.resolution)),
            int(np.ceil(size_z / self.resolution))
        )

    def generate_voxelization_parameters(self):
        """
        Genere les parametres de voxellisation et ecrit dans le fichier de sortie.

        """
        self.calculate_num_voxels()

        xmin = min(x for x, y, z in self.coordinates)
        ymin = min(y for x, y, z in self.coordinates)
        zmin = min(z for x, y, z in self.coordinates)

        with open(self.output_file_path, 'w') as output_file:
            output_file.write(f"xmin ymin zmin resolution nbex nbey nbez\n")
            output_file.write(f"{xmin} {ymin} {zmin} {self.resolution} {self.num_voxels[0]} {self.num_voxels[1]} {self.num_voxels[2]}\n")
