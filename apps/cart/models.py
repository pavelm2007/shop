# -*- coding: utf-8 -*-
import decimal
from django.utils.encoding import smart_str, smart_unicode
from django.core.mail import send_mail
from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _
from django.dispatch import receiver
from django.template import loader

def query_set_factory(model_name, query_set_class):
    class ChainedManager(models.Manager):

        def get_query_set(self):
            model = models.get_model('Order', model_name)
            return query_set_class(model)

        def __getattr__(self, attr, *args):
            try:
                return getattr(self.__class__, attr, *args)
            except AttributeError:
                return getattr(self.get_query_set(), attr, *args)

    return ChainedManager()


class OrderQuerySet(models.query.QuerySet):
    def active_orders(self):
        '''Filters active orders, which can be changed by user'''
        return self.filter(status=1)


class ActiveOrders(models.Manager):
    def get_query_set(self):
        return super(ActiveOrders, self).get_query_set().filter(status=1).all()


class Order(models.Model):
    class Meta:
        verbose_name = u'Заказ'
        verbose_name_plural = u'Заказы'

        # each individual status

    SUBMITTED = 1
    PROCESSED = 2
    SHIPPED = 3
    CANCELLED = 4

    # set of possible order statuses
    ORDER_STATUSES = ((SUBMITTED, u'Формируется'), (PROCESSED, u'В процессе'),
                      (SHIPPED, u'Отправлено'), (CANCELLED, u'Отменено'),)

    # order info
    cart_id = models.CharField(u'ID заказа', max_length=50)
    date = models.DateTimeField(u'Дата', auto_now_add=True)
    last_updated = models.DateTimeField(u'Обновено', auto_now=True)
    status = models.IntegerField(u'Статус', choices=ORDER_STATUSES, default=SUBMITTED)
    ip_address = models.IPAddressField(u'IP адрес', blank=True, null=True)
    user = models.ForeignKey(User, null=True, blank=True, verbose_name=u'Пользователь')
    transaction_id = models.CharField(u'ID транзакции', max_length=20, blank=True, null=True)
    comment = models.TextField(u'Комментарий заказчика', blank=True, null=True)

    # objects = query_set_factory('Order', OrderQuerySet)
    objects = models.Manager()
    status_object = ActiveOrders()


    def __unicode__(self):
        return 'Order #' + unicode(self.id)

    @property
    def total(self):
        total = decimal.Decimal('0.00')

        order_items = OrderItem.objects.filter(order=self)
        for item in order_items:
            total += item.total
        return total

    @property
    def goods(self):
        count = 0
        goods = self.order_items.all()
        # for item in goods:
        #     count += item.quantity

        return goods.count()


class OrderItem(models.Model):
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')
    name = models.CharField(u'Наименование товара', max_length=255, blank=True, null=True)
    quantity = models.IntegerField(u'Количество', default=1)
    price = models.DecimalField(u'Цена за ед.', max_digits=9, decimal_places=2)
    order = models.ForeignKey(Order, related_name='order_items', verbose_name=_('Order'))

    # def save(self, *args, **kwargs):
    #     product = self.content_object
    #     self.name = product
    #     super(OrderItem).save(*args, **kwargs)

    @property
    def product(self):
        obj = self.content_object
        return obj

    @property
    def total(self):
        return self.quantity * self.price

    @property
    def name(self):
        return self.product.name

    @property
    def sku(self):
        return self.product.SKU

    def __unicode__(self):
        return self.product.name + ' (' + self.product.SKU + ')'

    def get_absolute_url(self):
        return self.product.get_absolute_url()

    def augment_quantity(self, quantity):
        """Изменение количества товара в корзине"""
        if quantity.isdigit():
            self.quantity = self.quantity + int(quantity)
            self.save()


# @receiver(post_save, sender=OrderItem)
# def product_image(sender, instance, **kwargs):
#     if bool(instance.image) is False:
#         instance.delete()
#         return False
#
#     if instance.is_main:
#         # removing is_main flag from all images
#         for product_image in instance.product.productmedia_set.all():
#             if product_image.pk != instance.pk:
#                 product_image.is_main = False
#                 product_image.save()
#
#         # making this image as main
#         instance.product.image = instance.image
#         instance.product.save()
#     else:
#         if instance.product.productmedia_set.count() == 1:
#             instance.is_main = True
#             # call this signal again
#             instance.save()



class Contact_info(models.Model):
    order = models.ForeignKey(Order, related_name='order_contact_info', verbose_name=u'Контакты заказа')
    # contact info
    name = models.CharField(u'Имя', max_length=50)
    phone = models.CharField(u'Телефон', max_length=20)
    email = models.EmailField(u'E-mail', max_length=50)
    comment = models.TextField(u'Комментарий к заказу', blank=True)



@receiver(post_save, sender=Contact_info)
def order_confirm(sender, instance, **kwargs):
    order = instance.order
    items = order.order_items.all()

    message = loader.render_to_string('cart/order.txt', {'order':order, 'items':items,'contact': instance,})
    order.comment = message
    order.save()

@receiver(post_save, sender=Order)
def CartSubmit(sender, instance, **kwargs):
    order = instance
    if order.status == 2:
        managers = [manager[1] for manager in settings.MANAGERS]
        subject = smart_unicode(u'Новый заказ ' +order.__unicode__())
        send_mail(subject, order.comment, settings.DEFAULT_FROM_MAIL,managers)