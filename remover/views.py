from django.shortcuts import render
from .models import UploadedImage
from rembg import remove
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile

def index(request):
    if request.method == 'POST':
        if 'image' in request.FILES:
            original_image_file = request.FILES['image']

            # Save the original image
            uploaded_image = UploadedImage(original_image=original_image_file)
            uploaded_image.save()

            # Process the image with rembg
            input_image = Image.open(original_image_file)
            output_image = remove(input_image)

            # Save the processed image
            buffer = BytesIO()
            output_image.save(buffer, format='PNG')
            processed_image_file = ContentFile(buffer.getvalue())
            uploaded_image.processed_image.save(f'processed_{original_image_file.name}', processed_image_file)

            return render(request, 'index.html', {'uploaded_image': uploaded_image})
    return render(request, 'index.html')