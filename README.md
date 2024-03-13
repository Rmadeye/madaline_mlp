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

![image](https://github.com/Rmadeye/madaline_mlp/assets/46814304/fd21322a-4d70-4a61-9229-2df9f8a7c067)

The sample letters (noisy and clean) are shown below (for the same font and noise level as in the example above):

![image](https://github.com/Rmadeye/madaline_mlp/assets/46814304/0cbef62c-db60-4227-923f-e284901e3c22) vs ![image](https://github.com/Rmadeye/madaline_mlp/assets/46814304/7e189882-8433-412f-bdcf-e5231cfb1646)    ![image](https://github.com/Rmadeye/madaline_mlp/assets/46814304/4cc43732-85f6-4bb6-8cc2-4a45cd546bff) vs    ![image](https://github.com/Rmadeye/madaline_mlp/assets/46814304/b4301ba8-f59d-4856-b21b-d0198e16a2e8)

![image](https://github.com/Rmadeye/madaline_mlp/assets/46814304/458482f4-0849-466f-9656-fbd39b5b4ddf) vs ![image](https://github.com/Rmadeye/madaline_mlp/assets/46814304/b18bc72b-3c13-4e23-b6c2-d142b67d8f09)    ![image](https://github.com/Rmadeye/madaline_mlp/assets/46814304/3eae65a3-fa24-444b-b630-cb0d066409af) vs ![image](https://github.com/Rmadeye/madaline_mlp/assets/46814304/40675a7b-2677-4b3a-a21d-8a05b0510bf5)







   
