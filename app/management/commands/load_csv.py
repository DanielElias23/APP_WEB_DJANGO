import os
import csv
from django.core.management.base import BaseCommand
from app.models import (
    brands, categories, customers, order_items, orders,
    products, staffs, stocks, stores
)
from datetime import datetime

date_format = "%Y-%m-%d"

class Command(BaseCommand):
    help = 'Carga archivos CSV desde la carpeta /datos en la base de datos, actualizando registros existentes'

    def handle(self, *args, **kwargs):
        # Ruta a la carpeta de datos
        data_folder = os.path.join(os.path.dirname(__file__), '../../../datos')

        # Mapeo de nombres de archivo a modelos
        file_model_map = {
            'brands.csv': brands,
            'categories.csv': categories,
            'customers.csv': customers,
            'order_items.csv': order_items,
            'orders.csv': orders,
            'products.csv': products,
            'staffs.csv': staffs,
            'stocks.csv': stocks,
            'stores.csv': stores,
        }

        # Iterar sobre todos los archivos en la carpeta
        for filename in os.listdir(data_folder):
            if filename in file_model_map:
                model = file_model_map[filename]
                file_path = os.path.join(data_folder, filename)
                self.stdout.write(f'Loading {filename} into {model.__name__}...')

                with open(file_path, newline='', encoding='utf-8') as csvfile:
                    reader = csv.DictReader(csvfile)
                    for row in reader:
                        if model == brands:
                            brand_id = int(row["brand_id"]) if row["brand_id"] and row["brand_id"] != 'NULL' else None
                            defaults = {
                                'brand_name': str(row["brand_name"]) if row["brand_name"] and row["brand_name"] != 'NULL' else None
                            }
                            qs = model.objects.filter(brand_id=brand_id)
                            if qs.exists():
                                qs.update(**defaults)
                                obj = qs.first()
                                created = False
                            else:
                                obj = model.objects.create(brand_id=brand_id, **defaults)
                                created = True

                        elif model == categories:
                            category_id = int(row["category_id"]) if row["category_id"] and row["category_id"] != 'NULL' else None
                            defaults = {
                                'category_name': str(row["category_name"]) if row["category_name"] and row["category_name"] != 'NULL' else None
                            }
                            qs = model.objects.filter(category_id=category_id)
                            if qs.exists():
                                qs.update(**defaults)
                                obj = qs.first()
                                created = False
                            else:
                                obj = model.objects.create(category_id=category_id, **defaults)
                                created = True

                        elif model == customers:
                            customer_id = int(row["customer_id"]) if row["customer_id"] and row["customer_id"] != 'NULL' else None
                            defaults = {
                                'first_name': str(row["first_name"]) if row["first_name"] and row["first_name"] != 'NULL' else None,
                                'last_name': str(row["last_name"]) if row["last_name"] and row["last_name"] != 'NULL' else None,
                                'phone': str(row["phone"]) if row["phone"] and row["phone"] != 'NULL' else None,
                                'email': str(row["email"]) if row["email"] and row["email"] != 'NULL' else None,
                                'street': str(row["street"]) if row["street"] and row["street"] != 'NULL' else None,
                                'city': str(row["city"]) if row["city"] and row["city"] != 'NULL' else None,
                                'state': str(row["state"]) if row["state"] and row["state"] != 'NULL' else None,
                                'zip_code': int(row["zip_code"]) if row["zip_code"] and row["zip_code"] != 'NULL' else None
                            }
                            qs = model.objects.filter(customer_id=customer_id)
                            if qs.exists():
                                qs.update(**defaults)
                                obj = qs.first()
                                created = False
                            else:
                                obj = model.objects.create(customer_id=customer_id, **defaults)
                                created = True

                        elif model == order_items:
                            # Suponemos que la combinación de order_id e item_id es única
                            key = {
                                'order_id': int(row["order_id"]) if row["order_id"] and row["order_id"] != 'NULL' else None,
                                'item_id': int(row["item_id"]) if row["item_id"] and row["item_id"] != 'NULL' else None,
                            }
                            defaults = {
                                'product_id': int(row["product_id"]) if row["product_id"] and row["product_id"] != 'NULL' else None,
                                'quantity': int(row["quantity"]) if row["quantity"] and row["quantity"] != 'NULL' else None,
                                'list_price': float(row["list_price"]) if row["list_price"] and row["list_price"] != 'NULL' else None,
                                'discount': float(row["discount"]) if row["discount"] and row["discount"] != 'NULL' else None,
                            }
                            qs = model.objects.filter(**key)
                            if qs.exists():
                                qs.update(**defaults)
                                obj = qs.first()
                                created = False
                            else:
                                obj = model.objects.create(**key, **defaults)
                                created = True

                        elif model == orders:
                            order_id = int(row["order_id"]) if row["order_id"] and row["order_id"] != 'NULL' else None
                            defaults = {
                                'customer_id': int(row["customer_id"]) if row["customer_id"] and row["customer_id"] != 'NULL' else None,
                                'order_status': int(row["order_status"]) if row["order_status"] and row["order_status"] != 'NULL' else None,
                                'order_date': str(row["order_date"]) if row["order_date"] and row["order_date"] != 'NULL' else None,
                                'required_date': str(row["required_date"]) if row["required_date"] and row["required_date"] != 'NULL' else None,
                                'shipped_date': str(row["shipped_date"]) if row["shipped_date"] and row["shipped_date"] != 'NULL' else None,
                                'store_id': int(row["store_id"]) if row["store_id"] and row["store_id"] != 'NULL' else None,
                                'staff_id': int(row["staff_id"]) if row["staff_id"] and row["staff_id"] != 'NULL' else None,
                            }
                            qs = model.objects.filter(order_id=order_id)
                            if qs.exists():
                                qs.update(**defaults)
                                obj = qs.first()
                                created = False
                            else:
                                obj = model.objects.create(order_id=order_id, **defaults)
                                created = True

                        elif model == products:
                            product_id = int(row["product_id"]) if row["product_id"] and row["product_id"] != 'NULL' else None
                            defaults = {
                                'brand_id': int(row["brand_id"]) if row["brand_id"] and row["brand_id"] != 'NULL' else None,
                                'category_id': int(row["category_id"]) if row["category_id"] and row["category_id"] != 'NULL' else None,
                                'model_year': int(row["model_year"]) if row["model_year"] and row["model_year"] != 'NULL' else None,
                                'list_price': float(row["list_price"]) if row["list_price"] and row["list_price"] != 'NULL' else None,
                                'product_name': str(row["product_name"]) if row["product_name"] and row["product_name"] != 'NULL' else None,
                            }
                            qs = model.objects.filter(product_id=product_id)
                            if qs.exists():
                                qs.update(**defaults)
                                obj = qs.first()
                                created = False
                            else:
                                obj = model.objects.create(product_id=product_id, **defaults)
                                created = True

                        elif model == staffs:
                            staff_id = int(row["staff_id"]) if row["staff_id"] and row["staff_id"] != 'NULL' else None
                            defaults = {
                                'first_name': str(row["first_name"]) if row["first_name"] and row["first_name"] != 'NULL' else None,
                                'last_name': str(row["last_name"]) if row["last_name"] and row["last_name"] != 'NULL' else None,
                                'email': str(row["email"]) if row["email"] and row["email"] != 'NULL' else None,
                                'phone': str(row["phone"]) if row["phone"] and row["phone"] != 'NULL' else None,
                                'active': int(row["active"]) if row["active"] and row["active"] != 'NULL' else None,
                                'store_id': int(row["store_id"]) if row["store_id"] and row["store_id"] != 'NULL' else None,
                                'manager_id': int(row["manager_id"]) if row["manager_id"] and row["manager_id"] != 'NULL' else None,
                            }
                            qs = model.objects.filter(staff_id=staff_id)
                            if qs.exists():
                                qs.update(**defaults)
                                obj = qs.first()
                                created = False
                            else:
                                obj = model.objects.create(staff_id=staff_id, **defaults)
                                created = True

                        elif model == stocks:
                            key = {
                                'store_id': int(row["store_id"]) if row["store_id"] and row["store_id"] != 'NULL' else None,
                                'product_id': int(row["product_id"]) if row["product_id"] and row["product_id"] != 'NULL' else None,
                            }
                            defaults = {
                                'quantity': int(row["quantity"]) if row["quantity"] and row["quantity"] != 'NULL' else None,
                            }
                            qs = model.objects.filter(**key)
                            if qs.exists():
                                qs.update(**defaults)
                                obj = qs.first()
                                created = False
                            else:
                                obj = model.objects.create(**key, **defaults)
                                created = True

                        elif model == stores:
                            store_id = int(row["store_id"]) if row["store_id"] and row["store_id"] != 'NULL' else None
                            defaults = {
                                'store_name': str(row["store_name"]) if row["store_name"] and row["store_name"] != 'NULL' else None,
                                'phone': str(row["phone"]) if row["phone"] and row["phone"] != 'NULL' else None,
                                'email': str(row["email"]) if row["email"] and row["email"] != 'NULL' else None,
                                'street': str(row["street"]) if row["street"] and row["street"] != 'NULL' else None,
                                'city': str(row["city"]) if row["city"] and row["city"] != 'NULL' else None,
                                'state': str(row["state"]) if row["state"] and row["state"] != 'NULL' else None,
                                'zip_code': str(row["zip_code"]) if row["zip_code"] and row["zip_code"] != 'NULL' else None,
                            }
                            qs = model.objects.filter(store_id=store_id)
                            if qs.exists():
                                qs.update(**defaults)
                                obj = qs.first()
                                created = False
                            else:
                                obj = model.objects.create(store_id=store_id, **defaults)
                                created = True

                self.stdout.write(self.style.SUCCESS(f'Successfully loaded {filename}'))

