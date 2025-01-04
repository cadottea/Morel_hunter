import requests
import os
import time

def download_flickr_images(api_key, search_terms, num_images):
    # Set the folder name for downloaded images
    folder_name = "new_flickr_morel"
    
    # Create the folder if it doesn't exist
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
        print(f"Created folder: {folder_name}")

    total_downloaded = 0
    page = 1

    while total_downloaded < num_images:
        print(f"\nFetching page {page}...")
        response = requests.get("https://api.flickr.com/services/rest/", params={
            'method': 'flickr.photos.search',
            'api_key': api_key,
            'text': search_terms,  # Use the entered search terms
            'format': 'json',
            'nojsoncallback': 1,
            'per_page': 100,  # Max per page
            'page': page
        })
        
        if response.status_code != 200:
            print(f"Failed to fetch page {page}. Status code: {response.status_code}")
            break  # Handle fetch errors gracefully

        data = response.json()
        
        if not data['photos']['photo']:
            print("No more images found on this page.")
            break

        print(f"Images found on page {page}: {len(data['photos']['photo'])}")

        for photo in data['photos']['photo']:
            img_url = f"https://live.staticflickr.com/{photo['server']}/{photo['id']}_{photo['secret']}.jpg"
            
            try:
                img_response = requests.get(img_url)
                if img_response.status_code == 200:
                    img_name = os.path.join(folder_name, f"image_{total_downloaded + 1}.jpg")
                    with open(img_name, 'wb') as f:
                        f.write(img_response.content)
                    print(f"Downloaded: {img_name}")
                    total_downloaded += 1

                    if total_downloaded >= num_images:
                        break  # Stop if we reach the desired number of images
                else:
                    print(f"Failed to download image {img_url}. Response code: {img_response.status_code}")
            except Exception as e:
                print(f"Error downloading image: {e}")

        page += 1
        time.sleep(1)  # Sleep to respect API rate limits

    print(f"\nDownload complete. Total images downloaded: {total_downloaded}")

if __name__ == "__main__":
    api_key "your API key here"  # Your Flickr API key
    search_suggestions = [
        "morel mushroom",
        "Morchella",
        "black morel",
        "yellow morel",
        "white morel",
        "edible mushrooms",
        "morel mushroom recipes",
        "hunting morel mushrooms"
    ]
    
    # Display search suggestions
    print("Suggested search terms for morel mushrooms:")
    for suggestion in search_suggestions:
        print(f"- {suggestion}")
        
    search_terms = input("Enter the search terms (e.g., 'morel mushroom, Morchella'): ")
    num_images = int(input("Enter the number of images to download: "))
    
    download_flickr_images(api_key, search_terms, num_images)
