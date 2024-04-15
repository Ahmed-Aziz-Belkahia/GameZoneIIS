from django.urls import path
from reports import views

app_name = "reports"

urlpatterns = [
    path("bidder-report/<bid>/", views.report_bidding_user, name="bidder-report"),
    path("report_offer_user/<oid>/", views.report_offer_user, name="report_offer_user"),
    path("product-report/<pid>/", views.report_product, name="product-report"),
    path("report-issue/", views.report_issue, name="report-issue"),
]
