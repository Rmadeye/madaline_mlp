### Simple MADALINE network for identification of letters and digits based on ttf file.

This is a simple implementation of a MADALINE network for identification of letters and digits based on a ttf file. The network is trained using the simple single-layer network. The network is implemented in Python using the numpy library for matrix operations.

### Usage

1. Create `conda`environment using `environment.yml` file:
   `conda env create -f environment.yml`
2. Activate the environment:
   `conda activate madaline`
3. Download the ttf file and put it in data/ directory. Exemplary [website](https://www.download-free-fonts.com/details/86847/times-roman). Sample Times Roman font is already included in the repository.
3. Generate the training and test data using `ttf` file. Example:
   `python3 font_generator.py --width 32 --height 32 --x_position 16 --y_position 16 --font_file data/times-ro.ttf --noise_level 0 --output_dir data/train --overwrite --all_letters`

   `python3 font_generator.py --width 32 --height 32 --x_position 16 --y_position 16 --font_file data/times-ro.ttf --noise_level 30 --output_dir data/test_noise_30 --overwrite --all_digits`

   You can also use 'all_letters' or use multiletter string like ABCDEFabcdef to generate only specified letters or digits
4. Train and test the network:
   `python3 madaline_ocr.py --train_path data/train/ --test_path data/test_90`
5. Enjoy the results!

Sample results:

`python3 font_generator.py --width 128 --height 128 --x_position 0 --y_position 0 --font_size 32 --font_file data/times-ro.ttf --noise_level 50 --output_dir data/test --overwrite --letter atyukjxZCVF1678`

`python3 font_generator.py --width 128 --height 128 --x_position 0 --y_position 0 --font_size 32 --font_file data/times-ro.ttf --noise_level 0 --output_dir data/train --overwrite -
-letter atyukjxZCVF1678`

`python3 madaline_ocr.py --train_path data/train --test_path data/test --plot_results`


![alt text](![image](https://github.com/Rmadeye/madaline_mlp/assets/46814304/3fbab6c6-6622-44f6-a463-43b81f130946)
)

The sample letters (noisy and clean) are shown below (for the same font and noise level as in the example above):

![alt text](![image](https://github.com/Rmadeye/madaline_mlp/assets/46814304/a28b4f55-ea8f-4ed6-9bf4-9ed7efcfe71b)
) vs ![alt text](![image](https://github.com/Rmadeye/madaline_mlp/assets/46814304/5829744c-deb5-4f2a-964d-e6aa0bc3039f)
)        ![alt text](![image](https://github.com/Rmadeye/madaline_mlp/assets/46814304/cf6fa109-c0a6-47f0-a7ea-198c2aed2cbb)
) vs ![alt text](![image](https://github.com/Rmadeye/madaline_mlp/assets/46814304/eb115b76-36cd-4f3c-9be3-8ca51db54347)
g)

![alt text](![image](https://github.com/Rmadeye/madaline_mlp/assets/46814304/642d9912-0d9c-4114-8133-0a6a3d36c070)
) vs ![alt text](![image](https://github.com/Rmadeye/madaline_mlp/assets/46814304/bc50519a-99a0-4e2a-a116-0a616d7a676b)
)        ![alt text](![image](https://github.com/Rmadeye/madaline_mlp/assets/46814304/04b32ae7-e2ab-410e-868b-32d8eeaba429)
) vs ![alt text](![image](https://github.com/Rmadeye/madaline_mlp/assets/46814304/a71f0668-8fc1-41d7-b445-645f8f8a0f4e)
)
