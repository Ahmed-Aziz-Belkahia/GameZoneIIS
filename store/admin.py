from django.contrib import admin
from store.models import (CallToActionBanner, CartOrderItem, Choice, Genre, Product, Category, CartOrder, Gallery,
                         Brand, ProductFaq, Review, ProductBidders, ProductOffers, SubCategory, Type, Specification,
                         SpecificationValue, Mapping, brandMetaTitle, categoryMetaTitle, productMetaTitle, subcategoryMetaTitle)
from import_export.admin import ImportExportModelAdmin
from django.contrib.auth.admin import UserAdmin
from django.db import models
from django.forms import ModelChoiceField
from userauths.models import User, Profile


@admin.action(description="Mark selected products as published")
def make_published(modeladmin, request, queryset):
    queryset.update(status="published")

@admin.action(description="Mark selected products as In Review")
def make_in_review(modeladmin, request, queryset):
    queryset.update(status="in_review")

@admin.action(description="Mark selected products as Featured")
def make_featured(modeladmin, request, queryset):
    queryset.update(featured=True)

class ProductImagesAdmin(admin.TabularInline):
    model = Gallery
    extra= 0

class SpecificationValueInline(admin.TabularInline):
    model = SpecificationValue
    extra= 0

class SpecificationInline(admin.TabularInline):
    model = Specification
    inlines = [SpecificationValueInline]
    extra= 0

class CartOrderItemsInlineAdmin(admin.StackedInline):
    model = CartOrderItem
    extra= 0

class categoryMetaTitleInlineAdmin(admin.StackedInline):
    model = categoryMetaTitle
    extra= 0

class subcategoryMetaTitleInlineAdmin(admin.StackedInline):
    model = subcategoryMetaTitle
    extra= 0

class brandMetaTitleInlineAdmin(admin.StackedInline):
    model = brandMetaTitle
    extra= 0

class productMetaTitleInlineAdmin(admin.StackedInline):
    model = productMetaTitle
    extra= 0

class StaffUserChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.username

class TypesChoicesAdmin(admin.TabularInline):
    model = Choice
    prepopulated_fields = {"meta_title": ("title", )}
    extra= 0

class InlineType(admin.TabularInline):
    model = Type
    list_display = ['title']
    prepopulated_fields = {"meta_title": ("title", )}
    extra= 0

class TypeAdmin(ImportExportModelAdmin):
    inlines = [TypesChoicesAdmin]
    """ list_display = ['__str__'] """
    prepopulated_fields = {"meta_title": ("title", )}
    extra= 0

from import_export import resources
from import_export.fields import Field

class ProductResource(resources.ModelResource):
    product_link = Field(column_name='Product Link', attribute='product_link')
    product_image_link = Field(column_name='Product Image Link', attribute='product_image_link')
    availability = Field(column_name='Availability', attribute='availability')

    class Meta:
        model = Product
        fields = (
            'pid', 'user', 'vendor', 'category', 'subcategory', 'brand', 
            'title', 'meta_title', 'title_meta_title', 'index', 'image', 
            'alt', 'description', 'meta_description', 'price', 'old_price', 
            'shipping_amount', 'gz_coins', 'show_old_price', 'tags', 'status', 
            'product_condition', 'product_condition_rating', 'product_condition_description', 
            'stock_qty', 'in_stock', 'featured', 'game', 'featured_game', 
            'featured_game_banner', 'featured_game_banner_alt', 'add_to_featured_games_slider', 
            'featured_game_slider_banner', 'featured_game_slider_mobile_banner', 
            'featured_game_slider_alt', 'hero_section_featured', 'hero_banner', 
            'hero_banner_mobile', 'hero_alt', 'deal_category', 'deal_image', 
            'deal_alt', 'deal_description', 'catalog_type', 'hot_deal', 
            'digital', 'sku', 'type', 'auction_status', 'ending_date', 
            'bidding_ended', 'suggested_products', 'related_products', 
            'views', 'saved', 'orders', 'liked', 'bidders', 'slug', 'date', 
            'release_date', 'product_link', 'product_image_link', 'availability'
        )

    def dehydrate_product_link(self, product):
        return product.get_product_link()

    def dehydrate_product_image_link(self, product):
        return product.get_product_image_link()

    def dehydrate_availability(self, product):
        return product.check_availability()

class ProductAdmin(ImportExportModelAdmin):
    resource_class = ProductResource
    inlines = [productMetaTitleInlineAdmin, ProductImagesAdmin, InlineType, SpecificationInline]
    search_fields = ['title', 'price']
    list_filter = ['featured', 'status', 'in_stock', 'type', 'vendor']
    list_editable = ['price', 'featured', 'status', 'shipping_amount', 'hot_deal', 'hero_section_featured']
    list_display = ['product_image', 'title', 'price', 'featured', 'shipping_amount', 'in_stock', 'stock_qty', 'order_count', 'vendor', 'status', 'hero_section_featured', 'hot_deal']
    actions = [make_published, make_in_review, make_featured]
    list_per_page = 1300
    prepopulated_fields = {"slug": ("title", )}
    extra = 0

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'user':
            kwargs['queryset'] = User.objects.filter(is_staff=True)
            kwargs['form_class'] = StaffUserChoiceField
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class CategoryAdmin(ImportExportModelAdmin):
    inlines = [categoryMetaTitleInlineAdmin]
    list_display = ['title', 'category_image']
    prepopulated_fields = {"meta_title": ("title", )}
    extra= 0

class SubCategoryAdmin(ImportExportModelAdmin):
    inlines = [subcategoryMetaTitleInlineAdmin]
    list_display = ['title', 'category_image']
    prepopulated_fields = {"meta_title": ("title", )}
    extra= 0

class GenreAdmin(ImportExportModelAdmin):
    list_display = ['title', 'genre_image']
    prepopulated_fields = {"meta_title": ("title", )}
    extra= 0

class CartOrderAdmin(ImportExportModelAdmin):
    inlines = [CartOrderItemsInlineAdmin]
    search_fields = ['oid', 'tracking_id', 'product__title']
    list_editable = ['order_status', 'payment_status' ,'delivery_status']
    list_filter = ['payment_status', 'order_status', 'delivery_status']
    list_display = ['oid', 'payment_status', 'order_status', 'delivery_status' ,'price', 'shipping', 'vat', 'service_fee' ,'total', 'saved' ,'email','date']
    extra= 0

class CartOrderItemsAdmin(ImportExportModelAdmin):
    search_fields = ['oid', 'tracking_id', 'product', 'coupon__code', 'order__oid', 'vendor__shop_name']
    list_filter = ['paid', 'paid_vendor', 'cancelled', 'delivery_couriers', 'applied_coupon']
    list_display = ['order',  'vendor' , 'order_img','product_obj' ,'qty', 'price', 'total', 'shipping' , 'service_fee', 'vat','total_payable', 'grand_total' , 'delivery_couriers' , 'paid', 'paid_vendor', 'applied_coupon' ,'cancelled']
    extra= 0

class BrandAdmin(ImportExportModelAdmin):
    inlines = [brandMetaTitleInlineAdmin]
    list_editable = ['featured', 'active']
    list_display = ['title', 'brand_image', 'active', 'featured']
    prepopulated_fields = {"meta_title": ("title", )}
    extra= 0

class ProductFaqAdmin(ImportExportModelAdmin):
    list_editable = [ 'active', 'answer']
    list_display = ['user', 'question', 'answer' ,'active']
    extra= 0

class ProductBiddersAdmin(ImportExportModelAdmin):
    list_display = ['user', 'product', 'price','winner', 'win_status' ,'email']
    extra= 0

class ProductReviewAdmin(admin.ModelAdmin):
    list_editable = ['active']
    list_display = ['user', 'product', 'review', 'reply' ,'rating', 'active']
    extra= 0

class ProductOfferAdmin(ImportExportModelAdmin):
    list_display = ['user', 'product', 'price','status', 'email']
    extra= 0

class CallToActionBannerAdmin(ImportExportModelAdmin):
    list_editable = ["CTA_type"]
    list_display = ['banner_image', 'product', "CTA_type"]
    extra= 0

class SpecificationValueAdmin(admin.ModelAdmin):
    list_display = ['specification', 'title', 'description']
    list_filter = ['specification']
    extra= 0

class SpecificationAdmin(admin.ModelAdmin):
    inlines = [SpecificationValueInline]
    list_display = ['sid', 'product', 'title']
    search_fields = ['title']
    list_filter = ['product']
    extra= 0

admin.site.register(ProductBidders, ProductBiddersAdmin)
admin.site.register(Review, ProductReviewAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(SubCategory, SubCategoryAdmin)
admin.site.register(CartOrder, CartOrderAdmin)
admin.site.register(CartOrderItem, CartOrderItemsAdmin)
admin.site.register(Brand, BrandAdmin)
admin.site.register(ProductFaq, ProductFaqAdmin)
admin.site.register(ProductOffers, ProductOfferAdmin)
admin.site.register(CallToActionBanner, CallToActionBannerAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Type, TypeAdmin)
admin.site.register(Specification, SpecificationAdmin)  # Added
admin.site.register(SpecificationValue, SpecificationValueAdmin)  # Added
admin.site.register(Mapping)  # Added
