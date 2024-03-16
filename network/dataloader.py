import numpy as np
import os

from PIL import Image


class DataLoader:
    """
    A class for loading and processing data.

    Args:
        data_dir (str): The directory path where the data is located.

    Attributes:
        data_dir (str): The directory path where the data is located.

    Methods:
        read_description: Reads the description file and returns a dictionary of PNG files and their descriptions.
        convert_to_vector: Converts the PNG files to vectors and returns a dictionary of vectorized PNG files.
        load_data: Loads the data by calling the read_description and convert_to_vector methods.

    """

    def __init__(self, data_dir: str):
        self.data_dir = data_dir
        assert os.path.exists(data_dir), f"{data_dir} does not exist"

    def read_description(self):
        """
        Reads the description file and returns a dictionary of PNG files and their descriptions.

        Returns:
            tuple: A tuple containing two dictionaries - pngdict and noise_levels.
                - pngdict (dict): A dictionary where the keys are PNG filenames and the values are their descriptions.
                - noise_levels (dict): A dictionary where the keys are noise data filenames and the values are the noise levels.

        """
        description_file = f"{self.data_dir}/description.txt"
        pngdict = {}
        noise_levels = {}
        with open(description_file, "r") as f:
            for line in f:
                if len(line) == 0:
                    continue
                data = line.split(",")[0]
                try:
                    png, description = data.split(":")
                except ValueError:
                    breakpoint()
                pngdict[png] = description
                noise_data = line.split(":")[-1].split(",")
                noise_level = noise_data[-1].split("%")[0].split("=")[-1]
                noise_levels[noise_data[0]] = int(noise_level)
        return pngdict, noise_levels

    def convert_to_vector(self, pngdict: dict) -> dict:
        """
        Converts the PNG files to vectors and returns a dictionary of vectorized PNG files.

        Args:
            pngdict (dict): A dictionary where the keys are PNG filenames and the values are their descriptions.

        Returns:
            dict: A dictionary where the keys are PNG filenames and the values are their vectorized representations.

        """
        numpy_dict = {v: k for k, v in pngdict.items()}
        numpy_dict = {k: np.array(Image.open(v)) for k, v in numpy_dict.items()}
        vector_dict = {k: v.flatten() for k, v in numpy_dict.items()}
        vector_dict = {k: v / 255 for k, v in vector_dict.items()}
        normalized_vector_dict = {
            k: np.array([v / sum([x for x in v]) ** 0.5])
            for k, v in vector_dict.items()
        }
        return normalized_vector_dict

    def load_data(self):
        """
        Loads the data by calling the read_description and convert_to_vector methods.

        Returns:
            tuple: A tuple containing two dictionaries - vector_dict and noise_levels.
                - vector_dict (dict): A dictionary where the keys are PNG filenames and the values are their vectorized representations.
                - noise_levels (dict): A dictionary where the keys are noise data filenames and the values are the noise levels.

        """
        pngdict, noise_levels = self.read_description()
        vector_dict = self.convert_to_vector(pngdict)
        return vector_dict, noise_levels


if __name__ == "__main__":
    data_loader = DataLoader("data/testing")
    a = data_loader.load_data()
    print(a[0]["letter a"].shape)
