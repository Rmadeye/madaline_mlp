import numpy as np
import os

from PIL import Image

class DataLoader:
    def __init__(self, data_dir: str, width: int = 16, height: int = 16):
        self.data_dir = data_dir
        assert os.path.exists(data_dir), f"{data_dir} does not exist"

    def read_description(self):
        description_file = f"{self.data_dir}/description.txt"
        pngdict = {}
        noise_levels = {}
        with open(description_file, 'r') as f:
            for line in f:
                if len(line) == 0:
                    continue
                elif line[0] == ",":
                    data =  line.split(",")[-2]
                else:
                    data =  line.split(",")[0]
                try:
                    png, description = data.split(":")
                except ValueError:
                    breakpoint()
                pngdict[png] = description
                noise_data = line.split(":")[-1].split(",")
                # breakpoint()
                noise_level = noise_data[-1].split("%")[0].split("=")[-1]
                noise_levels[noise_data[0]] = int(noise_level)
        return pngdict, noise_levels 
    
    def convert_to_vector(self, pngdict: dict) -> dict:
        numpy_dict = {v:k for k,v in pngdict.items()}
        numpy_dict = {k: np.array(Image.open(v)) for k,v in numpy_dict.items()}
        vector_dict = {k: v.flatten() for k,v in numpy_dict.items()}
        vector_dict = {k: v/255 for k,v in vector_dict.items()}
        normalized_vector_dict = {k: np.array([
            v/sum([x for x in v])**0.5]) for k,v in vector_dict.items()}
        return normalized_vector_dict

    def load_data(self):
        pngdict, noise_levels = self.read_description()
        vector_dict = self.convert_to_vector(pngdict)
        # vectorized_dict = self.vectorize(vector_dict)
        return vector_dict, noise_levels


if __name__ == "__main__":
    data_loader = DataLoader("data/testing")
    a = data_loader.load_data()
    print(a[0]['letter a'].shape)

