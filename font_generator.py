import argparse
import os
import string

import numpy as np
import PIL
from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw

class FontImageGenerator:

    def __init__(self, width: int, height: int, x_position: int, y_position: int, 
                 font_file: str, letter: str, noise_level: int = 0, 
                 output_dir: str = 'data/training_set', overwrite: bool = False, 
                 all_letters: bool = False):
        self.width = width
        self.height = height
        self.x_position = x_position
        self.y_position = y_position
        self.font_file = font_file
        self.letter = letter
        self.noise_level = noise_level
        self.output_dir = output_dir
        self.overwrite = overwrite
        self.all_letters = all_letters

        assert self.width > 0 and self.height > 0, "Width and height must be greater than 0"
        assert self.x_position >= 0 and self.y_position >= 0, "x and y position must be greater than or equal to 0"
        assert self.noise_level >= 0 and self.noise_level <= 100, "Noise level must be between 0 and 100"
        assert self.font_file is not None, "Font file must be provided"
        assert self.font_file.endswith('.ttf'), "Font file must be a .ttf file"

    def save_description(self, letter: str, output_path)-> str:
        """
        Saves the description of a letter or number with the specified noise level.

        Args:
            output_path (str): The path where the description will be saved.
            letter (str): The letter or number to be described.
            noise_level (int): The level of noise to be applied to the description.

        Returns:
            str: The formatted description with the output path, label, and noise level.
        """
        if self.letter.isdigit():
            label = f"number {letter}"
        else:
            label = f"letter {letter}" 

        return f"{output_path}:{label}, noise_level={self.noise_level}%\n"
    
    def add_noise(self, image: PIL.Image) -> PIL.Image:
        """
        Adds random noise to the given image.

        Args:
            image (PIL.Image): The input image.
            noise_level (int): The percentage of the image to be filled with random noise.

        Returns:
            PIL.Image: The image with added noise.
        """
        im_as_array = np.array(image)
        noise = np.zeros(im_as_array.shape, dtype=np.uint8)
        # fill noise_level % of the image with random noise
        noise_level = int(self.noise_level / 100 * im_as_array.size)
        for i in range(noise_level):
            x = np.random.randint(0, im_as_array.shape[0])
            y = np.random.randint(0, im_as_array.shape[1])
            noise[x, y] = np.random.randint(0, 255)

        return Image.fromarray(np.clip(im_as_array + noise, 0, 255))
    
    def generate_font_image(self) -> str:

        os.makedirs(self.output_dir, exist_ok=True)
        if self.all_letters:
            letters = string.ascii_uppercase + string.ascii_lowercase + string.digits
            
            for letter in letters:
                font  = ImageFont.truetype(self.font_file, 40)
                image = Image.new("L", (self.width, self.height), color=255)
                draw = ImageDraw.Draw(image)

                draw.textbbox((self.x_position, self.y_position), letter, font=font)
                draw.text((self.x_position, self.y_position), letter, font=font, fill=0)

                if self.noise_level > 0: 
                    image = self.add_noise(image)
                output_path = f'{self.output_dir}/{letter}.png'
                if f"{letter}.png" in os.listdir(self.output_dir) and not self.overwrite:
                    print(f"{letter} already exists in the output directory")
                    continue

                else:
                    image.save(output_path)
                    print(f"Saved {letter}.png to {self.output_dir}")

                description = self.save_description(output_path, letter)
                with open(f'{self.output_dir}/description.txt', 'a') as f:
                    f.write(description)
            return "All letters generated successfully"
        else:
            assert self.letter.isalpha() or self.letter.isdigit(), "Letter must be a letter or a number"
            font  = ImageFont.truetype(self.font_file, 40)
            image = Image.new("L", (self.width, self.height), color=255)
            draw = ImageDraw.Draw(image)
            draw.textbbox((self.x_position, self.y_position), letter, font=font)
            draw.text((self.x_position, self.y_position), letter, font=font, fill=0)

        if self.noise_level > 0: 
            image = self.add_noise(image, self.noise_level)
        output_path = f'{self.output_dir}/{self.letter}.png'
        if f"{letter}.png" in os.listdir(self.output_dir) and not self.overwrite:
            print(f"{letter} already exists in the output directory")

        else:
            image.save(output_path)
            print(f"Saved {letter}.png to {self.output_dir}")

        description = self.save_description(output_path, self.letter)
        with open(f'{self.output_dir}/description.txt', 'a') as f:
            f.write(description)
        return f"{self.letter} generated successfully"

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate a font image")
    parser.add_argument("--width", type=int, help="Width of the image", required=True)
    parser.add_argument("--height", type=int, help="Height of the image", required=True)
    parser.add_argument("--x_position", type=int, help="X position of the letter", required=True)
    parser.add_argument("--y_position", type=int, help="Y position of the letter", required=True)
    parser.add_argument("--font_file", type=str, help="Font file", default='times-ro.ttf')   
    parser.add_argument("--letter", type=str, help="Letter to generate", required=False, default='A')
    parser.add_argument("--noise_level", type=int, help="Noise level", default=0)   
    parser.add_argument("--output_dir", type=str, help="Output directory", default='data/training_set')
    parser.add_argument("--overwrite", action="store_true", help="Overwrite existing files")
    parser.add_argument("--all_letters", action="store_true", help="Generate all letters")
    args = vars(parser.parse_args())
    generator = FontImageGenerator(**args)
    generator.generate_font_image()