
import base64

def image_to_base64_string(image_path):
    """Convert an image file to a Base64 string."""
    with open(image_path, "rb") as img_file:
        img_bytes = img_file.read()
        base64_str = base64.b64encode(img_bytes).decode("utf-8")
        return base64_str


image_path = r".png"


base64_string = image_to_base64_string(image_path)
print(base64_string)

