import os
import shutil
import random

# Paths to your images and labels
image_folder = './morel_images'  # Path to the folder with your images
label_folder = './yolo_labels'   # Path to the folder with your YOLO label files
train_image_folder = './train_images'  # Destination for training images
train_label_folder = './train_labels'  # Destination for training labels
test_image_folder = './test_images'  # Destination for test images
test_label_folder = './test_labels'   # Destination for test labels

# Ensure the destination folders exist
os.makedirs(train_image_folder, exist_ok=True)
os.makedirs(train_label_folder, exist_ok=True)
os.makedirs(test_image_folder, exist_ok=True)
os.makedirs(test_label_folder, exist_ok=True)

# Get all image and label files
image_files = [f for f in os.listdir(image_folder) if f.endswith('.jpg')]
label_files = [f for f in os.listdir(label_folder) if f.endswith('.txt')]

# Print out counts and the first few filenames to check the contents
print(f"Number of images: {len(image_files)}")
print(f"Number of labels: {len(label_files)}")

# Print the first 10 filenames for both image and label files (if there are enough files)
print("First 10 image files:", image_files[:10])
print("First 10 label files:", label_files[:10])

# Check for missing labels
missing_labels = []
for image_file in image_files:
    label_file = image_file.replace('.jpg', '.txt')
    if label_file not in label_files:
        missing_labels.append(image_file)

# Print missing labels
if missing_labels:
    print(f"Missing label files for the following images: {missing_labels}")
else:
    print("All image files have corresponding label files.")

# Check that the number of image and label files match
assert len(image_files) == len(label_files), "Mismatch between images and label files."

# Shuffle the data for random splitting
random.seed(42)  # For reproducibility
combined_files = list(zip(image_files, label_files))
random.shuffle(combined_files)

# Calculate the split index for 80% training and 20% testing
split_idx = int(0.8 * len(combined_files))

# Split into training and testing sets
train_files = combined_files[:split_idx]
test_files = combined_files[split_idx:]

# Move files to their respective folders
for file in train_files:
    image_src = os.path.join(image_folder, file[0])
    label_src = os.path.join(label_folder, file[1])
    
    image_dest = os.path.join(train_image_folder, file[0])
    label_dest = os.path.join(train_label_folder, file[1])
    
    shutil.copy(image_src, image_dest)
    shutil.copy(label_src, label_dest)

for file in test_files:
    image_src = os.path.join(image_folder, file[0])
    label_src = os.path.join(label_folder, file[1])
    
    image_dest = os.path.join(test_image_folder, file[0])
    label_dest = os.path.join(test_label_folder, file[1])
    
    shutil.copy(image_src, image_dest)
    shutil.copy(label_src, label_dest)

print(f"Finished splitting data into {len(train_files)} training files and {len(test_files)} testing files.")
