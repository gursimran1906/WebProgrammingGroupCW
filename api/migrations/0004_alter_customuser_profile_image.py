# Generated by Django 4.2.5 on 2023-12-14 01:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_customuser_alter_category_id_alter_comment_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='profile_image',
            field=models.ImageField(default='default.jpg', null=True, upload_to='media/profile_images/'),
        ),
    ]
