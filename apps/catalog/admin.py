# -*- coding: utf-8 -*-
from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.http import HttpResponseRedirect
from django.shortcuts import render

from imperavi.admin import ImperaviAdmin
from feincms.admin import tree_editor
from sorl.thumbnail.admin import AdminImageMixin
from copy import deepcopy
from common.admin import PhotoStakedAdmin

from .forms import CopyProductForm
from .models import SiteTowns, Product, ProductMedia, Category, Option, Country, Producer, ProductOption, OptionValue

admin.site.register(Country)
admin.site.register(OptionValue)


class ProducerAdmin(AdminImageMixin, admin.ModelAdmin):
    list_display = ('thumbnail', 'name', 'country', 'position', 'is_active',  )
    list_editable = ('position', 'is_active')
    list_display_links = ('name', 'country')


admin.site.register(Producer, ProducerAdmin)


class SiteTownsAdmin(admin.ModelAdmin):
    list_display = ( 'name', 'position', 'is_active', )
    list_editable = ('position', 'is_active')
    save_on_top = True


admin.site.register(SiteTowns, SiteTownsAdmin)


class OptionMPTTModelAdmin(tree_editor.TreeEditor):
    # specify pixel amount for this ModelAdmin only:
    mptt_level_indent = 20
    actions = ['hide_category', 'un_hide_category']


class ProductOptionAdmin(admin.TabularInline):
    model = ProductOption
    extra = 1


class CategoryMPTTModelAdmin(tree_editor.TreeEditor):
    # specify pixel amount for this ModelAdmin only:
    list_display = ('name', 'slug', 'is_active', 'count_products')
    mptt_level_indent = 20
    actions = ['hide_category', 'un_hide_category']
    # sets up slug to be generated from category name
    prepopulated_fields = {'slug': ('name',)}

    inlines = [PhotoStakedAdmin, ]

    def hide_category(self, request, queryset):
        rows_updated = 0
        for category in queryset.all():
            rows_updated += category.get_descendants(include_self=True).update(is_active=False)

        if rows_updated == 1:
            message_bit = "1 category was"
        else:
            message_bit = "%s categories were" % rows_updated
        self.message_user(request, "%s successfully marked as hidden." % message_bit)

    def un_hide_category(self, request, queryset):
        rows_updated = 0
        for category in queryset.all():
            rows_updated += category.get_ancestors(include_self=True).update(is_active=True)

        if rows_updated == 1:
            message_bit = "1 category was"
        else:
            message_bit = "%s categories were" % rows_updated
        self.message_user(request, "%s successfully marked as active." % message_bit)

    un_hide_category.short_description = "Mark selected as active"
    hide_category.short_description = "Mark selected as hidden"


class ProductMediaInline(AdminImageMixin, admin.TabularInline):
    model = ProductMedia
    extra = 0

def copy_product(modeladmin, request, queryset):
    form = None
    if 'apply' in request.POST:
        form = CopyProductForm(request.POST)
        for q in queryset:
            product = deepcopy(q)
            product.id = None
            product.save()
            media_list = q.productmedia_set.all()
            for m in media_list:
                media = deepcopy(m)
                media.product = product
                media.id = None
                media.save()
            variants = q.product_variants.all()
            for v in variants:
                variant = deepcopy(v)
                variant.product = product
                variant.id = None
                variant.save()

        if form.is_valid():
            #category = form.cleaned_data['category']

            count = 0
            #for item in queryset:
            #    item.category = category
            #    item.save()
            #    count += 1

            modeladmin.message_user(request, "Было скопировано %s товаров." % (count))
            return HttpResponseRedirect(request.get_full_path())

    if not form:
        form = CopyProductForm(initial={'_selected_action': request.POST.getlist(admin.ACTION_CHECKBOX_NAME)})

    return render(request, 'admin/catalog/product/copy_product.html',
                  {'items': queryset, 'form': form, 'title': u'Копировать товар'})


copy_product.short_description = u"Копировать товар"

class ProductAdmin(AdminImageMixin, ImperaviAdmin):
    list_display = ('thumbnail', 'SKU', 'city', 'name', 'price', 'old_price', 'producer', 'category', 'updated_at',)
    list_display_links = ('name', )
    list_per_page = 50
    search_fields = ['name', 'description', 'meta_keywords', 'meta_description', 'slug', 'city__name', 'producer__name',
                     'category__name',
                     'SKU', ]
    exclude = ('image',)
    list_filter = ('producer', 'category', 'city',)
    filter_horizontal = ('related_products', )
    fieldsets = (
        (None, {
            'fields': ('is_active', 'category', 'producer', 'SKU', 'name', 'slug', ('price', 'old_price'),
                       'city', ('is_deal', 'is_popular', 'is_novelty'), 'description',)
        }),
        (u'SEO оптимизайция', {
            'classes': ('grp-collapse grp-closed',),
            'fields': ('meta_keywords', 'meta_description',)
        }),
        ('Related products', {
            'classes': ('grp-collapse grp-closed',),
            'fields': ('related_products',)
        }),
    )
    # sets up slug to be generated from product name
    prepopulated_fields = {'slug': ('name',)}

    inlines = [ProductOptionAdmin, ProductMediaInline]
    actions_on_top = True
    actions = [copy_product]


class CarouselAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'category', 'product', 'is_active',)


admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryMPTTModelAdmin)
admin.site.register(Option, OptionMPTTModelAdmin)
# admin.site.register(Carousel, CarouselAdmin)
