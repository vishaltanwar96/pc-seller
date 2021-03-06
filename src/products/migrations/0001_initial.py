# Generated by Django 3.2.3 on 2021-05-22 16:14

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cpu_company', models.CharField(choices=[('Intel', 'Intel'), ('AMD', 'AMD')], max_length=7, verbose_name='CPU Company')),
                ('ram_capacity', models.IntegerField(choices=[(8, 'Gigs 8'), (16, 'Gigs 16'), (32, 'Gigs 32'), (64, 'Gigs 64'), (124, 'Gigs 124')], verbose_name='RAM Capacity')),
                ('secondary_memory', models.CharField(choices=[('HDD', 'Hard Disk Drive'), ('SSD', 'Solid State Drive')], max_length=3, verbose_name='Secondary Memory Capacity')),
                ('secondary_storage', models.CharField(choices=[('256 GB', 'Gigabyte 256'), ('512 GB', 'Gigabyte 512'), ('1 TB', 'Terrabyte 1'), ('2 TB', 'Terrabyte 2')], max_length=6, verbose_name='Secondary Storage Capacity')),
                ('external_cooling', models.BooleanField(verbose_name='Is External Cooling Required?')),
                ('case', models.CharField(max_length=255, verbose_name='Case Name')),
                ('psu', models.CharField(max_length=255, verbose_name='PSU Name')),
                ('motherboard', models.CharField(max_length=255, verbose_name='Motherboard Name')),
            ],
        ),
    ]
