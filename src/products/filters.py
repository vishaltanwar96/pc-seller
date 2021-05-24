from django_filters import rest_framework as filters

from products.models import Product


class ProductFilterSet(filters.FilterSet):

    class Meta:
        model = Product
        fields = {
            'cpu_company': ['exact'],
            'ram_capacity': ['gt', 'lt', 'exact'],
            'secondary_memory': ['exact'],
            'secondary_storage': ['gt', 'lt', 'exact'],
            'external_cooling': ['exact'],
            'case': ['icontains'],
            'psu': ['icontains'],
            'motherboard': ['icontains'],
        }
