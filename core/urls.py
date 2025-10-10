from django.urls import path
from . import views

urlpatterns = [
    # Dashboard
    path('', views.dashboard, name='dashboard'),
    
    # Export CSV
    path('export/csv/', views.export_csv, name='export_csv'),
    
    # Conseillers
    path('conseillers/', views.conseiller_list, name='conseiller_list'),
    path('conseillers/nouveau/', views.conseiller_create, name='conseiller_create'),
    path('conseillers/<int:pk>/', views.conseiller_detail, name='conseiller_detail'),
    path('conseillers/<int:pk>/modifier/', views.conseiller_edit, name='conseiller_edit'),
    
    # Clients
    path('clients/', views.client_list, name='client_list'),
    path('clients/nouveau/', views.client_create, name='client_create'),
    path('clients/<int:pk>/', views.client_detail, name='client_detail'),
    path('clients/<int:pk>/modifier/', views.client_edit, name='client_edit'),
    
    # Sociétés
    path('societes/', views.societe_list, name='societe_list'),
    path('societes/nouvelle/', views.societe_create, name='societe_create'),
    path('societes/<int:pk>/', views.societe_detail, name='societe_detail'),
    path('societes/<int:pk>/modifier/', views.societe_edit, name='societe_edit'),
    
    # Enfants
    path('enfants/nouveau/', views.enfant_create, name='enfant_create'),
    path('enfants/<int:pk>/modifier/', views.enfant_edit, name='enfant_edit'),
    
    # Revenus Emploi
    path('revenus-emploi/', views.revenus_emploi_list, name='revenus_emploi_list'),
    path('revenus-emploi/nouveau/', views.revenus_emploi_create, name='revenus_emploi_create'),
    
    # Actifs Placements
    path('actifs-placements/', views.actifs_placements_list, name='actifs_placements_list'),
    path('actifs-placements/nouveau/', views.actifs_placements_create, name='actifs_placements_create'),
    
    # Assurances Vie
    path('assurances-vie/', views.assurances_vie_list, name='assurances_vie_list'),
    path('assurances-vie/nouvelle/', views.assurances_vie_create, name='assurances_vie_create'),
]