from BingScraperClass import BingScraper
from ImageDownloaderClass import ImageDownloader
import asyncio

# Reverse image search image using Bing. Gather all unqiue content URLs. Export to .json file. 
bing = BingScraper()
for i, file in enumerate(bing.files_input):
    base64string = bing.image_jpeg_base64(bing.dir_input + file)
    image_search_url = bing.get_search_url(base64string)
    print(image_search_url)
    results = asyncio.run(bing.gather_content_urls(image_search_url))
    bing.write_to_json(bing.dir_searchresults + bing.results_content_urls[i], results)    

# Import .json file containing image URLs. Download all images with GPS information.
downloader = ImageDownloader()
asyncio.run(downloader.download_all())