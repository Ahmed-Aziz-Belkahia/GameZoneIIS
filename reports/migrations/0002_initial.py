# Generated by Django 3.2.18 on 2024-08-04 08:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('reports', '0001_initial'),
        ('vendor', '0001_initial'),
        ('store', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='vendoreport',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='vendor_reporting_user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='vendoreport',
            name='vendor',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='vendor_report', to='vendor.vendor'),
        ),
        migrations.AddField(
            model_name='productreport',
            name='product',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='product_report', to='store.product'),
        ),
        migrations.AddField(
            model_name='productreport',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='product_reporting_user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='productreport',
            name='vendor',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='product_vendor_report', to='vendor.vendor'),
        ),
        migrations.AddField(
            model_name='orderitemreport',
            name='order_item',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='order_item_report', to='store.cartorderitem'),
        ),
        migrations.AddField(
            model_name='orderitemreport',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='order_item_reporting_user', to='vendor.vendor'),
        ),
        migrations.AddField(
            model_name='offeruserreport',
            name='product_offer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='offer_report', to='store.productoffers'),
        ),
        migrations.AddField(
            model_name='offeruserreport',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='offer_reporting_user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='offeruserreport',
            name='vendor',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='offer_reporting_user', to='vendor.vendor'),
        ),
        migrations.AddField(
            model_name='generalissue',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='general_issueuser', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='biddinguserreport',
            name='product_bidding',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='bidding_report', to='store.productbidders'),
        ),
        migrations.AddField(
            model_name='biddinguserreport',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='bidding_reporting_user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='biddinguserreport',
            name='vendor',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='bidding_reporting_user', to='vendor.vendor'),
        ),
    ]