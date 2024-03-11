import argparse
import os
import string

import numpy as np
import PIL
from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw

def save_description(output_path: str, letter: str, noise_level: int):
    # if letter  can be a number, change letter name to number
    if letter.isdigit():
        label = f"number {letter}"
    else:
        label = f"letter {letter}" 
    return f"{output_path}:{label}, noise_level={noise_level}%\n"

def add_noise(image: PIL.Image, noise_level: int):
    im_as_array = np.array(image)
    noise = np.zeros(im_as_array.shape, dtype=np.uint8)
    # fill noise_level % of the image with random noise
    noise_level = int(noise_level / 100 * im_as_array.size)
    for i in range(noise_level):
        x = np.random.randint(0, im_as_array.shape[0])
        y = np.random.randint(0, im_as_array.shape[1])
        noise[x, y] = np.random.randint(0, 255)

    return Image.fromarray(np.clip(im_as_array + noise, 0, 255))    


def generate_font_image(width: int, height: int, x_position: int,
                        y_position: int, font_file: str, letter: str,
                        noise_level: int =  0, 
                        output_dir: str = 'data/training_set', 
                        overwrite: bool = False,
                        all_letters: bool = False):
    assert width > 0 and height > 0, "Width and height must be greater than 0"
    assert x_position >= 0 and y_position >= 0, "x and y position must be greater than or equal to 0"   
    assert noise_level >= 0 and noise_level <= 100, "Noise level must be between 0 and 100"
    assert font_file is not None, "Font file must be provided"
    assert font_file.endswith('.ttf'), "Font file must be a .ttf file"
    os.makedirs(output_dir, exist_ok=True)
    # breakpoint()
    if all_letters:
        letters = string.ascii_uppercase + string.ascii_lowercase + string.digits
        
        for letter in letters:
            font  = ImageFont.truetype(font_file, 40)
            image = Image.new("L", (width, height), color=255)
            draw = ImageDraw.Draw(image)
            draw.textsize(letter, font=font)
            draw.text((x_position, y_position), letter, font=font, fill=0)

            if noise_level > 0: 
                image = add_noise(image, noise_level)
            output_path = f'{output_dir}/{letter}.png'
            if f"{letter}.png" in os.listdir(output_dir) and not overwrite:
                print(f"{letter} already exists in the output directory")
                continue

            else:
                image.save(output_path)
                print(f"Saved {letter}.png to {output_dir}")

            description = save_description(output_path, letter, noise_level)
            with open(f'{output_dir}/description.txt', 'a') as f:
                f.write(description)
        return "All letters generated successfully"
    else:
        assert letter.isalpha() or letter.isdigit(), "Letter must be a letter or a number"
        font  = ImageFont.truetype(font_file, 40)
        image = Image.new("L", (width, height), color=255)
        draw = ImageDraw.Draw(image)
        draw.textsize(letter, font=font)
        draw.text((x_position, y_position), letter, font=font, fill=0)

        if noise_level > 0: 
            image = add_noise(image, noise_level)
        output_path = f'{output_dir}/{letter}.png'
        if f"{letter}.png" in os.listdir(output_dir) and not overwrite:
            print(f"{letter} already exists in the output directory")

        else:
            image.save(output_path)
            print(f"Saved {letter}.png to {output_dir}")

        description = save_description(output_path, letter, noise_level)
        with open(f'{output_dir}/description.txt', 'a') as f:
            f.write(description)

    return f"Letter '{letter}' generated successfully"

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
    args = parser.parse_args()
    generate_font_image(args.width, args.height, args.x_position, args.y_position, args.font_file, args.letter, args.noise_level, args.output_dir, args.overwrite, args.all_letters)