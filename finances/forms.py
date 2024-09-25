from datetime import date, timedelta
from decimal import Decimal
from django import forms
from django.shortcuts import render, redirect, get_object_or_404
from finances.views import definir_date_fin_pret
from .models import TransactionAdhesionkha,TransactionFondateur,CompteFondateur, TransactionInteret,TransactionKha,Statuts,TransactionEpargneact, Confconstantes, Sponsors,Presentation, Actionnaire, Depense,Clients,Aides, CompteEpargnes, ComptePrets, Documents, Echeancier,Echeancieract, Rachats, Tontines,TransactionEpargne, TransactionKha, TransactionPenaliteHist, TransactionPret, Agent,Genres, Matrimoniales, TransactionRetraitcommercial, TransactionRetraitdemarcheur, TransactionRetraitsponsor, TransactionRistourne, TransactionTontine, Typeprets, Msg,ComptePretsact

# FORM MATRIMONIALE _________________________________________________________________________________________________________________________________________
class GenreForm(forms.ModelForm):
    class Meta:
        model = Genres
        fields = ['sexe']
#____________________________________________________________________________________________________________________________________________________________


# FORM MATRIMONIALE _________________________________________________________________________________________________________________________________________
class MatrimonialeForm(forms.ModelForm):
    class Meta:
        model = Matrimoniales
        fields = ['matrimoniale']
#_____________________________________________________________________________________________________________________________________________________________

# FORM TYPE PRET _____________________________________________________________________________________________________________________________________________
class TypepretForm(forms.ModelForm):
    class Meta:
        model = Typeprets
        fields = ['type_pret']

class TypePretForm(forms.Form):
    type_pret = forms.ModelChoiceField(queryset=Typeprets.objects.all())
#____________________________________________________________________________________________________________________________________________________________


# FORM CLIENT ________________________________________________________________________________________________________________________________________________
class ClientForm(forms.ModelForm):
    class Meta:
        model = Clients
        fields = ['nom', 'prenom', 'adresse', 'telephone', 'sexe', 'email', 'photo', 'piece_identite_scan',
                  'profession', 'date_naissance', 'lieu_naissance', 'type_piece_identite', 'numero_piece_identite',
                  'validite_piece_identite_debut', 'validite_piece_identite_fin', 'ville_village', 'matrimoniale']
        widgets = {
            'nom': forms.TextInput(attrs={'class':'form-control','placeholder': 'Entrez le nom du client'}),
            'prenom': forms.TextInput(attrs={'class':'form-control','placeholder': 'Entrez le prénom du client'}),
            'telephone': forms.TextInput(attrs={'class':'form-control','placeholder': 'Entrez le numéro de téléphone'}),
            'date_naissance': forms.DateInput(attrs={'class':'form-control docs-date','type': 'date','placeholder': 'Sélectionnez la date de naissance'}),
            'email': forms.EmailInput(attrs={'class':'form-control','placeholder': 'Entrez l\'adresse e-mail'}),
            'adresse': forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Entrez l\'adresse'}),
            'photo': forms.ClearableFileInput(attrs={'class': 'form-control','accept': 'image/*'}),
            'piece_identite_scan': forms.ClearableFileInput(attrs={'class': 'form-control','accept': 'image/*'}),
            'profession': forms.TextInput(attrs={'class':'form-control','placeholder': 'Entrez la profession du client'}),
            'lieu_naissance': forms.TextInput(attrs={'class':'form-control','placeholder': 'Entrez le lieu de naissance'}),
            'type_piece_identite': forms.Select(attrs={'class':'form-select','placeholder': 'Sélectionnez le type de pièce d\'identité'}),
            'numero_piece_identite': forms.TextInput(attrs={'class':'form-control','placeholder': 'Entrez le numéro de pièce d\'identité'}),
            'validite_piece_identite_debut': forms.DateInput(attrs={'class':'form-control docs-date','type': 'date','placeholder': 'Sélectionnez la date de début de validité'}),
            'validite_piece_identite_fin': forms.DateInput(attrs={'class':'form-control docs-date','type': 'date','placeholder': 'Sélectionnez la date de fin de validité'}),
            'ville_village': forms.TextInput(attrs={'class':'form-control','placeholder': 'Entrez la ville ou le village'}),
            'matrimoniale': forms.Select(attrs={'class':'form-select','placeholder': 'Sélectionnez l\'état matrimonial'}),
            'sexe': forms.Select(attrs={'class':'form-select','placeholder': 'Sélectionnez l\'état matrimonial'}),
            
        }
#_________________________________________________________________________________________________________________________________________________________


# FORM COMPTE EPARGNE _________________________________________________________________________________________________________________________________
class CompteEpargneForm(forms.ModelForm):
    class Meta:
        model = CompteEpargnes
        fields = ['client', 'numero_compte', 'solde', 'statut']
#_________________________________________________________________________________________________________________________________________________________


# FORM COMPTE PRET CLIENT _________________________________________________________________________________________________________________________________    
class ComptePretForm(forms.ModelForm):
    class Meta:
        model = ComptePrets
        fields = ['client', 'taux_interet', 'duree_en_mois', 'date_debut_pret', 'somme_initiale', 'domicile_bancaire', 'type_pret', 'type_client','com']
        
        widgets = {
            'client': forms.TextInput(attrs={'class': 'form-control'}),
            'taux_interet': forms.NumberInput(attrs={'class': 'form-control'}),
            'duree_en_mois': forms.NumberInput(attrs={'class': 'form-control'}),
            'date_debut_pret': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'somme_initiale': forms.NumberInput(attrs={'class': 'form-control'}),
            'domicile_bancaire': forms.TextInput(attrs={'class': 'form-control'}),
            'type_pret': forms.Select(attrs={'class': 'form-select'}),
            'type_client': forms.Select(attrs={'class': 'form-select'}),
            'com': forms.Select(attrs={'class': 'form-select'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtrer le champ client pour inclure uniquement les clients sponsorisés
        self.fields['com'].queryset = Agent.objects.filter(type_agent=2)

    def save(self, commit=True):
        compte_pret = super().save(commit=False)
        compte_pret.date_demande = date.today()
        definir_date_fin_pret(compte_pret)
        
        if compte_pret.type_pret_id == 1:  # Prêt avec un compte d'épargne
            montant_interets = compte_pret.calculer_interets()
            compte_pret.solde += montant_interets

        elif compte_pret.type_pret_id == 2:  # Prêt avec versement initial d’une garantie
            garantie = compte_pret.solde
            montant_pret = compte_pret.somme_initiale + compte_pret.calculer_interets()
            compte_pret.solde = garantie + montant_pret

        elif compte_pret.type_pret_id == 3:  # Prêt sans versement initial d'une garantie
            montant_pret = compte_pret.somme_initiale + compte_pret.calculer_interets()
            compte_pret.solde += montant_pret

                
        elif compte_pret.type_pret_id == 4:  # NOUVELLE FORMULE
            montant_interets = compte_pret.calculer_interets()
            compte_pret.solde += montant_interets

        if compte_pret.type_pret_id == 1:  # TYPE DE PRET avec versement d’une garantie
                interets = (compte_pret.somme_initiale * Decimal(compte_pret.taux_interet) * compte_pret.duree_en_mois)/100
        elif compte_pret.type_pret_id == 2:  # TYPE DE PRET sans versement de la garantie au préalable
                interets = ((compte_pret.somme_initiale *Decimal(compte_pret.taux_garantie))+compte_pret.somme_initiale * Decimal(compte_pret.taux_interet) * 10)/100  # 10 mois de remboursement par défaut
        elif compte_pret.type_pret_id == 3:  # TYPE DE PRET le client ayant un compte avec KHA
                interets = (compte_pret.somme_initiale * Decimal(compte_pret.taux_interet) * compte_pret.duree_en_mois)/100
        else:
                interets = 0

        statut_actif = get_object_or_404(Statuts, statut='Actif')
        Conf = Confconstantes.objects.filter(statut=statut_actif).first()
        taux_kha = Conf.partepargne
        taux_khaa = Conf.partfraisdos
        if compte_pret.type_client_id == 1:  # Pour un client avec des échéances chaque semaine
            montant_interet =  interets/(compte_pret.duree_en_mois * 4)
            montant_epargne = (compte_pret.somme_initiale *Decimal(taux_kha)) / (compte_pret.duree_en_mois * 4)
            montant_adhesion = (compte_pret.somme_initiale *Decimal(taux_khaa)) / (compte_pret.duree_en_mois * 4)
            montant_echeance = ((compte_pret.somme_initiale + interets) / (compte_pret.duree_en_mois * 4)) + montant_epargne + montant_adhesion
            
        elif compte_pret.type_client_id == 2:  # Pour un client avec des échéances chaque mois
            montant_interet =  interets/compte_pret.duree_en_mois
            montant_epargne = (compte_pret.somme_initiale *Decimal(taux_kha)) / compte_pret.duree_en_mois
            montant_adhesion = (compte_pret.somme_initiale *Decimal(taux_khaa)) / compte_pret.duree_en_mois
            montant_echeance = ((compte_pret.somme_initiale + interets) / compte_pret.duree_en_mois) + montant_epargne + montant_adhesion
        else:
            montant_epargne = 0
            montant_adhesion = 0

        echeances = compte_pret.calculer_echeances()
        for echeance in echeances:
            Echeancier.objects.create(compte_pret=compte_pret, date_echeance=echeance,
                                       montant_echeance=montant_echeance, montant_interet=montant_interet,
                                       montant_epargne=montant_epargne, montant_adhesion=montant_adhesion)
        
        if commit:
            compte_pret.save()
            
        return compte_pret
#____________________________________________________________________________________________________________________________________________________________


# SPONSOR _______________________________________________________________________________________________________________________________________________________
from django import forms
from datetime import date
from decimal import Decimal
from .models import Contratsponsor, Echeancier

class ContratSponsorForm(forms.ModelForm):
    class Meta:
        model = Contratsponsor
        fields = ['sponsor', 'taux_interet', 'duree_en_mois', 'date_debut_pret', 'somme_initiale', 'domicile_bancaire', 'type_pret', 'type_client', 'nom', 'prenom', 'adresse', 'telephone', 'sexe', 'email', 'photo', 'piece_identite_scan',
                  'profession', 'date_naissance', 'lieu_naissance', 'type_piece_identite', 'numero_piece_identite',
                  'validite_piece_identite_debut', 'validite_piece_identite_fin', 'ville_village', 'matrimoniale','com','duree_contrat']
        
        widgets = {
            'nom': forms.TextInput(attrs={'class':'form-control','placeholder': 'Entrez le nom du client'}),
            'prenom': forms.TextInput(attrs={'class':'form-control','placeholder': 'Entrez le prénom du client'}),
            'telephone': forms.TextInput(attrs={'class':'form-control','placeholder': 'Entrez le numéro de téléphone'}),
            'date_naissance': forms.DateInput(attrs={'class':'form-control docs-date','type': 'date','placeholder': 'Sélectionnez la date de naissance'}),
            'email': forms.EmailInput(attrs={'class':'form-control','placeholder': 'Entrez l\'adresse e-mail'}),
            'adresse': forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Entrez l\'adresse'}),
            'photo': forms.ClearableFileInput(attrs={'class': 'form-control','accept': 'image/*'}),
            'piece_identite_scan': forms.ClearableFileInput(attrs={'class': 'form-control','accept': 'image/*'}),
            'profession': forms.TextInput(attrs={'class':'form-control','placeholder': 'Entrez la profession du client'}),
            'lieu_naissance': forms.TextInput(attrs={'class':'form-control','placeholder': 'Entrez le lieu de naissance'}),
            'type_piece_identite': forms.Select(attrs={'class':'form-select','placeholder': 'Sélectionnez le type de pièce d\'identité'}),
            'numero_piece_identite': forms.TextInput(attrs={'class':'form-control','placeholder': 'Entrez le numéro de pièce d\'identité'}),
            'validite_piece_identite_debut': forms.DateInput(attrs={'class':'form-control docs-date','type': 'date','placeholder': 'Sélectionnez la date de début de validité'}),
            'validite_piece_identite_fin': forms.DateInput(attrs={'class':'form-control docs-date','type': 'date','placeholder': 'Sélectionnez la date de fin de validité'}),
            'ville_village': forms.TextInput(attrs={'class':'form-control','placeholder': 'Entrez la ville ou le village'}),
            'matrimoniale': forms.Select(attrs={'class':'form-select','placeholder': 'Sélectionnez l\'état matrimonial'}),
            'sexe': forms.Select(attrs={'class':'form-select','placeholder': 'Sélectionnez le sexe'}),
            'sponsor': forms.TextInput(attrs={'class': 'form-control'}),
            'taux_interet': forms.NumberInput(attrs={'class': 'form-control'}),
            'duree_en_mois': forms.NumberInput(attrs={'class': 'form-control'}),
            'date_debut_pret': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'somme_initiale': forms.NumberInput(attrs={'class': 'form-control'}),
            'domicile_bancaire': forms.TextInput(attrs={'class': 'form-control'}),
            'type_pret': forms.Select(attrs={'class': 'form-select'}),
            'type_client': forms.Select(attrs={'class': 'form-select'}),
            'com' : forms.Select(attrs={'class': 'form-select'}),
            'duree_contrat': forms.NumberInput(attrs={'class': 'form-control'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtrer le champ client pour inclure uniquement les clients sponsorisés
        self.fields['com'].queryset = Agent.objects.filter(type_agent=2)

    def save(self, commit=True):
        # D'abord, sauvegardez les données du formulaire pour créer l'instance ComptePrets
        compte_pret = super().save(commit=False)
        compte_pret.date_demande = date.today()
        definir_date_fin_pret(compte_pret)
        
        # Calculer les intérêts
        montant_interets = self.calculate_interests(compte_pret)
        compte_pret.solde += montant_interets
        
        # Logique additionnelle en fonction du type de prêt
        if compte_pret.type_pret_id in [1, 3]:
            compte_pret.solde += compte_pret.somme_initiale
        
        if compte_pret.type_pret_id == 2:
            garantie = compte_pret.solde
            montant_pret = compte_pret.somme_initiale + montant_interets
            compte_pret.solde = garantie + montant_pret

        # Calculer les détails des échéances
        montant_echeance, montant_interet, montant_epargne, montant_adhesion = self.calculate_echeance(compte_pret, montant_interets)

# Sauvegarder l'instance de ComptePrets si commit est True
        if commit:
            compte_pret.save()

        return compte_pret

    def calculate_interests(self, compte_pret):
        # Calculating interests based on loan type
        if compte_pret.type_pret_id in [1, 3]:
            return (compte_pret.somme_initiale * Decimal(compte_pret.taux_interet) * compte_pret.duree_en_mois) / 100
        elif compte_pret.type_pret_id == 2:
            return ((compte_pret.somme_initiale * Decimal(compte_pret.taux_garantie)) + compte_pret.somme_initiale * Decimal(compte_pret.taux_interet) * 10) / 100
        elif compte_pret.type_pret_id == 4:
            return (compte_pret.somme_initiale * Decimal(compte_pret.taux_interet) * compte_pret.duree_en_mois) / 100
        return 0

    def calculate_echeance(self, compte_pret, interets):
        statut_actif = get_object_or_404(Statuts, statut='Actif')
        Conf = Confconstantes.objects.filter(statut=statut_actif).first()
        taux_kha = Conf.partepargne
        taux_khaa = Conf.partfraisdos
        if compte_pret.type_client_id == 1:  # Échéances chaque semaine
            montant_interet = interets / (compte_pret.duree_en_mois * 4)
            montant_epargne = (compte_pret.somme_initiale * Decimal(taux_kha)) / (compte_pret.duree_en_mois * 4)
            montant_adhesion = (compte_pret.somme_initiale * Decimal(taux_khaa)) / (compte_pret.duree_en_mois * 4)
            montant_echeance = ((compte_pret.somme_initiale + interets) / (compte_pret.duree_en_mois * 4)) + montant_epargne + montant_adhesion
        elif compte_pret.type_client_id == 2:  # Échéances chaque mois
            montant_interet = interets / compte_pret.duree_en_mois
            montant_epargne = (compte_pret.somme_initiale * Decimal(taux_kha)) / compte_pret.duree_en_mois
            montant_adhesion = (compte_pret.somme_initiale * Decimal(taux_khaa)) / (compte_pret.duree_en_mois * 4)
            montant_echeance = ((compte_pret.somme_initiale + interets) / compte_pret.duree_en_mois) + montant_epargne + montant_adhesion
        else:
            montant_interet = 0
            montant_epargne = 0
            montant_echeance = 0
            montant_adhesion = 0

        return montant_echeance, montant_interet, montant_epargne, montant_adhesion

# Form ancien client ----------------------------------------------------------------------------------------------------------------------
class ContratSponsoracForm(forms.ModelForm):
   
    class Meta:
        model = Contratsponsor
        fields = ['sponsor', 'com','duree_contrat','taux_interet', 'duree_en_mois', 'date_debut_pret', 'somme_initiale', 'domicile_bancaire', 'type_pret', 'type_client', 'client']
        
        widgets = {
            'sponsor': forms.TextInput(attrs={'class': 'form-control'}),
            'taux_interet': forms.NumberInput(attrs={'class': 'form-control'}),
            'duree_en_mois': forms.NumberInput(attrs={'class': 'form-control'}),
            'date_debut_pret': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'somme_initiale': forms.NumberInput(attrs={'class': 'form-control'}),
            'domicile_bancaire': forms.TextInput(attrs={'class': 'form-control'}),
            'type_pret': forms.Select(attrs={'class': 'form-select'}),
            'type_client': forms.Select(attrs={'class': 'form-select'}),
            'client': forms.Select(attrs={'class':'form-select','placeholder': 'Sélectionnez le client'}),
            'com' : forms.Select(attrs={'class': 'form-select'}),
            'duree_contrat': forms.NumberInput(attrs={'class': 'form-control'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtrer le champ client pour inclure uniquement les clients sponsorisés
        self.fields['client'].queryset = Clients.objects.filter(nat_client=3)
        # Filtrer le champ client pour inclure uniquement les clients sponsorisés
        self.fields['com'].queryset = Agent.objects.filter(type_agent=2)    

    def clean(self):
        cleaned_data = super().clean()
        client = cleaned_data.get('client')
        
        # Valider que le client est bien sélectionné
        if client is None:
            raise forms.ValidationError("Veuillez sélectionner un client valide.")
        
        return cleaned_data

    def save(self, commit=True):
        # D'abord, sauvegardez les données du formulaire pour créer l'instance ComptePrets
        compte_pret = super().save(commit=False)
        compte_pret.date_demande = date.today()
        definir_date_fin_pret(compte_pret)
        
        # Calculer les intérêts
        montant_interets = self.calculate_interests(compte_pret)
        compte_pret.solde += montant_interets
        
        # Logique additionnelle en fonction du type de prêt
        if compte_pret.type_pret_id in [1, 3]:
            compte_pret.solde += compte_pret.somme_initiale
        
        if compte_pret.type_pret_id == 2:
            garantie = compte_pret.solde
            montant_pret = compte_pret.somme_initiale + montant_interets
            compte_pret.solde = garantie + montant_pret

        # Calculer les détails des échéances
        montant_echeance, montant_interet, montant_epargne, montant_adhesion = self.calculate_echeance(compte_pret, montant_interets)

# Sauvegarder l'instance de ComptePrets si commit est True
        if commit:
            compte_pret.save()
          
        return compte_pret


    def calculate_interests(self, compte_pret):
        # Calculating interests based on loan type
        if compte_pret.type_pret_id in [1, 3]:
            return (compte_pret.somme_initiale * Decimal(compte_pret.taux_interet) * compte_pret.duree_en_mois) / 100
        elif compte_pret.type_pret_id == 2:
            return ((compte_pret.somme_initiale * Decimal(compte_pret.taux_garantie)) + compte_pret.somme_initiale * Decimal(compte_pret.taux_interet) * 10) / 100
        elif compte_pret.type_pret_id == 4:
            return (compte_pret.somme_initiale * Decimal(compte_pret.taux_interet) * compte_pret.duree_en_mois) / 100
        return 0

    def calculate_echeance(self, compte_pret, interets):
        statut_actif = get_object_or_404(Statuts, statut='Actif')
        Conf = Confconstantes.objects.filter(statut=statut_actif).first()
        taux_kha = Conf.partepargne
        taux_khaa = Conf.partfraisdos
        if compte_pret.type_client_id == 1:  # Échéances chaque semaine
            montant_interet = interets / (compte_pret.duree_en_mois * 4)
            montant_epargne = (compte_pret.somme_initiale * Decimal(taux_kha)) / (compte_pret.duree_en_mois * 4)
            montant_adhesion = (compte_pret.somme_initiale * Decimal(taux_khaa)) / (compte_pret.duree_en_mois * 4)
            montant_echeance = ((compte_pret.somme_initiale + interets) / (compte_pret.duree_en_mois * 4)) + montant_epargne + montant_adhesion
        elif compte_pret.type_client_id == 2:  # Échéances chaque mois
            montant_interet = interets / compte_pret.duree_en_mois
            montant_epargne = (compte_pret.somme_initiale * Decimal(taux_kha)) / compte_pret.duree_en_mois
            montant_adhesion = (compte_pret.somme_initiale * Decimal(taux_khaa)) / (compte_pret.duree_en_mois * 4)
            montant_echeance = ((compte_pret.somme_initiale + interets) / compte_pret.duree_en_mois) + montant_epargne + montant_adhesion
        else:
            montant_interet = 0
            montant_epargne = 0
            montant_echeance = 0
            montant_adhesion = 0

        return montant_echeance, montant_interet, montant_epargne, montant_adhesion
#____________________________________________________________________________________________________________________________________________________________


# AGENT _______________________________________________________________________________________________________________________________________________________
class AgentForm(forms.ModelForm):
    class Meta:
        model = Agent
        fields = ['nom', 'prenom', 'adresse', 'telephone', 'email']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control'}),
            'prenom': forms.TextInput(attrs={'class': 'form-control'}),
            'adresse': forms.TextInput(attrs={'class': 'form-control'}),
            'telephone': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }
#____________________________________________________________________________________________________________________________________________________________


# DEPENSES _______________________________________________________________________________________________________________________________________________________
class DepenseForm(forms.ModelForm):
    class Meta:
        model = Depense
        fields = ['nom', 'montant']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control'}),
            'montant': forms.NumberInput(attrs={'class': 'form-control'}),
            
        }
#____________________________________________________________________________________________________________________________________________________________


# FORM ACTIONNAIRE ACTIF _________________________________________________________________________________________________________________________________
class ActionnaireForm(forms.ModelForm):
    class Meta:
        model = Actionnaire
        fields = ['nom', 'prenom', 'adresse', 'telephone', 'email', 'apport', 'com']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control'}),
            'prenom': forms.TextInput(attrs={'class': 'form-control'}),
            'adresse': forms.TextInput(attrs={'class': 'form-control'}),
            'telephone': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'com': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtrer le champ 'com' pour inclure uniquement les agents sponsorisés (type_agent = 2)
        self.fields['com'].queryset = Agent.objects.filter(type_agent=3)
        # Ajouter des widgets personnalisés pour le champ 'apport'
        self.fields['apport'].widget = forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': "Entrez l'apport"}
        )
#_________________________________________________________________________________________________________________________________________________________


# FORM ACTIONNAIRE PASSIF _________________________________________________________________________________________________________________________________
class ActionnairenForm(forms.ModelForm):
    class Meta:
        model = Actionnaire
        fields = ['nom', 'prenom', 'adresse', 'telephone', 'email', 'apport', 'com']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control'}),
            'prenom': forms.TextInput(attrs={'class': 'form-control'}),
            'adresse': forms.TextInput(attrs={'class': 'form-control'}),
            'telephone': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'com': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtrer le champ 'com' pour inclure uniquement les agents sponsorisés (type_agent = 2)
        self.fields['com'].queryset = Agent.objects.filter(type_agent=2)
        # Ajouter des widgets personnalisés pour le champ 'apport'
        self.fields['apport'].widget = forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': "Entrez l'apport"}
        )

#_________________________________________________________________________________________________________________________________________________________


# FORM SPONSOR _________________________________________________________________________________________________________________________________
class SponsorForm(forms.ModelForm):
    class Meta:
        model = Sponsors
        fields = ['nom', 'prenom', 'adresse', 'telephone', 'email','pourcentage']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control'}),
            'prenom': forms.TextInput(attrs={'class': 'form-control'}),
            'adresse': forms.TextInput(attrs={'class': 'form-control'}), 
            'telephone': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'pourcentage': forms.NumberInput(attrs={'class': 'form-control'}),
        }    
#_________________________________________________________________________________________________________________________________________________________


# FORM TRANSACTION EPARGNE _________________________________________________________________________________________________________________________________
class TransactionEpargneForm(forms.ModelForm):
    class Meta:
        model = TransactionEpargne
        fields = ['compte_epargne', 'montant', 'type_transaction']
        widgets = {
            'type_transaction': forms.Select(attrs={'class': 'form-select'}),
            'montant': forms.NumberInput(attrs={'class': 'form-control'}),
            'compte_epargne': forms.TextInput(attrs={'class':'form-control'} ),
        }
#_________________________________________________________________________________________________________________________________________________________


# FORM TRANSACTION EPARGNE _________________________________________________________________________________________________________________________________
class TransactionEpargneactForm(forms.ModelForm):
    class Meta:
        model = TransactionEpargneact
        fields = ['compte_epargne', 'montant', 'type_transaction']
        widgets = {
            'type_transaction': forms.Select(attrs={'class': 'form-select'}),
            'montant': forms.NumberInput(attrs={'class': 'form-control'}),
            'compte_epargne': forms.TextInput(attrs={'class':'form-control'} ),
        }
#_________________________________________________________________________________________________________________________________________________________

# FORM TRANSACTION PRET _________________________________________________________________________________________________________________________________        
class TransactionPretForm(forms.ModelForm):
    class Meta:
        model = TransactionPret
        fields = ['type_transaction', 'montant', 'compte_pret']

        widgets = {
            'type_transaction': forms.Select(attrs={'class': 'form-select'}),
            'montant': forms.NumberInput(attrs={'class': 'form-control'}),
            'compte_pret': forms.Select(attrs={'class': 'form-select'}),
        }
#_________________________________________________________________________________________________________________________________________________________


# FORM MESSAGE _________________________________________________________________________________________________________________________________
class MessagesForm(forms.ModelForm):
    class Meta:
        model = Msg
        fields = ['titre', 'message']
        widgets = {
            'titre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Sujet'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Message'}),
        }
#_________________________________________________________________________________________________________________________________________________________


# FORM COMPTE PRET ACTIONNAIRE _________________________________________________________________________________________________________________________________
class ComptePretactForm(forms.ModelForm):
    class Meta:
        model = ComptePretsact
        fields = ['actionnaire', 'taux_interet', 'duree_en_mois', 'date_debut_pret', 'somme_initiale', 'domicile_bancaire', 'type_pret','type_client','com']
        
        widgets = {
            'actionnaire': forms.TextInput(attrs={'class': 'form-control'}),
            'taux_interet': forms.NumberInput(attrs={'class': 'form-control'}),
            'duree_en_mois': forms.NumberInput(attrs={'class': 'form-control'}),
            'date_debut_pret': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'somme_initiale': forms.NumberInput(attrs={'class': 'form-control'}),
            'domicile_bancaire': forms.TextInput(attrs={'class': 'form-control'}),
            'type_pret': forms.Select(attrs={'class': 'form-select'}),
            'type_client': forms.Select(attrs={'class': 'form-select'}),
            'com': forms.Select(attrs={'class': 'form-select'}),
           
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtrer le champ client pour inclure uniquement les clients sponsorisés
        self.fields['com'].queryset = Agent.objects.filter(type_agent=2)
#_________________________________________________________________________________________________________________________________________________________


# FORM AIDE _________________________________________________________________________________________________________________________________
class AideForm(forms.ModelForm):
    class Meta:
        model = Aides
        fields = ['client', 'montant_aide']  
        widgets = {
            'montant_aide': forms.NumberInput(attrs={'class': 'form-control'}), 
            'client': forms.Select(attrs={'class': 'form-select'}),
        }
#_________________________________________________________________________________________________________________________________________________________


# FORM TONTINE _________________________________________________________________________________________________________________________________
class TontineForm(forms.ModelForm):
    class Meta:
        model = Tontines
        fields = ['client', 'numero_tontine', 'solde', 'cotite', 'statut', 'agent', 'nbreaide', 'dateaide', 'montant_aide']

class TontineAForm(forms.ModelForm):
    class Meta:
        model = Tontines
        fields = ['client','type_tontine','montant_min','com',]
        widgets = {
            'client': forms.TextInput(attrs={'class': 'form-control'}),
            'montant_min': forms.NumberInput(attrs={'class': 'form-control'}),
            'type_tontine': forms.Select(attrs={'class': 'form-select'}),
            'com': forms.Select(attrs={'class': 'form-select'}),
           
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtrer le champ client pour inclure uniquement les clients sponsorisés
        self.fields['com'].queryset = Agent.objects.filter(type_agent=2)
#_________________________________________________________________________________________________________________________________________________________


# FORM TRANSACTION TONTINE _________________________________________________________________________________________________________________________________
class TransactionTontineForm(forms.ModelForm):
    class Meta:
        model = TransactionTontine
        fields = ['tontine', 'montant']
        widgets = {
            'montant': forms.NumberInput(attrs={'class': 'form-control'}), 
            'tontine': forms.Select(attrs={'class': 'form-select'}),
        }
#_________________________________________________________________________________________________________________________________________________________


# FORM RACHAT DE PRET CLIENT _________________________________________________________________________________________________________________________________
class RachatForm(forms.ModelForm):
    class Meta:
        model = Rachats
        fields = ['client', 'compte_pretactuel', 'montant_actuel', 'reste_actuel',  'montant_new']

class CompteRaPretForm(forms.ModelForm):
    class Meta:
        model = ComptePrets
        fields = ['client', 'com','taux_interet', 'duree_en_mois', 'date_debut_pret', 'somme_initiale', 'domicile_bancaire', 'type_pret', 'type_client','statut']
        
        widgets = {
            'client': forms.TextInput(attrs={'class': 'form-control'}),
            'taux_interet': forms.NumberInput(attrs={'class': 'form-control'}),
            'duree_en_mois': forms.NumberInput(attrs={'class': 'form-control'}),
            'date_debut_pret': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'somme_initiale': forms.NumberInput(attrs={'class': 'form-control'}),
            'domicile_bancaire': forms.TextInput(attrs={'class': 'form-control'}),
            'type_pret': forms.Select(attrs={'class': 'form-select'}),
            'type_client': forms.Select(attrs={'class': 'form-select'}),
            'statut': forms.Select(attrs={'class': 'form-select'}),
            'com': forms.Select(attrs={'class': 'form-select'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtrer le champ client pour inclure uniquement les clients sponsorisés
        self.fields['com'].queryset = Agent.objects.filter(type_agent=2)

    def save(self, commit=True):
        compte_pret = super().save(commit=False)
        compte_pret.date_demande = date.today()
        definir_date_fin_pret(compte_pret)
        
        if compte_pret.type_pret_id == 1:  # Prêt avec un compte d'épargne
            montant_interets = compte_pret.calculer_interets()
            compte_pret.solde += montant_interets

        elif compte_pret.type_pret_id == 2:  # Prêt avec versement initial d’une garantie
            garantie = compte_pret.solde
            montant_pret = compte_pret.somme_initiale + compte_pret.calculer_interets()
            compte_pret.solde = garantie + montant_pret

        elif compte_pret.type_pret_id == 3:  # Prêt sans versement initial d'une garantie
            montant_pret = compte_pret.somme_initiale + compte_pret.calculer_interets()
            compte_pret.solde += montant_pret

                
        elif compte_pret.type_pret_id == 4:  # NOUVELLE FORMULE
            montant_interets = compte_pret.calculer_interets()
            compte_pret.solde += montant_interets

        if compte_pret.type_pret_id == 1:  # TYPE DE PRET avec versement d’une garantie
                interets = (compte_pret.somme_initiale * Decimal(compte_pret.taux_interet) * compte_pret.duree_en_mois)/100
        elif compte_pret.type_pret_id == 2:  # TYPE DE PRET sans versement de la garantie au préalable
                interets = ((compte_pret.somme_initiale *Decimal(compte_pret.taux_garantie))+compte_pret.somme_initiale * Decimal(compte_pret.taux_interet) * 10)/100  # 10 mois de remboursement par défaut
        elif compte_pret.type_pret_id == 3:  # TYPE DE PRET le client ayant un compte avec KHA
                interets = (compte_pret.somme_initiale * Decimal(compte_pret.taux_interet) * compte_pret.duree_en_mois)/100
        else:
                interets = 0
        # Calculer et enregistrer les dates d'échéance
        #montant_interet =  interets/compte_pret.duree_en_mois
        #montant_echeance = (compte_pret.somme_initiale + interets) / compte_pret.duree_en_mois

                #API___ Juillet 2
        statut_actif = get_object_or_404(Statuts, statut='Actif')
        Conf = Confconstantes.objects.filter(statut=statut_actif).first()
        taux_kha = Conf.partepargne
        taux_khaa = Conf.partfraisdos
        if compte_pret.type_client_id == 1:  # Pour un client avec des échéances chaque semaine
            montant_interet =  interets/(compte_pret.duree_en_mois * 4)
            montant_epargne = (compte_pret.somme_initiale *Decimal(taux_kha)) / (compte_pret.duree_en_mois * 4)
            montant_adhesion = (compte_pret.somme_initiale *Decimal(taux_khaa)) / (compte_pret.duree_en_mois * 4)
            montant_echeance = ((compte_pret.somme_initiale + interets) / (compte_pret.duree_en_mois * 4)) + montant_epargne + montant_adhesion
            
        elif compte_pret.type_client_id == 2:  # Pour un client avec des échéances chaque mois
            montant_interet =  interets/compte_pret.duree_en_mois
            montant_epargne = (compte_pret.somme_initiale *Decimal(taux_kha)) / compte_pret.duree_en_mois
            montant_adhesion = (compte_pret.somme_initiale *Decimal(taux_khaa)) / compte_pret.duree_en_mois
            montant_echeance = ((compte_pret.somme_initiale + interets) / compte_pret.duree_en_mois) + montant_epargne + montant_adhesion
        else:
            montant_epargne = 0
            montant_adhesion = 0

        echeances = compte_pret.calculer_echeances()
        for echeance in echeances:
            Echeancier.objects.create(compte_pret=compte_pret, date_echeance=echeance,
                                       montant_echeance=montant_echeance, montant_interet=montant_interet,
                                       montant_epargne=montant_epargne, montant_adhesion=montant_adhesion)
        
        if commit:
            compte_pret.save()
            
        return compte_pret
#_________________________________________________________________________________________________________________________________________________________
class CompteRaPretFormact(forms.ModelForm):
    class Meta:
        model = ComptePretsact
        fields = ['actionnaire', 'com','taux_interet', 'duree_en_mois', 'date_debut_pret', 'somme_initiale', 'domicile_bancaire', 'type_pret', 'type_client','statut']
        
        widgets = {
            'actionnaire': forms.TextInput(attrs={'class': 'form-control'}),
            'taux_interet': forms.NumberInput(attrs={'class': 'form-control'}),
            'duree_en_mois': forms.NumberInput(attrs={'class': 'form-control'}),
            'date_debut_pret': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'somme_initiale': forms.NumberInput(attrs={'class': 'form-control'}),
            'domicile_bancaire': forms.TextInput(attrs={'class': 'form-control'}),
            'type_pret': forms.Select(attrs={'class': 'form-select'}),
            'type_client': forms.Select(attrs={'class': 'form-select'}),
            'statut': forms.Select(attrs={'class': 'form-select'}),
            'com': forms.Select(attrs={'class': 'form-select'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtrer le champ client pour inclure uniquement les clients sponsorisés
        self.fields['com'].queryset = Agent.objects.filter(type_agent=2)

    def save(self, commit=True):
        compte_pret = super().save(commit=False)
        compte_pret.date_demande = date.today()
        definir_date_fin_pret(compte_pret)
        
        if compte_pret.type_pret_id == 1:  # Prêt avec un compte d'épargne
            montant_interets = compte_pret.calculer_interets()
            compte_pret.solde += montant_interets

        elif compte_pret.type_pret_id == 2:  # Prêt avec versement initial d’une garantie
            garantie = compte_pret.solde
            montant_pret = compte_pret.somme_initiale + compte_pret.calculer_interets()
            compte_pret.solde = garantie + montant_pret

        elif compte_pret.type_pret_id == 3:  # Prêt sans versement initial d'une garantie
            montant_pret = compte_pret.somme_initiale + compte_pret.calculer_interets()
            compte_pret.solde += montant_pret

                
        elif compte_pret.type_pret_id == 4:  # NOUVELLE FORMULE
            montant_interets = compte_pret.calculer_interets()
            compte_pret.solde += montant_interets

        if compte_pret.type_pret_id == 1:  # TYPE DE PRET avec versement d’une garantie
                interets = (compte_pret.somme_initiale * Decimal(compte_pret.taux_interet) * compte_pret.duree_en_mois)/100
        elif compte_pret.type_pret_id == 2:  # TYPE DE PRET sans versement de la garantie au préalable
                interets = ((compte_pret.somme_initiale *Decimal(compte_pret.taux_garantie))+compte_pret.somme_initiale * Decimal(compte_pret.taux_interet) * 10)/100  # 10 mois de remboursement par défaut
        elif compte_pret.type_pret_id == 3:  # TYPE DE PRET le client ayant un compte avec KHA
                interets = (compte_pret.somme_initiale * Decimal(compte_pret.taux_interet) * compte_pret.duree_en_mois)/100
        else:
                interets = 0
        # Calculer et enregistrer les dates d'échéance
        #montant_interet =  interets/compte_pret.duree_en_mois
        #montant_echeance = (compte_pret.somme_initiale + interets) / compte_pret.duree_en_mois

                #API___ Juillet 2
        statut_actif = get_object_or_404(Statuts, statut='Actif')
        Conf = Confconstantes.objects.filter(statut=statut_actif).first()
        taux_kha = Conf.partepargne
        taux_khaa = Conf.partfraisdos
        if compte_pret.type_client_id == 1:  # Pour un client avec des échéances chaque semaine
            montant_interet =  interets/(compte_pret.duree_en_mois * 4)
            montant_epargne = (compte_pret.somme_initiale *Decimal(taux_kha)) / (compte_pret.duree_en_mois * 4)
            montant_adhesion = (compte_pret.somme_initiale *Decimal(taux_khaa)) / (compte_pret.duree_en_mois * 4)
            montant_echeance = ((compte_pret.somme_initiale + interets) / (compte_pret.duree_en_mois * 4)) + montant_epargne + montant_adhesion
            
        elif compte_pret.type_client_id == 2:  # Pour un client avec des échéances chaque mois
            montant_interet =  interets/compte_pret.duree_en_mois
            montant_epargne = (compte_pret.somme_initiale *Decimal(taux_kha)) / compte_pret.duree_en_mois
            montant_adhesion = (compte_pret.somme_initiale *Decimal(taux_khaa)) / compte_pret.duree_en_mois
            montant_echeance = ((compte_pret.somme_initiale + interets) / compte_pret.duree_en_mois) + montant_epargne + montant_adhesion
        else:
            montant_epargne = 0
            montant_adhesion = 0

        echeances = compte_pret.calculer_echeances()
        for echeance in echeances:
            Echeancier.objects.create(compte_pret=compte_pret, date_echeance=echeance,
                                       montant_echeance=montant_echeance, montant_interet=montant_interet,
                                       montant_epargne=montant_epargne, montant_adhesion=montant_adhesion)
        
        if commit:
            compte_pret.save()
            
        return compte_pret
#_________________________________________________________________________________________________________________________________________________________

# FORM DOCUMENT _________________________________________________________________________________________________________________________________
class DocumentForm(forms.ModelForm):
    class Meta:
        model = Documents
        fields = ['Title', 'File','Typedoc']
        widgets = {
            'Title':forms.TextInput(attrs={'class':'form-control','placeholder': 'Titre'} ),
            'File': forms.FileInput(attrs={'class': 'form-control','type':'file'}),
            'Typedoc' : forms.Select(attrs={'class':'form-select'} ),
            } 
#_________________________________________________________________________________________________________________________________________________________


# FORM PRESENTATION _________________________________________________________________________________________________________________________________
class PresentationForm(forms.ModelForm):
    class Meta:
        model = Presentation
        fields = [
            'logo', 'contact','presentation_text','welcome_message','video_url','pub'
        ]

        widgets = {
            'logo': forms.FileInput(attrs={'class': 'form-control','type':'file'}),
            'pub': forms.FileInput(attrs={'class': 'form-control','type':'file'}),
            'contact': forms.TextInput(attrs={'class':'form-control','placeholder': 'Entrez le contact'}),
            'presentation_text': forms.TextInput(attrs={'class':'form-control','placeholder': 'Entrez la presentation'}),
            'welcome_message': forms.TextInput(attrs={'class':'form-control','placeholder': 'Entrez le message de bienvenue'}),
            'video_url': forms.FileInput(attrs={'class': 'form-control','placeholder': 'Entrez l\'URL de la vidéo'}),
        }
#_________________________________________________________________________________________________________________________________________________________


# FORM TRANSACTION CPTE KHA RETRAIT _________________________________________________________________________________________________________________________________
class TransactionretraitcptekhaForm(forms.ModelForm):
    class Meta:
        model = TransactionKha
        fields = ['montant']
        widgets = {
            'montant': forms.NumberInput(attrs={'class': 'form-control'})
        }
#_________________________________________________________________________________________________________________________________________________________

# FORM TRANSACTION CPTE ADHESION RETRAIT _________________________________________________________________________________________________________________________________
class TransactionretraitcpteadhForm(forms.ModelForm):
    class Meta:
        model = TransactionAdhesionkha
        fields = ['montant']
        widgets = {
            'montant': forms.NumberInput(attrs={'class': 'form-control'})
        }
#_________________________________________________________________________________________________________________________________________________________

# FORM TRANSACTION FONDATEUR KHA RETRAIT _________________________________________________________________________________________________________________________________
class TransactionretraitcptefondForm(forms.ModelForm):
    class Meta:
        model = TransactionFondateur
        fields = ['montant']
        widgets = {
            'montant': forms.NumberInput(attrs={'class': 'form-control'})
        }
#_________________________________________________________________________________________________________________________________________________________

# FORM TRANSACTION INTERET RETRAIT _________________________________________________________________________________________________________________________________
class TransactionretraitcpteintForm(forms.ModelForm):
    class Meta:
        model = TransactionInteret
        fields = ['montant']
        widgets = {
            'montant': forms.NumberInput(attrs={'class': 'form-control'})
        }
#_________________________________________________________________________________________________________________________________________________________

# FORM TRANSACTION INTERET RETRAIT _________________________________________________________________________________________________________________________________
class TransactionretraitcptepenForm(forms.ModelForm):
    class Meta:
        model = TransactionPenaliteHist
        fields = ['montant']
        widgets = {
            'montant': forms.NumberInput(attrs={'class': 'form-control'})
        }
#_________________________________________________________________________________________________________________________________________________________

# FORM TRANSACTION COM RETRAIT _________________________________________________________________________________________________________________________________
class TransactionretraitcomForm(forms.ModelForm):
    class Meta:
        model = TransactionRetraitcommercial
        fields = ['montant','Motif']
        widgets = {
            'montant': forms.NumberInput(attrs={'class': 'form-control'}),
            'Motif': forms.TextInput(attrs={'class':'form-control','placeholder': 'Entrez le motif'}),
        }
#_________________________________________________________________________________________________________________________________________________________

# FORM TRANSACTION COMPTE COOPERATEUR _________________________________________________________________________________________________________________________________
class TransactionretraitactForm(forms.ModelForm):
    class Meta:
        model = TransactionRistourne
        fields = ['montant']
        widgets = {
            'montant': forms.NumberInput(attrs={'class': 'form-control'}),
        }
#_________________________________________________________________________________________________________________________________________________________

# FORM TRANSACTION DEM RETRAIT _________________________________________________________________________________________________________________________________
class TransactionretraitdemForm(forms.ModelForm):
    class Meta:
        model = TransactionRetraitdemarcheur
        fields = ['montant','Motif']
        widgets = {
            'montant': forms.NumberInput(attrs={'class': 'form-control'}),
            'Motif': forms.TextInput(attrs={'class':'form-control','placeholder': 'Entrez le motif'}),
        }
#_________________________________________________________________________________________________________________________________________________________

# FORM TRANSACTION SPONSOR DIV RETRAIT _________________________________________________________________________________________________________________________________
class TransactionretraitspoForm(forms.ModelForm):
    class Meta:
        model = TransactionRetraitsponsor
        fields = ['montant','Motif']
        widgets = {
            'montant': forms.NumberInput(attrs={'class': 'form-control'}),
            'Motif': forms.TextInput(attrs={'class':'form-control','placeholder': 'Entrez le motif'}),
        }
#_________________________________________________________________________________________________________________________________________________________

# :::::::::::::::::::::: _________________________________________________________________________________________________________________________________
from django import forms
from .models import Confconstantes

class Confconstantes1Form(forms.ModelForm):
    class Meta:
        model = Confconstantes
        fields = [
            'partrespo', 'partactif', 'partnonactif', 'partpalierun', 'partpalierd', 'partparliert', 
            'partparlierq', 'partparlierc', 'partfraisdos', 'partfraisdossous', 'partcom', 'partpenalite',
            'partepargne', 'partepargnesous', 'partdemarch', 'statut', 'dureecoopa', 'dureecoopn', 
            'partprelev'
        ]

from django import forms
from .models import Confconstantes
from .models import Statuts  # Assuming 'Statuts' is the model used for 'statut' field

class ConfconstantesForm(forms.ModelForm):
    class Meta:
        model = Confconstantes
        fields = [
            'partrespo', 'partactif', 'partnonactif', 'partpalierun', 'partpalierd', 
            'partparliert', 'partparlierq', 'partparlierc', 'partfraisdos', 
            'partfraisdossous', 'partcom', 'partpenalite', 'partepargne', 
            'partepargnesous', 'partdemarch', 'dureecoopa', 'dureecoopn', 
            'partprelev'
        ]
        
