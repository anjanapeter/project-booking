# Generated by Django 5.1.4 on 2024-12-12 13:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_customuser'),
    ]

    operations = [
        migrations.AddField(
            model_name='hall',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='hall_images/'),
        ),
        migrations.AddField(
            model_name='hall',
            name='is_booked',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='hall',
            name='name',
            field=models.CharField(max_length=255),
        ),
        migrations.DeleteModel(
            name='CustomUser',
        ),
    ]
