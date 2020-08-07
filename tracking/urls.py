from django.urls import path

from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('display_all', views.display_all, name='display_all'),
    path('add_case', views.add_case, name='add_case'),
    # path('add_person', views.add_person, name='add_person'),
    # path('add_test', views.add_test, name='add_test'),
]