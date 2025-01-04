import requests
from bs4 import BeautifulSoup
import os
from PIL import Image
from io import BytesIO

def download_images(search_term, num_images):
    # Create a directory to save images
    if not os.path.exists(search_term):
        os.makedirs(search_term)
        print(f"Created directory: {search_term}")

    # Create Google Image Search URL
    url = f"https://www.google.com/search?hl=en&tbm=isch&q={search_term}"
    print(f"Fetching URL: {url}")

    response = requests.get(url)
    if response.status_code == 200:
        print("Successfully fetched the webpage.")
    else:
        print(f"Failed to fetch the webpage. Status code: {response.status_code}")
        return

    soup = BeautifulSoup(response.text, 'html.parser')

    images = soup.find_all('img', limit=num_images)
    print(f"Found {len(images)} images.")

    downloaded_count = 0

    for i, img in enumerate(images):
        try:
            img_url = img['src']
            print(f"Image {i + 1} URL: {img_url}")

            # Only download if the URL is complete
            if img_url.startswith('http'):
                print(f"Downloading image from {img_url}")
                
                # Download image
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
                print("Reached the desired number of images.")
                break

        except Exception as e:
            print(f"Could not download image {i + 1}: {e}")

if __name__ == "__main__":
    search_term = input("Enter the search term: ")
    num_images = int(input("Enter the number of images to download: "))
    
    download_images(search_term, num_images)
