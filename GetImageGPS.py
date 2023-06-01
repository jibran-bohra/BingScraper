import requests, json
from PIL import Image
from PIL.ExifTags import TAGS

def has_gps_info(image_url):
    try:
        # Download the image from the URL
        response = requests.get(image_url, stream=True, verify=False)

        if response.status_code == 200:
            # Open the image using PIL
            img = Image.open(response.raw)

            # Check if the image has EXIF metadata
            exif_data = img._getexif()
            if exif_data is not None:

                # Iterate over the EXIF tags
                for tag, value in exif_data.items():

                    tag_name = TAGS.get(tag, tag)
                    
                    if tag_name == 'GPSInfo' and bool(value):
                        return True

    except Exception as e:
        print("An error occurred:", str(e))

    return False

# Read the JSON file
with open('url-searchresults/Image_0001.json', 'r') as f:
    image_urls = json.load(f)


# Example usage
for image_url in image_urls:
    contains_gps = has_gps_info(image_url)
    print(f"{'Y' if contains_gps else 'N'} | {image_url} ")


response = requests.get("https://i.pinimg.com/originals/52/c3/88/52c3885137eba46faef1c02c7d4adf4c.jpg", stream=True)

live = Image.open(response.raw)
meta = Image.open("testimages/IMG_1914-meta.jpeg")
none = Image.open("testimages/IMG_1914-none.jpeg")


exif_live = live._getexif()
exif_meta = meta._getexif()
exif_none = none._getexif()

print(exif_live)

for tag, value in exif_live.items():
    tag_name = TAGS.get(tag, tag)
    print(tag_name, value)
    print(bool(value))