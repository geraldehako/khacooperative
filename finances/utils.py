from datetime import date, timedelta, datetime

def definir_date_fin_pret(compte_pret):
    if compte_pret.date_debut_pret is None or compte_pret.duree_en_mois is None:
        raise ValueError("Les informations du compte de prêt sont incomplètes.")

    # Calculez la date de fin en ajoutant la durée en mois à la date de début
    date_debut = compte_pret.date_debut_pret
    duree_en_mois = compte_pret.duree_en_mois
    date_fin = date_debut + timedelta(days=duree_en_mois * 30)  # Supposant 30 jours par mois

    # Assurez-vous que le champ date_fin_pret du modèle est mis à jour avec la date calculée
    compte_pret.date_fin_pret = date_fin
    compte_pret.save()