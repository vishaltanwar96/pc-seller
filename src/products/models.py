from django.db import models
from django.utils.translation import gettext_lazy as _


class Product(models.Model):

    INTEL = 'Intel'
    AMD = 'AMD'
    CPU_COMPANY = [
        (INTEL, INTEL),
        (AMD, AMD),
    ]

    class RAMCapacity(models.IntegerChoices):

        GIGS_8 = 8, '8 GB'
        GIGS_16 = 16, '16 GB'
        GIGS_32 = 32, '32 GB'
        GIGS_64 = 64, '64 GB'
        GIGS_128 = 128, '128 GB'

    class SecondaryMemoryType(models.TextChoices):

        HARD_DISK_DRIVE = 'HDD'
        SOLID_STATE_DRIVE = 'SSD'

    class SecondaryStorageCapacity(models.IntegerChoices):

        GIGABYTE_256 = 256, '256 GB'
        GIGABYTE_512 = 512, '512 GB'
        TERRABYTE_1 = 1024, '1 TB'
        TERRABYTE_2 = 2048, '2 TB'

    cpu_company = models.CharField(_('CPU Company'), max_length=7, choices=CPU_COMPANY)
    ram_capacity = models.IntegerField(_('RAM Capacity'), choices=RAMCapacity.choices)
    secondary_memory = models.CharField(_('Secondary Memory Type'), max_length=3, choices=SecondaryMemoryType.choices)
    secondary_storage = models.IntegerField(_('Secondary Storage Capacity'), choices=SecondaryStorageCapacity.choices)
    external_cooling = models.BooleanField(_('Is External Cooling Required?'))
    case = models.CharField(_('Case Name'), max_length=255)
    psu = models.CharField(_('PSU Name'), max_length=255)
    motherboard = models.CharField(_('Motherboard Name'), max_length=255)
