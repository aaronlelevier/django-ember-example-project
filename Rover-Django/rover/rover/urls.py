from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include

from customer import views as customer_views


urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'api/sitters', customer_views.SitterListAPIView.as_view()),
    url(r'^$', customer_views.IndexView.as_view())
]
