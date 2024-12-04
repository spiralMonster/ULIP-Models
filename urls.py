from django.contrib import admin
from django.urls import path
from views import get_routes,get_stock_forecasting

urlpatterns = [
    path('admin/', admin.site.urls),
    path('routes/', get_routes),
    path('forecast/',get_stock_forecasting),
]
