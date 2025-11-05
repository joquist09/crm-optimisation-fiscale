from django import forms
from .models import (
    Conseiller, Client, Societe, Enfant, RevenusEmploi, RevenusEntreprise,
    AutresRevenus, ActifPlacements, AssuranceVie, InformationsFiscalesClient,
    RevenusRRQ, RevenusDividendes, FondPensionCD, FondPensionRRE, ProjectionRRE,
    FondPensionPD, CotisationComptePersonnel, BudgetPermanent, BudgetExtraordinaire,
    ProjectionAssuranceVie, InformationsFiscalesSociete, ProfilInvestisseur, Actif,
    FluxMonetaire
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
            'conseiller', 'prenom', 'nom', 'province', 'etat_civil', 'sexe',
            'courriel', 'telephone', 'langue', 'date_naissance', 'fumeur', 'conjoint'
        ]
        widgets = {
            'conseiller': forms.Select(attrs={'class': 'form-control'}),
            'prenom': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Prénom'}),
            'nom': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom'}),
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
            'client', 'nom', 'type_societe', 
            'solde_crtg_operante', 'revenus', 'date_debut_revenus', 'date_fin_revenus',
            'depenses_deductibles', 'date_debut_depenses_ded', 'date_fin_depenses_ded',
            'depenses_non_deductibles', 'date_debut_depenses_non_ded', 'date_fin_depenses_non_ded',
            'salaire_client', 'date_debut_salaire_client', 'date_fin_salaire_client',
            'salaire_conjoint', 'date_debut_salaire_conjoint', 'date_fin_salaire_conjoint',
            'salaire_employe', 'date_debut_salaire_employe', 'date_fin_salaire_employe',
            'dpa_federale', 'dpa_provinciale', 'pourcentage_benefices_investis',
            'solde_imrtd_non_determines', 'solde_imrtd_determines', 'solde_cdc', 
            'solde_crtg_gestion', 'paqc_reportee', 'annee_maximale_paqc', 'perte_capitale',
            'pbr_actions_ordinaires', 'capital_verse', 'actions_dividendes_discretionnaires'
        ]
        labels = {
            'solde_crtg_operante': 'Solde CRTG opérante ($)',
            'revenus': 'Revenus ($)',
            'depenses_deductibles': 'Dépenses déductibles ($)',
            'depenses_non_deductibles': 'Dépenses non déductibles ($)',
            'salaire_client': 'Salaire client ($)',
            'salaire_conjoint': 'Salaire conjoint ($)',
            'salaire_employe': 'Salaire employé ($)',
            'dpa_federale': 'DPA fédérale ($)',
            'dpa_provinciale': 'DPA provinciale ($)',
            'solde_imrtd_non_determines': 'Solde IMRTD non déterminés ($)',
            'solde_imrtd_determines': 'Solde IMRTD déterminés ($)',
            'solde_cdc': 'Solde CDC ($)',
            'solde_crtg_gestion': 'Solde CRTG gestion ($)',
            'paqc_reportee': 'PAQC reportée ($)',
            'perte_capitale': 'Perte capitale ($)',
            'pbr_actions_ordinaires': 'PBR actions ordinaires ($)',
            'capital_verse': 'Capital versé ($)',
            'actions_dividendes_discretionnaires': 'Actions dividendes discrétionnaires ($)',
        }
        widgets = {
            'client': forms.Select(attrs={'class': 'form-control'}),
            'nom': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom de la société'}),
            'type_societe': forms.Select(attrs={'class': 'form-control'}),
            'solde_crtg_operante': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'value': '0'}),
            'revenus': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'value': '0'}),
            'date_debut_revenus': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'date_fin_revenus': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'depenses_deductibles': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'value': '0'}),
            'date_debut_depenses_ded': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'date_fin_depenses_ded': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'depenses_non_deductibles': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'value': '0'}),
            'date_debut_depenses_non_ded': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'date_fin_depenses_non_ded': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'salaire_client': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'value': '0'}),
            'date_debut_salaire_client': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'date_fin_salaire_client': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'salaire_conjoint': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'value': '0'}),
            'date_debut_salaire_conjoint': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'date_fin_salaire_conjoint': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'salaire_employe': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'value': '0'}),
            'date_debut_salaire_employe': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'date_fin_salaire_employe': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'dpa_federale': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'value': '0'}),
            'dpa_provinciale': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'value': '0'}),
            'pourcentage_benefices_investis': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'value': '0'}),
            'solde_imrtd_non_determines': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'value': '0'}),
            'solde_imrtd_determines': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'value': '0'}),
            'solde_cdc': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'value': '0'}),
            'solde_crtg_gestion': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'value': '0'}),
            'paqc_reportee': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'value': '0'}),
            'annee_maximale_paqc': forms.NumberInput(attrs={'class': 'form-control', 'value': '0'}),
            'perte_capitale': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'value': '0'}),
            'pbr_actions_ordinaires': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'value': '0'}),
            'capital_verse': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'value': '0'}),
            'actions_dividendes_discretionnaires': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'value': '0'}),
        }

class EnfantForm(forms.ModelForm):
    class Meta:
        model = Enfant
        fields = [
            'client', 'nom', 'date_naissance', 'garde_partagee',
            'garderie_subventionnee', 'garderie_non_subventionnee',
            'date_debut', 'date_fin', 'cout_par_jour'
        ]
        labels = {
            'cout_par_jour': 'Coût par jour ($)',
        }
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
        labels = {
            'revenus_emploi': 'Revenus d\'emploi ($)',
        }
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
        labels = {
            'montant': 'Montant ($)',
        }
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
        labels = {
            'droits_reer_inutilises': 'Droits REER inutilisés ($)',
            'droits_celi_inutilises': 'Droits CELI inutilisés ($)',
        }
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
        labels = {
            'budget_annuel_permanent': 'Budget annuel permanent ($)',
        }
        widgets = {
            'client': forms.Select(attrs={'class': 'form-select'}),
            'date_debut_budget_annuel_permanent': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'budget_annuel_permanent': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }

class RevenusEntrepriseForm(forms.ModelForm):
    class Meta:
        model = RevenusEntreprise
        fields = ['client', 'revenus_entreprise', 'date_debut', 'date_fin', 'depenses_deductibles']
        labels = {
            'revenus_entreprise': 'Revenus d\'entreprise ($)',
            'depenses_deductibles': 'Dépenses déductibles ($)',
        }
        widgets = {
            'client': forms.Select(attrs={'class': 'form-select'}),
            'revenus_entreprise': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'date_debut': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'date_fin': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'depenses_deductibles': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }

class AutresRevenusForm(forms.ModelForm):
    class Meta:
        model = AutresRevenus
        fields = ['client', 'type', 'date_debut', 'date_fin', 'montant', 'description', 'pourcentage_imposable']
        widgets = {
            'client': forms.Select(attrs={'class': 'form-select'}),
            'type': forms.Select(attrs={'class': 'form-select'}),
            'date_debut': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'date_fin': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'montant': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'description': forms.TextInput(attrs={'class': 'form-control'}),
            'pourcentage_imposable': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }

class RevenusRRQForm(forms.ModelForm):
    class Meta:
        model = RevenusRRQ
        fields = ['client', 'type', 'rentes_revenus_rrq_rpc', 'date_debut_rrq_rpc', 'revenu_admissible', 'annee']
        widgets = {
            'client': forms.Select(attrs={'class': 'form-select'}),
            'type': forms.Select(attrs={'class': 'form-select'}),
            'rentes_revenus_rrq_rpc': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'date_debut_rrq_rpc': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'revenu_admissible': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'annee': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class RevenusDividendesForm(forms.ModelForm):
    class Meta:
        model = RevenusDividendes
        fields = ['client', 'societe', 'date_debut', 'date_fin', 'revenus_dividendes', 
                  'dividende_ordinaire', 'dividende_determine', 'dividende_capital']
        widgets = {
            'client': forms.Select(attrs={'class': 'form-select'}),
            'societe': forms.Select(attrs={'class': 'form-select'}),
            'date_debut': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'date_fin': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'revenus_dividendes': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'dividende_ordinaire': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'dividende_determine': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'dividende_capital': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }

class FondPensionCDForm(forms.ModelForm):
    class Meta:
        model = FondPensionCD
        fields = ['client', 'cotisation_totale', 'date_debut_cotisation_totale', 'date_fin_cotisation_totale',
                  'cotisation_employeur', 'date_debut_cotisation_employeur', 'date_fin_cotisation_employeur']
        widgets = {
            'client': forms.Select(attrs={'class': 'form-select'}),
            'cotisation_totale': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'date_debut_cotisation_totale': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'date_fin_cotisation_totale': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'cotisation_employeur': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'date_debut_cotisation_employeur': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'date_fin_cotisation_employeur': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

class FondPensionRREForm(forms.ModelForm):
    class Meta:
        model = FondPensionRRE
        fields = ['participant', 'promoteur', 'transfert_initial_pd', 'transfert_initial_cva', 
                  'transfert_initial_cd', 'solde_immobilise', 'solde_cva', 'transfert_intergenerationnel']
        widgets = {
            'participant': forms.Select(attrs={'class': 'form-select'}),
            'promoteur': forms.Select(attrs={'class': 'form-select'}),
            'transfert_initial_pd': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'transfert_initial_cva': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'transfert_initial_cd': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'solde_immobilise': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'solde_cva': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'transfert_intergenerationnel': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class ProjectionRREForm(forms.ModelForm):
    class Meta:
        model = ProjectionRRE
        fields = ['fonds_pension_rre', 'annee', 'cotisation_regulieres', 'cotisation_service_passe',
                  'cotisation_volontaire_additionnelles', 'rente', 'ajustements_frais_annuels']
        widgets = {
            'fonds_pension_rre': forms.Select(attrs={'class': 'form-select'}),
            'annee': forms.NumberInput(attrs={'class': 'form-control'}),
            'cotisation_regulieres': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'cotisation_service_passe': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'cotisation_volontaire_additionnelles': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'rente': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'ajustements_frais_annuels': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }

class FondPensionPDForm(forms.ModelForm):
    class Meta:
        model = FondPensionPD
        fields = ['client', 'revenu_pension_1', 'date_debut_revenu_pension_1', 'date_fin_revenu_pension_1',
                  'revenu_pension_2', 'date_debut_revenu_pension_2', 'date_fin_revenu_pension_2',
                  'cotisation_employe', 'date_debut_cotisation_employe', 'date_fin_cotisation_employe',
                  'facteur_equivalence']
        widgets = {
            'client': forms.Select(attrs={'class': 'form-select'}),
            'revenu_pension_1': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'date_debut_revenu_pension_1': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'date_fin_revenu_pension_1': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'revenu_pension_2': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'date_debut_revenu_pension_2': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'date_fin_revenu_pension_2': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'cotisation_employe': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'date_debut_cotisation_employe': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'date_fin_cotisation_employe': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'facteur_equivalence': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }

class CotisationComptePersonnelForm(forms.ModelForm):
    class Meta:
        model = CotisationComptePersonnel
        fields = ['actif', 'cotisation_annuelle', 'date_debut', 'date_fin', 'indexation']
        widgets = {
            'actif': forms.Select(attrs={'class': 'form-select'}),
            'cotisation_annuelle': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'date_debut': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'date_fin': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'indexation': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }

class BudgetExtraordinaireForm(forms.ModelForm):
    class Meta:
        model = BudgetExtraordinaire
        fields = ['client', 'date_debut', 'date_fin', 'budget_extraordinaire', 'indexation']
        widgets = {
            'client': forms.Select(attrs={'class': 'form-select'}),
            'date_debut': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'date_fin': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'budget_extraordinaire': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'indexation': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }

class ProjectionAssuranceVieForm(forms.ModelForm):
    class Meta:
        model = ProjectionAssuranceVie
        fields = ['assurance_vie', 'annee', 'capital_deces', 'cout_base_rajuste', 'valeur_rachat', 'prime_annuelle']
        widgets = {
            'assurance_vie': forms.Select(attrs={'class': 'form-select'}),
            'annee': forms.NumberInput(attrs={'class': 'form-control'}),
            'capital_deces': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'cout_base_rajuste': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'valeur_rachat': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'prime_annuelle': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }

class InformationsFiscalesSocieteForm(forms.ModelForm):
    class Meta:
        model = InformationsFiscalesSociete
        fields = ['societe', 'solde_imrtd_non_determines', 'solde_imrtd_determines', 'solde_crtg', 'solde_cdc',
                  'seuil_cdc', 'frais_cdc', 'paqc_reportee', 'annee_maximale_paqc', 'perte_capitale',
                  'pbr_actions_ordinaires', 'capital_verse', 'actions_dividendes_discretionnaires']
        widgets = {
            'societe': forms.Select(attrs={'class': 'form-select'}),
            'solde_imrtd_non_determines': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'solde_imrtd_determines': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'solde_crtg': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'solde_cdc': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'seuil_cdc': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'frais_cdc': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'paqc_reportee': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'annee_maximale_paqc': forms.NumberInput(attrs={'class': 'form-control'}),
            'perte_capitale': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'pbr_actions_ordinaires': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'capital_verse': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'actions_dividendes_discretionnaires': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }

class ProfilInvestisseurForm(forms.ModelForm):
    class Meta:
        model = ProfilInvestisseur
        fields = ['client', 'profil', 'profil_fixe', 'ajustement_revenus_fixe', 'ajustement_frais_action',
                  'ajustement_honoraires', 'honoraires', 'taux_roulement_portefeuille']
        widgets = {
            'client': forms.Select(attrs={'class': 'form-select'}),
            'profil': forms.Select(attrs={'class': 'form-select'}),
            'profil_fixe': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'ajustement_revenus_fixe': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'ajustement_frais_action': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'ajustement_honoraires': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'honoraires': forms.Select(attrs={'class': 'form-select'}),
            'taux_roulement_portefeuille': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }

class ActifForm(forms.ModelForm):
    class Meta:
        model = Actif
        fields = ['client', 'societe', 'type', 'descriptif', 'proprietaire', 'pourcentage_detenu',
                  'juste_valeur_marchande', 'indexation_jvm', 'pbr_total', 'pbr_terrain', 'fnacc',
                  'taux_dpa', 'annee_acquisition_futur', 'date_disposition', 'emprunts', 'revenus',
                  'dons', 'au_deces', 'solde_pret', 'date_solde', 'versement_mensuel', 
                  'date_dernier_versement', 'taux_estime', 'debut_mois', 'interet_seulement',
                  'interets_deductibles', 'net_avant_interet', 'indexation', 'entreprise', 
                  'du_vivant', 'contrepartie']
        widgets = {
            'client': forms.Select(attrs={'class': 'form-select'}),
            'societe': forms.Select(attrs={'class': 'form-select'}),
            'type': forms.Select(attrs={'class': 'form-select'}),
            'descriptif': forms.TextInput(attrs={'class': 'form-control'}),
            'proprietaire': forms.TextInput(attrs={'class': 'form-control'}),
            'pourcentage_detenu': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'juste_valeur_marchande': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'indexation_jvm': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'pbr_total': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'pbr_terrain': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'fnacc': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'taux_dpa': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'annee_acquisition_futur': forms.NumberInput(attrs={'class': 'form-control'}),
            'date_disposition': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'emprunts': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'revenus': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'dons': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'au_deces': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'solde_pret': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'date_solde': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'versement_mensuel': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'date_dernier_versement': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'taux_estime': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'debut_mois': forms.Select(attrs={'class': 'form-select'}),
            'interet_seulement': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'interets_deductibles': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'net_avant_interet': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'indexation': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'entreprise': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'du_vivant': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'contrepartie': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }

class FluxMonetaireForm(forms.ModelForm):
    class Meta:
        model = FluxMonetaire
        fields = ['societe', 'annee', 'entree_fonds_imposable', 'entree_fonds_non_imposable',
                  'sortie_fonds_deductible', 'sortie_fonds_non_deductible']
        widgets = {
            'societe': forms.Select(attrs={'class': 'form-select'}),
            'annee': forms.NumberInput(attrs={'class': 'form-control'}),
            'entree_fonds_imposable': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'entree_fonds_non_imposable': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'sortie_fonds_deductible': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'sortie_fonds_non_deductible': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }