from django.db import models

class Conseiller(models.Model):
    nom = models.CharField(max_length=255)
    prenom = models.CharField(max_length=255)
    courriel = models.EmailField()
    telephone = models.CharField(max_length=20)
    langue = models.CharField(max_length=2, choices=[("fr", "Français"), ("en", "Anglais")])
    date_creation = models.DateTimeField(auto_now_add=True)


class Client(models.Model):
    PROVINCES = [("QC", "Québec"), ("ON", "Ontario"), ("BC", "Colombie-Britannique"), ("AB", "Alberta")]
    STATUTS = [("célibataire", "Célibataire"), ("marié", "Marié"), ("divorcé", "Divorcé"), ("veuf", "Veuf")]
    SEXES = [("H", "Homme"), ("F", "Femme"), ("A", "Autre")]
    LANGUES = [("fr", "Français"), ("en", "Anglais"), ("es", "Espagnol")]

    conseiller = models.ForeignKey(Conseiller, on_delete=models.CASCADE, related_name="clients", null=True, blank=True)
    prenom = models.CharField(max_length=255)
    nom = models.CharField(max_length=255)
    province = models.CharField(max_length=2, choices=PROVINCES)
    etat_civil = models.CharField(max_length=20, choices=STATUTS)
    sexe = models.CharField(max_length=1, choices=SEXES)
    courriel = models.EmailField()
    telephone = models.CharField(max_length=20)
    langue = models.CharField(max_length=2, choices=LANGUES)
    date_naissance = models.DateField()
    fumeur = models.BooleanField()
    conjoint = models.ForeignKey('self', on_delete=models.CASCADE, related_name="conjoints", null=True, blank=True)

class Societe(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    nom = models.CharField(max_length=255)
    type_societe = models.CharField(max_length=100, choices=[("gestion", "Gestion"), ("operante", "Opérante")])

    ## Champs de societe operante
    solde_crtg_operante = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    revenus = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    date_debut_revenus = models.DateField(null=True, blank=True)
    date_fin_revenus = models.DateField(null=True, blank=True)
    depenses_deductibles = models.DecimalField(max_digits=12, decimal_places=2, default=0) # Excluant salaire
    date_debut_depenses_ded = models.DateField(null=True, blank=True)
    date_fin_depenses_ded = models.DateField(null=True, blank=True)
    depenses_non_deductibles = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    date_debut_depenses_non_ded = models.DateField(null=True, blank=True)
    date_fin_depenses_non_ded = models.DateField(null=True, blank=True)
    salaire_client = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    date_debut_salaire_client = models.DateField(null=True, blank=True)
    date_fin_salaire_client = models.DateField(null=True, blank=True)
    salaire_conjoint = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    date_debut_salaire_conjoint = models.DateField(null=True, blank=True)
    date_fin_salaire_conjoint = models.DateField(null=True, blank=True)
    salaire_employe = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    date_debut_salaire_employe = models.DateField(null=True, blank=True)
    date_fin_salaire_employe = models.DateField(null=True, blank=True)
    dpa_federale = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    dpa_provinciale = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    pourcentage_benefices_investis = models.DecimalField(max_digits=5, decimal_places=2, default=0)

    ## Champs de societe gestion
    solde_imrtd_non_determines = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    solde_imrtd_determines = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    solde_cdc = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    solde_crtg_gestion = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    paqc_reportee = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    annee_maximale_paqc = models.PositiveIntegerField(default=0)
    perte_capitale = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    pbr_actions_ordinaires = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    capital_verse = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    actions_dividendes_discretionnaires = models.DecimalField(max_digits=12, decimal_places=2, default=0)

class Enfant(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="enfants")
    nom = models.CharField(max_length=255)
    date_naissance = models.DateField()
    garde_partagee = models.BooleanField()
    garderie_subventionnee = models.BooleanField()
    garderie_non_subventionnee = models.BooleanField()
    date_debut = models.DateField()
    date_fin = models.DateField()
    cout_par_jour = models.DecimalField(max_digits=8, decimal_places=2)

class RevenusEmploi(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="revenus_emploi")
    societe = models.ForeignKey(Societe, on_delete=models.CASCADE, related_name="revenus_societe_emploi", null=True, blank=True)
    date_debut = models.DateField()
    date_fin = models.DateField()
    revenus_emploi = models.DecimalField(max_digits=12, decimal_places=2)

class RevenusEntreprise(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="revenus_entreprise")
    revenus_entreprise = models.DecimalField(max_digits=12, decimal_places=2)
    date_debut = models.DateField()
    date_fin = models.DateField()
    depenses_deductibles = models.DecimalField(max_digits=12, decimal_places=2)


class AutresRevenus(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="revenus_personnels")
    type = models.CharField(max_length=100, choices=[("heritage", "Héritage"),
                                                    ("autres", "Autres")])
    date_debut = models.DateField()
    date_fin = models.DateField()
    montant = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    description = models.CharField(max_length=255, null=True, blank=True)
    pourcentage_imposable = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)


class RevenusRRQ(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="revenus_rrq")
    type = models.CharField(max_length=100, choices=[("relevé", "Relevé"), ("rente", "Rente")])
    rentes_revenus_rrq_rpc = models.DecimalField(max_digits=12, decimal_places=2)
    date_debut_rrq_rpc = models.DateField()
    # Champs de 18 ans du client jusqu'à année
    revenu_admissible = models.DecimalField(max_digits=12, decimal_places=2)
    annee = models.PositiveIntegerField(null=True, blank=True)

class RevenusDividendes(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="revenus_dividendes")
    societe = models.ForeignKey(Societe, on_delete=models.CASCADE, related_name="revenus_societe_dividendes", null=True, blank=True)
    date_debut = models.DateField()
    date_fin = models.DateField()

    revenus_dividendes = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    dividende_ordinaire = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    dividende_determine = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    dividende_capital = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)

class FondPensionCD(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    cotisation_totale = models.DecimalField(max_digits=12, decimal_places=2)
    date_debut_cotisation_totale = models.DateField()
    date_fin_cotisation_totale = models.DateField()
    cotisation_employeur = models.DecimalField(max_digits=12, decimal_places=2)
    date_debut_cotisation_employeur = models.DateField()
    date_fin_cotisation_employeur = models.DateField()

class FondPensionRRE(models.Model):
    participant = models.ForeignKey(Client, on_delete=models.CASCADE)
    promoteur = models.ForeignKey(Societe, on_delete=models.CASCADE, related_name="promoteur")
    transfert_initial_pd = models.DecimalField(max_digits=12, decimal_places=2)
    transfert_initial_cva = models.DecimalField(max_digits=12, decimal_places=2)
    transfert_initial_cd = models.DecimalField(max_digits=12, decimal_places=2)
    solde_immobilise = models.DecimalField(max_digits=12, decimal_places=2) # Si RRE existant
    solde_cva = models.DecimalField(max_digits=12, decimal_places=2) # Si RRE existant
    transfert_intergenerationnel = models.BooleanField()

class ProjectionRRE(models.Model):
    fonds_pension_rre = models.ForeignKey(FondPensionRRE, on_delete=models.CASCADE)
    annee = models.DecimalField(max_digits=4, decimal_places=0)
    cotisation_regulieres = models.DecimalField(max_digits=12, decimal_places=2)
    cotisation_service_passe = models.DecimalField(max_digits=12, decimal_places=2)
    cotisation_volontaire_additionnelles = models.DecimalField(max_digits=12, decimal_places=2)
    rente = models.DecimalField(max_digits=12, decimal_places=2)
    ajustements_frais_annuels = models.DecimalField(max_digits=12, decimal_places=2)

class FondPensionPD(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    revenu_pension_1 = models.DecimalField(max_digits=12, decimal_places=2)
    date_debut_revenu_pension_1 = models.DateField()
    date_fin_revenu_pension_1 = models.DateField()
    revenu_pension_2 = models.DecimalField(max_digits=12, decimal_places=2)
    date_debut_revenu_pension_2 = models.DateField()
    date_fin_revenu_pension_2 = models.DateField()
    cotisation_employe = models.DecimalField(max_digits=12, decimal_places=2)
    date_debut_cotisation_employe = models.DateField()
    date_fin_cotisation_employe = models.DateField()
    facteur_equivalence = models.DecimalField(max_digits=12, decimal_places=2)

class ActifPlacements(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="actifs_placements")
    type = models.CharField(max_length=100, choices=[("reer", "REER"), ("celi", "CELI"), ("non enregistré","Non enregistré")])
    montant = models.DecimalField(max_digits=12, decimal_places=2)
    description = models.CharField(max_length=100)

class CotisationComptePersonnel(models.Model):
    actif = models.ForeignKey(ActifPlacements, on_delete=models.CASCADE, related_name="cotisations_compte_personnel")
    cotisation_annuelle = models.DecimalField(max_digits=12, decimal_places=2)
    date_debut = models.DateField(null=True, blank=True)
    date_fin = models.DateField(null=True, blank=True)
    indexation = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

class BudgetPermanent(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="budget_permanent")
    date_debut_budget_annuel_permanent = models.DateField()
    budget_annuel_permanent = models.DecimalField(max_digits=12, decimal_places=2)

class BudgetExtraordinaire(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="budget_extraordinaire")
    date_debut = models.DateField(null=True, blank=True)
    date_fin = models.DateField(null=True, blank=True)
    budget_extraordinaire = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    indexation = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

class AssuranceVie(models.Model):
    categorie = models.CharField(max_length=100, choices=[("personnelle", "Personnelle"), ("societe", "Société")])
    preneur_client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="assurances_preneur", null=True, blank=True)
    preneur_societe = models.ForeignKey(Societe, on_delete=models.CASCADE, related_name="assurances_preneur", null=True, blank=True)
    preneur_externe = models.CharField(max_length=100, null=True, blank=True)
    personne_assuree = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="assurances_assuree", null=True, blank=True)
    personne_assuree_externe = models.CharField(max_length=100, null=True, blank=True)
    type = models.CharField(max_length=100,choices=[("permanente", "Permanante"),
                                                    ("temporaire", "Temporaire"),
                                                    ("vie universelle","Vie universelle")])
    police_existante = models.BooleanField()

class ProjectionAssuranceVie(models.Model):
    assurance_vie = models.ForeignKey(AssuranceVie, on_delete=models.CASCADE)
    annee = models.PositiveIntegerField(null=True, blank=True)
    capital_deces = models.DecimalField(max_digits=12, decimal_places=2)
    cout_base_rajuste = models.DecimalField(max_digits=12, decimal_places=2) # CBR
    valeur_rachat = models.DecimalField(max_digits=12, decimal_places=2)
    prime_annuelle = models.DecimalField(max_digits=12, decimal_places=2)

class InformationsFiscalesClient(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    droits_reer_inutilises = models.DecimalField(max_digits=12, decimal_places=2)
    cotisations_reer_non_deduites = models.DecimalField(max_digits=12, decimal_places=2)
    droits_celi_inutilises = models.DecimalField(max_digits=12, decimal_places=2)
    droits_celiapp = models.DecimalField(max_digits=12, decimal_places=2)
    fe_pd_annee_precedente = models.DecimalField(max_digits=12, decimal_places=2)
    assurance_medicament_privee = models.BooleanField()
    srg_allocation = models.BooleanField()
    report_psv = models.PositiveIntegerField()
    ecgc_passe = models.DecimalField(max_digits=12, decimal_places=2)
    impot_minimum_remplacement_federal = models.DecimalField(max_digits=12, decimal_places=2)
    annee_maximale_recuperation_federale = models.PositiveIntegerField()
    impot_minimum_remplacement_provincial = models.DecimalField(max_digits=12, decimal_places=2)
    annee_maximale_recuperation_provinciale = models.PositiveIntegerField()
    revenus_nets_federaux_passe = models.DecimalField(max_digits=12, decimal_places=2)
    paqc_reportee = models.DecimalField(max_digits=12, decimal_places=2)
    annee_maximale_paqc = models.PositiveIntegerField()
    perte_capitale = models.DecimalField(max_digits=12, decimal_places=2)

class InformationsFiscalesSociete(models.Model):
    societe = models.ForeignKey(Societe, on_delete=models.CASCADE)
    solde_imrtd_non_determines = models.DecimalField(max_digits=12, decimal_places=2)
    solde_imrtd_determines = models.DecimalField(max_digits=12, decimal_places=2)
    solde_crtg = models.DecimalField(max_digits=12, decimal_places=2)
    solde_cdc = models.DecimalField(max_digits=12, decimal_places=2)
    seuil_cdc = models.DecimalField(max_digits=12, decimal_places=2) # Par défaut: 50 000 $
    frais_cdc = models.DecimalField(max_digits=12, decimal_places=2) # Par défaut: 1 000 $
    paqc_reportee = models.DecimalField(max_digits=12, decimal_places=2)
    annee_maximale_paqc = models.PositiveIntegerField()
    perte_capitale = models.DecimalField(max_digits=12, decimal_places=2)
    pbr_actions_ordinaires = models.DecimalField(max_digits=12, decimal_places=2)
    capital_verse = models.DecimalField(max_digits=12, decimal_places=12)
    actions_dividendes_discretionnaires = models.DecimalField(max_digits=12, decimal_places=2)

    # ACTIONS DIVIDENDES DISCRETIONNAIRES + PREVOIR DETENTION %

class ProfilInvestisseur(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    profil = models.CharField(max_length=100, choices=[("depots garantis", "Dépôts garantis"), ("conservateur", "Conservateur"), ("modére", "Modéré"), ("audacieux", "Audacieux")])
    profil_fixe = models.BooleanField()
    ## QUELQUE CHOSE À AJOUTER!
    ajustement_revenus_fixe = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    ajustement_frais_action = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    ajustement_honoraires = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    honoraires = models.CharField(max_length=100, choices=[("grille", "Grille"), ("fixe", "Fixe")])
    taux_roulement_portefeuille = models.DecimalField(max_digits=5, decimal_places=2)

class Actif(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    societe = models.ForeignKey(Societe, on_delete=models.CASCADE)
    type = models.CharField(max_length=100, choices=[("residence principale", "Résidence principale"), ("immeuble à revenu", "Immeuble à Revenu"), ("autre immeuble","Autre Immeuble"), ("aape/agricole", "AAPE/Agricole"), ("action accréditive", "Action Accréditive"), ("titres cotés en bourse", "Titres cotés en bourse"),("autre", "Autre"),("biens écosensibles", "Biens écosensibles")])
    descriptif = models.CharField(max_length=100)
    proprietaire = models.CharField(max_length=100, null=True, blank=True) # Client name, Spouse name, Client and Spouse, Societies linked as choices
    pourcentage_detenu = models.DecimalField(max_digits=5, decimal_places=2)
    juste_valeur_marchande = models.DecimalField(max_digits=12, decimal_places=2)
    indexation_jvm = models.DecimalField(max_digits=5, decimal_places=2)
    pbr_total = models.DecimalField(max_digits=12, decimal_places=2)
    pbr_terrain = models.DecimalField(max_digits=12, decimal_places=2)
    fnacc = models.DecimalField(max_digits=12, decimal_places=2)
    taux_dpa = models.DecimalField(max_digits=5, decimal_places=2)
    annee_acquisition_futur = models.PositiveIntegerField()
    date_disposition = models.DateField()

    emprunts = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Emprunts")
    revenus = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Revenus")
    dons = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Dons")
    au_deces = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Au décès")

    solde_pret = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Solde prêt")
    date_solde = models.DateField(verbose_name="Date solde")
    versement_mensuel = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Versement mensuel")
    date_dernier_versement = models.DateField(verbose_name="Date dernier versement")
    taux_estime = models.FloatField(verbose_name="Taux estimé")

    debut_mois = models.PositiveSmallIntegerField(
        verbose_name="Mois de début",
        choices=[(i, i) for i in range(1, 13)],
        null=True,
        blank=True
    )
    interet_seulement = models.BooleanField(verbose_name="Intérêt seulement")
    interets_deductibles = models.BooleanField(verbose_name="Intérêts déductibles")
    net_avant_interet = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Net avant intérêt")
    indexation = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Indexation")

    entreprise =  models.BooleanField(verbose_name="Entreprise")
    du_vivant = models.BooleanField(verbose_name="Du vivant")

    contrepartie = models.DecimalField(max_digits=5, decimal_places=2)


class FluxMonetaire(models.Model):
    societe = models.ForeignKey(Societe, on_delete=models.CASCADE)
    annee = models.PositiveIntegerField()
    entree_fonds_imposable = models.DecimalField(max_digits=12, decimal_places=2)
    entree_fonds_non_imposable = models.DecimalField(max_digits=12, decimal_places=2)
    sortie_fonds_deductible = models.DecimalField(max_digits=12, decimal_places=2)
    sortie_fonds_non_deductible = models.DecimalField(max_digits=12, decimal_places=2)