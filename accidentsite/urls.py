"""accidentsite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from accidentsite import views
from django.conf.urls.static import static
from django.conf import settings

from django.contrib.auth import views as auth_views
# from django.contrib.auth.views import LoginView
# from django.contrib.auth.views import LogoutView

# 정규표현식 ^=begin ,$=end
# http://127.0.0.1/admin 이라는 의미임
urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^home/', views.HomeView.as_view(), name='home'),
    path('list/', views.list_view, name='list'),
#    url(r'^chart_csv/$', views.chart_csv, name='chart_csv'),
    url(r'^show_pandas', views.show_pandas, name='show_pandas'),
    url(r'^show_map', views.show_map, name='show_map'),
#    url(r'^chart_csv1/$', views.chart_csv1, name='chart_csv1'),
    url(r'^show_time', views.show_time, name='show_time'),
    url(r'^show_chart', views.show_chart, name='show_chart'),
    path('a/', views.all_map, name='a'),
    url(r'^chart_hap/$', views.chart_hap, name='chart_hap'),
    url(r'^chart_hap2/$', views.chart_hap2, name='chart_hap2'),
    url(r'^show_att_vic', views.show_att_vic, name='show_att_vic'),
    url(r'^show_casualties', views.show_casualties, name='show_casualties'),
    url(r'^chart_casualtie/$', views.chart_casualtie, name='chart_casualtie'),
    url(r'^open_patients/$', views.open_patients, name='open_patients'),
    url(r'^carousel/', views.carouselView.as_view(), name='carousel'),
    url(r'^law_violations/', views.law_violations, name='law_violations'),
    url(r'^chart_law', views.chart_law, name='chart_law'),
    url(r'^chart_road', views.chart_road, name='chart_road'),
    url(r'^road_shape', views.road_shape, name='road_shape'),
#    url(r'^accident_road', views.accident_road, name='accient_road'),
    url(r'^patients_chart/$', views.patients_chart, name='patients_chart'),


]
urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)