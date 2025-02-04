from django.contrib.postgres.fields import ArrayField
from django.db import models
import random

# Create your models here.
class Category(models.Model):
    title = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = 'Categories'
    def __str__(self):
        return self.title

class Negocios(models.Model):
    name = models.CharField(max_length=100)
    cat_name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to ='uploads/', blank=True, null=True)
    date_created = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ['-date_created']

    def __str__(self):
        return self.name

class Contact(models.Model):
    name = models.CharField(max_length=255)
    mail = models.EmailField(max_length = 254)
    description = models.TextField()

    def __str__(self):
        return self.name


class Competencia(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to ='uploads/', blank=True, null=True)
    date_created = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ['-date_created']
    def __str__(self):
        return self.title

def random_string():
      return str(random.randint(1000000, 99999999))

class Producto(models.Model):
    name = models.CharField(max_length=155)
    description = models.TextField()
    price = models.IntegerField()
    negocio_parent = models.ForeignKey(Negocios, on_delete=models.CASCADE, null=True)
    buy_order = models.CharField(default=random_string, max_length=100)
    session_id = models.CharField(default=random_string, max_length=100)
    image = models.ImageField(upload_to ='uploads/', blank=True, null=True)
    date_created = models.DateField(auto_now_add=True)
    token = models.CharField(max_length=500, blank=True, null=True)
    url = models.CharField(max_length=500, blank=True, null=True)
    token_ws = models.CharField(max_length=500, blank=True, null=True)


    def __str__(self):
        return self.name

class ProductoImage(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, null=True)
    image = models.ImageField(upload_to ='uploads/', blank=True, null=True)

class Cart(models.Model):
    name = models.CharField(max_length=155, blank=True, null=True)
    total_price = models.IntegerField(blank=True, null=True) ##change name to amount then fetch
    buy_order = models.CharField(default=random_string, max_length=100)
    session_id = models.CharField(default=random_string, max_length=100)
    # date_created = models.DateField(auto_now_add=True)
    token = models.CharField(max_length=500, blank=True, null=True)
    url = models.CharField(max_length=500, blank=True, null=True)
    token_ws = models.CharField(max_length=500, blank=True, null=True)

class Token(models.Model):
    token_ws = models.TextField(blank=True, null=True)

class PurchaseData(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    mail = models.EmailField(max_length = 254, blank=True, null=True)
    info = models.TextField(blank=True, null=True)
    direccion = models.CharField(max_length=255, blank=True, null=True)
    telefono = models.CharField(max_length=255, blank=True, null=True)
    total_price = models.IntegerField(blank=True, null=True) ##change name to amount then fetch
    buy_order = models.CharField(blank=True, null=True, max_length=100)
    session_id = models.CharField(blank=True, null=True, max_length=100)
    token_ws = models.CharField(max_length=500, blank=True, null=True)
    status = models.CharField(max_length=500, blank=True, null=True)
    items = ArrayField(ArrayField(models.CharField(max_length=1000, blank=True)), blank=True, null=True)
    def __str__(self):
        return self.name
    

###ENCALBUCO MODELS API###

class ECCategoria(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = 'ECCategories'
    def __str__(self):
        return self.name

#NEGOCIO
class ECNegocios(models.Model):
    name = models.CharField(max_length=100)
    cat_name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to ='uploads/negocios', blank=True, null=True)
    categoria = models.ForeignKey(ECCategoria, on_delete=models.CASCADE, null=True)
    date_created = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ['-date_created']

    def __str__(self):
        return self.name


#PRODUCTOS DEL NEGOCIO

class ECProducto(models.Model):
    name = models.CharField(max_length=155)
    description = models.TextField()
    price = models.IntegerField()
    ecnegocio_parent = models.ForeignKey(ECNegocios, on_delete=models.CASCADE, null=True, related_name='hijos')
    buy_order = models.CharField(default=random_string, max_length=100)
    session_id = models.CharField(default=random_string, max_length=100)
    image = models.ImageField(upload_to ='uploads/productos', blank=True, null=True)
    date_created = models.DateField(auto_now_add=True)
    token = models.CharField(max_length=500, blank=True, null=True)
    url = models.CharField(max_length=500, blank=True, null=True)
    token_ws = models.CharField(max_length=500, blank=True, null=True)


    def __str__(self):
        return self.name

#CONTACT FORM
class ECContact(models.Model):
    name = models.CharField(max_length=255)
    mail = models.EmailField(max_length = 254)
    description = models.TextField()

    def __str__(self):
        return self.name
