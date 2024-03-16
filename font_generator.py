import argparse
import os
import string
import numpy as np
import PIL
from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw


class FontImageGenerator:

    def __init__(
        self,
        width: int,
        height: int,
        font_file: str,
        letter: str,
        output_dir: str,
        x_position: int = 0,
        y_position: int = 0,
        noise_level: int = 0,
        overwrite: bool = False,
        all_letters: bool = False,
        font_size: int = 40,
    ):
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
        self.font_size = font_size
        self.font = ImageFont.truetype(self.font_file, size=self.font_size)

        if len(self.letter) > 1:
            print(f"Generating letters from {self.letter}")
            self.letters = [x for x in self.letter]
        else:
            self.letters = None

        if self.overwrite:
            print("Overwriting existing files")
            if os.path.exists(f"{self.output_dir}/description.txt"):
                os.unlink(f"{self.output_dir}/description.txt")

        assert (
            self.width > 0 and self.height > 0
        ), "Width and height must be greater than 0"
        if not self.all_letters and not self.letter:
            raise ValueError("Letter must be provided")
        assert (
            self.x_position >= 0 and self.y_position >= 0
        ), "x and y position must be greater than or equal to 0"
        if x_position == 0 and y_position == 0:
            print("x and y position not provided, pseudo autocentering applied")
        assert (
            self.noise_level >= 0 and self.noise_level <= 100
        ), "Noise level must be between 0 and 100"
        assert self.font_file is not None, "Font file must be provided"
        assert self.font_file.endswith(".ttf"), "Font file must be a .ttf file"

    def save_description(self, letter: str, output_path: str) -> str:
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

    def centerize_letter(self, image: Image) -> Image:
        """
        Centerizes the given letter image within a new image of specified width and height.

        Args:
            image (Image): The letter image to be centerized.

        Returns:
            Image: The centerized letter image.

        """
        # pseudo-centerize the letter
        arr = np.array(image)
        let_matrix = np.where(arr != 255)
        let_width = let_matrix[1].max() - let_matrix[1].min()
        x_center = (self.width - let_width) // 2
        y_center = self.height // 2
        new_image = Image.new("L", (self.width, self.height), color=255)
        draw = ImageDraw.Draw(new_image)
        draw.text((x_center, y_center), self.letter, font=self.font, fill=0)
        draw.textbbox((x_center, y_center), self.letter, font=self.font)

        return new_image

    def generate_font_image(self) -> str:
        """
        Generates font images based on the specified parameters.

        Returns:
            str: A message indicating the success of the generation process.
        """
        os.makedirs(self.output_dir, exist_ok=True)

        if self.all_letters or isinstance(self.letters, list):
            if self.all_letters:
                letters = (
                    string.ascii_uppercase + string.ascii_lowercase + string.digits
                )
            else:
                letters = self.letters

            for letter in letters:
                self.letter = letter
                image = Image.new("L", (self.width, self.height), color=255)
                draw = ImageDraw.Draw(image)
                if self.x_position == 0 and self.y_position == 0:
                    self.x_position = 0
                    self.y_position = self.height // 2
                    draw.textbbox(
                        (self.x_position, self.y_position), letter, font=self.font
                    )
                    draw.text(
                        (self.x_position, self.y_position),
                        letter,
                        font=self.font,
                        fill=0,
                    )
                    image = self.centerize_letter(image)
                    self.y_position = 0
                else:
                    draw.textbbox(
                        (self.x_position, self.y_position), letter, font=self.font
                    )
                    draw.text(
                        (self.x_position, self.y_position),
                        letter,
                        font=self.font,
                        fill=0,
                    )

                if self.noise_level > 0:
                    image = self.add_noise(image)
                output_path = os.path.join(self.output_dir, f"{self.letter}.png")
                if (
                    f"{self.letter}.png" in os.listdir(self.output_dir)
                    and not self.overwrite
                ):
                    print(f"{self.letter} already exists in the output directory")
                    continue

                else:
                    image.save(output_path)
                    print(f"Saved {letter}.png to {self.output_dir}")

                description = self.save_description(self.letter, output_path)
                with open(f"{self.output_dir}/description.txt", "a") as f:
                    f.write(description)
            return "All letters generated successfully"
        else:
            assert (
                self.letter.isalpha() or self.letter.isdigit()
            ), "Letter must be a letter or a number"
            image = Image.new("L", (self.width, self.height), color=255)
            draw = ImageDraw.Draw(image)
            if self.x_position == 0 and self.y_position == 0:
                self.x_position = self.width // 2
                self.y_position = self.height // 2
                draw.textbbox(
                    (self.x_position, self.y_position), self.letter, font=self.font
                )
                draw.text(
                    (self.x_position, self.y_position),
                    self.letter,
                    font=self.font,
                    fill=0,
                )
                image = self.centerize_letter(image)
            else:
                draw.text(
                    (self.x_position, self.y_position),
                    self.letter,
                    font=self.font,
                    fill=0,
                )
                draw.textbbox(
                    (self.x_position, self.y_position), self.letter, font=self.font
                )
        if self.noise_level > 0:
            image = self.add_noise(image, self.noise_level)
        output_path = os.path.join(self.output_dir, f"{self.letter}.png")
        if f"{self.letter}.png" in os.listdir(self.output_dir) and not self.overwrite:
            print(f"{letter} already exists in the output directory")

        else:
            image.save(output_path)
            print(f"Saved {self.letter}.png to {self.output_dir}")

        description = self.save_description(self.letter, output_path)
        with open(f"{self.output_dir}/description.txt", "a") as f:
            f.write(description)
        return f"{self.letter} generated successfully"


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate a font image")
    parser.add_argument("--width", type=int, help="Width of the image", required=True)
    parser.add_argument("--height", type=int, help="Height of the image", required=True)
    parser.add_argument(
        "--x_position", type=int, help="X position of the letter", default=0
    )
    parser.add_argument(
        "--y_position", type=int, help="Y position of the letter", default=0
    )
    parser.add_argument(
        "--font_file", type=str, help="Font file", default="times-ro.ttf"
    )
    parser.add_argument(
        "--letter",
        type=str,
        help="Letter or letters to generate. List in form of ABCDEFG...",
        required=False,
        default="A",
    )
    parser.add_argument("--noise_level", type=int, help="Noise level", default=0)
    parser.add_argument(
        "--output_dir", type=str, help="Output directory", default="data/training_set"
    )
    parser.add_argument(
        "--overwrite", action="store_true", help="Overwrite existing files"
    )
    parser.add_argument(
        "--all_letters", action="store_true", help="Generate all letters"
    )
    parser.add_argument("--font_size", type=int, help="Font size", default=40)
    args = vars(parser.parse_args())
    generator = FontImageGenerator(**args)
    generator.generate_font_image()
