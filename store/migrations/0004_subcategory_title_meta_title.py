# Generated by Django 3.2.18 on 2024-09-18 17:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_brandmetatitle_categorymetatitle_productmetatitle'),
    ]

    operations = [
        migrations.AddField(
            model_name='subcategory',
            name='title_meta_title',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
