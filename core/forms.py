from django import forms
from .models import (
    Conseiller, Client, Societe, Enfant, RevenusEmploi, 
    ActifPlacements, AssuranceVie, InformationsFiscalesClient,
    RevenusRRQ, BudgetPermanent, BudgetExtraordinaire
)

class ConseillerForm(forms.ModelForm):
    class Meta:
        model = Conseiller
        fields = ['nom', 'prenom', 'courriel', 'telephone', 'langue']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom'}),
            'prenom': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Prénom'}),
            'courriel': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'telephone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Téléphone'}),
            'langue': forms.Select(attrs={'class': 'form-control'}),
        }

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = [
            'conseiller', 'nom', 'prenom', 'province', 'etat_civil', 'sexe',
            'courriel', 'telephone', 'langue', 'date_naissance', 'fumeur', 'conjoint'
        ]
        widgets = {
            'conseiller': forms.Select(attrs={'class': 'form-control'}),
            'nom': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom'}),
            'prenom': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Prénom'}),
            'province': forms.Select(attrs={'class': 'form-control'}),
            'etat_civil': forms.Select(attrs={'class': 'form-control'}),
            'sexe': forms.Select(attrs={'class': 'form-control'}),
            'courriel': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'telephone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Téléphone'}),
            'langue': forms.Select(attrs={'class': 'form-control'}),
            'date_naissance': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'fumeur': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'conjoint': forms.Select(attrs={'class': 'form-control'}),
        }

class SocieteForm(forms.ModelForm):
    class Meta:
        model = Societe
        fields = [
            'client', 'nom', 'type_societe', 'revenus', 'depenses_deductibles',
            'depenses_non_deductibles', 'salaire_client', 'salaire_conjoint', 
            'salaire_employe', 'dpa_federale', 'dpa_provinciale', 'pourcentage_benefices_investis'
        ]
        widgets = {
            'client': forms.Select(attrs={'class': 'form-control'}),
            'nom': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom de la société'}),
            'type_societe': forms.Select(attrs={'class': 'form-control'}),
            'revenus': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'value': '0'}),
            'depenses_deductibles': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'value': '0'}),
            'depenses_non_deductibles': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'value': '0'}),
            'salaire_client': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'value': '0'}),
            'salaire_conjoint': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'value': '0'}),
            'salaire_employe': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'value': '0'}),
            'dpa_federale': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'value': '0'}),
            'dpa_provinciale': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'value': '0'}),
            'pourcentage_benefices_investis': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'value': '0'}),
        }

class EnfantForm(forms.ModelForm):
    class Meta:
        model = Enfant
        fields = [
            'client', 'nom', 'date_naissance', 'garde_partagee',
            'garderie_subventionnee', 'garderie_non_subventionnee',
            'date_debut', 'date_fin', 'cout_par_jour'
        ]
        widgets = {
            'client': forms.Select(attrs={'class': 'form-control'}),
            'nom': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom de l\'enfant'}),
            'date_naissance': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'garde_partagee': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'garderie_subventionnee': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'garderie_non_subventionnee': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'date_debut': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'date_fin': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'cout_par_jour': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }

class RevenusEmploiForm(forms.ModelForm):
    class Meta:
        model = RevenusEmploi
        fields = ['client', 'societe', 'date_debut', 'date_fin', 'revenus_emploi']
        widgets = {
            'client': forms.Select(attrs={'class': 'form-select'}),
            'societe': forms.Select(attrs={'class': 'form-select'}),
            'date_debut': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'date_fin': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'revenus_emploi': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }

class ActifPlacementsForm(forms.ModelForm):
    class Meta:
        model = ActifPlacements
        fields = ['client', 'type', 'montant', 'description']
        widgets = {
            'client': forms.Select(attrs={'class': 'form-select'}),
            'type': forms.Select(attrs={'class': 'form-select'}),
            'montant': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'description': forms.TextInput(attrs={'class': 'form-control'}),
        }

class AssuranceVieForm(forms.ModelForm):
    class Meta:
        model = AssuranceVie
        fields = ['categorie', 'preneur_client', 'personne_assuree', 'type', 'police_existante']
        widgets = {
            'categorie': forms.Select(attrs={'class': 'form-select'}),
            'preneur_client': forms.Select(attrs={'class': 'form-select'}),
            'personne_assuree': forms.Select(attrs={'class': 'form-select'}),
            'type': forms.Select(attrs={'class': 'form-select'}),
            'police_existante': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class InformationsFiscalesClientForm(forms.ModelForm):
    class Meta:
        model = InformationsFiscalesClient
        fields = ['client', 'droits_reer_inutilises', 'droits_celi_inutilises', 
                 'assurance_medicament_privee', 'report_psv']
        widgets = {
            'client': forms.Select(attrs={'class': 'form-select'}),
            'droits_reer_inutilises': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'droits_celi_inutilises': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'assurance_medicament_privee': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'report_psv': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class BudgetPermanentForm(forms.ModelForm):
    class Meta:
        model = BudgetPermanent
        fields = ['client', 'date_debut_budget_annuel_permanent', 'budget_annuel_permanent']
        widgets = {
            'client': forms.Select(attrs={'class': 'form-select'}),
            'date_debut_budget_annuel_permanent': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'budget_annuel_permanent': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }