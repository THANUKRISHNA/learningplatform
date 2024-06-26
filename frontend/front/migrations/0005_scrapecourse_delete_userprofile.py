# Generated by Django 5.0.3 on 2024-04-27 06:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('front', '0004_userprofile'),
    ]

    operations = [
        migrations.CreateModel(
            name='ScrapeCourse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('num_modules', models.PositiveIntegerField(default=0)),
                ('image', models.ImageField(default='default.jpg', upload_to='scraped_course_images/')),
            ],
        ),
        migrations.DeleteModel(
            name='UserProfile',
        ),
    ]
