import numpy as np
import os

import PIL

class DataLoader:
    def __init__(self, data_dir: str):
        self.data_dir = data_dir
        assert os.path.exists(data_dir), f"{data_dir} does not exist"

    def load_data(self):
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
                noise_data = line.split("noise_level=")
                noise_level = noise_data[1].split("%")[0]
                noise_levels[png] = int(noise_level)
        print(pngdict,  noise_levels)
        return pngdict, noise_levels 

if __name__ == "__main__":
    data_loader = DataLoader("data/testing")
    data_loader.load_data()  
