# Generated by Django 4.2.7 on 2023-11-09 07:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='welfare',
            field=models.ManyToManyField(through='data.CompanyWelfareMapping', to='data.welfare'),
        ),
        migrations.AlterField(
            model_name='company',
            name='loc_info_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='data.locationinfo'),
        ),
        migrations.AlterField(
            model_name='job',
            name='loc_info_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='data.locationinfo'),
        ),
    ]
