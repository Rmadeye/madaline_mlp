import os
import sys

import numpy as np
import PIL

sys.path.append("..")
import pytest
from font_generator import FontImageGenerator

INPUTFONT = "data/times-ro.ttf"


@pytest.fixture
def output_dir(tmpdir):
    return str(tmpdir.mkdir("output"))


def test_generate_font_image(output_dir):
    generator = FontImageGenerator(
        width=100,
        height=100,
        font_file=INPUTFONT,
        letter="A",
        output_dir=output_dir,
        overwrite=True,
    )
    result = generator.generate_font_image()
    assert isinstance(result, PIL.Image.Image)
    assert os.path.isfile(os.path.join(output_dir, "A.png"))
    assert os.path.isfile(os.path.join(output_dir, "description.txt"))


def test_invalid_width_height():
    with pytest.raises(AssertionError):
        FontImageGenerator(
            width=0, height=100, font_file=INPUTFONT, letter="A", output_dir="output"
        )


def test_noise_levels():
    generator = FontImageGenerator(
        width=100,
        height=100,
        font_file=INPUTFONT,
        letter="A",
        output_dir="output",
        noise_level=50,
    )
    clean_image = generator.generate_font_image()
    noisy_image = FontImageGenerator.add_noise(image=clean_image, noise_level=50)

    assert isinstance(noisy_image, PIL.Image.Image)

    clean_image = np.array(clean_image)
    noisy_image = np.array(noisy_image)

    assert clean_image.shape == noisy_image.shape
    assert clean_image.dtype == noisy_image.dtype
    assert not np.array_equal(noisy_image, clean_image), "Arrays are equal"
