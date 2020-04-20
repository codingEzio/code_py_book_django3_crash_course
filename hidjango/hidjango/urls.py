from django.contrib import admin
from django.urls import path
from homepage.views import HomepageView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomepageView.as_view(), name='home'),
]
