# pc-seller
A Sample PC Seller Backend

# Running project locally

```shell
git clone https://github.com/vishaltanwar96/pc-seller.git
cd pc-seller
python3.9 -m venv venv
pip install -r requirements.txt
source venv/bin/activate
```

Rename ```.env.sample``` to ```.env``` and add proper values to all the given variables

Migrate changes to database and serve the application locally
```shell
cd src
python manage.py migrate
python manage.py runserver
```
Create admin user using
```shell
python manage.py createsuperuser
```

APIs are accessible at following endpoints:
```shell
[POST] localhost:8000/api/users/register/ (For non admin user registration)
[POST] localhost:8000/api/users/login/ (Generating token for authentication)
[GET] localhost:8000/api/products/ (Listing all products)
[POST] localhost:8000/api/products/ (Create a product)
[GET] localhost:8000/api/products/:id/ (Get a single product)
[PUT] localhost:8000/api/products/:id/ (Update a product)
[PATCH] localhost:8000/api/products/:id/ (Update a product)
[DELETE] localhost:8000/api/products/:id/ (Delete a product)
```

# Running tests
```shell
python manage.py test --verbosity 2
```