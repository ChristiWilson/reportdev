# Generated by Django 2.1.8 on 2019-05-19 22:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reportapp', '0003_auto_20190519_1544'),
    ]

    operations = [
        migrations.AddField(
            model_name='glossary',
            name='abbrev_text',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
