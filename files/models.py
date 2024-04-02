from django.db import models
from django.core.exceptions import ValidationError


def validate_file_extension(value):
    if not value.name.endswith('.pdf'):
        raise ValidationError(u'Неверный тип файла: только PDF.')
    if value.size > 512*1024*1024:  # 512 MB
        raise ValidationError(u'Файл слишком большой: максимум 512 МБ.')


def validate_image_extension(value):
    if not value.name.lower().endswith(('.png', '.jpg', '.jpeg')):
        raise ValidationError(u'Неверный тип файла: только PNG, JPG или JPEG.')
    if value.size > 5*1024*1024:  # 5 MB
        raise ValidationError(u'Фото-обложка слишком большая: максимум 5 МБ.')


class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    cover = models.ImageField(upload_to='books/covers/', null=True, blank=True, validators=[validate_image_extension])
    id = models.AutoField(primary_key=True)
    pdf = models.FileField(upload_to='books/pdfs/', validators=[validate_file_extension])

    def __str__(self):
        return self.title

    def delete(self, *args, **kwargs):
        self.pdf.delete()
        self.cover.delete()
        super().delete(*args, **kwargs)
