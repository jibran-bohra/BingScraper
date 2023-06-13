# Geolocating Images using Bing

This Bing Scraper is designed to provide an efficient solution for extracting GPS information from images. The script employs an asynchronous approach, similar to multithreading, to ensure faster computation using the asyncio library.

## Key Features

- Reverse Search: The script performs a reverse search using Bing's API to extract GPS information for given images.
- Asynchronous Computation: The implementation of asynchronous programming allows for efficient and concurrent image processing.
- Data Collection: The script collects geolocation data for images and extracts their GPS coordinates.
- Bing API Integration: Utilizing Bing's reverse search feature, the script interacts with the Bing API to retrieve relevant GPS information.

## Usage

1. Clone the project repository from [here](link-to-repository).
2. Install the required dependencies using the package manager of your choice (e.g., pip).
3. Obtain Bing API credentials by creating an account on the Bing Developers portal.
4. Update the script with your Bing API credentials.
5. Provide the image(s) for which you want to gather GPS information in the images-input/ directory.
6. Run main.py to find and download all image search results with GPS exif tags.  

Alternatively:
1. Run BingScraper.py to gather search result content URLs - saved in url-searchresults/ directory.
2. Run ImageDownloader.py to download all images with GPS exif tags. 


