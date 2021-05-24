from rest_framework.serializers import ModelSerializer
from rest_framework.exceptions import ValidationError

from products.models import Product


class ProductSerializer(ModelSerializer):

    def validate(self, attrs):

        if (
            attrs.get("secondary_memory") == Product.SecondaryMemoryType.SOLID_STATE_DRIVE
            and
            attrs.get("secondary_storage") > Product.SecondaryStorageCapacity.GIGABYTE_512
        ) or (
            attrs.get("cpu_company") == Product.AMD
            and
            attrs.get("ram_capacity") > Product.RAMCapacity.GIGS_32
        ):
            raise ValidationError(
                detail="Selected combination is invalid -> (SSD & Secondary Storage > 512GB) or (CPU AMD & RAM > 32 GB)"
            )

        return attrs

    class Meta:

        model = Product
        fields = "__all__"
