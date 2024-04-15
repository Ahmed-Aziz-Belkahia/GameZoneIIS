from django.core.management.base import BaseCommand
from userauths.models import User
import pandas as pd
from vendor.models import Vendor
from store.models import Product, Category
from userauths.models import User
import urllib
import urllib.request
from django.core.files import File
import shortuuid
from django.utils.text import slugify



class Command(BaseCommand):
    def add_arguments(self, parser):
        pass
    
    def handle(self, *args, **options):
        # Delete every other product from the database if the need be
        Product.objects.all().delete()
        
        # Get the path to the csv file
        df = pd.read_csv('products.csv')
        for vendor_id, title, image, total_sales, post_content, status, stock_qty, price, date, category in zip(df.post_author, df.post_title, df.images, df.total_sales, df.post_content, df.post_status, df.stock, df.regular_price, df.post_date, df.product_cat):
            product = Product(
                vendor=Vendor.objects.get(id=vendor_id),
                user=User.objects.get(id=vendor_id),
                title=title,
                stock_qty=stock_qty,
                price=price,
                orders=total_sales,
                description=post_content,
                date=date,
                status=None
            )
            product.save()

            uuid_key = shortuuid.uuid()
            uniqueid = uuid_key[:4]

            product.slug = slugify(product.title) + "-" + str(uniqueid.lower())

            image_url = image
            image_name = image_url.split('/')[-1]
            response = urllib.request.urlopen(image_url)
            image_file = File(response)
            product.image.save(image_name, image_file)
            product.save()
            
            if status == "publish":
                product.status = "published"
                product.save()
                
            if status == "draft":
                product.status = "draft"
                product.save()
                
            if product.price == None or product.price == "":
                product.price = 1.99
                product.save()
            
            
            print(vendor_id)
            category_list = category.split(",")
            for c in category_list:
                category_ = Category.objects.get(title=c)
                product.category.add(category_)
                product.save()

            
            
            
            