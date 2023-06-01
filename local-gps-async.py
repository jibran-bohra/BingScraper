import asyncio, time
from PIL import Image, ExifTags

async def has_gps_info(image_path):
    try:
        # Open the image using PIL
        img = Image.open(image_path)

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
    image_paths = [
        "images-test/IMG_1914-meta.jpeg",
        "images-test/IMG_1914-none.jpeg"
    ]

    tasks = []
    for image_path in image_paths:
        task = asyncio.create_task(has_gps_info(image_path))
        tasks.append(task)

    results = await asyncio.gather(*tasks)
    for i, path in enumerate(image_paths):
        contains_gps = results[i]
        print(f"{'Y' if contains_gps else 'N'} | {path}")



if __name__ == '__main__':
    start = time.time()
    asyncio.run(main())
    end = time.time()
    print(end - start)
