import requests
from bs4 import BeautifulSoup
import os
from PIL import Image
from io import BytesIO

def download_images(search_term, num_images):
    # Create a directory to save images
    if not os.path.exists(search_term):
        os.makedirs(search_term)

    # Create Google Image Search URL
    url = f"https://www.google.com/search?hl=en&tbm=isch&q={search_term}"

    # Fetch the webpage with a user-agent
    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(response.text, 'html.parser')

    images = soup.find_all('img')
    print(f"Found {len(images)} images.")

    downloaded_count = 0

    for i, img in enumerate(images):
        try:
            img_url = img['src']
            print(f"Image {i + 1} URL: {img_url}")  # Debug: print image URL

            # Attempt to download image
            print(f"Downloading image from {img_url}")
            img_response = requests.get(img_url)
            img_response.raise_for_status()  # Check for errors

            # Save image
            img_name = os.path.join(search_term, f"{search_term}_{downloaded_count + 1}.jpg")
            image = Image.open(BytesIO(img_response.content))
            image.save(img_name)
            print(f"Downloaded: {img_name}")
            downloaded_count += 1
            
            # Stop downloading if we've reached the desired number of images
            if downloaded_count >= num_images:
                break

        except Exception as e:
            print(f"Could not download image {i + 1}: {e}")

if __name__ == "__main__":
    search_term = input("Enter the search term: ")
    num_images = int(input("Enter the number of images to download: "))
    
    download_images(search_term, num_images)
