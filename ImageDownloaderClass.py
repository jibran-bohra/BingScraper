import os, json, asyncio, httpx, io
from PIL import Image, ExifTags

class ImageDownloader:
    def __init__(self):
        self.dir_output = "images-output/"
        self.dir_searchresults = "url-searchresults/"

        self.files_json_url = os.listdir(self.dir_searchresults)

    async def download_image_with_gps(self, image_url, image_path):
        try:
            # Download the image from the URL
            async with httpx.AsyncClient() as client:
                response = await client.get(image_url)

            if response.status_code == 200:
                # If the response status code is 200 (success)
                # Open the image using PIL
                with Image.open(io.BytesIO(response.content)) as img:
                    # Check if the image has EXIF metadata
                    exif_data = img._getexif()
                    if exif_data is not None:
                        # Iterate over the EXIF tags
                        for tag, value in exif_data.items():
                            tag_name = ExifTags.TAGS.get(tag, tag)
                            if tag_name == 'GPSInfo' and bool(value):
                                # If the image has GPSInfo tag and the value is not empty
                                # Print the GPS info
                                print(f"GPS info: {image_url}\n")
                                # Save the image
                                self.save_image(img, image_path)
                            
            else:
                # If the response status code is not 200 (failure)
                print(f"Response != 200. Failed to fetch image.")

        except Exception as e:
            # If any exception occurs during the process
            print(str(e))


    def save_image(self, image, image_path):
        if os.path.exists(image_path):
            # If the image path already exists
            # Save the image with a ".png" extension appended to the existing path
            image.save(image_path + ".png")
        else:
            # If the image path does not exist
            # Create the path and save the image
            os.makedirs(os.path.dirname(image_path), exist_ok=True)
            image.save(image_path + ".png")

        # Print the path where the image is saved
        print(f"Saved image to {image_path}")

    async def download_all(self, json_urls = None):
        if json_urls is None:
            json_urls = self.files_json_url

        # Iterate over the provided JSON URLs
        for file in json_urls:
            print(file)
            file_path = self.dir_searchresults + file

            # Open the JSON file and load the image URLs
            with open(file_path, 'r') as f:
                image_urls = json.load(f)
            
            tasks = []
            
            # Iterate over the image URLs
            for i, image_url in enumerate(image_urls):
                # Create a unique image path based on the file name and index
                image_path = downloader.dir_output + ''.join(file.split('.')[:-1]) + f"-{i}"
                # Append the download task to the list of tasks
                tasks.append(self.download_image_with_gps(image_url, image_path))

            # Wait for all the download tasks to complete using asyncio.gather
            await asyncio.gather(*tasks)
            


    
        

downloader = ImageDownloader()

"""for file in ["test.json"]:
    print(file)
    file_path = downloader.dir_searchresults + file

    with open(file_path, 'r') as f:
        image_urls = json.load(f)
    
    for i, image_url in enumerate(image_urls):
        image_path = downloader.dir_output + ''.join(file.split('.')[:-1]) + f"-{i}"
        asyncio.run(downloader.download_image_with_gps(image_url, image_path))
"""

asyncio.run(downloader.download_all())