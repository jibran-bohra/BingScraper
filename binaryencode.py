from PIL import Image
import io, base64

def image_jpeg_base64(image_path):
    "Bing converts input images to jpeg and then generates a base64 string for search URLs"

    # Open the image file
    image = Image.open(image_path)

    # Convert the image to JPEG format
    jpeg_image = image.convert('RGB')

    # Save the converted image as JPEG to the in-memory file object
    image_file = io.BytesIO()
    jpeg_image.save(image_file, format='JPEG')

    # Retrieve the binary data of the image
    image_binary_data = image_file.getvalue()   

    #Encode in base64
    base64_encoded_data = base64.b64encode(image_binary_data)

    return base64_encoded_data.decode("utf-8")


print(image_jpeg_base64("images-input/Image_0001.png"))