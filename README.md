### Simple MADALINE network for identification of letters and digits based on ttf file.

This is a simple implementation of a MADALINE network for identification of letters and digits based on a ttf file. The network is trained using the backpropagation algorithm. The network is implemented in Python using the numpy library for matrix operations.

### Usage

1. Create `conda`environment using `environment.yml` file:
   `conda env create -f environment.yml`
2. Activate the environment:
   `conda activate madaline`
3. Generate the training and test data using `ttf` file. Example:
   `python3 font_generator.py --width 32 --height 32 --x_position 16 --y_position 16 --font_file data/times-ro.ttf --noise_level 0 --output_dir data/dupa --overwrite --all_letters`