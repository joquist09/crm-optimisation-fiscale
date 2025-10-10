from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponse
import csv
from datetime import datetime
from .models import (
    Conseiller, Client, Societe, Enfant, RevenusEmploi, RevenusEntreprise,
    AutresRevenus, ActifPlacements, AssuranceVie, InformationsFiscalesClient,
    RevenusRRQ, RevenusDividendes, FondPensionCD, FondPensionRRE, FondPensionPD,
    BudgetPermanent, BudgetExtraordinaire, InformationsFiscalesSociete,
    ProfilInvestisseur, Actif, FluxMonetaire
)
from .forms import (
    ConseillerForm, ClientForm, SocieteForm, EnfantForm,
    RevenusEmploiForm, ActifPlacementsForm, AssuranceVieForm,
    InformationsFiscalesClientForm, BudgetPermanentForm
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
    societes = client.societe_set.all()
    enfants = client.enfants.all()
    revenus_emploi = client.revenus_emploi.all()
    actifs = client.actifs_placements.all()
    
    return render(request, 'core/client_detail.html', {
        'client': client,
        'societes': societes,
        'enfants': enfants,
        'revenus_emploi': revenus_emploi,
        'actifs': actifs
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