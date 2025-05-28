import logging
from typing import Any

from django.core.management.base import BaseCommand
from django.db import connections, transaction
from tqdm import tqdm

from market.catalog.models import Product, Category

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Import products from external SQLite table `external_products`."

    def add_arguments(self, parser):
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Run the import without saving any data",
        )

    def handle(self, *args: Any, **options: Any):
        dry_run = options["dry_run"]

        self.stdout.write("Starting product import from SQLite...")
        rows = self.fetch_data()
        if not rows:
            self.stdout.write(self.style.WARNING("No data to import."))
            return

        created, updated, skipped = self.import_rows(rows, dry_run)

        self.stdout.write(self.style.SUCCESS(
            f"Import complete. Created: {created}, "
            f"Updated: {updated}, Skipped: {skipped}."
        ))

    def fetch_data(self):
        try:
            cursor = connections["external"].cursor()
            cursor.execute("""
                SELECT p.slug, p.name, p.description, p.price, c.slug
                as category_slug
                FROM catalog_product p
                JOIN catalog_category c ON p.category_id = c.id
            """)
            return cursor.fetchall()
        except Exception as e:
            logger.exception("Failed to read from SQLite")
            self.stderr.write(self.style.ERROR(f"SQLite read error: {e}"))
            return []

    def import_rows(self, rows, dry_run=False):
        created = updated = skipped = 0

        with (transaction.atomic()):
            for slug, name, description, price, category_slug in tqdm(rows, desc="Processing"):
                category = Category.objects.filter(slug=category_slug).first()
                if not category:
                    self.stderr.write(f"Category '{category_slug}'"
                                      f" not found. Skipping.")
                    skipped += 1
                    continue

                defaults = {
                    "name": name,
                    "description": description,
                    "price": price,
                    "category": category,
                    "is_active": True,
                }

                if dry_run:
                    exists = Product.objects.filter(slug=slug).exists()
                    if exists:
                        updated += 1
                    else:
                        created += 1
                else:
                    product, created_flag = Product.objects.update_or_create(
                        slug=slug,
                        defaults=defaults,
                    )
                    if created_flag:
                        created += 1
                    else:
                        updated += 1

            if dry_run:
                self.stdout.write(self.style.NOTICE(
                    "Dry run mode — no data was saved."))
                transaction.set_rollback(True)

        return created, updated, skipped
