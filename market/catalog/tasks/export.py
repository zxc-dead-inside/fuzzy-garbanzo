from celery import shared_task
from openpyxl import Workbook
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from datetime import datetime
from market.catalog.models import Product


@shared_task
def generate_product_xls():
    wb = Workbook()
    ws = wb.active
    ws.title = "Product"
    ws.append(["ID", "Name", "Price", "Category"])

    for product in Product.objects.select_related("category").all():
        ws.append([
            product.id,
            product.name,
            product.price,
            product.category.name if product.category else ""
        ])

    filename = f"exports/products_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    file_obj = ContentFile(b"")
    wb.save(file_obj)
    default_storage.save(filename, file_obj)
    return filename
