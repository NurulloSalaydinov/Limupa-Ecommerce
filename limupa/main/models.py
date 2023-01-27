from django.db import models
from ckeditor.fields import RichTextField


class Brand(models.Model):
    title = models.CharField(max_length=255, verbose_name='Brend')
    slug = models.SlugField('*', unique=True)
    
    def __str__(self):
        return f"{self.title}"


class Category(models.Model):
    title = models.CharField(max_length=255, verbose_name='Kategoriya')
    slug = models.SlugField('*', unique=True)
    
    def __str__(self):
        return f"{self.title}"


class Tag(models.Model):
    title = models.CharField(max_length=255, verbose_name='Teg')
    slug = models.SlugField('*', unique=True)
    
    def __str__(self):
        return f"{self.title}"


class Color(models.Model):
    title = models.CharField(max_length=255, verbose_name='Rang')
    color_code = models.CharField('Rang nomi inglizcha yoki kod (#000)', max_length=255)
    
    def __str__(self):
        return f"{self.title}"


class Banner(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField('Banner sarlavhasi', max_length=255)
    subtitle = models.CharField('Banner sub sarlavhasi', max_length=255)
    text = models.CharField('Banner Text', max_length=255)
    image = models.ImageField('Banner rasmi', upload_to='banner/%y/%m/%d/')
    
    def __str__(self):
        return f"{self.title}"


class SubBanner(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField('Banner sarlavhasi', max_length=255)
    image = models.ImageField('Banner rasmi', upload_to='banner/%y/%m/%d/')
    
    def __str__(self):
        return f"{self.title}"


# class AdditionalData(models.Model):
#     title = models.CharField(max_length=255, verbose_name='Sarlavha')
#     data_value = models.CharField(max_length=255, verbose_name='Qiymati')
#     cost = models.IntegerField(default=0, verbose_name='Qoshimcha narx')

#     def __str__(self):
#         return f"{self.title}"

class ProductImage(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='product_images/%y/%m/%d/')


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    color = models.ForeignKey(Color, on_delete=models.CASCADE)
    tag = models.ManyToManyField(Tag)
    images = models.ManyToManyField(ProductImage)
    title = models.CharField(max_length=255)
    slug = models.SlugField('*', unique=True)
    cost = models.FloatField(default=0)
    discount = models.IntegerField(default=0)
    base_count = models.IntegerField(default=1, verbose_name='Bazadagi soni')
    description = RichTextField()
    rating_count = models.IntegerField(default=0)
    poster = models.ImageField(upload_to='posters/%y/%m/%d/')
    
    def get_cost(self):
        return self.cost * (( 100 - self.discount ) / 100)

    def get_rating(self):
        count = Review.objects.filter(product__id=self.id).count()
        if count:
            return round(self.rating_count / count, 2)
        else:
            return 0

    def __str__(self):
        return f"{self.title}"


class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    name = models.CharField(max_length=155)
    review = models.TextField(max_length=355)
    email = models.EmailField()
    rating = models.IntegerField(default=0)
    
    def __str__(self):
        return f"{self.name}"
