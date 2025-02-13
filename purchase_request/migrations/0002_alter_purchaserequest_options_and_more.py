# Generated by Django 4.2.19 on 2025-02-13 10:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('purchase_request', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='purchaserequest',
            options={'default_permissions': (), 'permissions': [('add_purchase_request', 'Can add purchase request'), ('change_purchase_request', 'Can change purchase request'), ('delete_purchase_request', 'Can delete purchase request'), ('view_purchase_request', 'Can view purchase request')]},
        ),
        migrations.AlterModelOptions(
            name='purchaserequestdetail',
            options={'default_permissions': (), 'permissions': [('add_purchase_request_detail', 'Can add purchase request detail'), ('change_purchase_request_detail', 'Can change purchase request detail'), ('delete_purchase_request_detail', 'Can delete purchase request detail'), ('view_purchase_request_detail', 'Can view purchase request detail')]},
        ),
        migrations.AlterModelTable(
            name='purchaserequest',
            table='purchase_request',
        ),
        migrations.AlterModelTable(
            name='purchaserequestdetail',
            table='purchase_request_detail',
        ),
    ]
