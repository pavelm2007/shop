# -*- coding: utf-8 -*-

import xml.etree.ElementTree as ET
from django.core.management.base import BaseCommand, CommandError
from optparse import make_option
from catalog.models import Product, Category, ProductMedia
import urllib2, urlparse
from django.core.files.base import ContentFile
import time
from django.db.models.signals import Signal, pre_save, post_delete
from catalog.models import counters_hook, product_image_delete


class Command(BaseCommand):
    option_list = BaseCommand.option_list + \
                  (
                      make_option('--delete', action='store_true',
                                  dest='delete',
                                  default=True,
                                  help='Delete poll instead of closing it'),
                  ) + (
                      make_option('--images',
                                  action='store_true',
                                  dest='images',
                                  default=False,
                                  help='Import images from YML'),
                  ) + (
                      make_option('--verbose',
                                  action='store_true',
                                  dest='verbose',
                                  default=False,
                                  help='Prints debug output'),
                  )
    args = '<poll_id poll_id ...>'
    help = 'Closes the specified YML for importing'

    def handle(self, *args, **options):
        start_time = time.time()

        # going to disconnect categories counter update hook from Product
        Signal.disconnect(pre_save, sender=Product, receiver=counters_hook)

        # going to disconnect product medial hook
        Signal.disconnect(post_delete, sender=ProductMedia, receiver=product_image_delete)

        if options['delete']:
            Category.objects.all().delete();
            Product.objects.all().delete();

        for file in args:
            if file[0:4] == 'http':
                try:
                    request = urllib2.Request(file, headers={"Accept": "application/xml"})
                    file = urllib2.urlopen(request)

                    tree = ET.parse(file)

                except ET.ParseError:
                    raise CommandError('YML "%s" is not valid' % file)
            else:
                tree = ET.parse(file)

            root = tree.getroot()

            trans_dct = {}

            # copy categories into databases
            for child in root.find('shop').find('categories'):
                category = Category(name=child.text);
                category.save()
                trans_dct[child.get('id')] = category.id;

            # setting child-parent relations
            for child in root.find('shop').find('categories'):
                # only for child elements
                if child.get('parentId') is not None:
                    # search for child a category
                    try:
                        category = Category.objects.get(pk=trans_dct[child.get('id')])
                    except Category.DoesNotExist:
                        raise CommandError('Category ID "%s" was not found' % child.get('id'))
                    pass
                    # adding relation to parent category
                    try:
                        category.parent = Category.objects.get(pk=trans_dct[child.get('parentId')])
                        category.save()
                    except Category.DoesNotExist:
                        raise CommandError('Category ID "%s" was not found' % child.get('id'))
                    pass

            self.stdout.write('Categories imported' + '\n')

            # import offers (products)
            product_counter = 0
            for child in root.find('shop').find('offers'):

                if options['verbose']:
                    u = u'import products)  %s ' % child.find('name').text
                    print u.encode('ascii', 'ignore')

                description = child.find('description').text;
                if description is None:
                    description = ""

                product = Product(
                    name=child.find('name').text,
                    price=child.find('price').text,
                    description=description,
                    category=Category.objects.get(pk=trans_dct[child.find('categoryId').text])

                );

                product.save()
                product_counter += 1

                if options['images']:
                    # importing images from <picture>http://...</picture>
                    if child.find('picture') is not None:
                        try:
                            image_data = urllib2.urlopen(child.find('picture').text, timeout=5)
                        except urllib2.HTTPError:
                            print 'Could not download image: ' + child.find('picture').text
                        else:
                            filename = urlparse.urlparse(image_data.geturl()).path.split('/')[-1] + '.jpg'

                            product_media = ProductMedia(image=filename, is_main=True, product=product)
                            product_media.image.save(filename, ContentFile(image_data.read()), save=False)
                            product_media.save()

            self.stdout.write('Products imported - ' + str(product_counter) + '\n' + str(round(time.time() - start_time, 2)) + " seconds")

            # fix categories counters

            categories = Category.objects.all()

            for category in categories:
                category.count_products = Product.active.filter(
                    category__in=category.get_descendants(include_self=True)).count()

                # deactivate empty categories
                if category.count_products == 0:
                    category.is_active = False

                category.save()
