from datetime import timedelta, timezone
from django.db import models
from django.db.models import Count, Q,Sum,F
from django.db.models import F 
from accounts.models import Utilisateurs
from dateutil.relativedelta import relativedelta

# GENRES ___________________________________________________________________________________________________________________________________________________________________________
class Genres(models.Model):
    sexe = models.CharField(max_length=10)
    def __str__(self):
        return f'{self.sexe}'
# __________________________________________________________________________________________________________________________________________________________________________________

# MATRIMONIALE _____________________________________________________________________________________________________________________________________________________________________
class Matrimoniales(models.Model):
    matrimoniale = models.CharField(max_length=50)
    def __str__(self):
        return f'{self.matrimoniale}'
# __________________________________________________________________________________________________________________________________________________________________________________

# TYPE DE PRETS _____________________________________________________________________________________________________________________________________________________________________    
class Typeprets(models.Model):
    type_pret = models.CharField(max_length=50,null=False)
    def __str__(self):
        return f'{self.type_pret}'
# __________________________________________________________________________________________________________________________________________________________________________________

# TYPE DE CLIENTS _____________________________________________________________________________________________________________________________________________________________________   
class Typeclients(models.Model):
    type_client = models.CharField(max_length=50,null=False)
    def __str__(self):
        return f'{self.type_client}'
# __________________________________________________________________________________________________________________________________________________________________________________

# TYPE DE TONTINES _____________________________________________________________________________________________________________________________________________________________________   
class Typetontines(models.Model):
    type_tontine = models.CharField(max_length=50,null=False)
    def __str__(self):
        return f'{self.type_tontine}'
# __________________________________________________________________________________________________________________________________________________________________________________

# NATURE DE CLIENTS _____________________________________________________________________________________________________________________________________________________________________
class Natclients(models.Model):
    nat_client = models.CharField(max_length=50,null=False)
    def __str__(self):
        return f'{self.nat_client}'
# __________________________________________________________________________________________________________________________________________________________________________________

# TYPE AGENTS _____________________________________________________________________________________________________________________________________________________________________
class Typeagent(models.Model):
    type_agent = models.CharField(max_length=250,null=False)
    def __str__(self):
        return f'{self.type_agent}'
# __________________________________________________________________________________________________________________________________________________________________________________

# AGENTS _____________________________________________________________________________________________________________________________________________________________________
class Agent(models.Model):
    user = models.OneToOneField(Utilisateurs, on_delete=models.CASCADE)
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    adresse = models.CharField(max_length=200)
    telephone = models.CharField(unique=True, max_length=20)
    email = models.EmailField(unique=True)
    type_agent = models.ForeignKey(Typeagent, on_delete=models.CASCADE, null=True)
    def __str__(self):
        return f"{self.prenom} {self.nom}"
# __________________________________________________________________________________________________________________________________________________________________________________

# TYPE ACTIONNAIRE _____________________________________________________________________________________________________________________________________________________________________        
class Typeactionnaire(models.Model):
    type_act = models.CharField(max_length=250,null=False)
    def __str__(self):
        return f'{self.type_act}' 
# __________________________________________________________________________________________________________________________________________________________________________________

# STATUTS _____________________________________________________________________________________________________________________________________________________________________
class Statuts(models.Model):
    statut = models.CharField(max_length=50,null=False)
    def __str__(self):
        return f'{self.statut}'
# __________________________________________________________________________________________________________________________________________________________________________________

# CLIENTS _____________________________________________________________________________________________________________________________________________________________________
class Clients(models.Model):
    TYPE_PIECE_CHOICES = [
        ('CNI', 'Carte Nationale d\'Identité'),
        ('passeport', 'Passeport'),
        ('Attestation', 'Attestation d\'identité'),
    ]
    nom = models.CharField(max_length=100, null=True)
    prenom = models.CharField(max_length=100, null=True)
    adresse = models.CharField(max_length=200, null=True)
    telephone = models.CharField(unique=True,max_length=20, null=True)
    sexe = models.ForeignKey(Genres, on_delete=models.CASCADE, null=True)
    statut = models.ForeignKey(Statuts, on_delete=models.CASCADE, null=True)
    email = models.EmailField(unique=True, null=True)
    date_inscription = models.DateField(auto_now_add=True, null=True)
    photo = models.ImageField(upload_to='Mediatheques/', blank=True, null=True)
    piece_identite_scan = models.ImageField(upload_to='Mediatheques/', blank=True, null=True)
    profession = models.CharField(max_length=100, blank=True, null=True)
    date_naissance = models.DateField()
    lieu_naissance = models.CharField(max_length=100, null=True)
    type_piece_identite = models.CharField(max_length=20, choices=TYPE_PIECE_CHOICES)
    numero_piece_identite = models.CharField(max_length=100, null=True)
    validite_piece_identite_debut = models.DateField()
    validite_piece_identite_fin = models.DateField()
    ville_village = models.CharField(max_length=100, null=True)
    matrimoniale = models.ForeignKey(Matrimoniales, on_delete=models.CASCADE,null=True)
    user = models.OneToOneField(Utilisateurs, on_delete=models.CASCADE, null=True)
    nat_client=models.ForeignKey(Natclients, on_delete=models.CASCADE, null=True)
    def __str__(self):
        return f"{self.prenom} {self.nom}"
# __________________________________________________________________________________________________________________________________________________________________________________

# COMPTE EPARGNES _____________________________________________________________________________________________________________________________________________________________________    
class CompteEpargnes(models.Model):
    client = models.ForeignKey(Clients, on_delete=models.CASCADE, null=True)
    numero_compte = models.CharField(max_length=20, unique=True)
    solde = models.DecimalField(max_digits=10, decimal_places=2, default=0) # type: ignore
    statut = models.ForeignKey(Statuts, on_delete=models.CASCADE, null=True)
    naturecompte = models.CharField(max_length=20, null=True)

    def __str__(self):
        return f"Compte épargne {self.numero_compte} - {self.client}"
# __________________________________________________________________________________________________________________________________________________________________________________

# COMPTE PRETS _____________________________________________________________________________________________________________________________________________________________________    
class ComptePrets(models.Model):
    client = models.ForeignKey(Clients, on_delete=models.CASCADE, null=True)
    numero_compte = models.CharField(max_length=20, unique=True)
    solde = models.DecimalField(max_digits=10, decimal_places=2, default=0) # type: ignore
    taux_interet = models.DecimalField(max_digits=5, decimal_places=2, default=1)  # type: ignore # 1% par mois
    duree_en_mois = models.PositiveIntegerField(default=12)
    date_debut_pret = models.DateField()
    agent = models.ForeignKey(Utilisateurs, on_delete=models.SET_NULL, blank=True, null=True)
    com = models.ForeignKey(Agent, on_delete=models.CASCADE, null=True)
    date_fin_pret = models.DateField()
    somme_initiale = models.DecimalField(max_digits=10, decimal_places=2)
    domicile_bancaire = models.CharField(max_length=200, null=True)
    type_pret = models.ForeignKey(Typeprets, on_delete=models.CASCADE, null=True)
    date_demande = models.DateField(auto_now_add=True, null=True)
    statut = models.ForeignKey(Statuts, on_delete=models.CASCADE)
    type_client = models.ForeignKey(Typeclients, on_delete=models.CASCADE, null=True)
    naturecompte = models.CharField(max_length=20, null=True)
    
    def calculer_interets(self):
        # Calculez les intérêts en fonction de la durée du prêt
        # Vous pouvez ajouter le code ici pour effectuer le calcul des intérêts
        # Assurez-vous d'utiliser la durée en mois et le taux d'intérêt du prêt
        # Pour cet exemple, supposons que le taux d'intérêt est exprimé en pourcentage (1% par mois)
        return self.solde * (self.taux_interet / 100) * self.duree_en_mois

    def __str__(self):
        return f"Compte prêt {self.numero_compte} - {self.client}"

    def calculer_echeances(self):
        echeances = []
        date_echeance = self.date_debut_pret

        # Déterminer le nombre d'échéances par mois en fonction du type de client
        if self.type_client_id == 1:
            nbr_echeances_par_mois = 4  # Échéances hebdomadaires
            intervalle = timedelta(weeks=1)
        elif self.type_client_id == 2:
            nbr_echeances_par_mois = 1  # Échéance mensuelle
            intervalle = relativedelta(months=1)
        else:
            raise ValueError("Type de client invalide")

        # Calculer le nombre total d'échéances
        total_echeances = self.duree_en_mois * nbr_echeances_par_mois

        for i in range(total_echeances):
            echeances.append(date_echeance)
            date_echeance += intervalle

        return echeances
# __________________________________________________________________________________________________________________________________________________________________________________

# SPONSORS _________________________________________________________________________________________________________________________________________________________________________
class Sponsors(models.Model):
    # Champs de l'Sponsors
    user = models.OneToOneField(Utilisateurs, on_delete=models.CASCADE)
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    adresse = models.CharField(max_length=200)
    telephone = models.CharField(unique=True,max_length=20)
    email = models.EmailField(unique=True)
    apport = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    pourcentage = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    date_adhesion = models.DateTimeField(auto_now_add=True)
    type_act = models.ForeignKey(Typeactionnaire, on_delete=models.CASCADE, null=True)
    dividende = models.DecimalField(max_digits=10, decimal_places=2, null=True)

    def __str__(self):
        return f"{self.nom} {self.prenom}"
# __________________________________________________________________________________________________________________________________________________________________________________

# CONTRAT SPONPORS _____________________________________________________________________________________________________________________________________________________________________
class Contratsponsor(models.Model):
    sponsor = models.ForeignKey(Sponsors, on_delete=models.CASCADE, null=True)
    numero_contrat = models.CharField(max_length=20, unique=True)
    TYPE_PIECE_CHOICES = [
        ('CNI', 'Carte Nationale d\'Identité'),
        ('passeport', 'Passeport'),
        ('Attestation', 'Attestation d\'identité'),
    ]
    nom = models.CharField(max_length=100, null=True)
    prenom = models.CharField(max_length=100, null=True)
    adresse = models.CharField(max_length=200, null=True)
    telephone = models.CharField(unique=True,max_length=20, null=True)
    sexe = models.ForeignKey(Genres, on_delete=models.CASCADE, null=True)
    statut = models.ForeignKey(Statuts, on_delete=models.CASCADE, null=True)
    email = models.EmailField(unique=True, null=True)
    date_inscription = models.DateField(auto_now_add=True, null=True)
    photo = models.ImageField(upload_to='Mediatheques/', blank=True, null=True)
    piece_identite_scan = models.ImageField(upload_to='Mediatheques/', blank=True, null=True)
    profession = models.CharField(max_length=100, blank=True, null=True)
    date_naissance = models.DateField(null=True)
    lieu_naissance = models.CharField(max_length=100, null=True)
    type_piece_identite = models.CharField(max_length=20, choices=TYPE_PIECE_CHOICES,null=True)
    numero_piece_identite = models.CharField(max_length=100, null=True)
    validite_piece_identite_debut = models.DateField(null=True)
    validite_piece_identite_fin = models.DateField(null=True)
    ville_village = models.CharField(max_length=100, null=True)
    matrimoniale = models.ForeignKey(Matrimoniales, on_delete=models.CASCADE,null=True)
    nat_client=models.ForeignKey(Natclients, on_delete=models.CASCADE, null=True)
    client = models.ForeignKey(Clients, on_delete=models.CASCADE, null=True)
    numero_compte = models.CharField(max_length=20, unique=True)
    solde = models.DecimalField(max_digits=10, decimal_places=2, default=0) # type: ignore
    taux_interet = models.DecimalField(max_digits=5, decimal_places=2, default=1)  # type: ignore # 1% par mois
    duree_en_mois = models.PositiveIntegerField(default=12)
    duree_contrat = models.PositiveIntegerField(default=12,null=True)
    date_fin_contrat = models.DateField(null=True)
    soldecontrat = models.DecimalField(max_digits=10, decimal_places=2, default=0,null=True) # type: ignore
    date_debut_pret = models.DateField()
    com = models.ForeignKey(Agent, on_delete=models.CASCADE, null=True)
    date_fin_pret = models.DateField()
    somme_initiale = models.DecimalField(max_digits=10, decimal_places=2)
    domicile_bancaire = models.CharField(max_length=200, null=True)
    type_pret = models.ForeignKey(Typeprets, on_delete=models.CASCADE, null=True)
    date_demande = models.DateField(auto_now_add=True, null=True)
    statut = models.ForeignKey(Statuts, on_delete=models.CASCADE)
    type_client = models.ForeignKey(Typeclients, on_delete=models.CASCADE, null=True)
   
    def calculer_interets(self):
        # Calculez les intérêts en fonction de la durée du prêt
        # Vous pouvez ajouter le code ici pour effectuer le calcul des intérêts
        # Assurez-vous d'utiliser la durée en mois et le taux d'intérêt du prêt
        # Pour cet exemple, supposons que le taux d'intérêt est exprimé en pourcentage (1% par mois)
        return self.solde * (self.taux_interet / 100) * self.duree_en_mois
    
    def calculer_echeances(self):
        echeances = []
        date_echeance = self.date_debut_pret

        # Déterminer le nombre d'échéances par mois en fonction du type de client
        if self.type_client_id == 1:
            nbr_echeances_par_mois = 4  # Échéances hebdomadaires
            intervalle = timedelta(weeks=1)
        elif self.type_client_id == 2:
            nbr_echeances_par_mois = 1  # Échéance mensuelle
            intervalle = relativedelta(months=1)
        else:
            raise ValueError("Type de client invalide")

        # Calculer le nombre total d'échéances
        total_echeances = self.duree_en_mois * nbr_echeances_par_mois

        for i in range(total_echeances):
            echeances.append(date_echeance)
            date_echeance += intervalle

        return echeances
    def __str__(self):
        return f"Compte prêt {self.numero_contrat} - {self.client}"
# __________________________________________________________________________________________________________________________________________________________________________________

# ACTIONNAIRES _____________________________________________________________________________________________________________________________________________________________________
class Actionnaire(models.Model):
    # Champs de l'actionnaire
    user = models.OneToOneField(Utilisateurs, on_delete=models.CASCADE)
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    adresse = models.CharField(max_length=200)
    telephone = models.CharField(unique=True,max_length=20)
    email = models.EmailField(unique=True)
    apport = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    pourcentage = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    date_adhesion = models.DateField(auto_now_add=True)
    type_act = models.ForeignKey(Typeactionnaire, on_delete=models.CASCADE, null=True)
    dividende = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    com = models.ForeignKey(Agent, on_delete=models.CASCADE, null=True)
    # Méthode pour sauvegarder l'actionnaire
    def save(self, *args, **kwargs):
        is_new = not self.pk  # Vérifier si l'objet est nouvellement créé
        super().save(*args, **kwargs)  # Enregistrer l'objet
        if is_new:
            self.update_percentages()  # Mettre à jour les pourcentages

    # Méthode pour mettre à jour les pourcentages
    def update_percentages(self):
        # Calculer le total des apports
        total_apport = Actionnaire.objects.aggregate(models.Sum('apport'))['apport__sum'] or 0
        if total_apport != 0:
            self.pourcentage = (self.apport / total_apport) * 100  # Calculer le pourcentage de l'apport
        else:
            self.pourcentage = 0
        self.save()  # Enregistrer les modifications

        # Mettre à jour les pourcentages des autres actionnaires
        autres_actionnaires = Actionnaire.objects.exclude(pk=self.pk)
        total_apport_autres = autres_actionnaires.aggregate(models.Sum('apport'))['apport__sum'] or 0
        total_pourcentage_autres = autres_actionnaires.aggregate(models.Sum('pourcentage'))['pourcentage__sum'] or 0
        if total_apport_autres != 0 and total_pourcentage_autres != 0:
            coefficient = (100 - self.pourcentage) / total_pourcentage_autres
            autres_actionnaires.update(pourcentage=models.F('pourcentage') * coefficient)
        else:
            autres_actionnaires.update(pourcentage=0)  # Mettre à jour les pourcentages à zéro pour les autres actionnaires

    def __str__(self):
        return f"{self.nom} {self.prenom}"
# __________________________________________________________________________________________________________________________________________________________________________________

# ECHEANCIER _____________________________________________________________________________________________________________________________________________________________________
class Echeancier(models.Model):
    compte_pret = models.ForeignKey(ComptePrets, on_delete=models.CASCADE)
    date_echeance = models.DateField()
    montant_echeance = models.DecimalField(max_digits=10, decimal_places=2)
    montant_interet = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    est_paye = models.BooleanField(default=False)
    montant_epargne = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    montant_adhesion = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    montant_penalite = models.DecimalField(max_digits=10, decimal_places=2,null=True, default=0)
    ancien_echeance = models.DecimalField(max_digits=10, decimal_places=2,null=True, default=0)

    def __str__(self):
        return f"Échéance pour le compte prêt {self.compte_pret.numero_compte} - Montant: {self.montant_echeance}"
# __________________________________________________________________________________________________________________________________________________________________________________

# TRANSACTION EPARGNE _____________________________________________________________________________________________________________________________________________________________________
class TransactionEpargne(models.Model):
    TYPE_CHOICES = [
        ('Depot', 'Dépôt'),
        ('Retrait', 'Retrait'),
        ('Virement', 'Virement'),
    ]

    compte_epargne = models.ForeignKey(
        CompteEpargnes,
        on_delete=models.CASCADE,
        related_name='transactions_epargne',
        null=True,
        blank=True
    )

    montant = models.DecimalField(max_digits=10, decimal_places=2)
    type_transaction = models.CharField(max_length=20, choices=TYPE_CHOICES)
    date_transaction = models.DateTimeField(auto_now_add=True)
    agent = models.ForeignKey(Utilisateurs, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        if self.type_transaction == 'Virement':
            return f"{self.type_transaction} de {self.montant} FCFA de {self.compte_epargne} à {self.compte_pret}"
        else:
            return f"{self.type_transaction} de {self.montant} FCFA sur le compte {self.compte_epargne}"
# __________________________________________________________________________________________________________________________________________________________________________________

# TRANSACTION PRET _____________________________________________________________________________________________________________________________________________________________________
class TransactionPret(models.Model):
    TYPE_CHOICES = [
        ('Depot', 'Dépôt'),
        ('Retrait', 'Retrait'),
        ('Virement', 'Virement'),
    ]

    compte_pret = models.ForeignKey(
        ComptePrets,
        on_delete=models.CASCADE,
        related_name='transactions_pret',
        null=True,
        blank=True
    )

    montant = models.DecimalField(max_digits=10, decimal_places=2)
    type_transaction = models.CharField(max_length=20, choices=TYPE_CHOICES)
    date_transaction = models.DateTimeField(auto_now_add=True)
    agent = models.ForeignKey(Utilisateurs, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        if self.type_transaction == 'Virement':
            return f"{self.type_transaction} de {self.montant} FCFA de {self.compte_pret} à {self.compte_epargne}"
        else:
            return f"{self.type_transaction} de {self.montant} FCFA sur le compte {self.compte_pret}"
# __________________________________________________________________________________________________________________________________________________________________________________

# DEPENSES _____________________________________________________________________________________________________________________________________________________________________
class Depense(models.Model):
    nom = models.CharField(max_length=100)
    montant = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(auto_now_add=True)
    agent = models.ForeignKey(Utilisateurs, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.nom
# __________________________________________________________________________________________________________________________________________________________________________________

# LICENCES _____________________________________________________________________________________________________________________________________________________________________   
class License(models.Model):
    client_name = models.CharField(max_length=100)
    license_key = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def calculate_valid_until(self):
        # Calculer la date d'expiration en ajoutant un an à la date de création
        return self.created_at + timezone.timedelta(days=365)

    def is_valid(self):
        return timezone.now() <= self.calculate_valid_until()
# __________________________________________________________________________________________________________________________________________________________________________________

# COMPTE PRET ACTIONNAIRE _____________________________________________________________________________________________________________________________________________________________________
class ComptePretsact(models.Model):
    actionnaire = models.ForeignKey(Actionnaire, on_delete=models.CASCADE, null=True)
    numero_compte = models.CharField(max_length=20, unique=True)
    solde = models.DecimalField(max_digits=10, decimal_places=2, default=0) # type: ignore
    taux_interet = models.DecimalField(max_digits=5, decimal_places=2, default=1)  # type: ignore # 1% par mois
    duree_en_mois = models.PositiveIntegerField(default=12)
    date_debut_pret = models.DateField()
    agent = models.ForeignKey(Utilisateurs, on_delete=models.SET_NULL, blank=True, null=True)
    com = models.ForeignKey(Agent, on_delete=models.CASCADE, null=True)
    date_fin_pret = models.DateField()
    somme_initiale = models.DecimalField(max_digits=10, decimal_places=2)
    domicile_bancaire = models.CharField(max_length=200, null=True)
    type_pret = models.ForeignKey(Typeprets, on_delete=models.CASCADE, null=True)
    date_demande = models.DateField(auto_now_add=True, null=True)
    statut = models.ForeignKey(Statuts, on_delete=models.CASCADE)
    type_client = models.ForeignKey(Typeclients, on_delete=models.CASCADE, null=True)
    def __str__(self):
        return f"Compte prêt {self.numero_compte} - {self.actionnaire}"

    def calculer_interets(self):
        # Calculez les intérêts en fonction de la durée du prêt
        # Vous pouvez ajouter le code ici pour effectuer le calcul des intérêts
        # Assurez-vous d'utiliser la durée en mois et le taux d'intérêt du prêt
        # Pour cet exemple, supposons que le taux d'intérêt est exprimé en pourcentage (1% par mois)
        return self.solde * (self.taux_interet / 100) * self.duree_en_mois

    def calculer_echeances(self):
        echeances = []
        date_echeance = self.date_debut_pret

        # Déterminer le nombre d'échéances par mois en fonction du type de client
        if self.type_client_id == 1:
            nbr_echeances_par_mois = 4  # Échéances hebdomadaires
            intervalle = timedelta(weeks=1)
        elif self.type_client_id == 2:
            nbr_echeances_par_mois = 1  # Échéance mensuelle
            intervalle = relativedelta(months=1)
        else:
            raise ValueError("Type de client invalide")

        # Calculer le nombre total d'échéances
        total_echeances = self.duree_en_mois * nbr_echeances_par_mois

        for i in range(total_echeances):
            echeances.append(date_echeance)
            date_echeance += intervalle

        return echeances
# __________________________________________________________________________________________________________________________________________________________________________________

# ECHEANCIER ACTIONNAIRE _____________________________________________________________________________________________________________________________________________________________________
class Echeancieract(models.Model):
    compte_pretact = models.ForeignKey(ComptePretsact, on_delete=models.CASCADE)
    date_echeance = models.DateField()
    montant_echeance = models.DecimalField(max_digits=10, decimal_places=2)
    montant_interet = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    est_paye = models.BooleanField(default=False)
    montant_epargne = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    montant_adhesion = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    montant_penalite = models.DecimalField(max_digits=10, decimal_places=2,null=True, default=0)
    ancien_echeance = models.DecimalField(max_digits=10, decimal_places=2,null=True, default=0)

    def __str__(self):
        return f"Échéance pour le compte prêt {self.compte_pretact.numero_compte} - Montant: {self.montant_echeance}"
 # __________________________________________________________________________________________________________________________________________________________________________________

# MESSAGES _____________________________________________________________________________________________________________________________________________________________________   
class Msg(models.Model):
    date_msg = models.DateTimeField(auto_now_add=True)
    titre = models.CharField(max_length=20, unique=True)
    message = models.CharField(max_length=2000)
    groupemsg = models.CharField(max_length=20)
# __________________________________________________________________________________________________________________________________________________________________________________

# TRANSACTION PRET ACTIONNAIRE _____________________________________________________________________________________________________________________________________________________________________
class TransactionPretact(models.Model):
    TYPE_CHOICES = [
        ('Depot', 'Dépôt'),
        ('Retrait', 'Retrait'),
        ('Virement', 'Virement'),
    ]

    compte_pret = models.ForeignKey(
        ComptePretsact,
        on_delete=models.CASCADE,
        related_name='transactions_pret',
        null=True,
        blank=True
    )

    montant = models.DecimalField(max_digits=10, decimal_places=2)
    type_transaction = models.CharField(max_length=20, choices=TYPE_CHOICES)
    date_transaction = models.DateTimeField(auto_now_add=True)
    agent = models.ForeignKey(Utilisateurs, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        if self.type_transaction == 'Virement':
            return f"{self.type_transaction} de {self.montant} FCFA de {self.compte_pret} à {self.compte_epargne}"
        else:
            return f"{self.type_transaction} de {self.montant} FCFA sur le compte {self.compte_pret}"
# __________________________________________________________________________________________________________________________________________________________________________________

# TONTINES _____________________________________________________________________________________________________________________________________________________________________
class Tontines(models.Model):
    client = models.ForeignKey(Clients, on_delete=models.CASCADE, null=True)
    numero_tontine = models.CharField(max_length=20, unique=True)
    date_tontine = models.DateField(auto_now_add=True)
    solde = models.DecimalField(max_digits=10, decimal_places=2, default=0) # type: ignore
    cotite = models.DecimalField(max_digits=10, decimal_places=2, default=0) # type: ignore
    statut = models.ForeignKey(Statuts, on_delete=models.CASCADE, null=True)
    agent = models.ForeignKey(Utilisateurs, on_delete=models.SET_NULL, blank=True, null=True)
    com = models.ForeignKey(Agent, on_delete=models.CASCADE, null=True)
    nbreaide = models.PositiveIntegerField(default=0)
    penaliteton = models.PositiveIntegerField(default=0)
    montant_min = models.DecimalField(max_digits=10, decimal_places=2, default=0) # type: ignore
    date_palier = models.DateField(null=True)
    duree = models.PositiveIntegerField(default=0)
    dateaide = models.DateField(null=True)
    montant_aide = models.DecimalField(max_digits=10, decimal_places=2, default=0) # type: ignore
    type_tontine = models.ForeignKey(Typetontines, on_delete=models.CASCADE, null=True)
    date_futurcotisation = models.DateField(null=True)
    
    def __str__(self):
        return f"Tontine {self.numero_tontine} - {self.client}"
# __________________________________________________________________________________________________________________________________________________________________________________

# AIDES _____________________________________________________________________________________________________________________________________________________________________    
class Aides(models.Model):
    client = models.ForeignKey(Clients, on_delete=models.CASCADE, null=True)
    date_aide = models.DateTimeField(auto_now_add=True)
    montant_aide = models.DecimalField(max_digits=10, decimal_places=2, default=0) # type: ignore
    statut = models.ForeignKey(Statuts, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"Aide {self.date_aide} - {self.client}"
# __________________________________________________________________________________________________________________________________________________________________________________

# TRANSACTION TONTINE _____________________________________________________________________________________________________________________________________________________________________     
class TransactionTontine(models.Model):
    TYPE_CHOICES = [
        ('Depot', 'Dépôt'),
        ('Retrait', 'Retrait'),
        ('Virement', 'Virement'),
        ('Mobile money', 'Mobile money'),
    ]

    tontine = models.ForeignKey(
        Tontines,
        on_delete=models.CASCADE,
        related_name='transactions_tontine',
        null=True,
        blank=True
    )

    montant = models.DecimalField(max_digits=10, decimal_places=2)
    type_transaction = models.CharField(max_length=20, choices=TYPE_CHOICES)
    date_transaction = models.DateTimeField(auto_now_add=True)
    agent = models.ForeignKey(Utilisateurs, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        if self.type_transaction == 'Mobile money':
            return f"{self.type_transaction} de {self.montant} FCFA de {self.tontine} à {self.type_transaction}"
        else:
            return f"{self.type_transaction} de {self.montant} FCFA sur le compte {self.tontine}"
# __________________________________________________________________________________________________________________________________________________________________________________

# RACHATS CLIENT _____________________________________________________________________________________________________________________________________________________________________
class Rachats(models.Model):
    client = models.ForeignKey(Clients, on_delete=models.CASCADE, null=True)
    date_rachat = models.DateTimeField(auto_now_add=True)
    compte_pretactuel = models.ForeignKey(ComptePrets, on_delete=models.CASCADE)
    montant_actuel = models.DecimalField(max_digits=10, decimal_places=2, default=0) # type: ignore
    reste_actuel = models.DecimalField(max_digits=10, decimal_places=2, default=0) # type: ignore
    compte_pretnew =  models.CharField(max_length=100)
    montant_new = models.DecimalField(max_digits=10, decimal_places=2, default=0) # type: ignore

    def __str__(self):
        return f"Aide {self.date_rachat} - {self.client} - {self.compte_pretactuel} - {self.compte_pretnew}"
# __________________________________________________________________________________________________________________________________________________________________________________

# RACHAT ACTIONNAIRE _____________________________________________________________________________________________________________________________________________________________________
class Rachatsact(models.Model):
    actionnaire = models.ForeignKey(Actionnaire, on_delete=models.CASCADE, null=True)
    date_rachat = models.DateTimeField(auto_now_add=True)
    compte_pretactuel = models.ForeignKey(ComptePretsact, on_delete=models.CASCADE)
    montant_actuel = models.DecimalField(max_digits=10, decimal_places=2, default=0) # type: ignore
    reste_actuel = models.DecimalField(max_digits=10, decimal_places=2, default=0) # type: ignore
    compte_pretnew =  models.CharField(max_length=100)
    montant_new = models.DecimalField(max_digits=10, decimal_places=2, default=0) # type: ignore

    def __str__(self):
        return f"Aide {self.date_rachat} - {self.actionnaire} - {self.compte_pretactuel} - {self.compte_pretnew}"
# __________________________________________________________________________________________________________________________________________________________________________________

# COMMISSIONS _____________________________________________________________________________________________________________________________________________________________________
class Commissions(models.Model):
    agent = models.ForeignKey(Utilisateurs, on_delete=models.SET_NULL, blank=True, null=True)
    solde = models.DecimalField(max_digits=10, decimal_places=2, default=0) # type: ignore
    datesolde = models.DateField()
    soldeprecedent = models.DecimalField(max_digits=10, decimal_places=2, default=0) # type: ignore
    date_aide = models.DateTimeField(auto_now_add=True)
    statut = models.ForeignKey(Statuts, on_delete=models.CASCADE, null=True)
# __________________________________________________________________________________________________________________________________________________________________________________

# TRANSACTION COMMISSION PRET _____________________________________________________________________________________________________________________________________________________________________
class TransactionCommissionpret(models.Model):
    TYPE_CHOICES = [
        ('Depot', 'Dépôt'),
        ('Retrait', 'Retrait'),
        ('Virement', 'Virement'),
        ('Mobile money', 'Mobile money'),
    ]

    commission = models.ForeignKey(
        Commissions,
        on_delete=models.CASCADE,
        related_name='transactions_commpret',
        null=True,
        blank=True
    )

    echeance = models.ForeignKey(
        Echeancier,
        on_delete=models.CASCADE,
        related_name='transactions_comm',
        null=True,
        blank=True
    )

    montant = models.DecimalField(max_digits=10, decimal_places=2)
    type_transaction = models.CharField(max_length=20, choices=TYPE_CHOICES)
    date_transaction = models.DateTimeField(auto_now_add=True)
    agent = models.ForeignKey(Utilisateurs, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        if self.type_transaction == 'Mobile money':
            return f"{self.type_transaction} de {self.montant} FCFA de {self.commission} à {self.type_transaction}"
        else:
            return f"{self.type_transaction} de {self.montant} FCFA sur le compte {self.tontine}"
# __________________________________________________________________________________________________________________________________________________________________________________

# TRANSACTION COMMISSION PRET COOP _____________________________________________________________________________________________________________________________________________________________________
class TransactionCommissionpretact(models.Model):
    TYPE_CHOICES = [
        ('Depot', 'Dépôt'),
        ('Retrait', 'Retrait'),
        ('Virement', 'Virement'),
        ('Mobile money', 'Mobile money'),
    ]

    commissionact = models.ForeignKey(
        Commissions,
        on_delete=models.CASCADE,
        related_name='transactions_commpretact',
        null=True,
        blank=True
    )

    echeance = models.ForeignKey(
        Echeancieract,
        on_delete=models.CASCADE,
        related_name='transactions_comm',
        null=True,
        blank=True
    )

    montant = models.DecimalField(max_digits=10, decimal_places=2)
    type_transaction = models.CharField(max_length=20, choices=TYPE_CHOICES)
    date_transaction = models.DateTimeField(auto_now_add=True)
    agent = models.ForeignKey(Utilisateurs, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        if self.type_transaction == 'Mobile money':
            return f"{self.type_transaction} de {self.montant} FCFA de {self.commission} à {self.type_transaction}"
        else:
            return f"{self.type_transaction} de {self.montant} FCFA sur le compte {self.tontine}"
# __________________________________________________________________________________________________________________________________________________________________________________


# TRANSACTION COMMISSION DEMACHEUR _____________________________________________________________________________________________________________________________________________________________________
class TransactionCommissioninves(models.Model):
    TYPE_CHOICES = [
        ('Depot', 'Dépôt'),
        ('Retrait', 'Retrait'),
        ('Virement', 'Virement'),
        ('Mobile money', 'Mobile money'),
    ]

    commissioninv = models.ForeignKey(
        Commissions,
        on_delete=models.CASCADE,
        related_name='transactions_cominves',
        null=True,
        blank=True
    )

    actionnaire = models.ForeignKey(
        Actionnaire,
        on_delete=models.CASCADE,
        related_name='transactions_commact',
        null=True,
        blank=True
    )

    montant = models.DecimalField(max_digits=10, decimal_places=2)
    type_transaction = models.CharField(max_length=20, choices=TYPE_CHOICES)
    date_transaction = models.DateTimeField(auto_now_add=True)
    agent = models.ForeignKey(Utilisateurs, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        if self.type_transaction == 'Mobile money':
            return f"{self.type_transaction} de {self.montant} FCFA de {self.commission} à {self.type_transaction}"
        else:
            return f"{self.type_transaction} de {self.montant} FCFA sur le compte {self.tontine}"
# __________________________________________________________________________________________________________________________________________________________________________________

# COMPTE PENALITE _____________________________________________________________________________________________________________________________________________________________________    
class ComptePenalites(models.Model):
    solde = models.DecimalField(max_digits=10, decimal_places=2, default=0) # type: ignore
    datesolde = models.DateField()
    soldeprecedent = models.DecimalField(max_digits=10, decimal_places=2, default=0) # type: ignore
    dateprecedent = models.DateField(auto_now_add=True)
    statut = models.ForeignKey(Statuts, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"Penalite {self.datesolde} - {self.solde}"
    
class TransactionPenaliteHist(models.Model):
    TYPE_CHOICES = [
        ('Depot', 'Dépôt'),
        ('Retrait', 'Retrait'),
        ('Virement', 'Virement'),
    ]

    comptepenalite = models.ForeignKey(
        ComptePenalites,
        on_delete=models.CASCADE,
        related_name='transactions_penal',
        null=True,
        blank=True
    )

    montant = models.DecimalField(max_digits=10, decimal_places=2)
    type_transaction = models.CharField(max_length=20, choices=TYPE_CHOICES)
    date_transaction = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.type_transaction == 'Virement':
            return f"{self.type_transaction} de {self.montant} FCFA de {self.comptepenalite} "
        else:
            return f"{self.type_transaction} de {self.montant} FCFA sur le compte {self.comptepenalite}"
# __________________________________________________________________________________________________________________________________________________________________________________

# COMPTE INTERETS PRET _____________________________________________________________________________________________________________________________________________________________________    
class CompteInterets(models.Model):
    solde = models.DecimalField(max_digits=10, decimal_places=2, default=0) # type: ignore
    datesolde = models.DateField()
    soldeprecedent = models.DecimalField(max_digits=10, decimal_places=2, default=0) # type: ignore
    dateprecedent = models.DateField(auto_now_add=True)
    statut = models.ForeignKey(Statuts, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"Penalite {self.datesolde} - {self.solde}"
    
class TransactionInteret(models.Model):
    TYPE_CHOICES = [
        ('Depot', 'Dépôt'),
        ('Retrait', 'Retrait'),
        ('Virement', 'Virement'),
    ]

    compteinteret = models.ForeignKey(
        CompteInterets,
        on_delete=models.CASCADE,
        related_name='transactions_interet',
        null=True,
        blank=True
    )

    montant = models.DecimalField(max_digits=10, decimal_places=2)
    type_transaction = models.CharField(max_length=20, choices=TYPE_CHOICES)
    date_transaction = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.type_transaction == 'Virement':
            return f"{self.type_transaction} de {self.montant} FCFA de {self.compteinteret} "
        else:
            return f"{self.type_transaction} de {self.montant} FCFA sur le compte {self.compteinteret}"
# __________________________________________________________________________________________________________________________________________________________________________________

# TRANSACTION PENALITE _____________________________________________________________________________________________________________________________________________________________________
class TransactionPenalite(models.Model):
    TYPE_CHOICES = [
        ('Depot', 'Dépôt'),
        ('Retrait', 'Retrait'),
        ('Virement', 'Virement'),
    ]

    compte_pret = models.ForeignKey(
        ComptePrets,
        on_delete=models.CASCADE,
        related_name='transactions_penalite',
        null=True,
        blank=True
    )

    echeance = models.ForeignKey(
        Echeancier,
        on_delete=models.CASCADE,
        related_name='transactions_penalite',
        null=True,
        blank=True
    )

    montant = models.DecimalField(max_digits=10, decimal_places=2)
    type_transaction = models.CharField(max_length=20, choices=TYPE_CHOICES)
    date_transaction = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.type_transaction == 'Virement':
            return f"{self.type_transaction} de {self.montant} FCFA de {self.compte_pret} "
        else:
            return f"{self.type_transaction} de {self.montant} FCFA sur le compte {self.compte_pret}"
# __________________________________________________________________________________________________________________________________________________________________________________

# TRANSACTION PENALITE ACTIONNAIRE _____________________________________________________________________________________________________________________________________________________________________        
class TransactionPenaliteact(models.Model):
    TYPE_CHOICES = [
        ('Depot', 'Dépôt'),
        ('Retrait', 'Retrait'),
        ('Virement', 'Virement'),
    ]

    compte_pret = models.ForeignKey(
        ComptePretsact,
        on_delete=models.CASCADE,
        related_name='transactions_penaliteact',
        null=True,
        blank=True
    )

    echeance = models.ForeignKey(
        Echeancieract,
        on_delete=models.CASCADE,
        related_name='transactions_penaliteact',
        null=True,
        blank=True
    )

    montant = models.DecimalField(max_digits=10, decimal_places=2)
    type_transaction = models.CharField(max_length=20, choices=TYPE_CHOICES)
    date_transaction = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.type_transaction == 'Virement':
            return f"{self.type_transaction} de {self.montant} FCFA de {self.compte_pret} "
        else:
            return f"{self.type_transaction} de {self.montant} FCFA sur le compte {self.compte_pret}"
# __________________________________________________________________________________________________________________________________________________________________________________

# TRANSACTION RISTOUNE _____________________________________________________________________________________________________________________________________________________________________        
class TransactionRistourne(models.Model):
    TYPE_CHOICES = [
        ('Depot', 'Dépôt'),
        ('Retrait', 'Retrait'),
    ]
    
    actionnaire = models.ForeignKey(
        Actionnaire,
        on_delete=models.CASCADE,
        related_name='transactions_ristourne',
        null=True,
        blank=True
    )
    type_transaction = models.CharField(max_length=20, choices=TYPE_CHOICES, null=True)
    montant = models.DecimalField(max_digits=10, decimal_places=2)
    date_transaction = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.actionnaire} d' un montant de {self.montant} FCFA sur l'apport"
# __________________________________________________________________________________________________________________________________________________________________________________

# COMPTE KHA _____________________________________________________________________________________________________________________________________________________________________    
class CompteKha(models.Model):
    solde = models.DecimalField(max_digits=10, decimal_places=2, default=0) # type: ignore
    datesolde = models.DateField()
    soldeprecedent = models.DecimalField(max_digits=10, decimal_places=2, default=0) # type: ignore
    dateprecedent = models.DateField(auto_now_add=True)
    statut = models.ForeignKey(Statuts, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"Aide {self.datesolde} - {self.solde}"
# __________________________________________________________________________________________________________________________________________________________________________________

# TRANSACTION COMPTE KHA _____________________________________________________________________________________________________________________________________________________________________    
class TransactionKha(models.Model):
    TYPE_CHOICES = [
        ('Depot', 'Dépôt'),
        ('Retrait', 'Retrait'),
        ('Virement', 'Virement'),
    ]

    comptekha = models.ForeignKey(
        CompteKha,
        on_delete=models.CASCADE,
        related_name='transactions_kha',
        null=True,
        blank=True
    )

    montant = models.DecimalField(max_digits=10, decimal_places=2)
    type_transaction = models.CharField(max_length=20, choices=TYPE_CHOICES)
    date_transaction = models.DateTimeField(auto_now_add=True)
    agent = models.ForeignKey(Utilisateurs, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        if self.type_transaction == 'Virement':
            return f"{self.type_transaction} de {self.montant} FCFA de {self.comptekha} "
        else:
            return f"{self.type_transaction} de {self.montant} FCFA sur le compte {self.comptekha}"
# __________________________________________________________________________________________________________________________________________________________________________________

# TRANSACTION ADHESION KHA _____________________________________________________________________________________________________________________________________________________________________        
class CompteAdhesionkhas(models.Model):
    solde = models.DecimalField(max_digits=10, decimal_places=2, default=0) # type: ignore
    datesolde = models.DateField()
    soldeprecedent = models.DecimalField(max_digits=10, decimal_places=2, default=0) # type: ignore
    dateprecedent = models.DateField(auto_now_add=True)
    statut = models.ForeignKey(Statuts, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"Aide {self.datesolde} - {self.solde}"

class TransactionAdhesionkha(models.Model):
    TYPE_CHOICES = [
        ('Depot', 'Dépôt'),
        ('Retrait', 'Retrait'),
        ('Virement', 'Virement'),
    ]

    compteAdhessionkha = models.ForeignKey(
        CompteAdhesionkhas,
        on_delete=models.CASCADE,
        related_name='transactions_adhesion',
        null=True,
        blank=True
    )

    montant = models.DecimalField(max_digits=10, decimal_places=2)
    type_transaction = models.CharField(max_length=20, choices=TYPE_CHOICES)
    date_transaction = models.DateTimeField(auto_now_add=True)
    agent = models.ForeignKey(Utilisateurs, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        if self.type_transaction == 'Virement':
            return f"{self.type_transaction} de {self.montant} FCFA de {self.compteAdhessionkha} "
        else:
            return f"{self.type_transaction} de {self.montant} FCFA sur le compte {self.compteAdhessionkha}"
# __________________________________________________________________________________________________________________________________________________________________________________

# COMPTE EPARGNE ACTIONNAIRE _____________________________________________________________________________________________________________________________________________________________________        
class CompteEpargnesact(models.Model):
    actionnaire = models.ForeignKey(Actionnaire, on_delete=models.CASCADE, null=True)
    numero_compte = models.CharField(max_length=20, unique=True)
    solde = models.DecimalField(max_digits=10, decimal_places=2, default=0) # type: ignore
    statut = models.ForeignKey(Statuts, on_delete=models.CASCADE, null=True)
# __________________________________________________________________________________________________________________________________________________________________________________

# TRANSACTION EPARGNE ACTIONNAIRE _____________________________________________________________________________________________________________________________________________________________________
class TransactionEpargneact(models.Model):
    TYPE_CHOICES = [
        ('Depot', 'Dépôt'),
        ('Retrait', 'Retrait'),
        ('Virement', 'Virement'),
    ]

    compte_epargne = models.ForeignKey(
        CompteEpargnesact,
        on_delete=models.CASCADE,
        related_name='transactions_epargneact',
        null=True,
        blank=True
    )

    montant = models.DecimalField(max_digits=10, decimal_places=2)
    type_transaction = models.CharField(max_length=20, choices=TYPE_CHOICES)
    date_transaction = models.DateTimeField(auto_now_add=True)
    agent = models.ForeignKey(Utilisateurs, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        if self.type_transaction == 'Virement':
            return f"{self.type_transaction} de {self.montant} FCFA de {self.compte_epargne} à {self.compte_pret}"
        else:
            return f"{self.type_transaction} de {self.montant} FCFA sur le compte {self.compte_epargne}"
# __________________________________________________________________________________________________________________________________________________________________________________

# TYPE DOCUMENTS _____________________________________________________________________________________________________________________________________________________________________
class Typedocuments(models.Model):
    Typedoc = models.CharField(max_length=50)
    def __str__(self):
        return f'{self.Typedoc}'
# __________________________________________________________________________________________________________________________________________________________________________________

# DOCUMENTS _____________________________________________________________________________________________________________________________________________________________________
class Documents(models.Model):
    Title = models.CharField(max_length=255)
    File = models.FileField(upload_to='Mediatheques/')
    Typedoc = models.ForeignKey(Typedocuments, on_delete=models.CASCADE,null=True)
# __________________________________________________________________________________________________________________________________________________________________________________

# HISTORISQUE DES APPELS _____________________________________________________________________________________________________________________________________________________________________
class CallHistory(models.Model):
    phone_number = models.CharField(max_length=15)
    call_date = models.DateTimeField(auto_now_add=True)
    call_duration = models.DurationField()

    def __str__(self):
        return f'{self.phone_number} - {self.call_date} - {self.call_duration}'
# __________________________________________________________________________________________________________________________________________________________________________________

# PRESENTATION _____________________________________________________________________________________________________________________________________________________________________
class Presentation(models.Model):
    logo = models.ImageField(upload_to='Mediatheques/', null=True, blank=True)
    contact = models.CharField(max_length=15)
    presentation_text = models.TextField()
    welcome_message = models.TextField()
    video_url = models.FileField(upload_to='Mediatheques/', null=True, blank=True)
    site = models.CharField(max_length=50, null=True)
    pub = models.ImageField(upload_to='Mediatheques/', null=True, blank=True)
    email = models.CharField(max_length=50, null=True)
    whatsapp = models.URLField(max_length=200, null=True, blank=True) 
    facebook = models.URLField(max_length=200, null=True, blank=True)
    def __str__(self):
        return "Presentation Data"
# __________________________________________________________________________________________________________________________________________________________________________________

# DEMANDES CLIENTS  _____________________________________________________________________________________________________________________________________________________________________
class Demandes(models.Model):
    date_dde = models.DateTimeField(auto_now_add=True)
    Nom_prenoms = models.CharField(max_length=250, unique=True)
    deja_beneficie = models.CharField(max_length=20)
    nombrefois = models.CharField(max_length=20)
    montant = models.DecimalField(max_digits=10, decimal_places=2)
    phone_number = models.CharField(max_length=15)
    lieuhabitation = models.CharField(max_length=20)
    typedde = models.CharField(max_length=20)
# __________________________________________________________________________________________________________________________________________________________________________________

# CONFIGURATION DES TAUX _____________________________________________________________________________________________________________________________________________________________________
class Confconstantes(models.Model):
    partrespo = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    partactif = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    partnonactif = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    partpalierun = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    partpalierd = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    partparliert = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    partparlierq = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    partparlierc = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    partfraisdos = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    partfraisdossous = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    partcom = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    partpenalite = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    partepargne = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    partepargnesous = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    partdemarch = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    statut = models.ForeignKey(Statuts, on_delete=models.CASCADE, null=True)
    dureecoopa = models.PositiveIntegerField(default=0)
    dureecoopn = models.PositiveIntegerField(default=0)
    partprelev =models.DecimalField(max_digits=10, decimal_places=2, null=True)
# __________________________________________________________________________________________________________________________________________________________________________________

# COMPTE FONDATEUR _____________________________________________________________________________________________________________________________________________________________________
class CompteFondateur(models.Model):
    solde = models.DecimalField(max_digits=10, decimal_places=2, default=0) # type: ignore
    datesolde = models.DateField()
    soldeprecedent = models.DecimalField(max_digits=10, decimal_places=2, default=0) # type: ignore
    dateprecedent = models.DateField(auto_now_add=True)
    statut = models.ForeignKey(Statuts, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"Aide {self.datesolde} - {self.solde}"
# __________________________________________________________________________________________________________________________________________________________________________________

# TRANSACTION ADHESION KHA _____________________________________________________________________________________________________________________________________________________________________
class TransactionFondateur(models.Model):
    TYPE_CHOICES = [
        ('Depot', 'Dépôt'),
        ('Retrait', 'Retrait'),
        ('Virement', 'Virement'),
    ]

    comptefond = models.ForeignKey(
        CompteFondateur,
        on_delete=models.CASCADE,
        related_name='transactions_adhesionkha',
        null=True,
        blank=True
    )

    montant = models.DecimalField(max_digits=10, decimal_places=2)
    type_transaction = models.CharField(max_length=20, choices=TYPE_CHOICES)
    date_transaction = models.DateTimeField(auto_now_add=True)
    agent = models.ForeignKey(Utilisateurs, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        if self.type_transaction == 'Virement':
            return f"{self.type_transaction} de {self.montant} FCFA de {self.comptekha} "
        else:
            return f"{self.type_transaction} de {self.montant} FCFA sur le compte {self.comptekha}"
# __________________________________________________________________________________________________________________________________________________________________________________

# COMPTE PORTEFEUILLE _____________________________________________________________________________________________________________________________________________________________________
class ComptePortefeuilles(models.Model):
    totalentree = models.DecimalField(max_digits=10, decimal_places=2, default=0) # type: ignore
    totalsortie = models.DecimalField(max_digits=10, decimal_places=2, default=0) # type: ignore
    totalreste = models.DecimalField(max_digits=10, decimal_places=2, default=0) # type: ignore
    statut = models.ForeignKey(Statuts, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"Aide {self.datesolde} - {self.solde}"
# __________________________________________________________________________________________________________________________________________________________________________________

# COMPTE PRINCIPALE _____________________________________________________________________________________________________________________________________________________________________
class ComptePrincipale(models.Model):
    capital = models.DecimalField(max_digits=10, decimal_places=2, default=0) # type: ignore
    datecapital = models.DateField(auto_now_add=True)
    totalentree = models.DecimalField(max_digits=10, decimal_places=2, default=0) # type: ignore
    dateentree = models.DateField(auto_now_add=True)
    totalsortie = models.DecimalField(max_digits=10, decimal_places=2, default=0) # type: ignore
    datesortie = models.DateField(auto_now_add=True)
    totalgain = models.DecimalField(max_digits=10, decimal_places=2, default=0) # type: ignore
    dategain = models.DateField(auto_now_add=True)
    totaldepenses = models.DecimalField(max_digits=10, decimal_places=2, default=0) # type: ignore
    datedepense = models.DateField(auto_now_add=True)
    statut = models.ForeignKey(Statuts, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"Domicialition {self.datecapital} - {self.capital}"
# __________________________________________________________________________________________________________________________________________________________________________________

# RETRAIT COMMERCIAL __________________________________________________________________________________________________________________________________________________________________________________
class TransactionRetraitcommercial(models.Model):
    TYPE_CHOICES = [
        ('Depot', 'Dépôt'),
        ('Retrait', 'Retrait'),
        ('Virement', 'Virement'),
    ]

    com = models.ForeignKey(
        Commissions,
        on_delete=models.CASCADE,
        related_name='transactions_retraitcom',
        null=True,
        blank=True
    )

    montant = models.DecimalField(max_digits=10, decimal_places=2)
    type_transaction = models.CharField(max_length=20, choices=TYPE_CHOICES)
    date_transaction = models.DateTimeField(auto_now_add=True)
    Motif = models.CharField(max_length=200, null=True)

    def __str__(self):
        if self.type_transaction == 'Virement':
            return f"{self.type_transaction} de {self.montant} FCFA de {self.com} "
        else:
            return f"{self.type_transaction} de {self.montant} FCFA sur le compte {self.com}"
# __________________________________________________________________________________________________________________________________________________________________________________

# RETRAIT COMMERCIAL __________________________________________________________________________________________________________________________________________________________________________________
class TransactionRetraitdemarcheur(models.Model):
    TYPE_CHOICES = [
        ('Depot', 'Dépôt'),
        ('Retrait', 'Retrait'),
        ('Virement', 'Virement'),
    ]

    dem = models.ForeignKey(
        Commissions,
        on_delete=models.CASCADE,
        related_name='transactions_retraitdem',
        null=True,
        blank=True
    )

    montant = models.DecimalField(max_digits=10, decimal_places=2)
    type_transaction = models.CharField(max_length=20, choices=TYPE_CHOICES)
    date_transaction = models.DateTimeField(auto_now_add=True)
    Motif = models.CharField(max_length=200, null=True)

    def __str__(self):
        if self.type_transaction == 'Virement':
            return f"{self.type_transaction} de {self.montant} FCFA de {self.com} "
        else:
            return f"{self.type_transaction} de {self.montant} FCFA sur le compte {self.com}"
# __________________________________________________________________________________________________________________________________________________________________________________

# RETRAIT SPONSOR __________________________________________________________________________________________________________________________________________________________________________________
class TransactionRetraitsponsor(models.Model):
    TYPE_CHOICES = [
        ('Depot', 'Dépôt'),
        ('Retrait', 'Retrait'),
        ('Virement', 'Virement'),
    ]

    gain = models.ForeignKey(
        Sponsors,
        on_delete=models.CASCADE,
        related_name='transactions_retraitgain',
        null=True,
        blank=True
    )

    montant = models.DecimalField(max_digits=10, decimal_places=2)
    type_transaction = models.CharField(max_length=20, choices=TYPE_CHOICES)
    date_transaction = models.DateTimeField(auto_now_add=True)
    Motif = models.CharField(max_length=200, null=True)

    def __str__(self):
        if self.type_transaction == 'Virement':
            return f"{self.type_transaction} de {self.montant} FCFA de {self.com} "
        else:
            return f"{self.type_transaction} de {self.montant} FCFA sur le compte {self.com}"
# __________________________________________________________________________________________________________________________________________________________________________________

# NNNNNNNNNNNNNNNNNNNNN _____________________________________________________________________________________________________________________________________________________________________