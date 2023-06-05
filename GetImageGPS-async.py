import httpx, json, asyncio, time
from PIL import Image, ExifTags

async def has_gps_info(image_url):
    try:
        # Download the image from the URL
        response = httpx.get(image_url, stream=True)

        if response.status_code == 200:
            # Open the image using PIL
            img = Image.open(response.raw)

            # Check if the image has EXIF metadata
            exif_data = img._getexif()
            if exif_data is not None:

                # Iterate over the EXIF tags
                for tag, value in exif_data.items():
                    tag_name = ExifTags.TAGS.get(tag, tag)
                    if tag_name == 'GPSInfo' and bool(value):
                        return True

    except Exception as e:
        print("An error occurred:", str(e))

    return False


async def main():
    # Read the JSON file
    with open('url-searchresults/Image_0001.json', 'r') as f:
        image_urls = json.load(f)

    tasks = []
    for image_url in image_urls:
        tasks.append(has_gps_info(image_url))

    results = await asyncio.gather(*tasks)

    print(results)

if __name__ == "__main__":
    asyncio.run(main())




