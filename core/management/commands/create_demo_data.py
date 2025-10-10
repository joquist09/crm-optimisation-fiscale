from django.core.management.base import BaseCommand
from datetime import date, datetime
from core.models import Conseiller, Client, Societe, Enfant, RevenusEmploi, ActifPlacements

class Command(BaseCommand):
    help = 'Créer des données de démonstration pour le CRM'

    def handle(self, *args, **options):
        # Créer des conseillers
        conseiller1, created = Conseiller.objects.get_or_create(
            courriel='marie.tremblay@exemple.com',
            defaults={
                'nom': 'Tremblay',
                'prenom': 'Marie',
                'telephone': '514-555-0101',
                'langue': 'fr'
            }
        )
        
        conseiller2, created = Conseiller.objects.get_or_create(
            courriel='jean.dupont@exemple.com',
            defaults={
                'nom': 'Dupont',
                'prenom': 'Jean',
                'telephone': '450-555-0202',
                'langue': 'fr'
            }
        )

        # Créer des clients
        client1, created = Client.objects.get_or_create(
            courriel='pierre.martin@exemple.com',
            defaults={
                'conseiller': conseiller1,
                'prenom': 'Pierre',
                'nom': 'Martin',
                'province': 'QC',
                'etat_civil': 'marié',
                'sexe': 'H',
                'telephone': '514-555-1001',
                'langue': 'fr',
                'date_naissance': date(1980, 5, 15),
                'fumeur': False
            }
        )

        client2, created = Client.objects.get_or_create(
            courriel='sophie.bernard@exemple.com',
            defaults={
                'conseiller': conseiller1,
                'prenom': 'Sophie',
                'nom': 'Bernard',
                'province': 'QC',
                'etat_civil': 'célibataire',
                'sexe': 'F',
                'telephone': '438-555-1002',
                'langue': 'fr',
                'date_naissance': date(1985, 9, 22),
                'fumeur': False
            }
        )

        client3, created = Client.objects.get_or_create(
            courriel='robert.lavoie@exemple.com',
            defaults={
                'conseiller': conseiller2,
                'prenom': 'Robert',
                'nom': 'Lavoie',
                'province': 'QC',
                'etat_civil': 'divorcé',
                'sexe': 'H',
                'telephone': '450-555-1003',
                'langue': 'fr',
                'date_naissance': date(1975, 12, 8),
                'fumeur': True
            }
        )

        # Créer des sociétés
        societe1, created = Societe.objects.get_or_create(
            nom='Consultants Martin Inc.',
            client=client1,
            defaults={
                'type_societe': 'operante',
                'revenus': 250000.00,
                'depenses_deductibles': 75000.00,
                'depenses_non_deductibles': 15000.00,
                'salaire_client': 80000.00,
                'salaire_conjoint': 0.00,
                'salaire_employe': 45000.00,
                'dpa_federale': 12000.00,
                'dpa_provinciale': 8000.00,
                'pourcentage_benefices_investis': 60.00
            }
        )

        societe2, created = Societe.objects.get_or_create(
            nom='Gestion Bernard',
            client=client2,
            defaults={
                'type_societe': 'gestion',
                'revenus': 150000.00,
                'depenses_deductibles': 25000.00,
                'depenses_non_deductibles': 5000.00,
                'salaire_client': 60000.00,
                'solde_imrtd_non_determines': 45000.00,
                'solde_imrtd_determines': 30000.00,
                'solde_cdc': 75000.00,
                'capital_verse': 100000.00
            }
        )

        # Créer des enfants
        enfant1, created = Enfant.objects.get_or_create(
            nom='Lucas Martin',
            client=client1,
            defaults={
                'date_naissance': date(2015, 3, 10),
                'garde_partagee': False,
                'garderie_subventionnee': True,
                'garderie_non_subventionnee': False,
                'date_debut': date(2020, 9, 1),
                'date_fin': date(2025, 6, 30),
                'cout_par_jour': 35.00
            }
        )

        enfant2, created = Enfant.objects.get_or_create(
            nom='Emma Martin',
            client=client1,
            defaults={
                'date_naissance': date(2018, 7, 20),
                'garde_partagee': False,
                'garderie_subventionnee': True,
                'garderie_non_subventionnee': False,
                'date_debut': date(2023, 9, 1),
                'date_fin': date(2028, 6, 30),
                'cout_par_jour': 35.00
            }
        )

        # Créer des revenus d'emploi
        revenu1, created = RevenusEmploi.objects.get_or_create(
            client=client2,
            societe=None,
            defaults={
                'date_debut': date(2024, 1, 1),
                'date_fin': date(2024, 12, 31),
                'revenus_emploi': 85000.00
            }
        )

        # Créer des actifs placements
        actif1, created = ActifPlacements.objects.get_or_create(
            client=client1,
            type='reer',
            defaults={
                'montant': 125000.00,
                'description': 'REER diversifié avec fonds communs'
            }
        )

        actif2, created = ActifPlacements.objects.get_or_create(
            client=client1,
            type='celi',
            defaults={
                'montant': 75000.00,
                'description': 'CELI avec FNB et actions'
            }
        )

        actif3, created = ActifPlacements.objects.get_or_create(
            client=client2,
            type='celi',
            defaults={
                'montant': 55000.00,
                'description': 'CELI conservateur avec obligations'
            }
        )

        self.stdout.write(
            self.style.SUCCESS(
                'Données de démonstration créées avec succès!\n'
                f'- {Conseiller.objects.count()} conseillers\n'
                f'- {Client.objects.count()} clients\n'
                f'- {Societe.objects.count()} sociétés\n'
                f'- {Enfant.objects.count()} enfants\n'
                f'- {RevenusEmploi.objects.count()} revenus d\'emploi\n'
                f'- {ActifPlacements.objects.count()} actifs placements'
            )
        )