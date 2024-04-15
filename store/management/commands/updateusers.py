from django.core.management.base import BaseCommand
from userauths.models import User
import pandas as pd
from addons.models import NewsLetter
from vendor.models import Vendor

class Command(BaseCommand):
    def add_arguments(self, parser):
        pass
    
    def handle(self, *args, **options):
        df = pd.read_csv('users.csv')
        for id, username, email, date_joined, first_name, last_name, roles, total_spent, billing_first_name, billing_last_name,billing_email,billing_phone,billing_address,billing_state,billing_country in zip(df.customer_id, df.user_nicename, df.user_email, df.user_registered, df.first_name, df.last_name, df.roles, df.total_spent, df.billing_first_name,df.billing_last_name,df.billing_email,df.billing_phone,df.billing_address_1,df.billing_state,df.billing_country):
            user = User(
                id=id,
                username=username,
                email=email,
                date_joined=date_joined,
                first_name=first_name,
                last_name=last_name,
                roles=roles,
                total_spent=total_spent,
                billing_first_name=billing_first_name,
                billing_last_name=billing_last_name,
                billing_email=billing_email,
                billing_phone=billing_phone,
                billing_address=billing_address,
                billing_state=billing_state,
                billing_country=billing_country,
            )
            
            
            user.save()
            # new_user = User.objects.filter(email=user.email).count()
            
            # if new_user > 1:
            #     user.email = email + "dup"
            #     user.save()
            if user.roles == "wcfm_vendor":
                vendor = Vendor(id=user.id, user=user, profile=user.profile, profile__seller=True, shop_name=user.username, shop_email=user.email, date=date_joined)
                vendor.save()
            
            NewsLetter.objects.create(email=user.email)
            
            print("id ======", id)
            
            