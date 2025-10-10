from django.contrib import admin
from .models import (
    Conseiller, Client, Societe, Enfant, RevenusEmploi, 
    ActifPlacements, AssuranceVie
)

@admin.register(Conseiller)
class ConseillerAdmin(admin.ModelAdmin):
    list_display = ['nom', 'prenom', 'courriel', 'telephone', 'langue', 'date_creation']
    list_filter = ['langue', 'date_creation']
    search_fields = ['nom', 'prenom', 'courriel']
    ordering = ['-date_creation']

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ['nom', 'prenom', 'courriel', 'province', 'conseiller', 'etat_civil']
    list_filter = ['province', 'etat_civil', 'sexe', 'langue', 'fumeur']
    search_fields = ['nom', 'prenom', 'courriel']
    list_select_related = ['conseiller']
    ordering = ['nom', 'prenom']

@admin.register(Societe)
class SocieteAdmin(admin.ModelAdmin):
    list_display = ['nom', 'client', 'type_societe', 'revenus']
    list_filter = ['type_societe']
    search_fields = ['nom', 'client__nom', 'client__prenom']
    list_select_related = ['client']
    ordering = ['nom']

@admin.register(Enfant)
class EnfantAdmin(admin.ModelAdmin):
    list_display = ['nom', 'client', 'date_naissance', 'garde_partagee', 'cout_par_jour']
    list_filter = ['garde_partagee', 'garderie_subventionnee', 'garderie_non_subventionnee']
    search_fields = ['nom', 'client__nom', 'client__prenom']
    list_select_related = ['client']
    ordering = ['client__nom', 'nom']
