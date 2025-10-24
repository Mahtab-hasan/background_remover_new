# from django.shortcuts import render
# from .models import UploadedImage
# from rembg import remove
# from PIL import Image
# from io import BytesIO
# from django.core.files.base import ContentFile

# def index(request):
#     if request.method == 'POST':
#         if 'image' in request.FILES:
#             original_image_file = request.FILES['image']

#             # Save the original image
#             uploaded_image = UploadedImage(original_image=original_image_file)
#             uploaded_image.save()

#             # Process the image with rembg
#             input_image = Image.open(original_image_file)
#             output_image = remove(input_image)

#             # Save the processed image
#             buffer = BytesIO()
#             output_image.save(buffer, format='PNG')
#             processed_image_file = ContentFile(buffer.getvalue())
#             uploaded_image.processed_image.save(f'processed_{original_image_file.name}', processed_image_file)

#             return render(request, 'index.html', {'uploaded_image': uploaded_image})
#     return render(request, 'index.html')

from django.shortcuts import render
from .models import UploadedImage
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile
import os

# ---------------------------
# Environment optimizations
# ---------------------------
# Disable GPU use (Render has no GPU)
os.environ["CUDA_VISIBLE_DEVICES"] = ""
# Prevent Numba from overusing CPU cores
os.environ["OMP_NUM_THREADS"] = "1"
# Prevent heavy Numba cache in root (use temp directory)
os.environ["NUMBA_CACHE_DIR"] = "/tmp"

# ---------------------------
# Import rembg safely
# ---------------------------
from rembg import remove, new_session

# Use lightweight model for low RAM servers
session = new_session("u2netp")

def index(request):
    if request.method == 'POST':
        if 'image' in request.FILES:
            original_image_file = request.FILES['image']

            # Save the original uploaded image
            uploaded_image = UploadedImage(original_image=original_image_file)
            uploaded_image.save()

            # Process with rembg using CPU-only mode
            input_image = Image.open(original_image_file).convert("RGBA")

            # Resize image to prevent memory errors
            # max_size = (1024, 1024) 
            # input_image.thumbnail(max_size, Image.Resampling.LANCZOS)

            output_image = remove(input_image, session=session)

            # Save processed image in memory
            buffer = BytesIO()
            output_image.save(buffer, format='PNG')
            processed_image_file = ContentFile(buffer.getvalue())

            # Save processed image to model
            uploaded_image.processed_image.save(
                f'processed_{original_image_file.name}', processed_image_file
            )

            return render(request, 'index.html', {'uploaded_image': uploaded_image})

    # GET request → just show upload page
    return render(request, 'index.html')

