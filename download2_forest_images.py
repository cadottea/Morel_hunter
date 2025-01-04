import requests
from bs4 import BeautifulSoup
import os
import time

def download_images(search_term, num_images):
    folder_name = "no_morel_images"
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    downloaded_count = 0
    page = 0  # To track pagination

    while downloaded_count < num_images:
        # Google search URL for images
        url = f"https://www.google.com/search?q={search_term.replace(' ', '+')}&tbm=isch&start={page * 20}"
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find image elements (You may need to adjust the class based on the current structure)
        images = soup.find_all('img')
        
        print(f"Found {len(images)} images on page {page + 1}.")

        if not images:
            print("No more images found. Exiting.")
            break

        for img in images:
            if downloaded_count >= num_images:
                break
            try:
                img_url = img['src']
                print(f"Downloading image from {img_url}")
                
                img_response = requests.get(img_url)
                img_response.raise_for_status()  # Check for errors

                img_name = os.path.join(folder_name, f"{downloaded_count + 1}.jpg")
                with open(img_name, 'wb') as f:
                    f.write(img_response.content)

                print(f"Downloaded: {img_name}")
                downloaded_count += 1
                time.sleep(2)  # Pause for 2 seconds between downloads

            except Exception as e:
                print(f"Could not download image: {e}")

        page += 1  # Move to the next page
        time.sleep(5)  # Pause before fetching the next page

if __name__ == "__main__":
    search_term = input("Enter the search term: ")
    num_images = int(input("Enter the number of images to download: "))
    
    download_images(search_term, num_images)