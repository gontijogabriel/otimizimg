from django.db import models

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class ImageUpload(BaseModel):
    url = models.ImageField(upload_to='image/')
    format = models.CharField(max_length=256, null=True, blank=True)
    filename = models.CharField(max_length=256, null=True, blank=True)
    file_size = models.IntegerField(default=0, null=True, blank=True)
    width = models.IntegerField(default=0, null=True, blank=True)
    height = models.IntegerField(default=0, null=True, blank=True)
    color_mode = models.CharField(max_length=256, null=True, blank=True)
    dpi = models.CharField(max_length=256, null=True, blank=True)
    metadata = models.CharField(max_length=256, null=True, blank=True)

    def __str__(self):
        return self.filename or str(self.id)

class ImageConverter(BaseModel):
    original_file = models.ForeignKey(
        "ImageUpload",
        on_delete=models.CASCADE,
        related_name="conversions",
        null=True,
        blank=True,
    )
    url = models.ImageField(upload_to='convert/')
    filename = models.CharField(max_length=256, null=True, blank=True)
    format = models.CharField(max_length=256, null=True, blank=True)
    file_size = models.IntegerField(default=0, null=True, blank=True)
    width = models.IntegerField(default=0, null=True, blank=True)
    height = models.IntegerField(default=0, null=True, blank=True)
    color_mode = models.CharField(max_length=256, null=True, blank=True)
    dpi = models.CharField(max_length=256, null=True, blank=True)
    metadata = models.CharField(max_length=256, null=True, blank=True)
    
    def __str__(self):
        return self.filename or str(self.id)