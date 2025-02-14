# Generated by Django 4.2.19 on 2025-02-14 06:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('purchase_request', '0005_alter_purchaserequestdetail_purchase_request'),
        ('spph', '0005_spphdetail'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='spphdetail',
            name='purchase_request',
        ),
        migrations.AddField(
            model_name='spphdetail',
            name='purchase_request_detail',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='purchase_request.purchaserequestdetail'),
            preserve_default=False,
        ),
    ]
