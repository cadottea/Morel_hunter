import json
import os

# Paths to your dataset
json_folder = "morel_images/"  # Folder containing both .jpg and .json files
output_folder = "yolo_labels/"  # Desired folder for the output YOLO label files

# Ensure the output folder exists
os.makedirs(output_folder, exist_ok=True)

# Class ID for Morel (YOLO class)
class_id = 0  # You can adjust this if you have more classes

# Loop through all the JSON files and convert
for json_file in os.listdir(json_folder):
    if json_file.endswith('.json'):
        json_path = os.path.join(json_folder, json_file)
        
        # Load JSON data
        with open(json_path, 'r') as f:
            data = json.load(f)

        # Get image dimensions (You may need to adjust this if your JSON has a different format)
        image_width = data['imageWidth']
        image_height = data['imageHeight']
        
        # Iterate through shapes (which contain the polygons)
        for shape in data['shapes']:
            # Get the label (for YOLO format, this will be the class ID, so you might need to map the label to class_id)
            label = shape['label']
            # We assume here that the label is always 'morel', but you can extend it for other cases

            # Extract points (polygon vertices)
            points = shape['points']

            # Calculate the bounding box
            xs = [p[0] for p in points]
            ys = [p[1] for p in points]
            xmin = min(xs)
            xmax = max(xs)
            ymin = min(ys)
            ymax = max(ys)

            # YOLO format (x_center, y_center, width, height) relative to image dimensions
            x_center = (xmin + xmax) / 2 / image_width
            y_center = (ymin + ymax) / 2 / image_height
            width = (xmax - xmin) / image_width
            height = (ymax - ymin) / image_height

            # Construct YOLO label format for this polygon
            yolo_label = f"{class_id} {x_center} {y_center} {width} {height}\n"
            
            # Create a label file for each image
            image_name = os.path.splitext(json_file)[0]  # Remove the .json extension
            label_filename = os.path.join(output_folder, f"{image_name}.txt")

            # Wri
