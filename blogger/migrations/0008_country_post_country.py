# Generated by Django 5.0.3 on 2024-03-29 06:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogger', '0007_address_author_address'),
    ]

    operations = [
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('code', models.CharField(max_length=10)),
            ],
        ),
        migrations.AddField(
            model_name='post',
            name='country',
            field=models.ManyToManyField(to='blogger.country'),
        ),
    ]