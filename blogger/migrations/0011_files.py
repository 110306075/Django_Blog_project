# Generated by Django 5.0.3 on 2024-04-07 10:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogger', '0010_review'),
    ]

    operations = [
        migrations.CreateModel(
            name='Files',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.FileField(upload_to='iamge')),
            ],
        ),
    ]
