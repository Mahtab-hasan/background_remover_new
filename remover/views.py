from django.shortcuts import render, redirect, get_object_or_404
from .models import UploadedImage
from rembg import remove
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile
import os

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

def remove_image(request, image_id):
    """Remove an uploaded image and its files"""
    uploaded_image = get_object_or_404(UploadedImage, id=image_id)
    
    # Delete the files from the filesystem
    if uploaded_image.original_image:
        if os.path.isfile(uploaded_image.original_image.path):
            os.remove(uploaded_image.original_image.path)
    
    if uploaded_image.processed_image:
        if os.path.isfile(uploaded_image.processed_image.path):
            os.remove(uploaded_image.processed_image.path)
    
    # Delete the database record
    uploaded_image.delete()
    
    return redirect('index')


