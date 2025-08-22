from django.db import models

# Create your models here.

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Product(BaseModel):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    qty = models.IntegerField()
    is_deleted = models.BooleanField(default=False)
    cat = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='inventarios')
    def __str__(self):
        return self.name


class Category(BaseModel):
    name = models.CharField(max_length=255)
    desc = models.TextField()
    def __str__(self):
        return self.name