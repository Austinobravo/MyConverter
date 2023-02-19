from django.db import models

# Create your models here.

class File(models.Model):
    music = models.FileField(verbose_name='Music Converter',upload_to='documents/', help_text='This is the file that got uploaded for conversion.')

    def __str__(self):
        return str(self.music)

# class upload(models.Model):
#     title=models.CharField(max_length=50)
#     upload=models.FileField(upload_to="documents/")

class Link(models.Model):
    link = models.CharField(max_length=500, null=True, blank=True, default='my_link')

    def __str__(self) :
        return str(self.link) 