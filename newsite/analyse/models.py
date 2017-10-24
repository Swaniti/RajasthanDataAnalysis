from django.db import models

# Create your models here.

class Random(models.Model):
  data = models.FileField(upload_to = './static')
