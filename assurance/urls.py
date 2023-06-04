from django.urls  import path
from . import views

urlpatterns = [
    path('', views.accueil, name='accueil'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('inscription/', views.inscription_view, name='inscription'),
    path('importdata/', views.import_data, name='import_data'),
    path('importsuccess/', views.import_success, name='import_success'),
    path('addvehicle/',views.create_vehicle,name='createvehicle'),
    path('recommendation/', views.recommendation, name='recommendation'),
    path('recommendation/successreco/', views.success_recommendation, name='success_recommendation'),

]