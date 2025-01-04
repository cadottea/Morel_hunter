import requests
import os
import time

def download_images(api_key, search_term, num_images, size_ratio, exclude_terms, max_pages=10):
    headers = {
        'Authorization': api_key
    }
    
    # Create the folder if it doesn't exist
    folder_name = "new_morel_images"
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
        print(f"Created folder: {folder_name}")

    # Ideal dimensions
    ideal_width, ideal_height = 640, 640
    min_width = int(ideal_width * size_ratio)
    min_height = int(ideal_height * size_ratio)
    max_width = int(ideal_width / size_ratio)
    max_height = int(ideal_height / size_ratio)

    print(f"\nSearching for images with size between {min_width}x{min_height} and {max_width}x{max_height} pixels.")
    
    total_downloaded = 0
    page = 1
    
    while total_downloaded < num_images and page <= max_pages:
        print(f"\nFetching page {page}...")
        response = requests.get(f'https://api.pexels.com/v1/search?query={search_term}&page={page}&per_page=80', headers=headers)
        
        if response.status_code != 200:
            print(f"Failed to fetch page {page}. Status code: {response.status_code}")
            break
        
        data = response.json()
        
        if 'photos' not in data or len(data['photos']) == 0:
            print("No more images found on this page.")
            break

        found_images = 0  # Track how many valid images are found in this round
        
        for photo in data['photos']:
            width = photo['width']
            height = photo['height']
            
            # Check if image dimensions are within the specified limits
            if min_width <= width <= max_width and min_height <= height <= max_height:
                img_url = photo['src']['original']  # URL of the original image
                
                # Check for exclusion terms in the description or alt description (if available)
                description = photo.get('alt', '').lower()  # Use 'alt' text from the API response
                if any(term.lower() in description for term in exclude_terms):
                    print(f"Excluding image due to match in description: {description}")
                    continue  # Exclude this image

                try:
                    img_response = requests.get(img_url)
                    if img_response.status_code == 200:
                        img_name = os.path.join(folder_name, f"image_{total_downloaded + 1}.jpg")  # Save in created folder
                        with open(img_name, 'wb') as f:
                            f.write(img_response.content)
                        print(f"Downloaded: {img_name}")
                        total_downloaded += 1
                        found_images += 1
                    else:
                        print(f"Failed to download image {img_url}. Response code: {img_response.status_code}")
                except Exception as e:
                    print(f"Error downloading image: {e}")

        if found_images > 0:
            print(f"Found {found_images} images on page {page} matching criteria.")
        else:
            print("No images found on this page matching criteria.")
        
        page += 1
        time.sleep(1)  # Sleep to respect API rate limits

    print(f"\nDownload complete. Total images downloaded: {total_downloaded}")

if __name__ == "__main__":
    api_key "your API key here"  # Your Pexels API key
    
    search_term = input("Enter the search term: ")
    num_images = int(input("Enter the number of images to download: "))
    size_ratio = float(input("Enter the size ratio (e.g., 0.8 for 80% of ideal size): "))
    
    exclude_input = input("Enter terms to exclude (comma-separated, e.g., 'animal, pet'): ")
    exclude_terms = [term.strip() for term in exclude_input.split(',')]  # Create a list of exclusion terms
    
    max_pages = 10  # Set the maximum pages to check
    download_images(api_key, search_term, num_images, size_ratio, exclude_terms, max_pages)
