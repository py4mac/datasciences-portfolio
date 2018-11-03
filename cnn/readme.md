
# Dog Breed Images classifier

This project aims to aims to implement Dog Breed classifier based on two methodologies:
- Visual Bag of Words (SIFT extraction)
- Convolutional Neural Network.

## Project structure


- [Preparation](notebook_prepare_train_and_test.ipynb) - Notebook to download images and prepare train/test folders.

- [Visual Bag of Words](notebook_bag_of_words.ipynb) - SIFT and Bag of Words approach.

Tags: OpenCV, KMeans, TSNE and LinearSVC.

- [CNN](nnotebook_cnn.ipynb) - CNN approach using GridSearchCV hyperoptimisation.

Tags: OpenCV, Keras and GridSearchCV.

- [CNN](notebook_cnn_hyperopt.ipynb) - CNN approach using HyperOpt hyperoptimisation.

Tags: OpenCV, Keras and HyperOpt.

- [Api](api/) - Create a simple API to predict dog breed from input image.
