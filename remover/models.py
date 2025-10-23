from django.db import models


class UploadedImage(models.Model):
    original_image = models.ImageField(upload_to="original/")
    processed_image = models.ImageField(upload_to="processed/", null=True, blank=True)
