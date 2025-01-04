import requests
from bs4 import BeautifulSoup
import os
import time
from PIL import Image
from io import BytesIO

def download_images(search_term, num_images, size_percentage):
    folder_name = "no_morel_images"
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    downloaded_count = 0
    page = 0  # To track pagination

    # Calculate the minimum width and height based on the ideal size and user input percentage
    ideal_width, ideal_height = 640, 640
    min_width = int(ideal_width * size_percentage)
    min_height = int(ideal_height * size_percentage)

    while downloaded_count < num_images:
        # Google search URL for images
        url = f"https://www.google.com/search?q={search_term.replace(' ', '+')}&tbm=isch&start={page * 20}"
        print(f"Fetching images from: {url}")
        try:
            response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
            soup = BeautifulSoup(response.text, 'html.parser')

            # Find image elements
            images = soup.find_all('img')
            print(f"Found {len(images)} images on page {page + 1}.")

            if not images:
                print("No more images found. Exiting.")
                break

            for img in images:
                if downloaded_count >= num_images:
                    break
                try:
                    # Attempt to get the image URL from either 'src' or 'data-src' attributes
                    img_url = img.get('data-src') or img.get('src')
                    if not img_url:
                        print("No image URL found, skipping.")
                        continue
                    
                    print(f"Downloading image from {img_url}")
                    img_response = requests.get(img_url)
                    img_response.raise_for_status()  # Check for errors

                    # Load the image from the response content
                    image = Image.open(BytesIO(img_response.content))

                    # Check if the image size meets the minimum dimensions
                    if image.width >= min_width and image.height >= min_height:
                        img_name = os.path.join(folder_name, f"{downloaded_count + 1}.jpg")
                        image.save(img_name)
                        print(f"Downloaded: {img_name} (Size: {image.width}x{image.height})")
                        downloaded_count += 1
                    else:
                        print(f"Skipped image due to size: {image.width}x{image.height} (Min: {min_width}x{min_height})")

                    time.sleep(2)  # Pause for 2 seconds between downloads

                except Exception as e:
                    print(f"Could not download image: {e}")

            page += 1  # Move to the next page
            time.sleep(5)  # Pause before fetching the next page

        except Exception as e:
            print(f"Error fetching images: {e}")
            break

if __name__ == "__main__":
    search_term = input("Enter the search term: ")
    num_images = int(input("Enter the number of images to download: "))
    size_percentage = float(input("Enter the percentage of the ideal size (e.g., 0.8 for 80%): "))
    
    download_images(search_term, num_images, size_percentage)