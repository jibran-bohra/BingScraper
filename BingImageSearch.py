import requests
from bs4 import BeautifulSoup
import urllib.parse
import os


def search_and_download_images(sample_image_path, num_images):
    # Read the content of the sample image
    with open(sample_image_path, 'rb') as f:
        sample_image_data = f.read()

    # Perform an image search on Bing Images using the sample image
    search_url = "https://www.bing.com/images/search"
    files = {'file': ('sample_image.jpg', sample_image_data, 'image/jpeg')}
    params = {'view': 'detailv2', 'iss': 'upload'}
    response = requests.post(search_url, params=params, files=files)

    if response.status_code == 200:
        # Parse the search result page
        soup = BeautifulSoup(response.text, 'html.parser')
        image_elements = soup.select('.imgpt > a > img')

        if len(image_elements) >= num_images:
            # Create a directory to store the downloaded images
            if not os.path.exists("images"):
                os.makedirs("images")

            # Download the images
            for i in range(num_images):
                image_url = image_elements[i]['src']
                filename = f"image_{i+1}.jpg"
                download_image(image_url, filename)
                print(f"Downloaded image {i+1}/{num_images}")
        else:
            print("Insufficient number of images in the search results")
    else:
        print("Failed to request the search result page")


def download_image(image_url, filename):
    response = requests.get(image_url)
    if response.status_code == 200:
        with open(os.path.join("images", filename), 'wb') as f:
            f.write(response.content)
    else:
        print(f"Failed to download image: {response.status_code}")


if __name__ == "__main__":
    sample_image_path = "/path/to/sample_image.jpg"  # Path to the sample image
    num_images = 10  # Number of images to download
    search_and_download_images(sample_image_path, num_images)
