import requests
from bs4 import BeautifulSoup
import os
from PIL import Image
from io import BytesIO
import time

def download_images(search_term, num_images):
    if not os.path.exists(search_term):
        os.makedirs(search_term)

    downloaded_count = 0
    start = 0  # For pagination

    while downloaded_count < num_images:
        url = f"https://www.google.com/search?hl=en&tbm=isch&q={search_term}&start={start}"

        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        soup = BeautifulSoup(response.text, 'html.parser')

        images = soup.find_all('img')
        print(f"Found {len(images)} images on page starting from {start}.")

        for i, img in enumerate(images):
            try:
                img_url = img.get('data-src') or img.get('src')
                if img_url and img_url.startswith('http'):
                    print(f"Image {downloaded_count + 1} URL: {img_url}")

                    print(f"Downloading image from {img_url}")
                    img_response = requests.get(img_url)
                    img_response.raise_for_status()

                    img_name = os.path.join(search_term, f"{search_term}_{downloaded_count + 1}.jpg")
                    image = Image.open(BytesIO(img_response.content))
                    image.save(img_name)
                    print(f"Downloaded: {img_name}")
                    downloaded_count += 1
                    
                    if downloaded_count >= num_images:
                        break

                    time.sleep(1)  # Delay between downloads

                else:
                    print(f"Skipping invalid image URL for image {downloaded_count + 1}")

            except Exception as e:
                print(f"Could not download image {downloaded_count + 1}: {e}")

        # Move to the next page
        start += 20  # Increment for the next batch of images

if __name__ == "__main__":
    search_term = input("Enter the search term: ")
    num_images = int(input("Enter the number of images to download: "))
    
    download_images(search_term, num_images)
