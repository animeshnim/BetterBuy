"""Order URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""



# Modules Import
from django.urls import path



# Import from Apps
from Order.views import MyViews
from Order.views import UtilityFunctions



# URL Patterns
urlpatterns = [
    path('order-summary', MyViews.OrderSummary, name='OrderSummary'),
    path('pending/order-summary', MyViews.PendingOrderSummaryPage, name='PendingOrderSummaryPage'),
    path('redirecting/payment-page', MyViews.PaymentPage, name='PaymentPage'),
    path('my-order/status/pending', MyViews.OrderPending, name='order-pending'),
    path('my-order/status/success', MyViews.OrderPaymentSuccess, name='OrderPaymentSuccess'),
]