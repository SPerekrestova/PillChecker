import base64
from django import template
from io import BytesIO
from PIL import Image

register = template.Library()


@register.filter
def image_to_base64(image_file):
    """
    Convert an uploaded image to a base64 string.
    """
    if not image_file:
        return ""

    # Open the image using Pillow
    image = Image.open(image_file)

    # Convert the image to base64
    buffer = BytesIO()
    image.save(buffer, format="JPEG")
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.read()).decode("utf-8")
    return f"data:image/jpeg;base64,{image_base64}"
