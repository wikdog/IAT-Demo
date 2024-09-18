from django.db import models

class UploadedImage(models.Model):
    image = models.ImageField(upload_to='images/')
    class Meta:
        app_label = 'backend'  # 这里填写你的应用程序名



