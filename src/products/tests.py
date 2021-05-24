from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

from products.models import Product
from products.serializers import ProductSerializer

User = get_user_model()


class ProductAPITests(APITestCase):

    def setUp(self):

        self.admin_email = "vishal.tanwar@somedomain.com"
        self.admin_password = "StrongPassword#!8928&"
        self.non_admin_email = "someuser@somedomain.com"
        self.non_admin_password = self.admin_password
        self.product_list_url = reverse("product-list")
        self.admin_user = User.objects.create_superuser(
            first_name="Vishal", last_name="Tanwar", email=self.admin_email, password=self.admin_password
        )
        self.user = User.objects.create_superuser(
            first_name="SomeFirstName",
            last_name="SomeLastName",
            email=self.non_admin_email,
            password=self.non_admin_password,
        )
        self.token = Token.objects.create(user=self.admin_user)

    def test_list_all_products_api(self):

        Product.objects.create(
            cpu_company=Product.INTEL,
            ram_capacity=Product.RAMCapacity.GIGS_32,
            secondary_memory=Product.SecondaryMemoryType.SOLID_STATE_DRIVE,
            secondary_storage=Product.SecondaryStorageCapacity.GIGABYTE_512,
            external_cooling=True,
            case="Full Tower",
            psu="ATX–EPS",
            motherboard="Intel Galileo Gen 2 Development Board",
        )
        Product.objects.create(
            cpu_company=Product.INTEL,
            ram_capacity=Product.RAMCapacity.GIGS_64,
            secondary_memory=Product.SecondaryMemoryType.HARD_DISK_DRIVE,
            secondary_storage=Product.SecondaryStorageCapacity.GIGABYTE_256,
            external_cooling=False,
            case="Slim Line Case",
            psu="CFX12V",
            motherboard="Gigabyte GA-F2A58M-DS2",
        )

        response = self.client.get(self.product_list_url)
        self.assertEqual(response.data, ProductSerializer(instance=Product.objects.all(), many=True).data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Product.objects.all().count(), 2)

    def test_product_detail(self):

        product = Product.objects.create(
            cpu_company=Product.INTEL,
            ram_capacity=Product.RAMCapacity.GIGS_64,
            secondary_memory=Product.SecondaryMemoryType.HARD_DISK_DRIVE,
            secondary_storage=Product.SecondaryStorageCapacity.GIGABYTE_256,
            external_cooling=False,
            case="Slim Line Case",
            psu="CFX12V",
            motherboard="Gigabyte GA-F2A58M-DS2",
        )
        url = reverse("product-detail", kwargs={"pk": product.pk})
        response = self.client.get(url)
        self.assertEqual(response.data, ProductSerializer(instance=product).data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_product_admin_accessible_endpoints_without_admin_credentials(self):

        product_detail_url = reverse("product-detail", kwargs={"pk": 1})

        self.assertEqual(self.client.post(self.product_list_url, data={}).status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(self.client.put(product_detail_url, data={}).status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(self.client.patch(product_detail_url, data={}).status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(self.client.delete(product_detail_url).status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_product(self):

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.post(
            self.product_list_url,
            data={
                "cpu_company": "Intel",
                "ram_capacity": 32,
                "secondary_memory": "SSD",
                "secondary_storage": 512,
                "external_cooling": True,
                "case": "Full Tower",
                "psu": "ATX–EPS",
                "motherboard": "Intel Galileo Gen 2 Development Board",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, ProductSerializer(instance=Product.objects.get()).data)
        self.assertEqual(Product.objects.all().count(), 1)

    def test_delete_product(self):

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        product = Product.objects.create(
            cpu_company=Product.INTEL,
            ram_capacity=Product.RAMCapacity.GIGS_64,
            secondary_memory=Product.SecondaryMemoryType.HARD_DISK_DRIVE,
            secondary_storage=Product.SecondaryStorageCapacity.GIGABYTE_256,
            external_cooling=False,
            case="Slim Line Case",
            psu="CFX12V",
            motherboard="Gigabyte GA-F2A58M-DS2",
        )
        product_detail_url = reverse('product-detail', kwargs={'pk': product.pk})
        response = self.client.delete(product_detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        with self.assertRaises(Product.DoesNotExist):
            Product.objects.get()

    def test_update_product(self):

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        product = Product.objects.create(
            cpu_company=Product.INTEL,
            ram_capacity=Product.RAMCapacity.GIGS_64,
            secondary_memory=Product.SecondaryMemoryType.HARD_DISK_DRIVE,
            secondary_storage=Product.SecondaryStorageCapacity.GIGABYTE_256,
            external_cooling=False,
            case="Slim Line Case",
            psu="CFX12V",
            motherboard="Gigabyte GA-F2A58M-DS2",
        )
        product_detail_url = reverse('product-detail', kwargs={'pk': product.pk})
        response = self.client.patch(product_detail_url, data={'external_cooling': True})
        self.assertEqual(response.data, ProductSerializer(instance=Product.objects.get()).data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.put(
            product_detail_url,
            data={
                'cpu_company': 'Intel',
                'ram_capacity': 64,
                'secondary_memory': 'HDD',
                'secondary_storage': 256,
                'external_cooling': False,
                'case': "Long Line Case",
                'psu': "CFVX12V-MAX",
                'motherboard': "Gigabyte FX-F2123A58M-Gen2",
            }
        )
        self.assertEqual(response.data, ProductSerializer(instance=Product.objects.get()).data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_product_validation(self):

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.post(
            self.product_list_url,
            data={
                'cpu_company': 'Random CPU Company',
                'ram_capacity': 2048,
                'secondary_memory': 'Some Memory',
                'secondary_storage': 4096,
                'external_cooling': False,
                'case': "Long Line Case",
                'psu': "CFVX12V-MAX",
                'motherboard': "Gigabyte FX-F2123A58M-Gen2",
            }
        )

        self.assertEqual(
            response.data,
            {
                "cpu_company": ["\"Random CPU Company\" is not a valid choice."],
                "ram_capacity": ["\"2048\" is not a valid choice."],
                "secondary_memory": ["\"Some Memory\" is not a valid choice."],
                "secondary_storage": ["\"4096\" is not a valid choice."]
            }
        )

        response = self.client.post(
            self.product_list_url,
            data={
                'cpu_company': 'Intel',
                'ram_capacity': 64,
                'secondary_memory': 'SSD',
                'secondary_storage': 1024,
                'external_cooling': False,
                'case': "Long Line Case",
                'psu': "CFVX12V-MAX",
                'motherboard': "Gigabyte FX-F2123A58M-Gen2",
            }
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data,
            {
                "non_field_errors": [
                    "Selected combination is invalid -> (SSD & Secondary Storage > 512GB) or (CPU AMD & RAM > 32 GB)"
                ]
            }
        )
        response = self.client.post(
            self.product_list_url,
            data={
                'cpu_company': 'AMD',
                'ram_capacity': 64,
                'secondary_memory': 'HDD',
                'secondary_storage': 1024,
                'external_cooling': False,
                'case': "Long Line Case",
                'psu': "CFVX12V-MAX",
                'motherboard': "Gigabyte FX-F2123A58M-Gen2",
            }
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data,
            {
                "non_field_errors": [
                    "Selected combination is invalid -> (SSD & Secondary Storage > 512GB) or (CPU AMD & RAM > 32 GB)"
                ]
            }
        )
