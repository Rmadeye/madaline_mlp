import os
import sys

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
    assert result == "A generated successfully"
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
        noise_levels=[0, 50],
    )
    clean_image = generator.generate_font_image()
    noisy_image = generator.generate_font_image()


# Add more test cases as needed
