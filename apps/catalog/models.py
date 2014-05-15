# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import Site
from mptt.models import MPTTModel, TreeForeignKey, TreeManyToManyField
from autoslug import AutoSlugField
from django.core.urlresolvers import reverse
from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver
from sorl.thumbnail import ImageField
from sorl.thumbnail.shortcuts import get_thumbnail
from django.utils.translation import ugettext as _

from common.models import Photo, SeoModel, Pos_Act
from common.utils import simple_upload_to


class SiteTowns(Pos_Act, models.Model):
    name = models.CharField(u'Название', max_length=100)
    item_name = models.CharField(u'Обозначение', max_length=100, blank=True, null=True)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ('position', 'name',)
        verbose_name = u'Город'
        verbose_name_plural = u'Города'


class Country(models.Model):
    name = models.CharField(u'Название', max_length=100)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ('name',)
        verbose_name = u'Страна'
        verbose_name_plural = u'Страны'


class Producer(SeoModel, Pos_Act, models.Model):
    name = models.CharField(u'Название', max_length=100)
    country = models.ForeignKey('Country', verbose_name=u'Страна')
    discount = models.PositiveSmallIntegerField(u'Скидка (%)', blank=True, null=True)
    image = models.ImageField(u'Логотип',
                              upload_to=simple_upload_to('image'),
                              blank=True
    )
    description = models.TextField(u'Описание')

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ('name',)
        verbose_name = u'Производитель'
        verbose_name_plural = u'Производители'
    def thumbnail(self, width=64, height=64):
        if self.image:
            thumbnail = get_thumbnail(self.image, str(width) + 'x' + str(height))
            img_resize_url = unicode(thumbnail.url)
            html = '<a style="height:%spx; display:block" class="image-picker" href="%s">' \
                   '<img src="%s" alt="%s" width="%s" height="%s" />' \
                   '</a>'
            return html % (height, self.image.url, img_resize_url, self.name, thumbnail.width, thumbnail.height)

        return '<img src="http://placehold.it/64x64" alt="False">'

    thumbnail.short_description = _('Thumbnail')
    thumbnail.allow_tags = True

class CategoryManager(models.Manager):
    def get_query_set(self):
        return super(CategoryManager, self).get_query_set().exclude(is_active=False)


class ProductManager(models.Manager):
    def get_query_set(self):
        return super(ProductManager, self).get_query_set().exclude(is_active=False)

    def get_city_object(self, city):
        qs = self.get_query_set().filter(city=city)
        return qs

# Create your models here.
class Category(MPTTModel):
    CATEGORY_TYPES = (
        ('P', 'Products'),
        ('S', 'Sub categories'),
    )
    name = models.CharField(max_length=255)
    slug = AutoSlugField(populate_from='name', unique=True, always_update=True, editable=True, blank=True,
                         help_text='Unique value for product page URL, created from name.')
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children')
    description = models.TextField(default="", blank=True)
    view = models.CharField(max_length=1, choices=CATEGORY_TYPES, default="P")
    count_products = models.IntegerField(default=0)

    is_active = models.BooleanField(default=True)
    main_page = models.BooleanField(default=True)
    image = models.ImageField(u'Лого', upload_to=simple_upload_to('image'), blank=True, null=True)
    # images = models.ForeignKey(Photo, related_name='images', verbose_name=u'Фото', blank=True, null=True, )
    images = generic.GenericRelation(Photo, verbose_name=u'Фото')
    meta_keywords = models.CharField("Meta Keywords", max_length=255, default="",
                                     help_text='Comma-delimited set of SEO keywords for meta tag',
                                     blank=True,
                                     null=True, )
    meta_description = models.CharField("Meta Description", max_length=255, default="",
                                        help_text='Content for description meta tag',
                                        blank=True,
                                        null=True, )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # managers
    objects = models.Manager()
    active = CategoryManager()

    class MPTTMeta:
        order_insertion_by = ['name']

    class Meta:
        verbose_name = u'Категория'
        verbose_name_plural = u'Категории'

    is_active.boolean = True
    is_active.short_description = 'Active'

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('catalog:category', args=[str(self.slug)])

    def get_main_page_leaf_nodes(self):
        return self.get_leafnodes().filter(is_active=True).filter(main_page=True)

    def get_leaf_nodes(self):
        return self.get_leafnodes().filter(is_active=True)

    def get_images(self):
        qs = self.images.exclude(main_image=True)
        if qs:
            return qs
        return None


class Option(MPTTModel):
    name = models.CharField(max_length=255)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children')

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['id']
        verbose_name = u'Характеристика'
        verbose_name_plural = u'Характеристики'


class OptionValue(MPTTModel):
    name = models.CharField(max_length=10)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children')

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = u'Единица измерения'
        verbose_name_plural = u'Единицы измерения'


class Product(models.Model):
    category = TreeForeignKey('Category', null=True, blank=False)
    name = models.CharField(u'Название',max_length=255)
    slug = AutoSlugField(populate_from='name', unique=True, always_update=True, editable=True, blank=True)
    intro = models.TextField(u'Короткое описание',default="")
    description = models.TextField(u'Описание',default="")
    producer = models.ForeignKey(Producer, verbose_name=u'Производитель', related_name='product_producer', blank=True,)
    image = models.ImageField(u'Главное фото',upload_to=simple_upload_to('image'), null=True, blank=True, max_length=255)
    option = TreeManyToManyField('Option', blank=True, verbose_name=u'Параметры товара')
    SKU = models.CharField(u'Артикул',max_length=64, default="", blank=True)
    price = models.DecimalField(u'Цена',max_digits=9, decimal_places=2)
    old_price = models.DecimalField(u'Старая цена',max_digits=9, decimal_places=2, blank=True, default=0.00)
    city = models.ForeignKey(SiteTowns, related_name='cities', verbose_name=u'Город', blank=True)
    site = models.ManyToManyField(Site, related_name='product_sites', verbose_name=u'Сайты', blank=True)
    is_active = models.BooleanField(u'Активный', default=True)
    is_deal = models.BooleanField(u'Лучшее предложение', default=True)
    is_popular = models.BooleanField(u'Популярный товар', default=True)
    is_novelty = models.BooleanField(u'Новинка', default=True)

    meta_keywords = models.CharField("Meta Keywords", max_length=255, default="", blank=True,
                                     help_text='Comma-delimited set of SEO keywords for meta tag')
    meta_description = models.CharField("Meta Description", max_length=255, default="", blank=True,
                                        help_text='Content for description meta tag')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    related_products = models.ManyToManyField('self', blank=True)

    # managers
    objects = models.Manager()
    active = ProductManager()

    class Meta:
        # ordering = ['id']
        verbose_name = u'Товар'
        verbose_name_plural = u'Товары'

    def __unicode__(self):
        return '%s (%s)' % (self.name, self.SKU)

    def is_sale(self):
        if self.old_price:
            return True
        else:
            return False

    def get_price(self):
        if self.old_price:
            return self.old_price
        else:
            return self.price

    price_result = property(get_price)

    def get_absolute_url(self):
        return reverse('catalog:product', args=[str(self.slug)])

    def get_options(self):
        qs = self.product_variants.all()
        return qs

    def get_images(self):
        qs = self.productmedia_set.all().order_by('-is_main')
        return qs

    def get_cart_param(self):
        """
            Метод формирует параметры продукта для создания ссылки для доавления в cart

        """
        content_type = ContentType.objects.get_for_model(self)
        object_id = self.id
        return {
            'content_type': content_type,
            'object_id': object_id,
        }

    cart = property(get_cart_param)

    def thumbnail(self, width=64, height=64):
        if self.image:
            thumbnail = get_thumbnail(self.image, str(width) + 'x' + str(height))
            img_resize_url = unicode(thumbnail.url)
            html = '<a style="height:%spx; display:block" class="image-picker" href="%s">' \
                   '<img src="%s" alt="%s" width="%s" height="%s" />' \
                   '</a>'
            return html % (height, self.image.url, img_resize_url, self.name, thumbnail.width, thumbnail.height)

        return '<img src="http://placehold.it/64x64" alt="False">'

    thumbnail.short_description = _('Thumbnail')
    thumbnail.allow_tags = True


class ProductOption(models.Model):
    product = models.ForeignKey(Product, related_name='product_variants', verbose_name=u'Продукт')
    option = models.ForeignKey(Option, related_name='options', verbose_name=u'Характеристика')
    value = models.CharField(u'Значение', max_length=20)
    option_value = models.ForeignKey(OptionValue, related_name='optionvalue', verbose_name=u'Ед.изм.', blank=True,
                                     null=True)

    class Meta:
        ordering = ['id']
        verbose_name = u'Характеристика продукта'
        verbose_name_plural = u'Характеристики продукта'


class ProductMedia(models.Model):
    product = models.ForeignKey(Product)
    image = ImageField(upload_to="product/", null=True, blank=True)
    description = models.CharField(default="", blank=True, max_length=255)
    is_main = models.BooleanField(default=False)


class Carousel(models.Model):
    name = models.CharField(max_length=255, default="")
    description = models.TextField(default="", blank=True)
    image = ImageField(upload_to="carousel/", null=True, blank=True)
    category = TreeForeignKey('Category', null=True, blank=True)
    product = models.ForeignKey(Product, null=True, blank=True)
    is_active = models.BooleanField(default=True)

# SIGNALS
@receiver(pre_save, sender=Product)
def counters_hook(sender, instance, **kwargs):
    try:
        old_category = sender.objects.get(pk=instance.pk).category
        new_category = instance.category

        if old_category != new_category:
            for ancestor in old_category.get_ancestors(include_self=True):
                ancestor.count_products -= 1
                ancestor.save()

            for ancestor in new_category.get_ancestors(include_self=True):
                ancestor.count_products += 1
                ancestor.save()

    except sender.DoesNotExist:
        for ancestor in instance.category.get_ancestors(include_self=True):
            ancestor.count_products += 1
            ancestor.save()

# copy main image into the product object
# this signal is disabled during the import process
@receiver(post_save, sender=ProductMedia)
def product_image(sender, instance, **kwargs):
    if bool(instance.image) is False:
        instance.delete()
        return False

    if instance.is_main:
        # removing is_main flag from all images
        for product_image in instance.product.productmedia_set.all():
            if product_image.pk != instance.pk:
                product_image.is_main = False
                product_image.save()

        # making this image as main
        instance.product.image = instance.image
        instance.product.save()
    else:
        if instance.product.productmedia_set.count() == 1:
            instance.is_main = True
            # call this signal again
            instance.save()


@receiver(post_delete, sender=ProductMedia)
def product_image_delete(sender, instance, **kwargs):
    if instance.is_main:
        try:
            product = instance.product
        except Product.DoesNotExist:
            return False

        if product.productmedia_set.exclude(image=None).count() > 0:
            product_image = product.productmedia_set.exclude(image=None).all()[0]
            product_image.is_main = True
            product_image.save()
        else:
            product.image = None
            product.save()
