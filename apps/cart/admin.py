# -*- coding: utf-8 -*-
from django.contrib import admin
from django import forms

from .models import Order, OrderItem


class ItemAdmin(admin.TabularInline):
    model = OrderItem
    extra = 0


class CommentForm(forms.ModelForm):
    class Meta:
        model = Order


class OrderAdmin(admin.ModelAdmin):
    model = Order
    form = CommentForm
    # exclude = ['user', 'session_key', ]
    list_display = ['__unicode__', 'date', 'goods', 'total', 'status', 'user']
    list_filter = ['status']
    # fieldsets = (
    #     (_('Order data'), {
    #         'classes': ('collapse',),
    #         'fields': ('status', 'created',
    #                    # 'comment'
    #         ),
    #     }),
    # )
    search_fields = ('user__username',)
    # inlines = [ItemAdmin]


try:
    admin.site.register(Order, OrderAdmin)
except admin.sites.AlreadyRegistered:
    pass
