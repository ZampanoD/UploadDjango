# Generated by Django 4.2.8 on 2023-12-06 15:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('files', '0003_task_alter_book_id'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Task',
        ),
        migrations.AlterField(
            model_name='book',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
