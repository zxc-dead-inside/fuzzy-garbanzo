from django.db import models
from django.urls import reverse
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill

from market.catalog.managers import ProductManager


class Category(models.Model):
    """Hierarchical tree of catalog categories"""
    name = models.CharField('Name', max_length=200)
    slug = models.SlugField('URL', unique=True)
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children',
        verbose_name='Parent category'
    )
    description = models.TextField('Description', blank=True)
    image = models.ImageField('Image', upload_to='categories/', blank=True)
    is_active = models.BooleanField('Active', default=True)
    sort_order = models.PositiveIntegerField('Sort order', default=0)
    created_at = models.DateTimeField('Created at', auto_now_add=True)
    updated_at = models.DateTimeField('Updated at', auto_now=True)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ['sort_order', 'name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('catalog:category_detail', kwargs={'slug': self.slug})

    def get_children(self):
        """Get active child categories"""
        return self.children.filter(is_active=True)

    def get_all_children(self):
        """Get all child categories recursively"""
        children = []
        for child in self.children.all():
            children.append(child)
            children.extend(child.get_all_children())
        return children

    def get_full_path(self):
        """Get the full path of the category"""
        parts = [self.name]
        parent = self.parent
        while parent:
            parts.append(parent.name)
            parent = parent.parent
        return ' / '.join(reversed(parts))

    def get_level(self):
        """Get the nesting level of the category"""
        level = 0
        parent = self.parent
        while parent:
            level += 1
            parent = parent.parent
        return level

    def is_root(self):
        """Check if the category is a root category"""
        return self.parent is None

    def is_leaf(self):
        """Check if the category is a leaf (has no children)"""
        return not self.children.exists()

    def get_root(self):
        """Get the root category"""
        if self.is_root():
            return self
        return self.parent.get_root()

    def get_siblings(self):
        """Get categories at the same level"""
        if self.parent:
            return self.parent.children.exclude(id=self.id)
        else:
            return Category.objects.filter(parent=None).exclude(id=self.id)

    @classmethod
    def get_root_categories(cls):
        """Get all root categories"""
        return cls.objects.filter(parent=None, is_active=True)

    def get_breadcrumbs(self):
        """Get breadcrumbs"""
        breadcrumbs = []
        current = self
        while current:
            breadcrumbs.insert(0, current)
            current = current.parent
        return breadcrumbs


class Product(models.Model):
    """Catalog product"""
    name = models.CharField('Name', max_length=255)
    slug = models.SlugField('URL', unique=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='products',
        verbose_name='Category'
    )
    description = models.TextField('Description', blank=True)
    price = models.DecimalField('Price', max_digits=10, decimal_places=2)
    image = models.ImageField('Image', upload_to='products/', blank=True)
    spec_file = models.FileField('Specification',
                                 upload_to='products/specs/', blank=True)
    is_active = models.BooleanField('Active', default=True)
    created_at = models.DateTimeField('Created at', auto_now_add=True)
    updated_at = models.DateTimeField('Updated at', auto_now=True)

    image_preview = ImageSpecField(
        source='image',
        processors=[ResizeToFill(100, 100)],
        format='JPEG',
        options={'quality': 70}
    )

    objects = ProductManager()

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('catalog:product_detail', kwargs={'slug': self.slug})
