import requests
from bs4 import BeautifulSoup
import os
from PIL import Image
from io import BytesIO

def download_images(search_terms, num_images):
    # Create a directory to save images
    save_folder = "no_morel_images"
    if not os.path.exists(save_folder):
        os.makedirs(save_folder)

    for term in search_terms:
        # Create Google Image Search URL for each term
        url = f"https://www.google.com/search?hl=en&tbm=isch&q={term}"

        # Fetch the webpage with a user-agent
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        soup = BeautifulSoup(response.text, 'html.parser')

        images = soup.find_all('img')
        print(f"Found {len(images)} images for search term '{term}'.")

        downloaded_count = 0

        for i, img in enumerate(images):
            try:
                img_url = img['src']
                print(f"Image {i + 1} URL: {img_url}")  # Debug: print image URL

                # Attempt to download image
                print(f"Downloading image from {img_url}")
                img_response = requests.get(img_url)
                img_response.raise_for_status()  # Check for errors

                # Save image with a shorter name
                img_name = os.path.join(save_folder, f"{term.replace(' ', '_')}_{downloaded_count + 1}.jpg")
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
    search_terms = input("Enter the search terms separated by commas: ").split(',')
    search_terms = [term.strip() for term in search_terms]  # Remove leading/trailing spaces
    num_images = int(input("Enter the number of images to download for each search term: "))
    
    download_images(search_terms, num_images)