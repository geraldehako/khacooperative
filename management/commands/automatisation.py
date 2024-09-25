import os
import sys
from datetime import date, datetime, timedelta
from decimal import Decimal
import django
from django.utils import timezone
from django.db.models import Sum
from django.shortcuts import get_object_or_404


# Configure the Django environment
sys.path.append('/home/geraldehako/Khacoop')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Prologicielsucces.settings')
django.setup()

from Gestions.models import (Echeancier, Echeancieract, TransactionPenalite, 
                             TransactionPenaliteact, Actionnaire, Depense, 
                             TransactionRistourne, Confconstantes, 
                             CompteFondateur, Statuts,Tontines,CompteInterets,TransactionInteret)


# Fonction pour calculer les pénalités
def calcul_penalites():
    echeances_non_payees = Echeancier.objects.filter(date_echeance__lt=date.today(), est_paye=False)
    echeances_non_payeesact = Echeancieract.objects.filter(date_echeance__lt=date.today(), est_paye=False)

    statut_actif = get_object_or_404(Statuts, statut='Actif')
    Conf = Confconstantes.objects.filter(statut=statut_actif).first()
    taux_penalite = Conf.partpenalite

    for echeance in echeances_non_payees:
        penalite = echeance.montant_echeance * taux_penalite
        echeance.montant_echeance += penalite
        echeance.save()

        TransactionPenalite.objects.create(
            compte_pret=echeance.compte_pret.id,
            echeance=echeance.id,
            montant=penalite,
            date_transaction=timezone.now(),
            type_transaction='Virement',
        )

    for echeanceact in echeances_non_payeesact:
        penalite = echeanceact.montant_echeance * taux_penalite
        echeanceact.montant_echeance += penalite
        echeanceact.save()

        TransactionPenaliteact.objects.create(
            compte_pretact=echeanceact.compte_pretact.id,
            echeance=echeanceact.id,
            montant=penalite,
            date_transaction=timezone.now(),
            type_transaction='Virement',
        )

    print("Penalties calculated and updated successfully.")


# Fonction pour calculer les dividendes
def calcul_dividendes():

     # Récupérer
    statut_actif = get_object_or_404(Statuts, statut='Actif')
    Conf = Confconstantes.objects.filter(statut=statut_actif).first()
    dureecoopa = Conf.dureecoopa
    dureecoopn = Conf.dureecoopn
    date_today = datetime.now().date()
    date_un_mois_actif = date_today - timedelta(days=dureecoopa)
    date_un_mois_passif = date_today - timedelta(days=dureecoopn)  
    actionnaires_type_1 = Actionnaire.objects.filter(type_act_id=1, date_adhesion__gte=date_un_mois_actif)
    #actionnaires_type_2 = Actionnaire.objects.filter(type_act_id=2)
    statut_actif = Statuts.objects.get(statut='Actif')
    actionnaires_type_2 = Actionnaire.objects.filter(
    type_act_id=2, date_adhesion__gte=date_un_mois_passif, 
    comptepretsact__isnull=True, 
    # comptepretsact__statut__statut=statut_actif
    )

    echeances_payees_mois = Echeancier.objects.filter(date_echeance__month=date.today().month, est_paye=True)
    echeances_payees_moisact = Echeancieract.objects.filter(date_echeance__month=date.today().month, est_paye=True)

    benefice_mois = sum(echeance.montant_interet for echeance in echeances_payees_mois) + \
                    sum(echeance.montant_interet for echeance in echeances_payees_moisact)

    today = timezone.localtime(timezone.now()).date()
    depenses_mois = Depense.objects.filter(date__month=today.month, date__year=today.year).aggregate(Sum('montant'))['montant__sum'] or 0
    montant_a_repartir = benefice_mois - depenses_mois

    statut_actif = get_object_or_404(Statuts, statut='Actif')
    Conf = Confconstantes.objects.filter(statut=statut_actif).first()

    montant_a_repartir_type_1 = montant_a_repartir * Decimal(Conf.partactif)
    montant_a_repartir_type_chef = montant_a_repartir * Decimal(Conf.partnonactif) * Decimal(Conf.partrespo)
    montant_a_repartir_type_2 = (montant_a_repartir * Decimal(Conf.partnonactif)) - montant_a_repartir_type_chef

    # Mise à jour des informations pour le chef de projet
    chef = get_object_or_404(CompteFondateur, statut=statut_actif)
    chef.dateprecedent = chef.datesolde
    chef.soldeprecedent = chef.solde
    chef.datesolde = timezone.now()
    chef.solde += montant_a_repartir_type_chef
    chef.save()

    # Calcul des parts pour les actionnaires de type 1
    total_apport_type_1 = sum(actionnaire.apport for actionnaire in actionnaires_type_1)
    for actionnaire in actionnaires_type_1:
        actionnaire.part = round((actionnaire.apport / total_apport_type_1) * 100, 2)
        actionnaire.montant_a_payer = round((actionnaire.part / 100) * montant_a_repartir_type_1, 2)
        actionnaire.dividende += actionnaire.montant_a_payer
        actionnaire.save()

        TransactionRistourne.objects.create(
            actionnaire=actionnaire,
            montant=actionnaire.montant_a_payer,
            date_transaction=timezone.now(),
            type_transaction='Virement',
        )
        # Mise à jour du solde du compte interet associé à l'actionnaire
        statut_actif = get_object_or_404(Statuts, statut='Actif')
        inter = get_object_or_404(CompteInterets, statut=statut_actif)
        inter.soldeprecedent = inter.solde
        inter.dateprecedent = inter.datesolde
        inter.datesolde = timezone.now()  # Conserve la date avec fuseau horaire
        inter.solde -= actionnaire.montant_a_payer,
        inter.save()

        transactionint = TransactionInteret.objects.create(
            compteinteret=inter,
            montant=actionnaire.montant_a_payer,
            type_transaction='Retrait',  # À adapter en fonction de votre logique
        )


    # Calcul des parts pour les actionnaires de type 2
    total_apport_type_2 = sum(actionnaire.apport for actionnaire in actionnaires_type_2)
    for actionnaire in actionnaires_type_2:
        actionnaire.part = round((actionnaire.apport / total_apport_type_2) * 100, 2)
        actionnaire.montant_a_payer = round((actionnaire.part / 100) * montant_a_repartir_type_2, 2)
        actionnaire.dividende += actionnaire.montant_a_payer
        actionnaire.save()

        TransactionRistourne.objects.create(
            actionnaire=actionnaire,
            montant=actionnaire.montant_a_payer,
            date_transaction=timezone.now(),
            type_transaction='Virement',
        )

        # Mise à jour du solde du compte interet associé à l'actionnaire
        statut_actif = get_object_or_404(Statuts, statut='Actif')
        inter = get_object_or_404(CompteInterets, statut=statut_actif)
        inter.soldeprecedent = inter.solde
        inter.dateprecedent = inter.datesolde
        inter.datesolde = timezone.now()  # Conserve la date avec fuseau horaire
        inter.solde -= actionnaire.montant_a_payer,
        inter.save()

        transactionint = TransactionInteret.objects.create(
            compteinteret=inter,
            montant=actionnaire.montant_a_payer,
            type_transaction='Retrait',  # À adapter en fonction de votre logique
        )

    print("Dividends calculated and updated successfully.")

def penalite_tontines(request):
    # Récupérer toutes les tontines
    tontines = Tontines.objects.all()

    for tontine in tontines:
        # Calculer la durée écoulée depuis la date de création de la tontine
        duree = (date.today() - tontine.date_tontine).days
        tontine.duree = duree

        # Vérifier si la date de cotisation future est dépassée
        if tontine.date_futurcotisation and tontine.date_futurcotisation < date.today():
            # Calculer le nombre de jours de retard
            penaliteton = (date.today() - tontine.date_futurcotisation).days
            if penaliteton > 0:
                # Ajouter les jours de pénalité au champ 'penaliteton'
                tontine.penaliteton += penaliteton

                # Mettre à jour la date du palier en ajoutant les jours de pénalité
                if tontine.date_palier:
                    tontine.date_palier += timedelta(days=penaliteton)
                else:
                    tontine.date_palier = date.today() + timedelta(days=penaliteton)

        # Sauvegarder les modifications dans la base de données
        tontine.save()


# Exécution des fonctions
if __name__ == "__main__":
    calcul_penalites()
    calcul_dividendes()
    penalite_tontines()
