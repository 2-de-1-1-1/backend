# Generated by Django 4.2.7 on 2023-11-09 09:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0003_merge_20231109_1708'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='tech_stack',
            field=models.ManyToManyField(through='data.CompanyTechMapping', to='data.techstack'),
        ),
    ]
