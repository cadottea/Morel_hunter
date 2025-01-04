import requests
import os
import time

def download_unsplash_images(api_key, search_term, num_images):
    headers = {
        'Authorization': f'Client-ID {api_key}'  # Unsplash API Key
    }
    
    folder_name = "new_morel_images"
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
        print(f"Created folder: {folder_name}")

    total_downloaded = 0
    page = 1
    
    while total_downloaded < num_images:
        print(f"\nFetching page {page}...")
        response = requests.get(f'https://api.unsplash.com/search/photos?query={search_term}&page={page}&per_page=30', headers=headers)
        
        if response.status_code != 200:
            print(f"Failed to fetch page {page}. Status code: {response.status_code}")
            break
        
        data = response.json()
        
        if 'results' not in data or len(data['results']) == 0:
            print("No more images found on this page.")
            break

        for photo in data['results']:
            img_url = photo['urls']['full']  # URL of the full image
            
            try:
                img_response = requests.get(img_url)
                if img_response.status_code == 200:
                    img_name = os.path.join(folder_name, f"image_{total_downloaded + 1}.jpg")  
                    with open(img_name, 'wb') as f:
                        f.write(img_response.content)
                    print(f"Downloaded: {img_name}")
                    total_downloaded += 1
                else:
                    print(f"Failed to download image {img_url}. Response code: {img_response.status_code}")
            except Exception as e:
                print(f"Error downloading image: {e}")

        page += 1
        time.sleep(1)  # Sleep to respect API rate limits

    print(f"\nDownload complete. Total images downloaded: {total_downloaded}")  # Corrected line

if __name__ == "__main__":
    api_key = "YOUR_UNSPLASH_API_KEY"  # Your Unsplash API key
    search_term = input("Enter the search term (e.g., morel mushroom): ")
    num_images = int(input("Enter the number of images to download: "))
    
    download_unsplash_images(api_key, search_term, num_images)
