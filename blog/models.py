from django.db import models

# Create your models here.
class Posts(models.Model):
    #id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=256)
    text = models.TextField()
    created = models.DateField(auto_now_add=True)
