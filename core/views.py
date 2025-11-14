from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponse
import csv
from datetime import datetime
from .models import (
    Conseiller, Client, Societe, Enfant, RevenusEmploi, RevenusEntreprise,
    AutresRevenus, ActifPlacements, AssuranceVie, InformationsFiscalesClient,
    RevenusRRQ, RevenusDividendes, FondPensionCD, FondPensionRRE, ProjectionRRE, 
    FondPensionPD, BudgetPermanent, BudgetExtraordinaire, InformationsFiscalesSociete,
    ProfilInvestisseur, Actif, FluxMonetaire, CotisationComptePersonnel, ProjectionAssuranceVie
)
from .forms import (
    ConseillerForm, ClientForm, SocieteForm, EnfantForm,
    RevenusEmploiForm, RevenusEntrepriseForm, AutresRevenusForm,
    ActifPlacementsForm, AssuranceVieForm, InformationsFiscalesClientForm, 
    BudgetPermanentForm, RevenusRRQForm, RevenusDividendesForm, FondPensionCDForm,
    FondPensionRREForm, ProjectionRREForm, FondPensionPDForm, CotisationComptePersonnelForm,
    BudgetExtraordinaireForm, ProjectionAssuranceVieForm, InformationsFiscalesSocieteForm,
    ProfilInvestisseurForm, ActifForm, FluxMonetaireForm
)

def dashboard(request):
    """Dashboard principal du CRM"""
    conseillers_count = Conseiller.objects.count()
    clients_count = Client.objects.count()
    societes_count = Societe.objects.count()
    
    recent_clients = Client.objects.order_by('-id')[:5]
    recent_conseillers = Conseiller.objects.order_by('-date_creation')[:5]
    
    context = {
        'conseillers_count': conseillers_count,
        'clients_count': clients_count,
        'societes_count': societes_count,
        'recent_clients': recent_clients,
        'recent_conseillers': recent_conseillers,
    }
    return render(request, 'core/dashboard.html', context)

# Vues Conseiller
def conseiller_list(request):
    """Liste des conseillers"""
    search = request.GET.get('search', '')
    conseillers = Conseiller.objects.all()
    
    if search:
        conseillers = conseillers.filter(
            Q(nom__icontains=search) | 
            Q(prenom__icontains=search) |
            Q(courriel__icontains=search)
        )
    
    return render(request, 'core/conseiller_list.html', {
        'conseillers': conseillers,
        'search': search
    })

def conseiller_detail(request, pk):
    """Détail d'un conseiller"""
    conseiller = get_object_or_404(Conseiller, pk=pk)
    clients = conseiller.clients.all()
    return render(request, 'core/conseiller_detail.html', {
        'conseiller': conseiller,
        'clients': clients
    })

def conseiller_create(request):
    """Création d'un conseiller"""
    if request.method == 'POST':
        form = ConseillerForm(request.POST)
        if form.is_valid():
            conseiller = form.save()
            messages.success(request, f'Conseiller {conseiller.nom} {conseiller.prenom} créé avec succès!')
            return redirect('conseiller_detail', pk=conseiller.pk)
    else:
        form = ConseillerForm()
    
    return render(request, 'core/conseiller_form.html', {
        'form': form,
        'title': 'Créer un conseiller'
    })

def conseiller_edit(request, pk):
    """Modification d'un conseiller"""
    conseiller = get_object_or_404(Conseiller, pk=pk)
    if request.method == 'POST':
        form = ConseillerForm(request.POST, instance=conseiller)
        if form.is_valid():
            form.save()
            messages.success(request, f'Conseiller {conseiller.nom} {conseiller.prenom} modifié avec succès!')
            return redirect('conseiller_detail', pk=conseiller.pk)
    else:
        form = ConseillerForm(instance=conseiller)
    
    return render(request, 'core/conseiller_form.html', {
        'form': form,
        'title': f'Modifier {conseiller.nom} {conseiller.prenom}',
        'conseiller': conseiller
    })

# Vues Client
def client_list(request):
    """Liste des clients"""
    search = request.GET.get('search', '')
    conseiller_id = request.GET.get('conseiller', '')
    
    clients = Client.objects.select_related('conseiller').all()
    
    if search:
        clients = clients.filter(
            Q(nom__icontains=search) | 
            Q(prenom__icontains=search) |
            Q(courriel__icontains=search)
        )
    
    if conseiller_id:
        clients = clients.filter(conseiller_id=conseiller_id)
    
    conseillers = Conseiller.objects.all()
    
    return render(request, 'core/client_list.html', {
        'clients': clients,
        'conseillers': conseillers,
        'search': search,
        'selected_conseiller': conseiller_id
    })

def client_detail(request, pk):
    """Détail d'un client"""
    client = get_object_or_404(Client, pk=pk)
    
    # Sociétés et Enfants
    societes = client.societe_set.all()
    enfants = client.enfants.all()
    
    # Revenus groupés
    revenus_emploi = client.revenus_emploi.all()
    revenus_entreprise = client.revenus_entreprise.all()
    revenus_dividendes = client.revenus_dividendes.all()
    revenus_rrq = client.revenus_rrq.all()
    autres_revenus = client.revenus_personnels.all()  # related_name="revenus_personnels"
    
    # Placements et Actifs
    actifs_placements = client.actifs_placements.all()
    actifs = client.actif_set.all()  # No related_name, so Django uses default
    profil_investisseur = client.profilinvestisseur_set.all()  # No related_name
    
    # Fonds de pension
    fonds_pension_cd = client.fondpensioncd_set.all()  # No related_name
    fonds_pension_rre = client.fondpensionrre_set.all()  # No related_name
    projections_rre = ProjectionRRE.objects.filter(fonds_pension_rre__participant=client)  # Through relation
    fonds_pension_pd = client.fondpensionpd_set.all()  # No related_name
    cotisations_compte_personnel = CotisationComptePersonnel.objects.filter(actif__client=client)  # Through relation
    
    # Assurances et finances
    assurances_vie = client.assurances_assuree.all()  # related_name="assurances_assuree"
    projections_assurance_vie = ProjectionAssuranceVie.objects.filter(assurance_vie__personne_assuree=client)  # Through relation
    budgets_permanents = client.budget_permanent.all()  # related_name="budget_permanent"
    budgets_extraordinaires = client.budget_extraordinaire.all()  # related_name="budget_extraordinaire"
    flux_monetaires = FluxMonetaire.objects.filter(societe__client=client)  # Through relation
    informations_fiscales = client.informationsfiscalesclient_set.all()  # No related_name
    
    return render(request, 'core/client_detail.html', {
        'client': client,
        'societes': societes,
        'enfants': enfants,
        # Revenus
        'revenus_emploi': revenus_emploi,
        'revenus_entreprise': revenus_entreprise,
        'revenus_dividendes': revenus_dividendes,
        'revenus_rrq': revenus_rrq,
        'autres_revenus': autres_revenus,
        # Placements
        'actifs_placements': actifs_placements,
        'actifs': actifs,
        'profil_investisseur': profil_investisseur,
        # Pensions
        'fonds_pension_cd': fonds_pension_cd,
        'fonds_pension_rre': fonds_pension_rre,
        'projections_rre': projections_rre,
        'fonds_pension_pd': fonds_pension_pd,
        'cotisations_compte_personnel': cotisations_compte_personnel,
        # Assurances et finances
        'assurances_vie': assurances_vie,
        'projections_assurance_vie': projections_assurance_vie,
        'budgets_permanents': budgets_permanents,
        'budgets_extraordinaires': budgets_extraordinaires,
        'flux_monetaires': flux_monetaires,
        'informations_fiscales': informations_fiscales,
    })

def client_create(request):
    """Création d'un client"""
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            client = form.save()
            messages.success(request, f'Client {client.nom} {client.prenom} créé avec succès!')
            return redirect('client_detail', pk=client.pk)
    else:
        form = ClientForm()
    
    return render(request, 'core/client_form.html', {
        'form': form,
        'title': 'Créer un client'
    })

def client_edit(request, pk):
    """Modification d'un client"""
    client = get_object_or_404(Client, pk=pk)
    if request.method == 'POST':
        form = ClientForm(request.POST, instance=client)
        if form.is_valid():
            form.save()
            messages.success(request, f'Client {client.nom} {client.prenom} modifié avec succès!')
            return redirect('client_detail', pk=client.pk)
    else:
        form = ClientForm(instance=client)
    
    return render(request, 'core/client_form.html', {
        'form': form,
        'title': f'Modifier {client.nom} {client.prenom}',
        'client': client
    })

# Vues Société
def societe_list(request):
    """Liste des sociétés"""
    search = request.GET.get('search', '')
    societes = Societe.objects.select_related('client').all()
    
    if search:
        societes = societes.filter(
            Q(nom__icontains=search) |
            Q(client__nom__icontains=search) |
            Q(client__prenom__icontains=search)
        )
    
    return render(request, 'core/societe_list.html', {
        'societes': societes,
        'search': search
    })

def societe_detail(request, pk):
    """Détail d'une société"""
    societe = get_object_or_404(Societe, pk=pk)
    return render(request, 'core/societe_detail.html', {
        'societe': societe
    })

def societe_create(request):
    """Création d'une société"""
    client_id = request.GET.get('client')
    if request.method == 'POST':
        form = SocieteForm(request.POST)
        if form.is_valid():
            societe = form.save()
            messages.success(request, f'Société {societe.nom} créée avec succès!')
            return redirect('societe_detail', pk=societe.pk)
    else:
        form = SocieteForm()
        if client_id:
            form.fields['client'].initial = client_id
    
    return render(request, 'core/societe_form.html', {
        'form': form,
        'title': 'Créer une société'
    })

def societe_edit(request, pk):
    """Modification d'une société"""
    societe = get_object_or_404(Societe, pk=pk)
    if request.method == 'POST':
        form = SocieteForm(request.POST, instance=societe)
        if form.is_valid():
            form.save()
            messages.success(request, f'Société {societe.nom} modifiée avec succès!')
            return redirect('societe_detail', pk=societe.pk)
    else:
        form = SocieteForm(instance=societe)
    
    return render(request, 'core/societe_form.html', {
        'form': form,
        'title': f'Modifier {societe.nom}',
        'societe': societe
    })

# Vues Enfant
def enfant_create(request):
    """Création d'un enfant"""
    client_id = request.GET.get('client')
    if request.method == 'POST':
        form = EnfantForm(request.POST)
        if form.is_valid():
            enfant = form.save()
            messages.success(request, f'Enfant {enfant.nom} créé avec succès!')
            return redirect('client_detail', pk=enfant.client.pk)
    else:
        form = EnfantForm()
        if client_id:
            form.fields['client'].initial = client_id
    
    return render(request, 'core/enfant_form.html', {
        'form': form,
        'title': 'Ajouter un enfant'
    })

def enfant_edit(request, pk):
    """Modification d'un enfant"""
    enfant = get_object_or_404(Enfant, pk=pk)
    if request.method == 'POST':
        form = EnfantForm(request.POST, instance=enfant)
        if form.is_valid():
            form.save()
            messages.success(request, f'Enfant {enfant.nom} modifié avec succès!')
            return redirect('client_detail', pk=enfant.client.pk)
    else:
        form = EnfantForm(instance=enfant)
    
    return render(request, 'core/enfant_form.html', {
        'form': form,
        'title': f'Modifier {enfant.nom}',
        'enfant': enfant
    })

# Vues Revenus Emploi
def revenus_emploi_list(request):
    """Liste des revenus d'emploi"""
    search = request.GET.get('search', '')
    revenus = RevenusEmploi.objects.select_related('client', 'societe').all()
    
    if search:
        revenus = revenus.filter(
            Q(client__nom__icontains=search) |
            Q(client__prenom__icontains=search) |
            Q(societe__nom__icontains=search)
        )
    
    return render(request, 'core/revenus_emploi_list.html', {
        'revenus': revenus,
        'search': search
    })

def revenus_emploi_create(request):
    """Création d'un revenu d'emploi"""
    client_id = request.GET.get('client')
    if request.method == 'POST':
        form = RevenusEmploiForm(request.POST)
        if form.is_valid():
            revenu = form.save()
            messages.success(request, 'Revenu d\'emploi créé avec succès!')
            return redirect('client_detail', pk=revenu.client.pk)
    else:
        form = RevenusEmploiForm()
        if client_id:
            form.fields['client'].initial = client_id
    
    return render(request, 'core/revenus_emploi_form.html', {
        'form': form,
        'title': 'Ajouter un revenu d\'emploi'
    })

# Vues Actifs Placements
def actifs_placements_list(request):
    """Liste des actifs placements"""
    search = request.GET.get('search', '')
    actifs = ActifPlacements.objects.select_related('client').all()
    
    if search:
        actifs = actifs.filter(
            Q(client__nom__icontains=search) |
            Q(client__prenom__icontains=search) |
            Q(description__icontains=search)
        )
    
    return render(request, 'core/actifs_placements_list.html', {
        'actifs': actifs,
        'search': search
    })

def actifs_placements_create(request):
    """Création d'un actif placement"""
    client_id = request.GET.get('client')
    if request.method == 'POST':
        form = ActifPlacementsForm(request.POST)
        if form.is_valid():
            actif = form.save()
            messages.success(request, 'Actif placement créé avec succès!')
            return redirect('client_detail', pk=actif.client.pk)
    else:
        form = ActifPlacementsForm()
        if client_id:
            form.fields['client'].initial = client_id
    
    return render(request, 'core/actifs_placements_form.html', {
        'form': form,
        'title': 'Ajouter un actif placement'
    })

# Vues Assurances Vie
def assurances_vie_list(request):
    """Liste des assurances vie"""
    search = request.GET.get('search', '')
    assurances = AssuranceVie.objects.select_related('preneur_client', 'personne_assuree').all()
    
    if search:
        assurances = assurances.filter(
            Q(preneur_client__nom__icontains=search) |
            Q(personne_assuree__nom__icontains=search)
        )
    
    return render(request, 'core/assurances_vie_list.html', {
        'assurances': assurances,
        'search': search
    })

def assurances_vie_create(request):
    """Création d'une assurance vie"""
    if request.method == 'POST':
        form = AssuranceVieForm(request.POST)
        if form.is_valid():
            assurance = form.save()
            messages.success(request, 'Assurance vie créée avec succès!')
            return redirect('assurances_vie_list')
    else:
        form = AssuranceVieForm()
    
    return render(request, 'core/assurances_vie_form.html', {
        'form': form,
        'title': 'Ajouter une assurance vie'
    })

def export_csv(request):
    """Exporter toutes les données en CSV"""
    response = HttpResponse(content_type='text/csv; charset=utf-8')
    response['Content-Disposition'] = f'attachment; filename="export_crm_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv"'
    response.write('\ufeff')  # BOM pour Excel UTF-8
    
    writer = csv.writer(response)
    
    # Export des Conseillers
    writer.writerow(['=== CONSEILLERS ==='])
    writer.writerow(['ID', 'Nom', 'Prénom', 'Email', 'Téléphone', 'Langue', 'Date création'])
    
    for conseiller in Conseiller.objects.all():
        writer.writerow([
            conseiller.id,
            conseiller.nom,
            conseiller.prenom,
            conseiller.courriel,
            conseiller.telephone,
            conseiller.langue,
            conseiller.date_creation.strftime('%Y-%m-%d %H:%M') if conseiller.date_creation else ''
        ])
    
    writer.writerow([])  # Ligne vide
    
    # Export des Clients
    writer.writerow(['=== CLIENTS ==='])
    writer.writerow(['ID', 'Conseiller', 'Nom', 'Prénom', 'Email', 'Téléphone', 'Date naissance', 'Province', 'État civil', 'Sexe', 'Langue', 'Fumeur'])
    
    for client in Client.objects.select_related('conseiller').all():
        writer.writerow([
            client.id,
            f"{client.conseiller.nom} {client.conseiller.prenom}" if client.conseiller else '',
            client.nom,
            client.prenom,
            client.courriel,
            client.telephone,
            client.date_naissance.strftime('%Y-%m-%d') if client.date_naissance else '',
            client.get_province_display(),
            client.get_etat_civil_display(),
            client.get_sexe_display(),
            client.get_langue_display(),
            'Oui' if client.fumeur else 'Non'
        ])
    
    writer.writerow([])  # Ligne vide
    
    # Export des Sociétés
    writer.writerow(['=== SOCIÉTÉS ==='])
    writer.writerow(['ID', 'Client', 'Nom', 'Type', 'Revenus', 'Dépenses déductibles', 'Dépenses non déductibles', 
                     'Salaire client', 'Salaire conjoint', 'Salaire employé', 'DPA fédérale', 'DPA provinciale', '% bénéfices investis'])
    
    for societe in Societe.objects.select_related('client').all():
        writer.writerow([
            societe.id,
            f"{societe.client.nom} {societe.client.prenom}" if societe.client else '',
            societe.nom,
            societe.type_societe,
            societe.revenus,
            societe.depenses_deductibles,
            societe.depenses_non_deductibles,
            societe.salaire_client,
            societe.salaire_conjoint,
            societe.salaire_employe,
            societe.dpa_federale,
            societe.dpa_provinciale,
            societe.pourcentage_benefices_investis
        ])
    
    writer.writerow([])  # Ligne vide
    
    # Export des Enfants
    writer.writerow(['=== ENFANTS ==='])
    writer.writerow(['ID', 'Client', 'Nom', 'Date naissance', 'Garde partagée', 'Garderie subventionnée', 'Garderie non subventionnée', 'Date début', 'Date fin', 'Coût par jour'])
    
    for enfant in Enfant.objects.select_related('client').all():
        writer.writerow([
            enfant.id,
            f"{enfant.client.nom} {enfant.client.prenom}" if enfant.client else '',
            enfant.nom,
            enfant.date_naissance.strftime('%Y-%m-%d') if enfant.date_naissance else '',
            'Oui' if enfant.garde_partagee else 'Non',
            'Oui' if enfant.garderie_subventionnee else 'Non',
            'Oui' if enfant.garderie_non_subventionnee else 'Non',
            enfant.date_debut.strftime('%Y-%m-%d') if enfant.date_debut else '',
            enfant.date_fin.strftime('%Y-%m-%d') if enfant.date_fin else '',
            enfant.cout_par_jour
        ])
    
    writer.writerow([])  # Ligne vide
    
    # Export des Revenus d'Emploi
    writer.writerow(['=== REVENUS D\'EMPLOI ==='])
    writer.writerow(['ID', 'Client', 'Société', 'Date début', 'Date fin', 'Revenus emploi'])
    
    for revenu in RevenusEmploi.objects.select_related('client', 'societe').all():
        writer.writerow([
            revenu.id,
            f"{revenu.client.nom} {revenu.client.prenom}" if revenu.client else '',
            revenu.societe.nom if revenu.societe else '',
            revenu.date_debut.strftime('%Y-%m-%d') if revenu.date_debut else '',
            revenu.date_fin.strftime('%Y-%m-%d') if revenu.date_fin else '',
            revenu.revenus_emploi
        ])
    
    writer.writerow([])  # Ligne vide
    
    # Export des Actifs Placements
    writer.writerow(['=== ACTIFS PLACEMENTS ==='])
    writer.writerow(['ID', 'Client', 'Type', 'Montant', 'Description'])
    
    for actif in ActifPlacements.objects.select_related('client').all():
        writer.writerow([
            actif.id,
            f"{actif.client.nom} {actif.client.prenom}" if actif.client else '',
            actif.get_type_display(),
            actif.montant,
            actif.description
        ])
    
    writer.writerow([])  # Ligne vide
    
    # Export des Assurances Vie
    writer.writerow(['=== ASSURANCES VIE ==='])
    writer.writerow(['ID', 'Catégorie', 'Preneur Client', 'Personne Assurée', 'Type', 'Police Existante'])
    
    for assurance in AssuranceVie.objects.select_related('preneur_client', 'personne_assuree').all():
        writer.writerow([
            assurance.id,
            assurance.get_categorie_display(),
            f"{assurance.preneur_client.nom} {assurance.preneur_client.prenom}" if assurance.preneur_client else '',
            f"{assurance.personne_assuree.nom} {assurance.personne_assuree.prenom}" if assurance.personne_assuree else '',
            assurance.get_type_display(),
            'Oui' if assurance.police_existante else 'Non'
        ])
    
    writer.writerow([])  # Ligne vide
    
    # Export des Informations Fiscales Clients
    writer.writerow(['=== INFORMATIONS FISCALES CLIENTS ==='])
    writer.writerow(['ID', 'Client', 'Droits REER inutilisés', 'Droits CELI inutilisés', 'Assurance médicament privée', 'Report PSV'])
    
    for info_fiscale in InformationsFiscalesClient.objects.select_related('client').all():
        writer.writerow([
            info_fiscale.id,
            f"{info_fiscale.client.nom} {info_fiscale.client.prenom}" if info_fiscale.client else '',
            info_fiscale.droits_reer_inutilises,
            info_fiscale.droits_celi_inutilises,
            'Oui' if info_fiscale.assurance_medicament_privee else 'Non',
            info_fiscale.report_psv
        ])
    
    writer.writerow([])  # Ligne vide
    
    # Export des Revenus RRQ
    writer.writerow(['=== REVENUS RRQ ==='])
    writer.writerow(['ID', 'Client', 'Type', 'Rentes revenus RRQ/RPC', 'Date début', 'Revenu admissible', 'Année'])
    
    for revenu_rrq in RevenusRRQ.objects.select_related('client').all():
        writer.writerow([
            revenu_rrq.id,
            f"{revenu_rrq.client.nom} {revenu_rrq.client.prenom}" if revenu_rrq.client else '',
            revenu_rrq.get_type_display(),
            revenu_rrq.rentes_revenus_rrq_rpc,
            revenu_rrq.date_debut_rrq_rpc.strftime('%Y-%m-%d') if revenu_rrq.date_debut_rrq_rpc else '',
            revenu_rrq.revenu_admissible,
            revenu_rrq.annee
        ])
    
    writer.writerow([])  # Ligne vide
    
    # Export des Budgets Permanents
    writer.writerow(['=== BUDGETS PERMANENTS ==='])
    writer.writerow(['ID', 'Client', 'Date début', 'Budget annuel permanent'])
    
    for budget in BudgetPermanent.objects.select_related('client').all():
        writer.writerow([
            budget.id,
            f"{budget.client.nom} {budget.client.prenom}" if budget.client else '',
            budget.date_debut_budget_annuel_permanent.strftime('%Y-%m-%d') if budget.date_debut_budget_annuel_permanent else '',
            budget.budget_annuel_permanent
        ])

    return response

# Vues Revenus Entreprise
def revenus_entreprise_list(request):
    """Liste des revenus d'entreprise (travailleur autonome)"""
    search = request.GET.get('search', '')
    revenus = RevenusEntreprise.objects.select_related('client').all()
    
    if search:
        revenus = revenus.filter(
            Q(client__nom__icontains=search) |
            Q(client__prenom__icontains=search)
        )
    
    return render(request, 'core/revenus_entreprise_list.html', {
        'revenus': revenus,
        'search': search
    })

def revenus_entreprise_create(request):
    """Création d'un revenu d'entreprise"""
    client_id = request.GET.get('client')
    if request.method == 'POST':
        form = RevenusEntrepriseForm(request.POST)
        if form.is_valid():
            revenu = form.save()
            messages.success(request, 'Revenu d\'entreprise créé avec succès!')
            return redirect('client_detail', pk=revenu.client.pk)
    else:
        form = RevenusEntrepriseForm()
        if client_id:
            form.fields['client'].initial = client_id
    
    return render(request, 'core/revenus_entreprise_form.html', {
        'form': form,
        'title': 'Ajouter un revenu d\'entreprise'
    })

# Vues Autres Revenus
def autres_revenus_list(request):
    """Liste des autres revenus"""
    search = request.GET.get('search', '')
    revenus = AutresRevenus.objects.select_related('client').all()
    
    if search:
        revenus = revenus.filter(
            Q(client__nom__icontains=search) |
            Q(client__prenom__icontains=search) |
            Q(description__icontains=search)
        )
    
    return render(request, 'core/autres_revenus_list.html', {
        'revenus': revenus,
        'search': search
    })

def autres_revenus_create(request):
    """Création d'un autre revenu"""
    client_id = request.GET.get('client')
    if request.method == 'POST':
        form = AutresRevenusForm(request.POST)
        if form.is_valid():
            revenu = form.save()
            messages.success(request, 'Autre revenu créé avec succès!')
            return redirect('client_detail', pk=revenu.client.pk)
    else:
        form = AutresRevenusForm()
        if client_id:
            form.fields['client'].initial = client_id
    
    return render(request, 'core/autres_revenus_form.html', {
        'form': form,
        'title': 'Ajouter un autre revenu'
    })

# Vues Revenus RRQ
def revenus_rrq_list(request):
    """Liste des revenus RRQ"""
    search = request.GET.get('search', '')
    revenus = RevenusRRQ.objects.select_related('client').all()
    
    if search:
        revenus = revenus.filter(
            Q(client__nom__icontains=search) |
            Q(client__prenom__icontains=search)
        )
    
    return render(request, 'core/revenus_rrq_list.html', {
        'revenus': revenus,
        'search': search
    })

def revenus_rrq_create(request):
    """Création d'un revenu RRQ"""
    client_id = request.GET.get('client')
    if request.method == 'POST':
        form = RevenusRRQForm(request.POST)
        if form.is_valid():
            revenu = form.save()
            messages.success(request, 'Revenu RRQ créé avec succès!')
            return redirect('client_detail', pk=revenu.client.pk)
    else:
        form = RevenusRRQForm()
        if client_id:
            form.fields['client'].initial = client_id
    
    return render(request, 'core/revenus_rrq_form.html', {
        'form': form,
        'title': 'Ajouter un revenu RRQ'
    })

# Vues Revenus Dividendes
def revenus_dividendes_list(request):
    """Liste des revenus de dividendes"""
    search = request.GET.get('search', '')
    revenus = RevenusDividendes.objects.select_related('client', 'societe').all()
    
    if search:
        revenus = revenus.filter(
            Q(client__nom__icontains=search) |
            Q(client__prenom__icontains=search) |
            Q(societe__nom__icontains=search)
        )
    
    return render(request, 'core/revenus_dividendes_list.html', {
        'revenus': revenus,
        'search': search
    })

def revenus_dividendes_create(request):
    """Création d'un revenu de dividendes"""
    client_id = request.GET.get('client')
    if request.method == 'POST':
        form = RevenusDividendesForm(request.POST)
        if form.is_valid():
            revenu = form.save()
            messages.success(request, 'Revenu de dividendes créé avec succès!')
            return redirect('client_detail', pk=revenu.client.pk)
    else:
        form = RevenusDividendesForm()
        if client_id:
            form.fields['client'].initial = client_id
    
    return render(request, 'core/revenus_dividendes_form.html', {
        'form': form,
        'title': 'Ajouter un revenu de dividendes'
    })

# Vues Fond Pension CD
def fond_pension_cd_list(request):
    """Liste des fonds de pension CD"""
    search = request.GET.get('search', '')
    fonds = FondPensionCD.objects.select_related('client').all()
    
    if search:
        fonds = fonds.filter(
            Q(client__nom__icontains=search) |
            Q(client__prenom__icontains=search)
        )
    
    return render(request, 'core/fond_pension_cd_list.html', {
        'fonds': fonds,
        'search': search
    })

def fond_pension_cd_create(request):
    """Création d'un fond de pension CD"""
    client_id = request.GET.get('client')
    if request.method == 'POST':
        form = FondPensionCDForm(request.POST)
        if form.is_valid():
            fond = form.save()
            messages.success(request, 'Fond de pension CD créé avec succès!')
            return redirect('client_detail', pk=fond.client.pk)
    else:
        form = FondPensionCDForm()
        if client_id:
            form.fields['client'].initial = client_id
    
    return render(request, 'core/fond_pension_cd_form.html', {
        'form': form,
        'title': 'Ajouter un fond de pension CD'
    })

# Vues Fond Pension RRE
def fond_pension_rre_list(request):
    """Liste des fonds de pension RRE"""
    search = request.GET.get('search', '')
    fonds = FondPensionRRE.objects.select_related('participant', 'promoteur').all()
    
    if search:
        fonds = fonds.filter(
            Q(participant__nom__icontains=search) |
            Q(participant__prenom__icontains=search) |
            Q(promoteur__nom__icontains=search)
        )
    
    return render(request, 'core/fond_pension_rre_list.html', {
        'fonds': fonds,
        'search': search
    })

def fond_pension_rre_create(request):
    """Création d'un fond de pension RRE"""
    if request.method == 'POST':
        form = FondPensionRREForm(request.POST)
        if form.is_valid():
            fond = form.save()
            messages.success(request, 'Fond de pension RRE créé avec succès!')
            return redirect('fond_pension_rre_list')
    else:
        form = FondPensionRREForm()
    
    return render(request, 'core/fond_pension_rre_form.html', {
        'form': form,
        'title': 'Ajouter un fond de pension RRE'
    })

# Vues Projection RRE
def projection_rre_list(request):
    """Liste des projections RRE"""
    projections = ProjectionRRE.objects.select_related('fonds_pension_rre').all()
    
    return render(request, 'core/projection_rre_list.html', {
        'projections': projections
    })

def projection_rre_create(request):
    """Création d'une projection RRE"""
    if request.method == 'POST':
        form = ProjectionRREForm(request.POST)
        if form.is_valid():
            projection = form.save()
            messages.success(request, 'Projection RRE créée avec succès!')
            return redirect('projection_rre_list')
    else:
        form = ProjectionRREForm()
    
    return render(request, 'core/projection_rre_form.html', {
        'form': form,
        'title': 'Ajouter une projection RRE'
    })

# Vues Fond Pension PD
def fond_pension_pd_list(request):
    """Liste des fonds de pension PD"""
    search = request.GET.get('search', '')
    fonds = FondPensionPD.objects.select_related('client').all()
    
    if search:
        fonds = fonds.filter(
            Q(client__nom__icontains=search) |
            Q(client__prenom__icontains=search)
        )
    
    return render(request, 'core/fond_pension_pd_list.html', {
        'fonds': fonds,
        'search': search
    })

def fond_pension_pd_create(request):
    """Création d'un fond de pension PD"""
    client_id = request.GET.get('client')
    if request.method == 'POST':
        form = FondPensionPDForm(request.POST)
        if form.is_valid():
            fond = form.save()
            messages.success(request, 'Fond de pension PD créé avec succès!')
            return redirect('client_detail', pk=fond.client.pk)
    else:
        form = FondPensionPDForm()
        if client_id:
            form.fields['client'].initial = client_id
    
    return render(request, 'core/fond_pension_pd_form.html', {
        'form': form,
        'title': 'Ajouter un fond de pension PD'
    })

# Vues Cotisation Compte Personnel
def cotisation_compte_personnel_list(request):
    """Liste des cotisations de compte personnel"""
    cotisations = CotisationComptePersonnel.objects.select_related('actif').all()
    
    return render(request, 'core/cotisation_compte_personnel_list.html', {
        'cotisations': cotisations
    })

def cotisation_compte_personnel_create(request):
    """Création d'une cotisation de compte personnel"""
    if request.method == 'POST':
        form = CotisationComptePersonnelForm(request.POST)
        if form.is_valid():
            cotisation = form.save()
            messages.success(request, 'Cotisation de compte personnel créée avec succès!')
            return redirect('cotisation_compte_personnel_list')
    else:
        form = CotisationComptePersonnelForm()
    
    return render(request, 'core/cotisation_compte_personnel_form.html', {
        'form': form,
        'title': 'Ajouter une cotisation de compte personnel'
    })

# Vues Budget Permanent
def budget_permanent_list(request):
    """Liste des budgets permanents"""
    search = request.GET.get('search', '')
    budgets = BudgetPermanent.objects.select_related('client').all()
    
    if search:
        budgets = budgets.filter(
            Q(client__nom__icontains=search) |
            Q(client__prenom__icontains=search)
        )
    
    return render(request, 'core/budget_permanent_list.html', {
        'budgets': budgets,
        'search': search
    })

def budget_permanent_create(request):
    """Création d'un budget permanent"""
    client_id = request.GET.get('client')
    if request.method == 'POST':
        form = BudgetPermanentForm(request.POST)
        if form.is_valid():
            budget = form.save()
            messages.success(request, 'Budget permanent créé avec succès!')
            return redirect('client_detail', pk=budget.client.pk)
    else:
        form = BudgetPermanentForm()
        if client_id:
            form.fields['client'].initial = client_id
    
    return render(request, 'core/budget_permanent_form.html', {
        'form': form,
        'title': 'Ajouter un budget permanent'
    })

# Vues Budget Extraordinaire
def budget_extraordinaire_list(request):
    """Liste des budgets extraordinaires"""
    search = request.GET.get('search', '')
    budgets = BudgetExtraordinaire.objects.select_related('client').all()
    
    if search:
        budgets = budgets.filter(
            Q(client__nom__icontains=search) |
            Q(client__prenom__icontains=search)
        )
    
    return render(request, 'core/budget_extraordinaire_list.html', {
        'budgets': budgets,
        'search': search
    })

def budget_extraordinaire_create(request):
    """Création d'un budget extraordinaire"""
    client_id = request.GET.get('client')
    if request.method == 'POST':
        form = BudgetExtraordinaireForm(request.POST)
        if form.is_valid():
            budget = form.save()
            messages.success(request, 'Budget extraordinaire créé avec succès!')
            return redirect('client_detail', pk=budget.client.pk)
    else:
        form = BudgetExtraordinaireForm()
        if client_id:
            form.fields['client'].initial = client_id
    
    return render(request, 'core/budget_extraordinaire_form.html', {
        'form': form,
        'title': 'Ajouter un budget extraordinaire'
    })

# Vues Projection Assurance Vie
def projection_assurance_vie_list(request):
    """Liste des projections d'assurance vie"""
    projections = ProjectionAssuranceVie.objects.select_related('assurance_vie').all()
    
    return render(request, 'core/projection_assurance_vie_list.html', {
        'projections': projections
    })

def projection_assurance_vie_create(request):
    """Création d'une projection d'assurance vie"""
    if request.method == 'POST':
        form = ProjectionAssuranceVieForm(request.POST)
        if form.is_valid():
            projection = form.save()
            messages.success(request, 'Projection d\'assurance vie créée avec succès!')
            return redirect('projection_assurance_vie_list')
    else:
        form = ProjectionAssuranceVieForm()
    
    return render(request, 'core/projection_assurance_vie_form.html', {
        'form': form,
        'title': 'Ajouter une projection d\'assurance vie'
    })

# Vues Informations Fiscales Société
def informations_fiscales_societe_list(request):
    """Liste des informations fiscales des sociétés"""
    search = request.GET.get('search', '')
    infos = InformationsFiscalesSociete.objects.select_related('societe').all()
    
    if search:
        infos = infos.filter(Q(societe__nom__icontains=search))
    
    return render(request, 'core/informations_fiscales_societe_list.html', {
        'infos': infos,
        'search': search
    })

def informations_fiscales_societe_create(request):
    """Création d'informations fiscales de société"""
    societe_id = request.GET.get('societe')
    if request.method == 'POST':
        form = InformationsFiscalesSocieteForm(request.POST)
        if form.is_valid():
            info = form.save()
            messages.success(request, 'Informations fiscales de société créées avec succès!')
            return redirect('societe_detail', pk=info.societe.pk)
    else:
        form = InformationsFiscalesSocieteForm()
        if societe_id:
            form.fields['societe'].initial = societe_id
    
    return render(request, 'core/informations_fiscales_societe_form.html', {
        'form': form,
        'title': 'Ajouter des informations fiscales de société'
    })

# Vues Profil Investisseur
def profil_investisseur_list(request):
    """Liste des profils investisseur"""
    search = request.GET.get('search', '')
    profils = ProfilInvestisseur.objects.select_related('client').all()
    
    if search:
        profils = profils.filter(
            Q(client__nom__icontains=search) |
            Q(client__prenom__icontains=search)
        )
    
    return render(request, 'core/profil_investisseur_list.html', {
        'profils': profils,
        'search': search
    })

def profil_investisseur_create(request):
    """Création d'un profil investisseur"""
    client_id = request.GET.get('client')
    if request.method == 'POST':
        form = ProfilInvestisseurForm(request.POST)
        if form.is_valid():
            profil = form.save()
            messages.success(request, 'Profil investisseur créé avec succès!')
            return redirect('client_detail', pk=profil.client.pk)
    else:
        form = ProfilInvestisseurForm()
        if client_id:
            form.fields['client'].initial = client_id
    
    return render(request, 'core/profil_investisseur_form.html', {
        'form': form,
        'title': 'Ajouter un profil investisseur'
    })

# Vues Actif
def actif_list(request):
    """Liste des actifs"""
    search = request.GET.get('search', '')
    actifs = Actif.objects.select_related('client', 'societe').all()
    
    if search:
        actifs = actifs.filter(
            Q(client__nom__icontains=search) |
            Q(client__prenom__icontains=search) |
            Q(descriptif__icontains=search)
        )
    
    return render(request, 'core/actif_list.html', {
        'actifs': actifs,
        'search': search
    })

def actif_create(request):
    """Création d'un actif"""
    client_id = request.GET.get('client')
    if request.method == 'POST':
        form = ActifForm(request.POST)
        if form.is_valid():
            actif = form.save()
            messages.success(request, 'Actif créé avec succès!')
            return redirect('client_detail', pk=actif.client.pk)
    else:
        form = ActifForm()
        if client_id:
            form.fields['client'].initial = client_id
    
    return render(request, 'core/actif_form.html', {
        'form': form,
        'title': 'Ajouter un actif'
    })

# Vues Flux Monétaire
def flux_monetaire_list(request):
    """Liste des flux monétaires"""
    search = request.GET.get('search', '')
    flux = FluxMonetaire.objects.select_related('societe').all()
    
    if search:
        flux = flux.filter(Q(societe__nom__icontains=search))
    
    return render(request, 'core/flux_monetaire_list.html', {
        'flux': flux,
        'search': search
    })

def flux_monetaire_create(request):
    """Création d'un flux monétaire"""
    societe_id = request.GET.get('societe')
    if request.method == 'POST':
        form = FluxMonetaireForm(request.POST)
        if form.is_valid():
            flux = form.save()
            messages.success(request, 'Flux monétaire créé avec succès!')
            return redirect('societe_detail', pk=flux.societe.pk)
    else:
        form = FluxMonetaireForm()
        if societe_id:
            form.fields['societe'].initial = societe_id
    
    return render(request, 'core/flux_monetaire_form.html', {
        'form': form,
        'title': 'Ajouter un flux monétaire'
    })

# Informations Fiscales Client
def informations_fiscales_client_list(request):
    """Liste des informations fiscales client"""
    query = request.GET.get('q', '')
    informations = InformationsFiscalesClient.objects.select_related('client').all()
    
    if query:
        informations = informations.filter(
            Q(client__nom__icontains=query) | Q(client__prenom__icontains=query)
        )
    
    return render(request, 'core/informations_fiscales_client_list.html', {
        'informations': informations,
        'query': query
    })


def informations_fiscales_client_create(request):
    """Création d'informations fiscales client"""
    client_id = request.GET.get('client')
    if request.method == 'POST':
        form = InformationsFiscalesClientForm(request.POST)
        if form.is_valid():
            info = form.save()
            messages.success(request, 'Informations fiscales créées avec succès!')
            return redirect('client_detail', pk=info.client.pk)
    else:
        form = InformationsFiscalesClientForm()
        if client_id:
            form.fields['client'].initial = client_id
    
    return render(request, 'core/informations_fiscales_client_form.html', {
        'form': form,
        'title': 'Ajouter informations fiscales client'
    })
