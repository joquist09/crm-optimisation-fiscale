from django.contrib import admin
from .models import (
    Conseiller, Client, Societe, Enfant, RevenusEmploi, 
    ActifPlacements, AssuranceVie,
    RevenusEntreprise, AutresRevenus, RevenusRRQ, RevenusDividendes, FondPensionCD,
    FondPensionRRE, ProjectionRRE, FondPensionPD, CotisationComptePersonnel,
    BudgetPermanent, BudgetExtraordinaire, ProjectionAssuranceVie, InformationsFiscalesClient,
    InformationsFiscalesSociete, ProfilInvestisseur, Actif, FluxMonetaire
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

@admin.register(RevenusEntreprise)
class RevenusEntrepriseAdmin(admin.ModelAdmin):
    list_display = ['client', 'revenus_entreprise', 'date_debut', 'date_fin']
    list_filter = ['date_debut', 'date_fin']
    search_fields = ['client__nom', 'client__prenom']
    ordering = ['client__nom', 'date_debut']

@admin.register(AutresRevenus)
class AutresRevenusAdmin(admin.ModelAdmin):
    list_display = ['client', 'type', 'montant', 'date_debut', 'date_fin']
    list_filter = ['type', 'date_debut', 'date_fin']
    search_fields = ['client__nom', 'client__prenom']
    ordering = ['client__nom', 'type']

@admin.register(RevenusRRQ)
class RevenusRRQAdmin(admin.ModelAdmin):
    list_display = ['client', 'type', 'rentes_revenus_rrq_rpc', 'date_debut_rrq_rpc']
    list_filter = ['type', 'date_debut_rrq_rpc']
    search_fields = ['client__nom', 'client__prenom']
    ordering = ['client__nom', 'type']

@admin.register(RevenusDividendes)
class RevenusDividendesAdmin(admin.ModelAdmin):
    list_display = ['client', 'societe', 'revenus_dividendes', 'date_debut', 'date_fin']
    list_filter = ['date_debut', 'date_fin']
    search_fields = ['client__nom', 'client__prenom', 'societe__nom']
    ordering = ['client__nom', 'date_debut']

@admin.register(FondPensionCD)
class FondPensionCDAdmin(admin.ModelAdmin):
    list_display = ['client', 'cotisation_totale', 'date_debut_cotisation_totale', 'date_fin_cotisation_totale']
    list_filter = ['date_debut_cotisation_totale', 'date_fin_cotisation_totale']
    search_fields = ['client__nom', 'client__prenom']
    ordering = ['client__nom', 'date_debut_cotisation_totale']

@admin.register(FondPensionRRE)
class FondPensionRREAdmin(admin.ModelAdmin):
    list_display = ['participant', 'promoteur', 'transfert_initial_pd', 'solde_immobilise']
    list_filter = ['transfert_intergenerationnel']
    search_fields = ['participant__nom', 'participant__prenom', 'promoteur__nom']
    ordering = ['participant__nom', 'promoteur__nom']

@admin.register(ProjectionRRE)
class ProjectionRREAdmin(admin.ModelAdmin):
    list_display = ['fonds_pension_rre', 'annee', 'cotisation_regulieres', 'rente']
    list_filter = ['annee']
    search_fields = ['fonds_pension_rre__participant__nom', 'fonds_pension_rre__participant__prenom']
    ordering = ['annee']

@admin.register(FondPensionPD)
class FondPensionPDAdmin(admin.ModelAdmin):
    list_display = ['client', 'revenu_pension_1', 'date_debut_revenu_pension_1', 'date_fin_revenu_pension_1']
    list_filter = ['date_debut_revenu_pension_1', 'date_fin_revenu_pension_1']
    search_fields = ['client__nom', 'client__prenom']
    ordering = ['client__nom', 'date_debut_revenu_pension_1']

@admin.register(CotisationComptePersonnel)
class CotisationComptePersonnelAdmin(admin.ModelAdmin):
    list_display = ['actif', 'cotisation_annuelle', 'date_debut', 'date_fin']
    list_filter = ['date_debut', 'date_fin']
    search_fields = ['actif__client__nom', 'actif__client__prenom']
    ordering = ['actif__client__nom', 'date_debut']

@admin.register(BudgetPermanent)
class BudgetPermanentAdmin(admin.ModelAdmin):
    list_display = ['client', 'date_debut_budget_annuel_permanent', 'budget_annuel_permanent']
    list_filter = ['date_debut_budget_annuel_permanent']
    search_fields = ['client__nom', 'client__prenom']
    ordering = ['client__nom', 'date_debut_budget_annuel_permanent']

@admin.register(BudgetExtraordinaire)
class BudgetExtraordinaireAdmin(admin.ModelAdmin):
    list_display = ['client', 'date_debut', 'date_fin', 'budget_extraordinaire']
    list_filter = ['date_debut', 'date_fin']
    search_fields = ['client__nom', 'client__prenom']
    ordering = ['client__nom', 'date_debut']

@admin.register(ProjectionAssuranceVie)
class ProjectionAssuranceVieAdmin(admin.ModelAdmin):
    list_display = ['assurance_vie', 'annee', 'capital_deces', 'prime_annuelle']
    list_filter = ['annee']
    search_fields = ['assurance_vie__preneur_client__nom', 'assurance_vie__preneur_client__prenom']
    ordering = ['annee']

@admin.register(InformationsFiscalesClient)
class InformationsFiscalesClientAdmin(admin.ModelAdmin):
    list_display = ['client', 'droits_reer_inutilises', 'droits_celi_inutilises']
    search_fields = ['client__nom', 'client__prenom']
    ordering = ['client__nom']

@admin.register(InformationsFiscalesSociete)
class InformationsFiscalesSocieteAdmin(admin.ModelAdmin):
    list_display = ['societe', 'solde_imrtd_non_determines', 'solde_cdc']
    search_fields = ['societe__nom']
    ordering = ['societe__nom']

@admin.register(ProfilInvestisseur)
class ProfilInvestisseurAdmin(admin.ModelAdmin):
    list_display = ['client', 'profil', 'profil_fixe', 'taux_roulement_portefeuille']
    list_filter = ['profil', 'profil_fixe']
    search_fields = ['client__nom', 'client__prenom']
    ordering = ['client__nom', 'profil']

@admin.register(Actif)
class ActifAdmin(admin.ModelAdmin):
    list_display = ['client', 'type', 'juste_valeur_marchande', 'proprietaire']
    list_filter = ['type']
    search_fields = ['client__nom', 'client__prenom', 'proprietaire']
    ordering = ['client__nom', 'type']

@admin.register(FluxMonetaire)
class FluxMonetaireAdmin(admin.ModelAdmin):
    list_display = ['societe', 'annee', 'entree_fonds_imposable', 'sortie_fonds_deductible']
    list_filter = ['annee']
    search_fields = ['societe__nom']
    ordering = ['annee']
