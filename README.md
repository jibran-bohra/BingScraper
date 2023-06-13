# Geolocating Images using Bing

The Geolocating Images using Bing project aims to provide an efficient solution for extracting GPS information from images. By utilizing Bing's reverse search feature, the script interacts with the Bing API to retrieve GPS data. To ensure faster computation, an asynchronous approach using the asyncio library is implemented for concurrent image processing.

## Key Features

- Reverse Search: The script performs a reverse search using Bing's API to extract GPS information for given images.
- Asynchronous Computation: The implementation of asynchronous programming allows for efficient and concurrent image processing.
- Data Collection: The script collects geolocation data for images and extracts their GPS coordinates.
- Bing API Integration: The project seamlessly integrates with Bing's reverse search feature to retrieve relevant GPS information.

## Usage

1. Clone the project repository from [here](link-to-repository).
2. Install the necessary dependencies using your preferred package manager (e.g., pip).
3. Create a Bing Developers account to obtain API credentials.
4. Update the script with your Bing API credentials.
5. Place the image(s) for geolocation in the `images-input/` directory.
6. Run `main.py` to initiate the process of finding and downloading all image search results with GPS exif tags.

Alternatively, you can follow these steps:
1. Run `BingScraper.py` to gather search result content URLs, which will be saved in the `url-searchresults/` directory.
2. Run `ImageDownloader.py` to download all images with GPS exif tags to the `images-output/` directory.

*For further details, including code implementation and documentation, please refer to the project repository.*
