# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Contact_info.shipping_name'
        db.delete_column(u'cart_contact_info', 'shipping_name')

        # Deleting field 'Contact_info.shipping_state'
        db.delete_column(u'cart_contact_info', 'shipping_state')

        # Deleting field 'Contact_info.billing_city'
        db.delete_column(u'cart_contact_info', 'billing_city')

        # Deleting field 'Contact_info.shipping_zip'
        db.delete_column(u'cart_contact_info', 'shipping_zip')

        # Deleting field 'Contact_info.shipping_country'
        db.delete_column(u'cart_contact_info', 'shipping_country')

        # Deleting field 'Contact_info.billing_name'
        db.delete_column(u'cart_contact_info', 'billing_name')

        # Deleting field 'Contact_info.billing_zip'
        db.delete_column(u'cart_contact_info', 'billing_zip')

        # Deleting field 'Contact_info.billing_address_1'
        db.delete_column(u'cart_contact_info', 'billing_address_1')

        # Deleting field 'Contact_info.billing_address_2'
        db.delete_column(u'cart_contact_info', 'billing_address_2')

        # Deleting field 'Contact_info.shipping_address_2'
        db.delete_column(u'cart_contact_info', 'shipping_address_2')

        # Deleting field 'Contact_info.shipping_address_1'
        db.delete_column(u'cart_contact_info', 'shipping_address_1')

        # Deleting field 'Contact_info.billing_country'
        db.delete_column(u'cart_contact_info', 'billing_country')

        # Deleting field 'Contact_info.billing_state'
        db.delete_column(u'cart_contact_info', 'billing_state')

        # Deleting field 'Contact_info.shipping_city'
        db.delete_column(u'cart_contact_info', 'shipping_city')

        # Adding field 'Contact_info.name'
        db.add_column(u'cart_contact_info', 'name',
                      self.gf('django.db.models.fields.CharField')(default=datetime.datetime(2013, 8, 14, 0, 0), max_length=50),
                      keep_default=False)

        # Adding field 'Contact_info.comment'
        db.add_column(u'cart_contact_info', 'comment',
                      self.gf('django.db.models.fields.TextField')(default='', blank=True),
                      keep_default=False)


        # Changing field 'Contact_info.phone'
        db.alter_column(u'cart_contact_info', 'phone', self.gf('django.db.models.fields.CharField')(default=datetime.datetime(2013, 8, 14, 0, 0), max_length=20))

        # Changing field 'Contact_info.email'
        db.alter_column(u'cart_contact_info', 'email', self.gf('django.db.models.fields.EmailField')(default=datetime.datetime(2013, 8, 14, 0, 0), max_length=50))

    def backwards(self, orm):
        # Adding field 'Contact_info.shipping_name'
        db.add_column(u'cart_contact_info', 'shipping_name',
                      self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Contact_info.shipping_state'
        db.add_column(u'cart_contact_info', 'shipping_state',
                      self.gf('django.db.models.fields.CharField')(max_length=2, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Contact_info.billing_city'
        db.add_column(u'cart_contact_info', 'billing_city',
                      self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Contact_info.shipping_zip'
        db.add_column(u'cart_contact_info', 'shipping_zip',
                      self.gf('django.db.models.fields.CharField')(max_length=10, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Contact_info.shipping_country'
        db.add_column(u'cart_contact_info', 'shipping_country',
                      self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Contact_info.billing_name'
        db.add_column(u'cart_contact_info', 'billing_name',
                      self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Contact_info.billing_zip'
        db.add_column(u'cart_contact_info', 'billing_zip',
                      self.gf('django.db.models.fields.CharField')(max_length=10, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Contact_info.billing_address_1'
        db.add_column(u'cart_contact_info', 'billing_address_1',
                      self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Contact_info.billing_address_2'
        db.add_column(u'cart_contact_info', 'billing_address_2',
                      self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Contact_info.shipping_address_2'
        db.add_column(u'cart_contact_info', 'shipping_address_2',
                      self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Contact_info.shipping_address_1'
        db.add_column(u'cart_contact_info', 'shipping_address_1',
                      self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Contact_info.billing_country'
        db.add_column(u'cart_contact_info', 'billing_country',
                      self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Contact_info.billing_state'
        db.add_column(u'cart_contact_info', 'billing_state',
                      self.gf('django.db.models.fields.CharField')(max_length=2, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Contact_info.shipping_city'
        db.add_column(u'cart_contact_info', 'shipping_city',
                      self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True),
                      keep_default=False)

        # Deleting field 'Contact_info.name'
        db.delete_column(u'cart_contact_info', 'name')

        # Deleting field 'Contact_info.comment'
        db.delete_column(u'cart_contact_info', 'comment')


        # Changing field 'Contact_info.phone'
        db.alter_column(u'cart_contact_info', 'phone', self.gf('django.db.models.fields.CharField')(max_length=20, null=True))

        # Changing field 'Contact_info.email'
        db.alter_column(u'cart_contact_info', 'email', self.gf('django.db.models.fields.EmailField')(max_length=50, null=True))

    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'cart.contact_info': {
            'Meta': {'object_name': 'Contact_info'},
            'comment': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '50'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'order': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'order_contact_info'", 'to': u"orm['cart.Order']"}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        u'cart.order': {
            'Meta': {'object_name': 'Order'},
            'cart_id': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip_address': ('django.db.models.fields.IPAddressField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'last_updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'transaction_id': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'null': 'True', 'blank': 'True'})
        },
        u'cart.orderitem': {
            'Meta': {'object_name': 'OrderItem'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'order': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'order_items'", 'to': u"orm['cart.Order']"}),
            'price': ('django.db.models.fields.DecimalField', [], {'max_digits': '9', 'decimal_places': '2'}),
            'quantity': ('django.db.models.fields.IntegerField', [], {'default': '1'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['cart']