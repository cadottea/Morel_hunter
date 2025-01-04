Morel Hunter - YOLO Mushroom Identification

This project aims to identify morel mushrooms using a YOLO (You Only Look Once) model. The current focus is on training the YOLO model to accurately classify morel mushrooms from images, with the long-term goal of integrating this technology into an iPhone app for real-time mushroom identification. The code includes dataset processing, YOLO model training, and evaluation scripts, providing the foundation for future development of a mobile application.

Features
    •   YOLO Model: A pre-trained YOLO model for identifying morel mushrooms in images.
    •   Dataset Processing: Includes code to process image datasets, convert annotations to YOLO format, and split data into training and testing sets.
    •   Model Training: Code for training the YOLO model with labeled data, allowing for morel mushroom detection.
    •   Data Augmentation: Various scripts to augment data by resizing images, applying filters, and other transformations.
    •   Future Application: The ultimate goal is to integrate this YOLO model into an iPhone app for real-time morel mushroom identification.

Installation

To use this project, you need to have Python 3.x and the necessary libraries installed.

Dependencies
    •   numpy
    •   opencv-python
    •   matplotlib
    •   pillow
    •   requests
    •   tensorflow
    •   torch
    •   yolo (for model training)

You can install the dependencies by running:
pip install -r requirements.txt

Note: You should set up a virtual environment for this project.

Usage
    1.  Download the Dataset: Start by downloading images and their labels from online sources such as Google, Flickr, or other platforms.
Example command for downloading morel mushroom images:

Note: Be careful to adhere to legalities concerning the use of image scrapers!


    2.  Prepare the Dataset: Convert your dataset to the appropriate format for YOLO, ensuring each image has a corresponding label file.
Use the following script to convert the annotations into YOLO format:

python convert_json_to_yolo.py


    3.  Split the Data: Split your dataset into training and testing sets by running:

    python train_yolo.py --train_images /path/to/train_images --train_labels /path/to/train_labels


    5.  Evaluate the Model: After training, use the evaluation script to test the model’s performance on the test set.

    python evaluate_model.py --test_images /path/to/test_images --test_labels /path/to/test_labels



Example

The project includes a sample of how you can use the trained model for predictions:

import cv2
from yolo import YOLO

# Load the trained YOLO model
model = YOLO('path_to_trained_model')

# Load an image of a morel mushroom
image = cv2.imread('path_to_image')

# Perform prediction
result = model.predict(image)

# Output the results
print("Predicted classes: ", result['classes'])

This code uses OpenCV to load an image and a YOLO model to predict the class of objects in the image. The result will show whether a morel mushroom is detected.

File Structure

/morel_images/
    /train_images/
    /train_labels/
    /test_images/
    /test_labels/
/yolo_labels/
    /train_labels/
    /test_labels/

    Contributions

Feel free to fork the project and submit pull requests. Contributions are welcome, especially for improving model accuracy or implementing the mobile app interface.

License

This project is licensed under the MIT License - see the LICENSE file for details.