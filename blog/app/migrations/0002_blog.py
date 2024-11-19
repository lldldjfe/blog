# Generated by Django 5.1.1 on 2024-10-16 13:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('image', models.ImageField(upload_to='blogs')),
                ('description', models.TextField()),
                ('full_text', models.TextField()),
                ('date', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
