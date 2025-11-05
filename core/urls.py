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
    
    # Revenus Entreprise
    path('revenus-entreprise/', views.revenus_entreprise_list, name='revenus_entreprise_list'),
    path('revenus-entreprise/nouveau/', views.revenus_entreprise_create, name='revenus_entreprise_create'),
    
    # Autres Revenus
    path('autres-revenus/', views.autres_revenus_list, name='autres_revenus_list'),
    path('autres-revenus/nouveau/', views.autres_revenus_create, name='autres_revenus_create'),
    
    # Revenus RRQ
    path('revenus-rrq/', views.revenus_rrq_list, name='revenus_rrq_list'),
    path('revenus-rrq/nouveau/', views.revenus_rrq_create, name='revenus_rrq_create'),
    
    # Revenus Dividendes
    path('revenus-dividendes/', views.revenus_dividendes_list, name='revenus_dividendes_list'),
    path('revenus-dividendes/nouveau/', views.revenus_dividendes_create, name='revenus_dividendes_create'),
    
    # Fonds Pension CD
    path('fonds-pension-cd/', views.fond_pension_cd_list, name='fond_pension_cd_list'),
    path('fonds-pension-cd/nouveau/', views.fond_pension_cd_create, name='fond_pension_cd_create'),
    
    # Fonds Pension RRE
    path('fonds-pension-rre/', views.fond_pension_rre_list, name='fond_pension_rre_list'),
    path('fonds-pension-rre/nouveau/', views.fond_pension_rre_create, name='fond_pension_rre_create'),
    
    # Projections RRE
    path('projections-rre/', views.projection_rre_list, name='projection_rre_list'),
    path('projections-rre/nouvelle/', views.projection_rre_create, name='projection_rre_create'),
    
    # Fonds Pension PD
    path('fonds-pension-pd/', views.fond_pension_pd_list, name='fond_pension_pd_list'),
    path('fonds-pension-pd/nouveau/', views.fond_pension_pd_create, name='fond_pension_pd_create'),
    
    # Cotisations Compte Personnel
    path('cotisations-compte-personnel/', views.cotisation_compte_personnel_list, name='cotisation_compte_personnel_list'),
    path('cotisations-compte-personnel/nouvelle/', views.cotisation_compte_personnel_create, name='cotisation_compte_personnel_create'),
    
    # Budgets Permanents
    path('budgets-permanents/', views.budget_permanent_list, name='budget_permanent_list'),
    path('budgets-permanents/nouveau/', views.budget_permanent_create, name='budget_permanent_create'),
    
    # Budgets Extraordinaires
    path('budgets-extraordinaires/', views.budget_extraordinaire_list, name='budget_extraordinaire_list'),
    path('budgets-extraordinaires/nouveau/', views.budget_extraordinaire_create, name='budget_extraordinaire_create'),
    
    # Projections Assurance Vie
    path('projections-assurance-vie/', views.projection_assurance_vie_list, name='projection_assurance_vie_list'),
    path('projections-assurance-vie/nouvelle/', views.projection_assurance_vie_create, name='projection_assurance_vie_create'),
    
    # Informations Fiscales Société
    path('informations-fiscales-societe/', views.informations_fiscales_societe_list, name='informations_fiscales_societe_list'),
    path('informations-fiscales-societe/nouvelle/', views.informations_fiscales_societe_create, name='informations_fiscales_societe_create'),
    
    # Informations Fiscales Client
    path('informations-fiscales-client/', views.informations_fiscales_client_list, name='informations_fiscales_client_list'),
    path('informations-fiscales-client/nouvelle/', views.informations_fiscales_client_create, name='informations_fiscales_client_create'),
    
    # Profils Investisseur
    path('profils-investisseur/', views.profil_investisseur_list, name='profil_investisseur_list'),
    path('profils-investisseur/nouveau/', views.profil_investisseur_create, name='profil_investisseur_create'),
    
    # Actifs
    path('actifs/', views.actif_list, name='actif_list'),
    path('actifs/nouveau/', views.actif_create, name='actif_create'),
    
    # Flux Monétaires
    path('flux-monetaires/', views.flux_monetaire_list, name='flux_monetaire_list'),
    path('flux-monetaires/nouveau/', views.flux_monetaire_create, name='flux_monetaire_create'),
]