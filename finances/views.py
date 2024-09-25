from django.urls import reverse
from decimal import Decimal
from datetime import date, timedelta, datetime
from django.db.models import F
from django.http import FileResponse, Http404, HttpResponse, JsonResponse
from sympy import Q
from .utils import definir_date_fin_pret
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import CompteInterets, ComptePenalites, ComptePortefeuilles, ComptePrincipale, TransactionCommissionpretact, TransactionFondateur, TransactionInteret,TransactionKha, TransactionPenaliteHist, TransactionRetraitcommercial, TransactionRetraitdemarcheur, TransactionRetraitsponsor,Typetontines,TransactionAdhesionkha,CompteAdhesionkhas,CompteFondateur,Confconstantes,Contratsponsor,Natclients,Sponsors, Presentation, Actionnaire, Aides, CompteEpargnesact,Depense, Documents, Echeancier,Echeancieract,ComptePretsact,CompteKha, Rachats, TransactionEpargneact,TransactionKha,TransactionCommissionpret,Commissions, Msg, Statuts, TransactionPenaliteact, Typedocuments, Utilisateurs, Clients, CompteEpargnes, ComptePrets,TransactionEpargne, TransactionPretact,TransactionPret, Genres, Matrimoniales, Typeprets, Agent
from .forms import CompteRaPretFormact, TransactionretraitactForm, TransactionretraitcomForm, TransactionretraitcpteadhForm,TransactionretraitcptefondForm, TransactionretraitcpteintForm,TransactionretraitcptekhaForm,TontineAForm,TransactionEpargneactForm, ActionnairenForm, ContratSponsoracForm,ContratSponsorForm,SponsorForm,PresentationForm,ActionnaireForm, CompteRaPretForm, DocumentForm,MessagesForm,ClientForm, CompteEpargneForm,ComptePretactForm,  ComptePretForm, DepenseForm, RachatForm, TontineForm, TransactionEpargneForm, GenreForm, MatrimonialeForm, TransactionPretForm, TransactionTontineForm, TransactionretraitcptekhaForm, TransactionretraitcptepenForm, TransactionretraitdemForm, TransactionretraitspoForm, TypePretForm, TypepretForm, AgentForm
from django.contrib.auth import login , logout , authenticate
from django.views.generic import ListView
from django.db.models.signals import post_save,pre_save
from django.dispatch import receiver
from datetime import date
from dateutil.relativedelta import relativedelta
from django.contrib.auth.hashers import make_password
from django.db.models import Sum
from django.utils import timezone
import pandas as pd
from django.views import View
from .serializers import (ActionnaireSerializer, PresentationSerializer)
from django.shortcuts import render

#API___ Juillet 2
from .models import Typeactionnaire,Typeagent,Tontines,TransactionCommissioninves,TransactionPenalite,TransactionRistourne,TransactionTontine
from django.db import transaction
#API___ Juillet 2

def custom_404_view(request, exception):
    return render(request, '404/404.html', status=404)



def menu(request):
    context = {
    }  
    return render(request, 'Pages/Log/menu.html', context)


class CandidateListView(ListView):
    model = Clients
    template_name = 'Pages/Client/liste_candidates.html'
    context_object_name = 'clients'
    paginate_by = 10

    def get_queryset(self):
        query = self.request.GET.get('search')
        if query:
            return Clients.objects.filter(nom__icontains=query)
        return Clients.objects.all()

# GENRES-____________________________________________________________________________________________________________________________________________
# Vue pour la liste des genres
@login_required(login_url='/accounts/')
def liste_genres(request):
    genres = Genres.objects.all()
    return render(request, 'Pages/Genre/liste_genres.html', {'genres': genres})

# Vue pour créer un genre
@login_required(login_url='/accounts/')
def creer_genre(request):
    if request.method == 'POST':
        genre_form = GenreForm(request.POST)
        if genre_form.is_valid():
            genre_form.save()
            return redirect('liste_genres')
    else:
        genre_form = GenreForm()
    return render(request, 'Pages/Genre/creer_genre.html', {'genre_form': genre_form})

# Vue pour modifier un genre
def modifier_genre(request, pk):
    genre = get_object_or_404(Genres, pk=pk)
    if request.method == 'POST':
        genre_form = GenreForm(request.POST, instance=genre)
        if genre_form.is_valid():
            genre_form.save()
            return redirect('liste_genres')
    else:
        genre_form = GenreForm(instance=genre)
    return render(request, 'Pages/Genre/modifier_genre.html', {'genre_form': genre_form, 'genre': genre})

# Vue pour supprimer un genre
def supprimer_genre(request, pk):
    genre = get_object_or_404(Genres, pk=pk)
    if request.method == 'POST':
        genre.delete()
        return redirect('liste_genres')
    return render(request, 'Pages/Genre/supprimer_genre.html', {'genre': genre})

# MATRIMONIALES______________________________________________________________________________________________________________________________________
# Vue pour la liste des matrimoniales
def liste_matrimoniales(request):
    matrimoniales = Matrimoniales.objects.all()
    return render(request, 'Pages/Matrimoniale/liste_matrimoniales.html', {'matrimoniales': matrimoniales})

# Vue pour créer une matrimoniale
def creer_matrimoniale(request):
    if request.method == 'POST':
        matrimoniale_form = MatrimonialeForm(request.POST)
        if matrimoniale_form.is_valid():
            matrimoniale_form.save()
            return redirect('liste_matrimoniales')
    else:
        matrimoniale_form = MatrimonialeForm()
    return render(request, 'Pages/Matrimoniale/creer_matrimoniale.html', {'matrimoniale_form': matrimoniale_form})

# Vue pour modifier une matrimoniale
def modifier_matrimoniale(request, pk):
    matrimoniale = get_object_or_404(Matrimoniales, pk=pk)
    if request.method == 'POST':
        matrimoniale_form = MatrimonialeForm(request.POST, instance=matrimoniale)
        if matrimoniale_form.is_valid():
            matrimoniale_form.save()
            return redirect('liste_matrimoniales')
    else:
        matrimoniale_form = MatrimonialeForm(instance=matrimoniale)
    return render(request, 'Pages/Matrimoniale/modifier_matrimoniale.html', {'matrimoniale_form': matrimoniale_form, 'matrimoniale': matrimoniale})

# Vue pour supprimer une matrimoniale
def supprimer_matrimoniale(request, pk):
    matrimoniale = get_object_or_404(Matrimoniales, pk=pk)
    if request.method == 'POST':
        matrimoniale.delete()
        return redirect('liste_matrimoniales')
    return render(request, 'Pages/Matrimoniale/supprimer_matrimoniale.html', {'matrimoniale': matrimoniale})

# TYPEPRETS ____________________________________________________________________________________________________________________________________________________
# Vue pour la liste des types de prêts
def liste_typeprets(request):
    typeprets = Typeprets.objects.all()
    return render(request, 'liste_typeprets.html', {'typeprets': typeprets})

# Vue pour créer un type de prêt
def creer_typepret(request):
    if request.method == 'POST':
        typepret_form = TypepretForm(request.POST)
        if typepret_form.is_valid():
            typepret_form.save()
            return redirect('liste_typeprets')
    else:
        typepret_form = TypepretForm()
    return render(request, 'creer_typepret.html', {'typepret_form': typepret_form})

# Vue pour modifier un type de prêt
def modifier_typepret(request, pk):
    typepret = get_object_or_404(Typeprets, pk=pk)
    if request.method == 'POST':
        typepret_form = TypepretForm(request.POST, instance=typepret)
        if typepret_form.is_valid():
            typepret_form.save()
            return redirect('liste_typeprets')
    else:
        typepret_form = TypepretForm(instance=typepret)
    return render(request, 'modifier_typepret.html', {'typepret_form': typepret_form, 'typepret': typepret})

# Vue pour supprimer un type de prêt
def supprimer_typepret(request, pk):
    typepret = get_object_or_404(Typeprets, pk=pk)
    if request.method == 'POST':
        typepret.delete()
        return redirect('liste_typeprets')
    return render(request, 'supprimer_typepret.html', {'typepret': typepret})

# AGENTS_____________________________________________________________________________________________________________________________________________________
def liste_agentstout(request):
    typeag = Typeagent.objects.get(type_agent='Administrateur')
    agents = Agent.objects.filter(type_agent=typeag)
    return render(request, 'Pages/Agent/liste_agentstout.html', {'agents': agents})

def liste_agentcons(request):
    typeag = Typeagent.objects.get(type_agent='Conseiller')
    agents = Agent.objects.filter(type_agent=typeag)
    return render(request, 'Pages/Agent/liste_agentscons.html', {'agents': agents})

def liste_agents(request):
    typeag = Typeagent.objects.get(type_agent='Assistant')
    agents = Agent.objects.filter(type_agent=typeag)
    return render(request, 'Pages/Agent/liste_agents.html', {'agents': agents})

def liste_com(request):
    typeag = Typeagent.objects.get(type_agent='Commercial')
    agents = Agent.objects.filter(type_agent=typeag)
    return render(request, 'Pages/Agent/liste_com.html', {'agents': agents})

def liste_dem(request):
    typeag = Typeagent.objects.get(type_agent='Démarcheur')
    agents = Agent.objects.filter(type_agent=typeag)
    return render(request, 'Pages/Agent/liste_demarcheur.html', {'agents': agents})


def ajouter_agent(request):
    if request.method == 'POST':
        agent_form = AgentForm(request.POST, request.FILES)
        
        if agent_form.is_valid():
            with transaction.atomic():
                # Assigner le type d'agent commercial
                statut_actif = Typeagent.objects.get(type_agent='Assistant')
                agent_form.instance.type_agent = statut_actif
                
                # Créer un utilisateur avec le même nom d'utilisateur et mot de passe que l'agent 
                userna = agent_form.cleaned_data['nom']
                usernam = agent_form.cleaned_data['prenom']
                FString = agent_form.cleaned_data['telephone']
                username = FString
                role = "ASSISTANT"
                statu = 'Personnel'
                password = 'P@ssword'
                encoded_password = make_password(password)
                email = agent_form.cleaned_data['email']
                
                user = Utilisateurs.objects.create(
                    statut=statu,
                    username=username,
                    last_name=usernam,
                    first_name=userna,
                    password=encoded_password,
                    email=email,
                    role=role
                )
                
                agent = agent_form.save(commit=False)
                agent.user = user
                agent.save()
                
                return redirect('liste_agents')
    else:
        agent_form = AgentForm()
    
    return render(request, 'Pages/Agent/ajouter_agent.html', {'agent_form': agent_form})

def ajouter_agentcons(request):
    if request.method == 'POST':
        agent_form = AgentForm(request.POST, request.FILES)
        
        if agent_form.is_valid():
            with transaction.atomic():
                # Assigner le type d'agent commercial
                statut_actif = Typeagent.objects.get(type_agent='Conseiller')
                agent_form.instance.type_agent = statut_actif
                
                # Créer un utilisateur avec le même nom d'utilisateur et mot de passe que l'agent 
                userna = agent_form.cleaned_data['nom']
                usernam = agent_form.cleaned_data['prenom']
                FString = agent_form.cleaned_data['telephone']
                username = FString
                role = "CONSEILLER"
                statu = 'Personnel'
                password = 'P@ssword'
                encoded_password = make_password(password)
                email = agent_form.cleaned_data['email']
                
                user = Utilisateurs.objects.create(
                    statut=statu,
                    username=username,
                    last_name=usernam,
                    first_name=userna,
                    password=encoded_password,
                    email=email,
                    role=role
                )
                
                agent = agent_form.save(commit=False)
                agent.user = user
                agent.save()
                
                return redirect('liste_agentcons')
    else:
        agent_form = AgentForm()
    
    return render(request, 'Pages/Agent/ajouter_agent.html', {'agent_form': agent_form})

def ajouter_agenttout(request):
    if request.method == 'POST':
        agent_form = AgentForm(request.POST, request.FILES)
        
        if agent_form.is_valid():
            with transaction.atomic():
                # Assigner le type d'agent commercial
                statut_actif = Typeagent.objects.get(type_agent='Personnel')
                agent_form.instance.type_agent = statut_actif
                
                # Créer un utilisateur avec le même nom d'utilisateur et mot de passe que l'agent
                userna = agent_form.cleaned_data['nom']
                usernam = agent_form.cleaned_data['prenom']
                FString = agent_form.cleaned_data['telephone']
                username = FString
                role = "ADMINISTRATEUR"
                statu = 'NON ACTIVE'
                password = 'P@ssword'
                encoded_password = make_password(password)
                email = agent_form.cleaned_data['email']
                
                user = Utilisateurs.objects.create(
                    statut=statu,
                    username=username,
                    last_name=usernam,
                    first_name=userna,
                    password=encoded_password,
                    email=email,
                    role=role
                )
                
                agent = agent_form.save(commit=False)
                agent.user = user
                agent.save()
                
                return redirect('liste_agentstout')
    else:
        agent_form = AgentForm()
    
    return render(request, 'Pages/Agent/ajouter_agent.html', {'agent_form': agent_form})


def ajouter_com(request):
    if request.method == 'POST':
        agent_form = AgentForm(request.POST, request.FILES)
        
        if agent_form.is_valid():
            with transaction.atomic():
                # Assigner le type d'agent commercial
                sty = Typeagent.objects.get(type_agent='Commercial')
                statut_actif = Statuts.objects.get(statut='Actif')
                agent_form.instance.type_agent = sty
                
                # Créer un utilisateur avec le même nom d'utilisateur et mot de passe que l'agent
                userna = agent_form.cleaned_data['nom']
                usernam = agent_form.cleaned_data['prenom']
                FString = agent_form.cleaned_data['telephone']
                username = FString
                role = "COMMERCIAL"
                statu = 'NON ACTIVE'
                password = 'P@ssword'
                encoded_password = make_password(password)
                email = agent_form.cleaned_data['email']
                
                user = Utilisateurs.objects.create(
                    statut=statu,
                    username=username,
                    last_name=usernam,
                    first_name=userna,
                    password=encoded_password,
                    email=email,
                    role=role
                )
                
                # Créer la commission pour l'agent
                Commissions.objects.create(
                    agent=user,
                    solde=0,
                    soldeprecedent=0,
                    datesolde=timezone.now(),
                    statut=statut_actif
                )
                
                agent = agent_form.save(commit=False)
                agent.type_agent = sty
                agent.user = user
                agent.save()
                
                return redirect('liste_com')
    else:
        agent_form = AgentForm()
    
    return render(request, 'Pages/Agent/ajouter_agent.html', {'agent_form': agent_form})

def ajouter_dem(request):
    if request.method == 'POST':
        agent_form = AgentForm(request.POST, request.FILES)
        
        if agent_form.is_valid():
            with transaction.atomic():
                # Assigner le type d'agent commercial
                ty = Typeagent.objects.get(type_agent='Démarcheur')
                statut_actif = Statuts.objects.get(statut='Actif')
                agent_form.instance.type_agent = ty
                
                # Créer un utilisateur avec le même nom d'utilisateur et mot de passe que l'agent
                userna = agent_form.cleaned_data['nom']
                usernam = agent_form.cleaned_data['prenom']
                FString = agent_form.cleaned_data['telephone']
                username = FString
                role = "DEMARCHEUR"
                statu = 'NON ACTIVE'
                password = 'P@ssword'
                encoded_password = make_password(password)
                email = agent_form.cleaned_data['email']
                
                user = Utilisateurs.objects.create(
                    statut=statu,
                    username=username,
                    last_name=usernam,
                    first_name=userna,
                    password=encoded_password,
                    email=email,
                    role=role
                )
                
                # Créer la commission pour l'agent
                Commissions.objects.create(
                    agent=user,
                    solde=0,
                    soldeprecedent=0,
                    datesolde=timezone.now(),
                    statut=statut_actif
                )
                
                agent = agent_form.save(commit=False)
                agent.type_agent = ty
                agent.user = user
                agent.save()
                
                return redirect('liste_dem')
    else:
        agent_form = AgentForm()
    
    return render(request, 'Pages/Agent/ajouter_agent.html', {'agent_form': agent_form})

def modifier_agent(request, pk):
    agent = get_object_or_404(Agent, pk=pk)
    if request.method == 'POST':
        agent_form = AgentForm(request.POST, instance=agent)
        if agent_form.is_valid():
            agent = agent_form.save()
            return redirect('liste_agents')
    else:
        agent_form = AgentForm(instance=agent)
    return render(request, 'Pages/Agent/modifier_agent.html', {'agent_form': agent_form})

def supprimer_agent(request, pk):
    agent = get_object_or_404(Agent, pk=pk)
    if request.method == 'POST':
        agent.user.delete()  # Supprimer l'utilisateur associé
        agent.delete()
        return redirect('liste_agents')
    return render(request, 'Pages/Agent/supprimer_agent.html', {'agent': agent})

# CLIENTS__________________________________________________________________________________________________________________________________________________
# Ordinaire
@login_required(login_url='/accounts/')
def liste_clients(request):
    clients = Clients.objects.filter(nat_client=1)
    statut_actif = Statuts.objects.get(statut='Actif')
    
    # Ajouter une méthode dans chaque client pour vérifier les comptes actifs
    for client in clients:
        client.a_compte_actif = ComptePrets.objects.filter(client=client, statut=statut_actif).exists()
    
    return render(request, 'Pages/Client/liste_clients.html', {'clients': clients})


# client sponsorié
@login_required(login_url='/accounts/')
def liste_clientss(request):
    clients = Clients.objects.filter(nat_client=3)
    return render(request, 'Pages/Client/liste_clientss.html', {'clients': clients})

# Bénéficiaire aide
@login_required(login_url='/accounts/')
def liste_clientsa(request):
    clients = Clients.objects.filter(nat_client=2)
    statut_actif = Statuts.objects.get(statut='Actif')
    
    # Ajouter une méthode dans chaque client pour vérifier les comptes actifs
    for client in clients:
        client.a_compte_actif = Aides.objects.filter(client=client, statut=statut_actif).exists()
    return render(request, 'Pages/Client/liste_clientsa.html', {'clients': clients})

@login_required(login_url='/accounts/')
def liste_clientsa1(request):
    clients = Clients.objects.filter(nat_client=2)
    return render(request, 'Pages/Client/liste_clientsa.html', {'clients': clients})

def detail_clients(request, client_id):
    client = Clients.objects.get(pk=client_id)
    comptes_prets = ComptePrets.objects.filter(client=client)
    comptes_epargnes = CompteEpargnes.objects.filter(client=client)
    comptes_epargne = CompteEpargnes.objects.filter(client=client)
    return render(request, 'Pages/Client/detail_clients.html', {'client': client, 'comptes_prets': comptes_prets, 'comptes_epargnes': comptes_epargnes,'comptes_epargne': comptes_epargne})

def detail_clientsa(request, client_id):
    statut_actif = Statuts.objects.get(statut='Actif')
    client = Clients.objects.get(pk=client_id)
    comptes_prets = Tontines.objects.filter(client=client)
    comptes_epargnes = Aides.objects.filter(client=client)
    return render(request, 'Pages/Client/detail_clientsa.html', {'client': client, 'comptes_prets': comptes_prets, 'comptes_epargnes': comptes_epargnes})

# Vue pour créer un client et son compte épargne
def creer_client(request):
    if request.method == 'POST':
        client_form = ClientForm(request.POST, request.FILES)
        if client_form.is_valid():
            statut_actif = Statuts.objects.get(statut='Actif')

            # API___ Juillet 2 Créer un utilisateur avec le même nom d'utilisateur et mot de passe que l'actionnaire
            userna = client_form.cleaned_data['nom']
            usernam = client_form.cleaned_data['prenom']
            FString = client_form.cleaned_data['telephone']
            username = FString
            role = "CLIENT"
            statu = 'ACTIVE'
            password = 'P@ssword'
            profile_photo = 'NON ACTIVE'
            encoded_password = make_password(password)
            email = client_form.cleaned_data['email']
            user = Utilisateurs.objects.create(statut=statu, username=username, last_name=usernam, first_name=userna, password=encoded_password, email=email, role=role)
            #API___ Juillet 2
            # Récupérer l'instance Typeactionnaire correspondant à type_act='3'
            try:
                nat_client = Natclients.objects.get(nat_client='Ordinaire')
            except Natclients.DoesNotExist:
                # Gérer le cas où le type d'actionnaire n'existe pas
                return redirect('erreur_page')  # Redirigez vers une page d'erreur ou créez une instance par défaut

            client_form.instance.statut = statut_actif
            client_form.instance.nat_client = nat_client
            client_form.instance.user = user
            client = client_form.save()
            CompteEpargnes.objects.create(client=client,solde=0, naturecompte='CLIENTORDINAIRE', numero_compte=f"EP{timezone.now().strftime('%Y%m%d%H%M%S')}", statut=statut_actif)
            return redirect('liste_clients')
    else:
        client_form = ClientForm()
    return render(request, 'Pages/Client/creer_client.html', {'form': client_form})

# Vue pour créer un client sponsorié
def creer_clients(request):
    if request.method == 'POST':
        client_form = ClientForm(request.POST, request.FILES)
        if client_form.is_valid():
            statut_actif = Statuts.objects.get(statut='Actif')

            # API___ Juillet 2 Créer un utilisateur avec le même nom d'utilisateur et mot de passe que l'actionnaire
            userna = client_form.cleaned_data['nom']
            usernam = client_form.cleaned_data['prenom']
            FString = client_form.cleaned_data['telephone']
            username = FString
            role = "CLIENT"
            statu = 'ACTIVE'
            password = 'P@ssword'
            profile_photo = 'NON ACTIVE'
            encoded_password = make_password(password)
            email = client_form.cleaned_data['email']
            user = Utilisateurs.objects.create(statut=statu, username=username, last_name=usernam, first_name=userna, password=encoded_password, email=email, role=role)
            #API___ Juillet 2
            try:
                nat_client = Natclients.objects.get(nat_client='Sponsor')
            except Natclients.DoesNotExist:
                # Gérer le cas où le type d'actionnaire n'existe pas
                return redirect('erreur_page')  # Redirigez vers une page d'erreur ou créez une instance par défaut

            client_form.instance.statut = statut_actif
            client_form.instance.nat_client = nat_client
            client_form.instance.user = user
            client = client_form.save()
            CompteEpargnes.objects.create(client=client,solde=0, naturecompte='CLIENTSPONSOR', numero_compte=f"EP{timezone.now().strftime('%Y%m%d%H%M%S')}", statut=statut_actif)
            return redirect('liste_clientss')
    else:
        client_form = ClientForm()
    return render(request, 'Pages/Client/creer_client.html', {'form': client_form})
#------------------------------------------------------------------------------------------------------------------------------------------------

# Vue pour créer un client aide --------------------------------------------------------------------------------------------------------------------
def creer_clienta(request):
    if request.method == 'POST':
        client_form = ClientForm(request.POST, request.FILES)
        if client_form.is_valid():
            statut_actif = Statuts.objects.get(statut='Non Actif')

            # API___ Juillet 2 Créer un utilisateur avec le même nom d'utilisateur et mot de passe que l'actionnaire
            userna = client_form.cleaned_data['nom']
            usernam = client_form.cleaned_data['prenom']
            FString = client_form.cleaned_data['telephone']
            username = FString
            role = "CLIENT"
            statu = 'ACTIVE'
            password = 'P@ssword'
            profile_photo = 'NON ACTIVE'
            encoded_password = make_password(password)
            email = client_form.cleaned_data['email']
            user = Utilisateurs.objects.create(statut=statu, username=username, last_name=usernam, first_name=userna, password=encoded_password, email=email, role=role)
            #API___ Juillet 2
            try:
                nat_client = Natclients.objects.get(nat_client='Aide')
            except Natclients.DoesNotExist:
                # Gérer le cas où le type d'actionnaire n'existe pas
                return redirect('erreur_page')  # Redirigez vers une page d'erreur ou créez une instance par défaut

            client_form.instance.statut = statut_actif
            client_form.instance.nat_client = nat_client
            client_form.instance.user = user
            client = client_form.save()
            CompteEpargnes.objects.create(client=client,solde=0, naturecompte='CLIENTAIDE', numero_compte=f"EP{timezone.now().strftime('%Y%m%d%H%M%S')}", statut=statut_actif)
            return redirect('liste_clientsa')
    else:
        client_form = ClientForm()
    return render(request, 'Pages/Client/creer_client.html', {'form': client_form})
#------------------------------------------------------------------------------------------------------------------------------------------------

# Vue pour modifier un client --------------------------------------------------------------------------------------------------------------------
def modifier_client(request, pk):
    client = get_object_or_404(Clients, pk=pk)
    if request.method == 'POST':
        client_form = ClientForm(request.POST, request.FILES, instance=client)
        if client_form.is_valid():
            client_form.save()
            return redirect('liste_clients')
    else:
        client_form = ClientForm(instance=client)
    return render(request, 'Pages/Client/modifier_client.html', {'form': client_form, 'client': client})
#------------------------------------------------------------------------------------------------------------------------------------------------

# Vue pour supprimer un client ------------------------------------------------------------------------------------------------------------------
def supprimer_client(request, pk):
    client = get_object_or_404(Clients, pk=pk)
    if request.method == 'POST':
        client.delete()
        return redirect('liste_clients')
    return render(request, 'Pages/Client/supprimer_client.html', {'client': client})


# COMPTE EPARGNE__________________________________________________________________________________________________________________________________________________
# Vue pour la liste des comptes épargne
def liste_comptes_epargne(request):
    comptes_epargne = CompteEpargnes.objects.filter(naturecompte='CLIENTORDINAIRE')
    return render(request, 'Pages/Compteepargne/liste_comptes_epargne.html', {'comptes_epargne': comptes_epargne})

def liste_comptes_epargnes(request):
    comptes_epargne = CompteEpargnes.objects.filter(naturecompte='CLIENTSPONSOR')
    return render(request, 'Pages/Compteepargne/liste_comptes_epargne.html', {'comptes_epargne': comptes_epargne})

def liste_comptes_epargnec(request):
    comptes_epargne = CompteEpargnesact.objects.all()
    return render(request, 'Pages/Compteepargneact/liste_comptes_epargne.html', {'comptes_epargne': comptes_epargne})

def detail_compte_epargne(request, compte_epargne_id):
    # Récupérer le compte d'épargne en fonction de l'ID passé en paramètre
    compte_epargne = get_object_or_404(CompteEpargnes, id=compte_epargne_id)

    context = {
        'compte_epargne': compte_epargne,
    }

    return render(request, 'Pages/Compteepargne/detail_compte_epargne.html', context)
#------------------------------------------------------------------------------------------------------------------------------------------------

# Vue pour créer un compte épargne --------------------------------------------------------------------------------------------------------------
def creer_compte_epargne(request):
    if request.method == 'POST':
        compte_epargne_form = CompteEpargneForm(request.POST)
        if compte_epargne_form.is_valid():
            compte_epargne_form.save()
            return redirect('liste_comptes_epargne')
    else:
        compte_epargne_form = CompteEpargneForm()
    return render(request, 'creer_compte_epargne.html', {'compte_epargne_form': compte_epargne_form})
#------------------------------------------------------------------------------------------------------------------------------------------------

# Vue pour modifier un compte épargne -----------------------------------------------------------------------------------------------------------
def modifier_compte_epargne(request, pk):
    compte_epargne = get_object_or_404(CompteEpargnes, pk=pk)
    if request.method == 'POST':
        compte_epargne_form = CompteEpargneForm(request.POST, instance=compte_epargne)
        if compte_epargne_form.is_valid():
            compte_epargne_form.save()
            return redirect('liste_comptes_epargne')
    else:
        compte_epargne_form = CompteEpargneForm(instance=compte_epargne)
    return render(request, 'modifier_compte_epargne.html', {'compte_epargne_form': compte_epargne_form, 'compte_epargne': compte_epargne})
#------------------------------------------------------------------------------------------------------------------------------------------------

# Vue pour supprimer un compte épargne ----------------------------------------------------------------------------------------------------------
def supprimer_compte_epargne(request, pk):
    compte_epargne = get_object_or_404(CompteEpargnes, pk=pk)
    if request.method == 'POST':
        compte_epargne.delete()
        return redirect('liste_comptes_epargne')
    return render(request, 'Pages/Compteepargne/supprimer_compte_epargne.html', {'compte_epargne': compte_epargne})
#____________________________________________________________________________________________________________________________________________________


# COMPTEPRET ____________________________________________________________________________________________________________________________________________________
def liste_comptes_prets(request):
    statut_actif = Statuts.objects.get(statut='Actif')
    comptes_prets = ComptePrets.objects.filter(naturecompte='CLIENTORDINAIRE',statut=statut_actif)
    return render(request, 'Pages/Comptepret/liste_comptes_prets.html', {'comptes_prets': comptes_prets})

def liste_comptes_pretss(request):
    statut_actif = get_object_or_404(Statuts, statut='Actif')
    comptes_prets = ComptePrets.objects.filter(naturecompte='CLIENTSPONSOR',statut=statut_actif)
    return render(request, 'Pages/Comptepret/liste_comptes_prets.html', {'comptes_prets': comptes_prets})

def liste_comptes_pretsna(request):
    statut_nactif = Statuts.objects.get(statut='Non Actif')
    comptes_prets = ComptePrets.objects.filter(naturecompte='CLIENTORDINAIRE',statut=statut_nactif)
    return render(request, 'Pages/Comptepret/liste_comptes_pretshisto.html', {'comptes_prets': comptes_prets})

def liste_comptes_pretssna(request):
    statut_nactif = Statuts.objects.get(statut='Non Actif')
    comptes_prets = ComptePrets.objects.filter(naturecompte='CLIENTSPONSOR',statut=statut_nactif)
    return render(request, 'Pages/Comptepret/liste_comptes_pretshisto.html', {'comptes_prets': comptes_prets})
#------------------------------------------------------------------------------------------------------------------------------------------------

# AFFICHER DETAIL UN PRET CLIENT -----------------------------------------------------------------------------------------------------------------------
def detail_compte_pret(request, compte_pret_id):
    compte_pret = get_object_or_404(ComptePrets, id=compte_pret_id)
    echeanciers = Echeancier.objects.filter(compte_pret=compte_pret)

    context = {
        'compte_pret': compte_pret,
        'echeanciers': echeanciers,
    }
    return render(request, 'Pages/Comptepret/detail_compte_pret.html', context)
#------------------------------------------------------------------------------------------------------------------------------------------------

# SUPPRIMER UN PRET CLIENT -----------------------------------------------------------------------------------------------------------------------
def supprimer_compte_pret(request, pk):
    compte_pret = get_object_or_404(ComptePrets, pk=pk)
    if request.method == 'POST':
        compte_pret.delete()
        return redirect('liste_comptes_prets')
    return render(request, 'Pages/Comptepret/supprimer_compte_pret.html', {'compte_pret': compte_pret})
#------------------------------------------------------------------------------------------------------------------------------------------------

# AJOUTER UN PRET CLIENT -----------------------------------------------------------------------------------------------------------------------
def ajouter_compte_pret(request, client_id):
    etud = Clients.objects.filter(id=client_id)

    etnon = Clients.objects.get(id=client_id)
    na = etnon.nat_client.nat_client   # Initialiser `na` pour éviter l'UnboundLocalError
    #na = None 
    if etnon:
        if na == 'Ordinaire':
            nat = 'CLIENTORDINAIRE'
        elif na == 'Sponsor':
            nat = 'CLIENTSPONSOR'
        elif na == 'Aide':
            nat = 'CLIENTAIDE'
    else:
        # Gérer le cas où aucun client n'est trouvé
        messages.error(request, "Aucun client trouvé avec cet ID.")

    # Vérifier si `na` a été défini correctement avant de l'utiliser
    if nat:
        # Utilisation de la variable `na`
        print(f"Client type: {nat}")
    else:
        # Gérer le cas où `na` est encore `None` (aucune condition `if` n'était remplie)
        messages.error(request, "Le type de client n'a pas pu être déterminé.")


    nombre = ComptePrets.objects.count()
    typp = Typeprets.objects.get(id=3)
    if request.method == 'POST':
        form = ComptePretForm(request.POST)
        if form.is_valid():

            # Assigner le type d'agent 
            if request.user.is_authenticated and isinstance(request.user, Utilisateurs):
                agent = request.user  # Assign the entire user object, not just the id

            typ = Typeprets.objects.get(id=3)
            form.instance.type_pret = typ

            statut_actif = Statuts.objects.get(statut='Actif')
            form.instance.statut = statut_actif
            compte_pret = form.save(commit=False)
            compte_pret.client_id = client_id  # Associer le compte prêt au client spécifié par l'ID
            compte_pret.date_demande = timezone.now()
            compte_pret.numero_compte = f"PR{timezone.now().strftime('%Y%m%d%H%M%S')}"
            compte_pret.naturecompte = nat
            # Calculer la date de fin en fonction de la date de début et de la durée en mois
            duree_en_mois = form.cleaned_data['duree_en_mois']
            compte_pret.date_fin_pret = compte_pret.date_debut_pret + timedelta(days=30 * duree_en_mois)

            # Calculer les intérêts en fonction du type de prêt
            somme_initiale = compte_pret.somme_initiale
            taux_interet = compte_pret.taux_interet / 100
            taux_garantie = 15 / 100
            statut_actif = get_object_or_404(Statuts, statut='Actif')
            Conf = Confconstantes.objects.filter(statut=statut_actif).first()
            taux_kha = Conf.partepargne
            taux_khaa = Conf.partfraisdos
            duree_en_mois = compte_pret.duree_en_mois

            if compte_pret.type_pret_id == 1:  # TYPE DE PRET avec versement d’une garantie
                interets = somme_initiale * Decimal(taux_interet) * duree_en_mois
            elif compte_pret.type_pret_id == 2:  # TYPE DE PRET sans versement de la garantie au préalable
                interets = (somme_initiale *Decimal(taux_garantie))+somme_initiale * Decimal(taux_interet) * 10  # 10 mois de remboursement par défaut
            elif compte_pret.type_pret_id == 3:  # TYPE DE PRET le client ayant un compte avec KHA
                interets = somme_initiale * Decimal(taux_interet) * duree_en_mois
            else:
                interets = 0

            compte_pret.solde = somme_initiale + interets + (somme_initiale *Decimal(taux_kha)) + (somme_initiale *Decimal(taux_khaa))
            compte_pret.agent = request.user
            # Calcul des échéances

            compte_pret.save()


            # Mise à jour du solde du compte portefeuilles KHA
            statut_actif = get_object_or_404(Statuts, statut='Actif')
            porte = get_object_or_404(ComptePortefeuilles, statut=statut_actif)
            porte.totalsortie += somme_initiale
            porte.totalreste = (porte.totalentree - somme_initiale)
            porte.save()

            # Mise à jour du solde du compte principal KHA
            statut_actif = get_object_or_404(Statuts, statut='Actif')
            princ = get_object_or_404(ComptePrincipale, statut=statut_actif)
            princ.totalsortie += somme_initiale
            princ.datesortie = timezone.now()  # Conserve la date avec fuseau horaire
            princ.save()

            # Redirection
            return redirect('liste_comptes_prets')

    else:
        form = ComptePretForm(initial={'client': client_id,'type_pret':typp}) 

    context = {
        'form': form,
        'client': client_id,  # Passer l'ID du client dans le contexte pour l'utiliser dans le formulaire
        'etud': etud
    }
    return render(request, 'Pages/Comptepret/ajouter_compte_pret.html', context)
#------------------------------------------------------------------------------------------------------------------------------------------------

# MODIFIER UN PRET CLIENT -----------------------------------------------------------------------------------------------------------------------
def modifier_compte_pret(request, pk):
    compte_pret = get_object_or_404(ComptePrets, pk=pk)
    ancisom = compte_pret.somme_initiale

    if request.method == 'POST':
        compte_pret_form = ComptePretForm(request.POST, instance=compte_pret)
        
        if compte_pret_form.is_valid():
            compte_pret = compte_pret_form.save()
            
            # Calculer la date de fin en fonction de la date de début et de la durée en mois
            duree_en_mois = compte_pret_form.cleaned_data['duree_en_mois']
            compte_pret.date_fin_pret = compte_pret.date_debut_pret + timedelta(days=30 * duree_en_mois)

            # Calculer les intérêts en fonction du type de prêt
            somme_initiale = compte_pret.somme_initiale
            taux_interet = compte_pret.taux_interet / 100
            taux_garantie = 15 / 100
            statut_actif = get_object_or_404(Statuts, statut='Actif')
            Conf = Confconstantes.objects.filter(statut=statut_actif).first()
            taux_kha = Conf.partepargne
            taux_khaa = Conf.partfraisdos
            duree_en_mois = compte_pret.duree_en_mois

            if compte_pret.type_pret_id == 1:  # TYPE DE PRET avec versement d’une garantie
                interets = somme_initiale * Decimal(taux_interet) * duree_en_mois
            elif compte_pret.type_pret_id == 2:  # TYPE DE PRET sans versement de la garantie au préalable
                interets = (somme_initiale * Decimal(taux_garantie)) + somme_initiale * Decimal(taux_interet) * 10  # 10 mois de remboursement par défaut
            elif compte_pret.type_pret_id == 3:  # TYPE DE PRET le client ayant un compte avec KHA
                interets = somme_initiale * Decimal(taux_interet) * duree_en_mois
            else:
                interets = 0

            compte_pret.solde = somme_initiale + interets+ (somme_initiale *Decimal(taux_kha)) + (somme_initiale *Decimal(taux_khaa))
            compte_pret.save()

             # Mise à jour du solde du compte portefeuilles KHA
            statut_actif = get_object_or_404(Statuts, statut='Actif')
            porte = get_object_or_404(ComptePortefeuilles, statut=statut_actif)
            porte.totalsortie += ( somme_initiale - ancisom )
            porte.totalreste += porte.totalentree - ( somme_initiale - ancisom )
            porte.save()

            # Mise à jour du solde du compte principal KHA
            statut_actif = get_object_or_404(Statuts, statut='Actif')
            princ = get_object_or_404(ComptePrincipale, statut=statut_actif)
            princ.totalsortie += ( somme_initiale - ancisom )
            princ.datesortie = timezone.now()  # Conserve la date avec fuseau horaire
            princ.save()

            # Récupérer le compte prêt via son identifiant (pk)
            compte_pret = get_object_or_404(ComptePrets, pk=pk)

            # Vérifier si un rachat existe pour ce compte
            rach = Rachats.objects.filter(compte_pretnew=compte_pret).first()

            # Si un rachat existe, mettre à jour le montant
            if rach:
                rach.montant_new += (somme_initiale - ancisom)
                rach.save()

            # MAJ FEV 
            if compte_pret.pk is not None:
                # Calculer les intérêts et les montants d'échéance en fonction des modifications apportées au prêt
                somme_initiale = compte_pret.somme_initiale
                taux_interet = compte_pret.taux_interet / 100
                taux_garantie = 15 / 100
                statut_actif = get_object_or_404(Statuts, statut='Actif')
                Conf = Confconstantes.objects.filter(statut=statut_actif).first()
                taux_kha = Conf.partepargne
                taux_khaa = Conf.partfraisdos
                duree_en_mois = compte_pret.duree_en_mois

                if compte_pret.type_pret_id == 1:
                    interets = somme_initiale * Decimal(taux_interet) * duree_en_mois
                elif compte_pret.type_pret_id == 2:
                    interets = (somme_initiale * Decimal(taux_garantie)) + somme_initiale * Decimal(taux_interet) * 10
                elif compte_pret.type_pret_id == 3:
                    interets = somme_initiale * Decimal(taux_interet) * duree_en_mois
                else:
                    interets = 0

                montant_echeance = (somme_initiale + interets+ (somme_initiale *Decimal(taux_kha))) / duree_en_mois
                montant_adhesion = (somme_initiale + interets+ (somme_initiale *Decimal(taux_khaa))) / duree_en_mois
                montant_interet = (interets) / duree_en_mois

                compte_pret.solde = somme_initiale + interets + (somme_initiale *Decimal(taux_kha)) + (somme_initiale *Decimal(taux_khaa))

            # Mettre à jour les échéances associées au prêt
                
                if compte_pret.type_client_id == 1:  # Pour un client avec des échéances chaque semaine
                    montant_interet =  interets/(compte_pret.duree_en_mois * 4)
                    montant_epargne = (compte_pret.somme_initiale *Decimal(taux_kha))  / (compte_pret.duree_en_mois * 4)
                    montant_adhesion = (compte_pret.somme_initiale *Decimal(taux_khaa)) / (compte_pret.duree_en_mois * 4)
                    montant_echeance = ((compte_pret.somme_initiale + interets) / (compte_pret.duree_en_mois * 4)) + montant_epargne + montant_adhesion

                elif compte_pret.type_client_id == 2:  # Pour un client avec des échéances chaque mois
                    montant_interet =  interets/compte_pret.duree_en_mois
                    montant_epargne = (compte_pret.somme_initiale *Decimal(taux_kha))  / compte_pret.duree_en_mois
                    montant_adhesion = (compte_pret.somme_initiale *Decimal(taux_khaa)) / compte_pret.duree_en_mois
                    montant_echeance = ((compte_pret.somme_initiale + interets) / compte_pret.duree_en_mois) + montant_epargne + montant_adhesion
                else:
                    montant_epargne = 0

                echeances = Echeancier.objects.filter(compte_pret=compte_pret)
                date_echeance = compte_pret.date_debut_pret + relativedelta(months=1)

                # Calculer le nombre d'échéances à conserver
                nouvelle_duree_en_mois = compte_pret.duree_en_mois
                if compte_pret.type_client_id == 1:  # Pour un client avec des échéances chaque semaine
                    nombre_echeances_a_conserver = nouvelle_duree_en_mois * 4
                elif compte_pret.type_client_id == 2:  # Pour un client avec des échéances chaque mois
                    nombre_echeances_a_conserver = nouvelle_duree_en_mois

                for echeance in echeances:
                    if nombre_echeances_a_conserver > 0:
                        echeance.date_echeance = date_echeance
                        echeance.montant_echeance = montant_echeance
                        echeance.montant_interet = montant_interet
                        echeance.montant_epargne = montant_epargne
                        echeance.montant_adhesion = montant_adhesion
                        echeance.save()

                        nombre_echeances_a_conserver -= 1
                    else:
                        # Supprimer les échéances excédentes
                        echeance.delete()

                    if compte_pret.type_client_id == 1:  # Pour un client avec des échéances chaque semaine
                        date_echeance += timedelta(days=7)
                    elif compte_pret.type_client_id == 2:  # Pour un client avec des échéances chaque mois
                        date_echeance += relativedelta(months=1)
            # MAJ FEV 
            return redirect('liste_comptes_prets')
    else:
        compte_pret_form = ComptePretForm(instance=compte_pret)
    
    return render(request, 'Pages/Comptepret/modifier_compte_pret.html', {'compte_pret_form': compte_pret_form})              
#___________________________________________________________________________________________________________________________________________________________


# AFFICHER LES ECHEANCES PAYEES OU NON PAYEES DES CLIENTS ____________________________________________________________________________________________________________________
def clients_proche_echeance(request):
    date_actuelle = date.today()
    #date_une_semaine_plus_tard = date_actuelle + timedelta(days=7)
    # MAJ FEV
    date_une_semaine_plus_tard = date_actuelle + timedelta(days=3)
    # MAJ FEV

    clients_proche_echeance = Echeancier.objects.filter(date_echeance__gte=date_actuelle, date_echeance__lte=date_une_semaine_plus_tard,est_paye=False).values(
        'compte_pret__client__nom',
        'compte_pret__client__prenom',
        'compte_pret__client__telephone',
        'compte_pret__numero_compte',
        'id'
    )


    context = {
        'clients': clients_proche_echeance,
    }

    return render(request, 'Pages/Comptepret/listeecheance.html', context)

def clients_proche_echeancesous(request):
    date_actuelle = date.today()
    #date_une_semaine_plus_tard = date_actuelle + timedelta(days=7)
    # MAJ FEV
    date_une_semaine_plus_tard = date_actuelle + timedelta(days=3)
    # MAJ FEV

    actionnaire_proche_echeance = Echeancieract.objects.filter(date_echeance__gte=date_actuelle, date_echeance__lte=date_une_semaine_plus_tard,est_paye=False).values(
        'compte_pretact__actionnaire__nom',
        'compte_pretact__actionnaire__prenom',
        'compte_pretact__actionnaire__telephone',
        'compte_pretact__numero_compte', 
        'id'
    )

    context = {
        'actionnaires': actionnaire_proche_echeance
    }

    return render(request, 'Pages/Comptepret/listeecheanceact.html', context)

def liste_echeances_non_payees(request):
    # Récupérer les échéances non payées dans le passé
    echeances_non_payees = Echeancier.objects.filter(date_echeance__lt=date.today(), est_paye=False)

    context = {
        'echeances_non_payees': echeances_non_payees,
    }

    return render(request, 'Pages/Comptepret/listeecheancenon.html', context)

def liste_echeances_non_payeesact(request):
    # Récupérer les échéances non payées dans le passé
    echeances_non_payeesact = Echeancieract.objects.filter(date_echeance__lt=date.today(), est_paye=False)

    context = {
        'echeances_non_payeesact': echeances_non_payeesact
    }

    return render(request, 'Pages/Comptepret/listeecheancenonact.html', context)
#____________________________________________________________________________________________________________________________________________________


# MARQUER LES ECHEANCES PAYEES DES CLIENTS ____________________________________________________________________________________________________________________

def modifier_est_paye1(request, actionnaire_id):
    echance = Echeancier.objects.get(pk=actionnaire_id)
    echance.est_paye = 1
    echance.save()

    # Créez une nouvelle transaction de prêt pour indiquer le paiement de l'échéance
    if request.user.is_authenticated and isinstance(request.user, Utilisateurs):
        agent = request.user

    transaction_pret = TransactionPret.objects.create(
        compte_pret=echance.compte_pret,
        montant=echance.montant_echeance,
        type_transaction='Depot',  # Mettez le type de transaction approprié
        agent=request.user  # Assurez-vous que cela pointe vers l'utilisateur connecté
    )

    # Mise à jour du solde du compte épargne associé à l'actionnaire
    compte_pret = echance.compte_pret
    clien = compte_pret.client
    epar = get_object_or_404(CompteEpargnes, client=clien)
    epar.solde += echance.montant_epargne
    epar.save()

    # Mise à jour du solde du compte épargne associé à l'actionnaire
    compte_pret = echance.compte_pret
    clien = compte_pret.client
    epar = get_object_or_404(CompteAdhesionkhas, client=clien)
    epar.solde += echance.montant_epargne
    epar.save()

    # Création de la transaction d'épargne
    transaction_epar = TransactionEpargne.objects.create(
        compte_epargne=epar,
        montant=echance.montant_epargne,
        type_transaction='Virement',  # À adapter en fonction de votre logique
        agent=request.user #if isinstance(request.user, Agent) else None  # Assurez-vous que cela pointe vers l'utilisateur connecté
    )
    # MAJ FEV

    # Vérifier si c'est la dernière échéance payée pour le compte prêt
    compte_pret = echance.compte_pret
    dernier_echeance_payee = Echeancier.objects.filter(compte_pret=compte_pret, est_paye=False).order_by('date_echeance').first()
    if not dernier_echeance_payee:
        # Si aucune échéance impayée, mettre le statut du compte prêt en inactif
        compte_pret.statut = Statuts.objects.get(statut='Non Actif')
        compte_pret.save()
        
        # Mettre à jour le statut du contrat sponsor
        try:
            cont = Contratsponsor.objects.get(numero_compte=compte_pret.numero_compte)
            cont.statut = Statuts.objects.get(statut='Non Actif')
            cont.save()
        except Contratsponsor.DoesNotExist:
            # Gérer le cas où le contrat sponsor n'existe pas
            pass
     
 
    statut_actif = Statuts.objects.get(statut='Actif')
    kha = get_object_or_404(CompteKha, statut=statut_actif)
    kha.soldeprecedent = kha.solde
    kha.dateprecedent = kha.datesolde
    kha.datesolde = timezone.now()
    kha.solde += echance.montant_epargne
    kha.save()

    transactionkha = TransactionKha.objects.create(
        comptekha=kha,
        montant=echance.montant_epargne,
        type_transaction='Virement',  # À adapter en fonction de votre logique
        agent=request.user #if isinstance(request.user, Agent) else None  # Assurez-vous que cela pointe vers l'utilisateur connecté
    )
    
    # Associer le compte prêt au client spécifié par l'ID
    statut_actif = get_object_or_404(Statuts, statut='Actif')
    Conf = Confconstantes.objects.filter(statut=statut_actif).first()
    taux_kha = Conf.partepargne
    taux_com = Conf.partcom

    compte_pret = echance.compte_pret
    comm = get_object_or_404(ComptePrets, id=compte_pret.id)
    etudian = get_object_or_404(Agent, user=comm.agent)

    # Assurez-vous que la commission existe pour l'agent, sinon créez-la
    commission, created = Commissions.objects.get_or_create(agent=etudian.user, defaults={
        'solde': 0,
        'soldeprecedent': 0,
        'datesolde': timezone.now(),
        'statut': statut_actif  # ou une valeur par défaut
    })

    # Mettre à jour la commission
    commission.soldeprecedent = commission.solde
    commission.date_aide = commission.datesolde
    commission.datesolde = timezone.now()
    commission.solde += (echance.montant_interet * Decimal(taux_com))
    commission.save()

    # Créer une nouvelle transaction de prêt
    transactioncom = TransactionCommissionpret.objects.create(
        commission=commission,
        echeance=echance,
        montant=(echance.montant_interet * Decimal(taux_com)),
        type_transaction='Virement',  # À adapter en fonction de votre logique
        agent=request.user  # Assurez-vous que cela pointe vers l'utilisateur connecté
    )
            #API___ Juillet 2

    return redirect('clients_proche_echeance')

# MARQUER UNE CHEANCES PAYEES ACTUALISÉ ------------------------------------------------------------------------------------------------------------------------
@login_required  # Décorateur pour s'assurer que l'utilisateur est connecté
def modifier_est_paye(request, actionnaire_id):
    echance = get_object_or_404(Echeancier, pk=actionnaire_id)
    echance.est_paye = True
    echance.save()

    if request.user.is_authenticated and isinstance(request.user, Utilisateurs):
        agent = request.user

    # Création de la transaction de prêt
    transaction_pret = TransactionPret.objects.create(
        compte_pret=echance.compte_pret,
        montant=echance.montant_echeance,
        type_transaction='Depot',  # À adapter en fonction de votre logique
        agent=request.user #if isinstance(request.user, Agent) else None  # Assurez-vous que cela pointe vers l'utilisateur connecté
    )

    # Mise à jour du solde du compte épargne associé à l'actionnaire
    compte_pret = echance.compte_pret
    clien = compte_pret.client
    epar = get_object_or_404(CompteEpargnes, client=clien)
    epar.solde += echance.montant_epargne
    epar.save()
#
    # Mise à jour du solde du compte adhesion associé à l'actionnaire
    statut_actif = get_object_or_404(Statuts, statut='Actif')
    adh = get_object_or_404(CompteAdhesionkhas, statut=statut_actif)
    adh.soldeprecedent = adh.solde
    adh.dateprecedent = adh.datesolde
    adh.datesolde = timezone.now()  # Conserve la date avec fuseau horaire
    adh.solde += echance.montant_adhesion
    adh.save()

    # Mise à jour du solde du compte interet associé à l'actionnaire
    statut_actif = get_object_or_404(Statuts, statut='Actif')
    inter = get_object_or_404(CompteInterets, statut=statut_actif)
    inter.soldeprecedent = inter.solde
    inter.dateprecedent = inter.datesolde
    inter.datesolde = timezone.now()  # Conserve la date avec fuseau horaire
    inter.solde += echance.montant_interet
    inter.save()

    transactionint = TransactionInteret.objects.create(
        compteinteret=inter,
        montant=echance.montant_interet,
        type_transaction='Virement',  # À adapter en fonction de votre logique
    )

    # Mise à jour du solde du compte interet associé à l'actionnaire
    statut_actif = get_object_or_404(Statuts, statut='Actif')
    penal = get_object_or_404(ComptePenalites, statut=statut_actif)
    penal.soldeprecedent = penal.solde
    penal.dateprecedent = penal.datesolde
    penal.datesolde = timezone.now()  # Conserve la date avec fuseau horaire
    penal.solde += echance.montant_penalite
    penal.save()

    if echance.montant_penalite > 0:
        transactionpenal = TransactionPenaliteHist.objects.create(
            comptepenalite=penal,
            montant=echance.montant_penalite,
            type_transaction='Virement',  # À adapter en fonction de votre logique
            agent=request.user  # Assurez-vous que cela pointe vers l'utilisateur connecté
        )

        # Créer une nouvelle transaction de prêt
        transactionpenalites = TransactionPenalite.objects.create(
            compte_pret=echance.compte_pret,
            echeance=echance,
            montant=echance.montant_penalite,
            type_transaction='Virement',  # À adapter en fonction de votre logique
            agent=request.user  # Assurez-vous que cela pointe vers l'utilisateur connecté
        )
    
    # Mise à jour du solde du compte principal KHA
    statut_actif = get_object_or_404(Statuts, statut='Actif')
    princ = get_object_or_404(ComptePrincipale, statut=statut_actif)
    princ.totalentree += echance.montant_echeance
    princ.dateentree = timezone.now()  # Conserve la date avec fuseau horaire
    princ.totalgain = ( princ.totalentree - (princ.totalsortie + princ.totaldepenses))
    princ.save()

    # Mise à jour du solde du compte portefeuilles KHA
    statut_actif = get_object_or_404(Statuts, statut='Actif')
    porte = get_object_or_404(ComptePortefeuilles, statut=statut_actif)
    porte.totalentree += (echance.montant_echeance - (echance.montant_interet + echance.montant_epargne + echance.montant_adhesion + echance.montant_penalite))
    porte.totalreste = porte.totalentree - porte.totalsortie
    porte.save()
#
    # Création de la transaction d'épargne
    transaction_epar = TransactionEpargne.objects.create(
        compte_epargne=epar,
        montant=echance.montant_epargne,
        type_transaction='Virement',  # À adapter en fonction de votre logique
        agent=request.user   # Assurez-vous que cela pointe vers l'utilisateur connecté
    )
    # MAJ FEV

    # Vérifier si c'est la dernière échéance payée pour le compte prêt
    compte_pret = echance.compte_pret
    dernier_echeance_payee = Echeancier.objects.filter(compte_pret=compte_pret, est_paye=False).order_by('date_echeance').first()
    if not dernier_echeance_payee:
        # Si aucune échéance impayée, mettre le statut du compte prêt en inactif
        compte_pret.statut = Statuts.objects.get(statut='Non Actif')
        compte_pret.save()

        # Mettre à jour le statut du contrat sponsor
        try:
            cont = Contratsponsor.objects.get(numero_compte=compte_pret.numero_compte)
            cont.statut = Statuts.objects.get(statut='Non Actif')
            cont.save()
        except Contratsponsor.DoesNotExist:
            # Gérer le cas où le contrat sponsor n'existe pas
            pass


            #API___ Juillet 2
    statut_actif = Statuts.objects.get(statut='Actif')
    kha = get_object_or_404(CompteKha, statut=statut_actif)
    kha.soldeprecedent = kha.solde
    kha.dateprecedent = kha.datesolde
    kha.datesolde = timezone.now()
    kha.solde += echance.montant_epargne
    kha.save()

    transactionkha = TransactionKha.objects.create(
        comptekha=kha,
        montant=echance.montant_epargne,
        type_transaction='Virement',  # À adapter en fonction de votre logique
        agent=request.user #if isinstance(request.user, Agent) else None  # Assurez-vous que cela pointe vers l'utilisateur connecté
    )

    transactionadh = TransactionAdhesionkha.objects.create(
        compteAdhessionkha=adh,
        montant=echance.montant_adhesion,
        type_transaction='Virement',  # À adapter en fonction de votre logique
        agent=request.user #if isinstance(request.user, Agent) else None  # Assurez-vous que cela pointe vers l'utilisateur connecté
    )

    # Associer le compte prêt au client spécifié par l'ID
    statut_actif = get_object_or_404(Statuts, statut='Actif')
    Conf = Confconstantes.objects.filter(statut=statut_actif).first()
    taux_kha = Conf.partepargne
    taux_com = Conf.partcom

    compte_pret = echance.compte_pret
    # Mettre à jour l'agent avec son ID
    comm = get_object_or_404(ComptePrets, id=compte_pret.id)
    com = get_object_or_404(Agent, id=comm.com.id)  # Utilisez .id pour obtenir l'ID de l'objet

    # Assurez-vous que la commission existe pour l'agent, sinon créez-la
    commission, created = Commissions.objects.get_or_create(agent=com.user, defaults={
        'solde': 0,
        'soldeprecedent': 0,
        'datesolde': timezone.now(),
        'statut': statut_actif.id  # ou une valeur par défaut
    })

    # Mettre à jour la commission
    commission.soldeprecedent = commission.solde
    commission.date_aide = commission.datesolde
    commission.datesolde = timezone.now()
    commission.solde += (echance.montant_interet * Decimal(taux_com))
    commission.save()

    # Créer une nouvelle transaction de prêt
    transactioncom = TransactionCommissionpret.objects.create(
        commission=commission,
        echeance=echance,
        montant=(echance.montant_interet * Decimal(taux_com)),
        type_transaction='Virement',  # À adapter en fonction de votre logique
        agent=request.user  # Assurez-vous que cela pointe vers l'utilisateur connecté
    )

    #messages.success(request, 'L\'échéance a été marquée comme payée avec succès.')
    return redirect('liste_echeances_non_payees')
#________________________________________________________________________________________________________________________________________________________________


# MARQUER UNE CHEANCES PAYEES ACTUALISÉ POUR LA LISTE EN RETARD --------------------------------------------------------------------------------------------------
@login_required  # Décorateur pour s'assurer que l'utilisateur est connecté
def modifier_est_payere(request, actionnaire_id):
    echance = get_object_or_404(Echeancier, pk=actionnaire_id)
    echance.est_paye = True
    echance.save()

    if request.user.is_authenticated and isinstance(request.user, Utilisateurs):
        agent = request.user

    # Création de la transaction de prêt
    transaction_pret = TransactionPret.objects.create(
        compte_pret=echance.compte_pret,
        montant=echance.montant_echeance,
        type_transaction='Depot',  # À adapter en fonction de votre logique
        agent=request.user #if isinstance(request.user, Agent) else None  # Assurez-vous que cela pointe vers l'utilisateur connecté
    )

    # Mise à jour du solde du compte épargne associé à l'actionnaire
    compte_pret = echance.compte_pret
    clien = compte_pret.client
    epar = get_object_or_404(CompteEpargnes, client=clien)
    epar.solde += echance.montant_epargne
    epar.save()

#
    # Mise à jour du solde du compte adhesion associé à l'actionnaire
    statut_actif = get_object_or_404(Statuts, statut='Actif')
    adh = get_object_or_404(CompteAdhesionkhas, statut=statut_actif)
    adh.soldeprecedent = adh.solde
    adh.dateprecedent = adh.datesolde
    adh.datesolde = timezone.now()  # Conserve la date avec fuseau horaire
    adh.solde += echance.montant_adhesion
    adh.save()

    # Mise à jour du solde du compte interet associé à l'actionnaire
    statut_actif = get_object_or_404(Statuts, statut='Actif')
    inter = get_object_or_404(CompteInterets, statut=statut_actif)
    inter.soldeprecedent = inter.solde
    inter.dateprecedent = inter.datesolde
    inter.datesolde = timezone.now()  # Conserve la date avec fuseau horaire
    inter.solde += echance.montant_interet
    inter.save()

    transactionint = TransactionInteret.objects.create(
        compteinteret=inter,
        montant=echance.montant_interet,
        type_transaction='Virement',  # À adapter en fonction de votre logique
        # agent=request.user #if isinstance(request.user, Agent) else None  # Assurez-vous que cela pointe vers l'utilisateur connecté
    )

    # Mise à jour du solde du compte interet associé à l'actionnaire
    statut_actif = get_object_or_404(Statuts, statut='Actif')
    penal = get_object_or_404(ComptePenalites, statut=statut_actif)
    penal.soldeprecedent = penal.solde
    penal.dateprecedent = penal.datesolde
    penal.datesolde = timezone.now()  # Conserve la date avec fuseau horaire
    penal.solde += echance.montant_penalite
    penal.save()

    if echance.montant_penalite > 0:
        transactionpenal = TransactionPenaliteHist.objects.create(
            comptepenalite=penal,
            montant=echance.montant_penalite,
            type_transaction='Virement',  # À adapter en fonction de votre logique
        )

        # Créer une nouvelle transaction de prêt
        transactionpenalites = TransactionPenalite.objects.create(
            compte_pret=echance.compte_pret,
            echeance=echance,
            montant=echance.montant_penalite,
            type_transaction='Virement',  # À adapter en fonction de votre logique
        )
    
    # Mise à jour du solde du compte principal KHA
    statut_actif = get_object_or_404(Statuts, statut='Actif')
    princ = get_object_or_404(ComptePrincipale, statut=statut_actif)
    princ.totalentree += echance.montant_echeance
    princ.dateentree = timezone.now()  # Conserve la date avec fuseau horaire
    princ.totalgain = ( princ.totalentree - (princ.totalsortie + princ.totaldepenses))
    princ.save()

    # Mise à jour du solde du compte portefeuilles KHA
    statut_actif = get_object_or_404(Statuts, statut='Actif')
    porte = get_object_or_404(ComptePortefeuilles, statut=statut_actif)
    porte.totalentree += (echance.montant_echeance - (echance.montant_interet + echance.montant_epargne + echance.montant_adhesion + echance.montant_penalite))
    porte.totalreste = porte.totalentree - porte.totalsortie
    porte.save()
#
    # Création de la transaction d'épargne
    transaction_epar = TransactionEpargne.objects.create(
        compte_epargne=epar,
        montant=echance.montant_epargne,
        type_transaction='Virement',  # À adapter en fonction de votre logique
        agent=request.user   # Assurez-vous que cela pointe vers l'utilisateur connecté
    )
    # MAJ FEV

    # Vérifier si c'est la dernière échéance payée pour le compte prêt
    compte_pret = echance.compte_pret
    dernier_echeance_payee = Echeancier.objects.filter(compte_pret=compte_pret, est_paye=False).order_by('date_echeance').first()
    if not dernier_echeance_payee:
        # Si aucune échéance impayée, mettre le statut du compte prêt en inactif
        compte_pret.statut = Statuts.objects.get(statut='Non Actif')
        compte_pret.save()

        # Mettre à jour le statut du contrat sponsor
        try:
            cont = Contratsponsor.objects.get(numero_compte=compte_pret.numero_compte)
            cont.statut = Statuts.objects.get(statut='Non Actif')
            cont.save()
        except Contratsponsor.DoesNotExist:
            # Gérer le cas où le contrat sponsor n'existe pas
            pass


            #API___ Juillet 2
    statut_actif = Statuts.objects.get(statut='Actif')
    kha = get_object_or_404(CompteKha, statut=statut_actif)
    kha.soldeprecedent = kha.solde
    kha.dateprecedent = kha.datesolde
    kha.datesolde = timezone.now()
    kha.solde += echance.montant_epargne
    kha.save()

    transactionkha = TransactionKha.objects.create(
        comptekha=kha,
        montant=echance.montant_epargne,
        type_transaction='Virement',  # À adapter en fonction de votre logique
        agent=request.user #if isinstance(request.user, Agent) else None  # Assurez-vous que cela pointe vers l'utilisateur connecté
    )

    transactionadh = TransactionAdhesionkha.objects.create(
        compteAdhessionkha=adh,
        montant=echance.montant_adhesion,
        type_transaction='Virement',  # À adapter en fonction de votre logique
    )

    # Associer le compte prêt au client spécifié par l'ID
    statut_actif = get_object_or_404(Statuts, statut='Actif')
    Conf = Confconstantes.objects.filter(statut=statut_actif).first()
    taux_kha = Conf.partepargne
    taux_com = Conf.partcom

    compte_pret = echance.compte_pret
    # Mettre à jour l'agent avec son ID
    comm = get_object_or_404(ComptePrets, id=compte_pret.id)
    com = get_object_or_404(Agent, id=comm.com.id)  # Utilisez .id pour obtenir l'ID de l'objet

    # Assurez-vous que la commission existe pour l'agent, sinon créez-la
    commission, created = Commissions.objects.get_or_create(agent=com.user, defaults={
        'solde': 0,
        'soldeprecedent': 0,
        'datesolde': timezone.now(),
        'statut': statut_actif.id  # ou une valeur par défaut
    })

    statut_actif = get_object_or_404(Statuts, statut='Actif')
    Conf = Confconstantes.objects.filter(statut=statut_actif).first()
    taux_kha = Conf.partepargne
    taux_com = Conf.partcom
    # Mettre à jour la commission
    commission.soldeprecedent = commission.solde
    commission.date_aide = commission.datesolde
    commission.datesolde = timezone.now()
    commission.solde += (echance.montant_interet * Decimal(taux_com))
    commission.save()

    # Créer une nouvelle transaction de prêt
    transactioncom = TransactionCommissionpret.objects.create(
        commission=commission,
        echeance=echance,
        montant=(echance.montant_interet * Decimal(taux_com)),
        type_transaction='Virement',  # À adapter en fonction de votre logique
        agent=request.user  # Assurez-vous que cela pointe vers l'utilisateur connecté
    )

    #messages.success(request, 'L\'échéance a été marquée comme payée avec succès.')
    return redirect('liste_echeances_non_payees')
#___________________________________________________________________________________________________________________________________________________________


# TRANSACTIONS EPARGNES ET PRETS ____________________________________________________________________________________________________________________________________________
def liste_transactions(request):
    transactions = TransactionEpargne.objects.all()
    return render(request, 'Pages/Transactionepargne/liste_transactions.html', {'transactions': transactions})

def liste_transactionss(request):
    transactions = TransactionPret.objects.all()
    return render(request, 'Pages/Transactionpret/liste_transactions.html', {'transactions': transactions})

# Vue pour créer une transaction d'épargne
def creer_transaction_epargne(request,id,idd):
    if request.method == 'POST':
        transaction_form = TransactionEpargneForm(request.POST)
        if transaction_form.is_valid():
            transaction = transaction_form.save(commit=False)
            # Effectuer les opérations spécifiques pour les transactions d'épargne
            # Vérifier si l'utilisateur est un agent avant de l'attribuer à la transaction
            if request.user.is_authenticated and isinstance(request.user, Utilisateurs):
                transaction.agent = request.user

            montant = transaction.montant
            if transaction.type_transaction == 'Depot':
                transaction.compte_epargne.solde += montant
            elif transaction.type_transaction == 'Virement':
                transaction.compte_epargne.solde += montant
            elif transaction.type_transaction == 'Retrait':
                transaction.compte_epargne.solde -= montant
            transaction.compte_epargne.save()
            transaction.save()
            return redirect(reverse('detail_clients', args=[idd]))
    else:
        transaction_form = TransactionEpargneForm(initial={'compte_epargne': id})
    context = {
        'transaction_form': transaction_form,
        'id': id,
    }

    return render(request, 'Pages/Transactionepargne/creer_transaction_epargne.html', context)

@login_required
def modifier_transaction_epargne(request, transaction_id):
    transaction = get_object_or_404(TransactionEpargne, pk=transaction_id)
    type_avant_modification = transaction.type_transaction
    montant_avant_modification = transaction.montant

    if request.method == 'POST':
        transaction_form = TransactionEpargneForm(request.POST, instance=transaction)
        if transaction_form.is_valid():
            transaction = transaction_form.save(commit=False)

            if request.user.is_authenticated and isinstance(request.user, Agent):
                transaction.agent = request.user

            montant_apres_modification = transaction.montant

            # Cas 1: Même type de transaction, montant modifié
            if type_avant_modification == transaction.type_transaction and montant_avant_modification != montant_apres_modification:
                ajustement_solde = montant_apres_modification - montant_avant_modification
                if type_avant_modification == 'Depot':
                    transaction.compte_epargne.solde += ajustement_solde
                elif type_avant_modification == 'Retrait':
                    transaction.compte_epargne.solde -= ajustement_solde
                transaction.compte_epargne.save()

            # Cas 2: Même type de transaction, montant inchangé
            elif type_avant_modification == transaction.type_transaction and montant_avant_modification == montant_apres_modification:
                pass  # Aucun ajustement de solde nécessaire

            # Cas 3: Changement de type de transaction, montant inchangé
            elif type_avant_modification != transaction.type_transaction and montant_avant_modification == montant_apres_modification:
                if type_avant_modification == 'Depot':
                    transaction.compte_epargne.solde -= montant_avant_modification
                elif type_avant_modification == 'Retrait':
                    transaction.compte_epargne.solde += montant_avant_modification
                transaction.compte_epargne.save()

                if transaction.type_transaction == 'Depot':
                    transaction.compte_epargne.solde += montant_apres_modification
                elif transaction.type_transaction == 'Retrait':
                    transaction.compte_epargne.solde -= montant_apres_modification
                transaction.compte_epargne.save()

            # Cas 4: Changement de type de transaction et montant modifié
            elif type_avant_modification != transaction.type_transaction and montant_avant_modification != montant_apres_modification:
                ajustement_solde_montant = montant_apres_modification - montant_avant_modification
                ajustement_solde_type = 2 * montant_avant_modification  # ajustement pour le changement de type
                ajustement_solde_total = ajustement_solde_montant + ajustement_solde_type

                

                if transaction.type_transaction == 'Depot':
                    transaction.compte_epargne.solde += ajustement_solde_total
                elif transaction.type_transaction == 'Retrait':
                    transaction.compte_epargne.solde -= ajustement_solde_total
                transaction.compte_epargne.save()

            transaction.save()
            return redirect(reverse('detail_clients', args=[transaction.compte_epargne.client.id]))
    else:
        transaction_form = TransactionEpargneForm(instance=transaction)

    context = {
        'transaction_form': transaction_form,
        'transaction_id': transaction_id,
    }
    return render(request, 'Pages/Transactionepargne/modifier_transaction_epargne.html', context)


def supprimer_transaction_epargne(request, transaction_id):
    transaction = get_object_or_404(TransactionEpargne, pk=transaction_id)

    if request.method == 'POST':
        montant = transaction.montant
        if transaction.type_transaction == 'Depot':
            transaction.compte_epargne.solde -= montant
        elif transaction.type_transaction == 'Retrait':
            transaction.compte_epargne.solde += montant
        transaction.compte_epargne.save()
        transaction.delete()
        return redirect(reverse('detail_clients', args=[transaction.compte_epargne.client.id]))

    context = {
        'transaction': transaction,
    }
    return render(request, 'Pages/Transactionepargne/supprimer_transaction_epargne.html', context)
#_________________________________________________________________________________________________________________________________________________________


# TRANSACTION SUR LES COMPTES EPARGNES SOUS COOPERATEUR ________________________________________________________________________________________________
def liste_transactionsous(request):
    transactions = TransactionEpargneact.objects.all()
    return render(request, 'Pages/Transactionepargneact/liste_transactions.html', {'transactions': transactions})

# Vue pour créer une transaction d'épargne
def creer_transaction_epargnesous(request,id,idd):
    if request.method == 'POST':
        transaction_form = TransactionEpargneactForm(request.POST)
        if transaction_form.is_valid():
            transaction = transaction_form.save(commit=False)
            # Effectuer les opérations spécifiques pour les transactions d'épargne
            # Vérifier si l'utilisateur est un agent avant de l'attribuer à la transaction
            if request.user.is_authenticated and isinstance(request.user, Utilisateurs):
                transaction.agent = request.user

            montant = transaction.montant
            if transaction.type_transaction == 'Depot':
                transaction.compte_epargne.solde += montant
            elif transaction.type_transaction == 'Virement':
                transaction.compte_epargne.solde += montant
            elif transaction.type_transaction == 'Retrait':
                transaction.compte_epargne.solde -= montant
            transaction.compte_epargne.save()
            transaction.agent = request.user
            transaction.save()
            return redirect(reverse('detail_actionnaire', args=[idd]))
    else:
        transaction_form = TransactionEpargneactForm(initial={'compte_epargne': id})
    context = {
        'transaction_form': transaction_form,
        'id': id,
    }

    return render(request, 'Pages/Transactionepargneact/creer_transaction_epargne.html', context)

@login_required
def modifier_transaction_epargnesous(request, transaction_id):
    transaction = get_object_or_404(TransactionEpargneact, pk=transaction_id)
    type_avant_modification = transaction.type_transaction
    montant_avant_modification = transaction.montant

    if request.method == 'POST':
        transaction_form = TransactionEpargneactForm(request.POST, instance=transaction)
        if transaction_form.is_valid():
            transaction = transaction_form.save(commit=False)

            if request.user.is_authenticated and isinstance(request.user, Agent):
                transaction.agent = request.user

            montant_apres_modification = transaction.montant

            # Cas 1: Même type de transaction, montant modifié
            if type_avant_modification == transaction.type_transaction and montant_avant_modification != montant_apres_modification:
                ajustement_solde = montant_apres_modification - montant_avant_modification
                if type_avant_modification == 'Depot':
                    transaction.compte_epargne.solde += ajustement_solde
                elif type_avant_modification == 'Retrait':
                    transaction.compte_epargne.solde -= ajustement_solde
                transaction.compte_epargne.save()

            # Cas 2: Même type de transaction, montant inchangé
            elif type_avant_modification == transaction.type_transaction and montant_avant_modification == montant_apres_modification:
                pass  # Aucun ajustement de solde nécessaire

            # Cas 3: Changement de type de transaction, montant inchangé
            elif type_avant_modification != transaction.type_transaction and montant_avant_modification == montant_apres_modification:
                if type_avant_modification == 'Depot':
                    transaction.compte_epargne.solde -= montant_avant_modification
                elif type_avant_modification == 'Retrait':
                    transaction.compte_epargne.solde += montant_avant_modification
                transaction.compte_epargne.save()

                if transaction.type_transaction == 'Depot':
                    transaction.compte_epargne.solde += montant_apres_modification
                elif transaction.type_transaction == 'Retrait':
                    transaction.compte_epargne.solde -= montant_apres_modification
                transaction.compte_epargne.save()

            # Cas 4: Changement de type de transaction et montant modifié
            elif type_avant_modification != transaction.type_transaction and montant_avant_modification != montant_apres_modification:
                ajustement_solde_montant = montant_apres_modification - montant_avant_modification
                ajustement_solde_type = 2 * montant_avant_modification  # ajustement pour le changement de type
                ajustement_solde_total = ajustement_solde_montant + ajustement_solde_type

                

                if transaction.type_transaction == 'Depot':
                    transaction.compte_epargne.solde += ajustement_solde_total
                elif transaction.type_transaction == 'Retrait':
                    transaction.compte_epargne.solde -= ajustement_solde_total
                transaction.compte_epargne.save()

            transaction.save()
            return redirect(reverse('detail_actionnaire', args=[transaction.compte_epargne.actionnaire.id]))
    else:
        transaction_form = TransactionEpargneactForm(instance=transaction)

    context = {
        'transaction_form': transaction_form,
        'transaction_id': transaction_id,
    }
    return render(request, 'Pages/Transactionepargneact/modifier_transaction_epargne.html', context)

# 
def supprimer_transaction_epargnesous(request, transaction_id):
    transaction = get_object_or_404(TransactionEpargne, pk=transaction_id)

    if request.method == 'POST':
        montant = transaction.montant
        if transaction.type_transaction == 'Depot':
            transaction.compte_epargne.solde -= montant
        elif transaction.type_transaction == 'Retrait':
            transaction.compte_epargne.solde += montant
        transaction.compte_epargne.save()
        transaction.delete()
        return redirect(reverse('detail_actionnaire', args=[transaction.compte_epargne.actionnaire.id]))

    context = {
        'transaction': transaction,
    }
    return render(request, 'Pages/Transactionepargneact/supprimer_transaction_epargne.html', context)
#_______________________________________________________________________________________________________________________________________________

# Vue pour créer une transaction de prêt
def creer_transaction_pret(request,id):
    if request.method == 'POST':
        transaction_form = TransactionPretForm(request.POST)
        if transaction_form.is_valid():
            transaction = transaction_form.save(commit=False)
            # Effectuer les opérations spécifiques pour les transactions de prêt
            montant = transaction.montant
            if transaction.type_transaction == 'Depot':
                transaction.compte_pret.solde += montant
            elif transaction.type_transaction == 'Retrait':
                transaction.compte_pret.solde -= montant
            transaction.compte_pret.save()
            transaction.save()
            return redirect('liste_transactionsepargne')
    else:
        transaction_form = TransactionPretForm(initial={'compte_epargne': id})

    context = {
        'transaction_form': transaction_form,
        'id': id,
    }

    return render(request, 'creer_transaction_pret.html', context)



# Vue pour modifier une transaction de prêt
def modifier_transaction_pret(request, pk):
    transaction = get_object_or_404(TransactionPret, pk=pk)
    if request.method == 'POST':
        transaction_form = TransactionPretForm(request.POST, instance=transaction)
        if transaction_form.is_valid():
            transaction = transaction_form.save(commit=False)
            # Effectuer les opérations spécifiques pour les transactions de prêt
            old_type_transaction = TransactionPret.objects.get(pk=transaction.pk).type_transaction
            if transaction.type_transaction == 'Depot':
                # Effectuer les opérations spécifiques au dépôt
                pass
            elif transaction.type_transaction == 'Retrait':
                # Effectuer les opérations spécifiques au retrait
                pass
            elif transaction.type_transaction == 'Virement':
                # Effectuer les opérations spécifiques au virement
                pass
            transaction.save()
            return redirect('liste_transactions')
    else:
        transaction_form = TransactionPretForm(instance=transaction)
    
    return render(request, 'modifier_transaction_pret.html', {'transaction_form': transaction_form})
# _____________________________________________________________________________________________________________________________________________________


# DEPENSES_____________________________________________________________________________________________________________________________________________
def liste_depenses(request):
    depenses = Depense.objects.all()
    return render(request, 'Pages/Depense/liste_depenses.html', {'depenses': depenses})

def ajouter_depense(request):
    if request.method == 'POST':
        form = DepenseForm(request.POST)
        if form.is_valid():
            if request.user.is_authenticated and isinstance(request.user, Utilisateurs):
                form.agent = request.user

            form.instance.agent = request.user
            form.save()

            # Mise à jour du solde du compte principal KHA
            statut_actif = get_object_or_404(Statuts, statut='Actif')
            princ = get_object_or_404(ComptePrincipale, statut=statut_actif)
            princ.totaldepenses += form.instance.montant
            princ.datedepense = timezone.now()  # Conserve la date avec fuseau horaire
            princ.totalgain = ( princ.totalentree - (princ.totalsortie + princ.totaldepenses))
            princ.save()

    
            return redirect('liste_depenses')
    else:
        form = DepenseForm()
    return render(request, 'Pages/Depense/ajouter_depense.html', {'form': form})

def modifier_depense(request, depense_id):
    depense = Depense.objects.get(pk=depense_id)
    ancidep = depense.montant
    if request.method == 'POST':
        form = DepenseForm(request.POST, instance=depense)
        if form.is_valid():
            if request.user.is_authenticated and isinstance(request.user, Utilisateurs):
                form.agent = request.user

            form.instance.agent = request.user
            form.save()

            # Mise à jour du solde du compte principal KHA
            statut_actif = get_object_or_404(Statuts, statut='Actif')
            princ = get_object_or_404(ComptePrincipale, statut=statut_actif)
            princ.totaldepenses += (ancidep - (form.instance.montant))
            princ.datedepense = timezone.now()  # Conserve la date avec fuseau horaire
            princ.totalgain = ( princ.totalentree - (princ.totalsortie + princ.totaldepenses))
            princ.save()

            return redirect('liste_depenses')
    else:
        form = DepenseForm(instance=depense)
    return render(request, 'Pages/Depense/modifier_depense.html', {'form': form})

def supprimer_depense(request, depense_id):
    depense = Depense.objects.get(pk=depense_id)
    if request.method == 'POST':
        depense.delete()
        return redirect('liste_depenses')
    return render(request, 'Pages/Depense/supprimer_depense.html', {'depense': depense})
# _____________________________________________________________________________________________________________________________________________________


#CALCUL BENEFICES ACTIONNAIRES _______________________________________________________________________________________________________________________________
def afficher_resultats(request):

    # Récupérer
    statut_actif = get_object_or_404(Statuts, statut='Actif')
    Conf = Confconstantes.objects.filter(statut=statut_actif).first()
    dureecoopa = Conf.dureecoopa
    dureecoopn = Conf.dureecoopn
    date_today = datetime.now().date()
    date_un_mois_actif = date_today - timedelta(days=dureecoopa)
    date_un_mois_passif = date_today - timedelta(days=dureecoopn)  
    # Récupérer les actionnaires et leurs informations
    actionnaires = Actionnaire.objects.all()

    actionn=actionnaires.count()
    # Récupérer le montant à répartir entre les actionnaires
    actionnaires_type_1 = Actionnaire.objects.filter(type_act_id=1, date_adhesion__gte=date_un_mois_actif)
    #actionnaires_type_2 = Actionnaire.objects.filter(type_act_id=2)
    statut_actif = Statuts.objects.get(statut='Actif')
    actionnaires_type_2 = Actionnaire.objects.filter(
    type_act_id=2 , date_adhesion__gte=date_un_mois_passif, 
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

    # Calculer les parts de chaque actionnaire en pourcentage
    total_apport = sum(actionnaire.apport for actionnaire in actionnaires)
    for actionnaire in actionnaires:
        actionnaire.part = round((actionnaire.apport / total_apport) * 100,2)

    # Calculer le montant à payer à chaque actionnaire en fonction de leur part dans le capital
        # Calcul des parts pour les actionnaires de type 1
    total_apport_type_1 = sum(actionnaire.apport for actionnaire in actionnaires_type_1)
    for actionnaire in actionnaires_type_1:
        actionnaire.part = round((actionnaire.apport / total_apport_type_1) * 100, 2)
        actionnaire.montant_a_payer = round((actionnaire.part / 100) * montant_a_repartir_type_1, 2)

        # Calcul des parts pour les actionnaires de type 2
    total_apport_type_2 = sum(actionnaire.apport for actionnaire in actionnaires_type_2)
    for actionnaire in actionnaires_type_2:
        actionnaire.part = round((actionnaire.apport / total_apport_type_2) * 100, 2)
        actionnaire.montant_a_payer = round((actionnaire.part / 100) * montant_a_repartir_type_2, 2)

    # Passer les données au template
    context = {
        
        'actionnaires': actionnaires,
        'actionnaires_type_1': actionnaires_type_1,
        'actionnaires_type_2': actionnaires_type_2,
        'montant_a_repartir_type_chef' :montant_a_repartir_type_chef,
        'benefice_mois': benefice_mois,
        'depenses_mois': depenses_mois,
        'montant_a_repartir': montant_a_repartir,
        'total_apport':total_apport,
        'actionn' : actionn
    }

    return render(request, 'Pages/Actionnaire/resultats.html', context)

def afficher_resultats1(request):
    # Récupérer les actionnaires et leurs informations
    actionnaires = Actionnaire.objects.all()

    actionn=actionnaires.count()
    # Récupérer le montant à répartir entre les actionnaires
    echeances_payees_mois = Echeancier.objects.filter(date_echeance__month=date.today().month, est_paye=True)
    benefice_mois = sum(echeance.montant_interet for echeance in echeances_payees_mois)
    depenses_mois = Depense.objects.filter(date__month=date.today().month).aggregate(Sum('montant'))['montant__sum'] or 0
    montant_a_repartir = benefice_mois - depenses_mois

    # Calculer les parts de chaque actionnaire en pourcentage
    total_apport = sum(actionnaire.apport for actionnaire in actionnaires)
    for actionnaire in actionnaires:
        actionnaire.part = round((actionnaire.apport / total_apport) * 100,2)

    # Calculer le montant à payer à chaque actionnaire en fonction de leur part dans le capital
    for actionnaire in actionnaires:
        actionnaire.montant_a_payer = round((actionnaire.part / 100) * montant_a_repartir)

    # Passer les données au template
    context = {
        
        'actionnaires': actionnaires,
        'benefice_mois': benefice_mois,
        'depenses_mois': depenses_mois,
        'montant_a_repartir': montant_a_repartir,
        'total_apport':total_apport,
        'actionn' : actionn
    }

    return render(request, 'Pages/Actionnaire/resultats.html', context)

def afficher_dashboard(request):
# MAJ
    # Récupérer l'utilisateur connecté
    user = request.user

    from django.core.exceptions import ObjectDoesNotExist

    try:
        etudian = Actionnaire.objects.get(user=user.id)
        et = etudian.nom + " " + etudian.prenom
        # Obtenez tous les messages avec groupemsg='ALL' ou groupemsg égal à l'ID de l'actionnaire
        messag = Msg.objects.filter(groupemsg='ALL').order_by('-date_msg') | Msg.objects.filter(groupemsg=et).order_by('-date_msg')

        # Obtenez la date d'aujourd'hui
        date_aujourdhui = timezone.now().date()

        # Supposons que vous avez déjà votre requête pour filtrer les messages.
        messages = Msg.objects.filter(groupemsg='ALL').order_by('-date_msg') | Msg.objects.filter(groupemsg=et).order_by('-date_msg')

        # Filtrez les messages pour obtenir ceux qui ont la date d'aujourd'hui
        messages_aujourdhui = messages.filter(date_msg__date=date_aujourdhui)

        # Obtenez le nombre de messages à la date d'aujourd'hui
        nombre_messages_aujourdhui = messages_aujourdhui.count()
        badge_class = "badge rounded-pill" if nombre_messages_aujourdhui == 0 else "badge bg-danger rounded-pill"
    except ObjectDoesNotExist:
        # Gérer le cas où aucun objet Actionnaire n'est trouvé pour l'utilisateur actuel
        etudian = None
        et = ""
        messag = Msg.objects.all().order_by('-date_msg')
        # Obtenez la date d'aujourd'hui
        date_aujourdhui = timezone.now().date()

        # Supposons que vous avez déjà votre requête pour filtrer les messages.
        messages = Msg.objects.all().order_by('-date_msg')

        # Filtrez les messages pour obtenir ceux qui ont la date d'aujourd'hui
        messages_aujourdhui = messages.filter(date_msg__date=date_aujourdhui)

        # Obtenez le nombre de messages à la date d'aujourd'hui
        nombre_messages_aujourdhui = messages_aujourdhui.count()
        badge_class = "badge rounded-pill" if nombre_messages_aujourdhui == 0 else "badge bg-danger rounded-pill"
 
   


    etudact = Actionnaire.objects.get(user=user.id)
    statut_nactif = Statuts.objects.get(statut='Non Actif')
    statut_actif = Statuts.objects.get(statut='Actif')
    comptes_actifsact = ComptePretsact.objects.filter(statut=statut_actif,actionnaire=etudact)
    comptes_nactifsact = ComptePretsact.objects.filter(statut=statut_nactif,actionnaire=etudact)
# Fin MAJ


    # Récupérer les actionnaires et leurs informations
    actionnaires = Actionnaire.objects.all()

    # Récupérer le montant à répartir entre les actionnaires
    echeances_payees_mois = Echeancier.objects.filter(date_echeance__month=date.today().month, est_paye=True)
    echeances_payees_moisact = Echeancieract.objects.filter(date_echeance__month=date.today().month, est_paye=True)
    benefice_mois = sum(echeance.montant_interet for echeance in echeances_payees_mois) + sum(echeance.montant_interet for echeance in echeances_payees_moisact)
    depenses_mois = Depense.objects.filter(date__month=date.today().month).aggregate(Sum('montant'))['montant__sum'] or 0
    montant_a_repartir = benefice_mois - depenses_mois

    # Calculer les parts de chaque actionnaire en pourcentage
    total_apport = sum(actionnaire.apport for actionnaire in actionnaires)
    for actionnaire in actionnaires:
        actionnaire.part = round((actionnaire.apport / total_apport) * 100,2)

    # Calculer le montant à payer à chaque actionnaire en fonction de leur part dans le capital
    for actionnaire in actionnaires:
        actionnaire.montant_a_payer = round((actionnaire.part / 100) * montant_a_repartir)

    # Récupérer les décomptes du nombre d'enseignants de chaque genre depuis la base de données-------------
    male_countens = Clients.objects.filter(sexe='1').count()
    female_countens = Clients.objects.filter(sexe='2').count()

    # Récupérer
    date_today = datetime.now().date()
    date_un_mois_avant = date_today - timedelta(days=30)

    echeances = Echeancier.objects.filter(date_echeance__gte=date_un_mois_avant, date_echeance__lte=date_today)
    total_echeances = echeances.count()
    echeances_payees = echeances.filter(est_paye=True).count()
    # echeances_non_payees = total_echeances - echeances_payees

    echeancesact = Echeancieract.objects.filter(date_echeance__gte=date_un_mois_avant, date_echeance__lte=date_today)
    total_echeancesact = echeancesact.count()
    echeances_payeesact = echeancesact.filter(est_paye=True).count()
    echeances_non_payees = total_echeancesact - echeances_payeesact+total_echeances - echeances_payees

    # Calculer le montant total des prêts actifs avec une durée prévisionnelle--------------
    statut_actif = Statuts.objects.get(statut='Actif')
    total_montant_pret_previsionnel = sum((pret.solde-pret.somme_initiale) for pret in ComptePrets.objects.filter(statut=statut_actif, duree_en_mois__gt=0)) + sum((pret.solde-pret.somme_initiale) for pret in ComptePretsact.objects.filter(statut=statut_actif, duree_en_mois__gt=0))

    # Calculer le montant à payer à chaque actionnaire en fonction de leur part dans le capital et des prêts prévisionnels
    for action in actionnaires:
        action.montant_a_paye = round((action.part / 100) * total_montant_pret_previsionnel)


    # Obtenez la date d'aujourd'hui---------------------------------------------------------------
    # Récupérer le nombre de transactions par type
    depot_count = TransactionEpargne.objects.filter(type_transaction='Depot').count()
    retrait_count = TransactionEpargne.objects.filter(type_transaction='Retrait').count()
    virement_count = TransactionEpargne.objects.filter(type_transaction='Virement').count()
    
    # Récupérer les montants des transactions par type-------------------------------
    depot_amount = TransactionEpargne.objects.filter(type_transaction='Depot').aggregate(total=Sum('montant'))['total'] or 0
    retrait_amount = TransactionEpargne.objects.filter(type_transaction='Retrait').aggregate(total=Sum('montant'))['total'] or 0
    virement_amount = TransactionEpargne.objects.filter(type_transaction='Virement').aggregate(total=Sum('montant'))['total'] or 0

    
        
    
    # Passer les données au template
    context = {
        'depot_count': depot_count,
        'retrait_count': retrait_count,
        'virement_count': virement_count,

        'total_montant_pret_previsionnel': total_montant_pret_previsionnel,  # Ajoutez cette variable au contexte
        'action': action,

        'actionnaires': actionnaires,
        'benefice_mois': benefice_mois,
        'depenses_mois': depenses_mois,
        'montant_a_repartir': montant_a_repartir,

        'male_countens': male_countens,
        'female_countens': female_countens, 

        'echeances_payees': echeances_payees,
        'echeances_non_payees': echeances_non_payees,


        'depot_amount': depot_amount,
        'retrait_amount': retrait_amount,
        'virement_amount': virement_amount,
        # MAJ
        'messag':messag,
        'comptes_actifsact':comptes_actifsact,
        'comptes_nactifsact':comptes_nactifsact,
        'nombre_messages_aujourdhui':nombre_messages_aujourdhui,
        'badge_class':badge_class

        # Fin 
    }

    return render(request, 'Pages/Actionnaire/dashboardact.html', context)
# ___________________________________________________________________________________________________________________________________________________________


# ACTIONNAIRES __________________________________________________________________________________________________________________________________________________
def liste_actionnaires(request):
    actionnaires = Actionnaire.objects.filter(type_act='1')
    return render(request, 'Pages/Actionnaire/liste_actionnaires.html', {'actionnaires': actionnaires})
# -------------------------------------------------------------------------------------------------------------------------------------

# liste actionnaire --------------------------------------------------------------------------------------------------------------------
def liste_actionnairesn(request):
    actionnaires = Actionnaire.objects.filter(type_act='2')
    return render(request, 'Pages/Actionnaire/liste_actionnairesn.html', {'actionnaires': actionnaires})


def detail_actionnaire(request, actionnaire_id):
    actionnaire = get_object_or_404(Actionnaire, id=actionnaire_id)
    return render(request, 'Pages/Actionnaire/detail_actionnaire.html', {'actionnaire': actionnaire})

def ajouter_actionnaire(request):
    if request.method == 'POST':
        form = ActionnaireForm(request.POST)
        if form.is_valid():
            # Créer un utilisateur avec le même nom d'utilisateur et mot de passe que l'actionnaire
            userna = form.cleaned_data['telephone']
            usernam = form.cleaned_data['prenom']
            usernamn = form.cleaned_data['nom']
            FString = userna # + " " + usernam
            username = FString
            role = "ACTIONNAIRE"
            statu = 'NON ACTIVE'
            password = 'P@ssword'
            profile_photo = 'NON ACTIVE'
            encoded_password = make_password(password)
            email = form.cleaned_data['email']
            user = Utilisateurs.objects.create(statut=statu, username=username, last_name=usernam, first_name=usernamn, password=encoded_password, email=email, role=role)
            
            # Récupérer l'instance Typeactionnaire correspondant à type_act='3'
            try:
                type_actionnaire = Typeactionnaire.objects.get(type_act='Actif')
            except Typeactionnaire.DoesNotExist:
                # Gérer le cas où le type d'actionnaire n'existe pas
                return redirect('erreur_page')  # Redirigez vers une page d'erreur ou créez une instance par défaut

            actionnaire = form.save(commit=False)
            actionnaire.type_act = type_actionnaire
            actionnaire.user = user
            actionnaire.dividende = 0
            actionnaire.save()

            # Mise à jour du solde du compte principal KHA
            statut_actif = get_object_or_404(Statuts, statut='Actif')
            princ = get_object_or_404(ComptePrincipale, statut=statut_actif)
            princ.capital += form.instance.apport
            princ.totalentree += form.instance.apport
            princ.totalgain = ( princ.totalentree - (princ.totalsortie + princ.totaldepenses))
            princ.datecapital = timezone.now()  # Conserve la date avec fuseau horaire
            princ.save()

            statu_actif = get_object_or_404(Statuts, statut='Actif')
            Conf = Confconstantes.objects.filter(statut=statu_actif).first()
            taux_com = Conf.partdemarch

            # Mettre à jour la commission
            app = form.cleaned_data['apport']
            com = form.cleaned_data['com']
            comm = Agent.objects.get(id=com.id)

            # Utilisation de get_or_create()
            commission, created = Commissions.objects.get_or_create(agent=comm.user)

            # Mise à jour de la commission
            commission.soldeprecedent = commission.solde
            commission.date_aide = commission.datesolde
            commission.datesolde = timezone.now()
            commission.solde += (app * Decimal(taux_com))
            commission.save()

            # Créer une nouvelle transaction de prêt
            transactioncominv = TransactionCommissioninves.objects.create(
                commissioninv=commission,
                actionnaire=actionnaire,
                montant=(app * Decimal(taux_com)),
                type_transaction='Virement',  # À adapter en fonction de votre logique
                agent=request.user  # Assurez-vous que cela pointe vers l'utilisateur connecté
            )
            
            return redirect('liste_actionnaires')
    else:
        form = ActionnaireForm()

    return render(request, 'Pages/Actionnaire/ajouter_actionnaire.html', {'form': form})
# __________________________________________________________________________________________________________________________________________________________________

# Ajout Actionnaire Passif -------------------------------------------------------------------------------------------------------------------------
def ajouter_actionnairen(request):
    if request.method == 'POST':
        form = ActionnairenForm(request.POST)
        if form.is_valid():
            # Créer un utilisateur avec le même nom d'utilisateur et mot de passe que l'actionnaire
            userna = form.cleaned_data['telephone']
            usernam = form.cleaned_data['prenom']
            usernamn = form.cleaned_data['nom']
            FString = userna # + " " + usernam
            username = FString
            role = "ACTIONNAIRE"
            statu = 'NON ACTIVE'
            password = 'P@ssword'
            profile_photo = 'NON ACTIVE'
            encoded_password = make_password(password)
            email = form.cleaned_data['email']
            user = Utilisateurs.objects.create(statut=statu, username=username, last_name=usernam, first_name=usernamn, password=encoded_password, email=email, role=role)
            
            
            # Récupérer l'instance Typeactionnaire correspondant à type_act='3'
            try:
                type_actionnaire = Typeactionnaire.objects.get(type_act='Passif')
            except Typeactionnaire.DoesNotExist:
                # Gérer le cas où le type d'actionnaire n'existe pas
                return redirect('erreur_page')  # Redirigez vers une page d'erreur ou créez une instance par défaut

            statut_actif = get_object_or_404(Statuts, statut='Actif')

            actionnaire = form.save(commit=False)
            actionnaire.type_act = type_actionnaire
            actionnaire.user = user
            actionnaire.dividende = 0
            actionnaire.save()

            # Mise à jour du solde du compte principal KHA
            statut_actif = get_object_or_404(Statuts, statut='Actif')
            princ = get_object_or_404(ComptePrincipale, statut=statut_actif)
            princ.capital += form.instance.apport
            princ.totalentree += form.instance.apport
            princ.totalgain = ( princ.totalentree - (princ.totalsortie + princ.totaldepenses))
            princ.datecapital = timezone.now()  # Conserve la date avec fuseau horaire
            princ.save()

            CompteEpargnesact.objects.create(actionnaire=actionnaire,solde=0, numero_compte=f"EP{timezone.now().strftime('%Y%m%d%H%M%S')}", statut=statut_actif)

            return redirect('liste_actionnairesn')
    else:
        form = ActionnairenForm()

    return render(request, 'Pages/Actionnaire/ajouter_actionnairen.html', {'form': form})
# _____________________________________________________________________________________________________________________________________________________________

# Modifier actionnaire -----------------------------------------------------------------------------------------------------------
def modifier_actionnaire(request, actionnaire_id):
    actionnaire = get_object_or_404(Actionnaire, id=actionnaire_id)
    ancien_apport = actionnaire.apport

    if request.method == 'POST':
        form = ActionnaireForm(request.POST, instance=actionnaire)
        if form.is_valid():
            form.save()

            # Mise à jour du solde du compte principal KHA
            statut_actif = get_object_or_404(Statuts, statut='Actif')
            princ = get_object_or_404(ComptePrincipale, statut=statut_actif)
            apport = form.cleaned_data['apport']
            ancien_apport = actionnaire.apport

            # Ajuster le capital et les entrées
            princ.capital += (apport - ancien_apport)
            princ.totalentree += (apport - ancien_apport)
            princ.datecapital = timezone.now()
            princ.save()

            # Mise à jour de la commission
            com = form.cleaned_data['com']
            comm = get_object_or_404(Agent, id=com.id)
            taux_com = Confconstantes.objects.filter(statut=statut_actif).first().partdemarch

            # Utilisation de get_or_create()
            commission, created = Commissions.objects.get_or_create(agent=comm.user)

            # Mise à jour de la commission
            commission.soldeprecedent = commission.solde
            commission.date_aide = commission.datesolde
            commission.datesolde = timezone.now()
            commission.solde += (apport * Decimal(taux_com)) - (ancien_apport * Decimal(taux_com))
            commission.save()

            # Créer une nouvelle transaction de commission
            TransactionCommissioninves.objects.create(
                commissioninv=commission,
                actionnaire=actionnaire,
                montant=(apport * Decimal(taux_com)),
                type_transaction='Virement',
                agent=request.user
            )

            
            # Calculer le total des apports après la suppression
            total_apport = Actionnaire.objects.aggregate(Sum('apport'))['apport__sum'] or 0
            # Recalculer les parts des actionnaires restants
            for actionnaire in Actionnaire.objects.all():
                actionnaire.pourcentage = (actionnaire.apport / total_apport) * 100 if total_apport != 0 else 0
                actionnaire.save()

            return redirect('liste_actionnaires')
    else:
        form = ActionnaireForm(instance=actionnaire)

    return render(request, 'Pages/Actionnaire/modifier_actionnaire.html', {'form': form})

def modifier_actionnairen(request, actionnaire_id):
    actionnaire = get_object_or_404(Actionnaire, id=actionnaire_id)
    ancapport = actionnaire.apport

    if request.method == 'POST':
        form = ActionnairenForm(request.POST, instance=actionnaire)
        if form.is_valid():
            form.save()

            # Mise à jour du solde du compte principal KHA
            statut_actif = get_object_or_404(Statuts, statut='Actif')
            princ = get_object_or_404(ComptePrincipale, statut=statut_actif)
            princ.capital += (ancapport - (form.instance.apport))
            princ.totalentree += (ancapport - (form.instance.apport))
            princ.totalgain = ( princ.totalentree - (princ.totalsortie + princ.totaldepenses))
            princ.datecapital = timezone.now()  # Conserve la date avec fuseau horaire
            princ.save()

            # Calculer le total des apports après la suppression
            total_apport = Actionnaire.objects.aggregate(Sum('apport'))['apport__sum'] or 0
            # Recalculer les parts des actionnaires restants
            for actionnaire in Actionnaire.objects.all():
                actionnaire.pourcentage = (actionnaire.apport / total_apport) * 100 if total_apport != 0 else 0
                actionnaire.save()
            return redirect('liste_actionnairesn')
    else:
        form = ActionnairenForm(instance=actionnaire)

    return render(request, 'Pages/Actionnaire/modifier_actionnairen.html', {'form': form})
# _____________________________________________________________________________________________________________________________________________________________

# SUPPRIMER UN COOPERATEUR---------------------------------------------------------------------------------------------------------------------
from django.db.models import Sum  # Importer la classe Sum depuis le module django.db.models
def supprimer_actionnaire(request, actionnaire_id):
    try:
        # Récupérer l'actionnaire à supprimer
        agent = get_object_or_404(Actionnaire, pk=actionnaire_id)

        if request.method == 'POST':
            # Supprimer l'utilisateur associé à l'actionnaire
            agent.user.delete()
            # Calculer le total des apports après la suppression
            total_apport = Actionnaire.objects.aggregate(Sum('apport'))['apport__sum'] or 0
            # Recalculer les parts des actionnaires restants
            for actionnaire in Actionnaire.objects.all():
                actionnaire.pourcentage = (actionnaire.apport / total_apport) * 100 if total_apport != 0 else 0
                actionnaire.save()
            # Supprimer l'actionnaire lui-même
            agent.delete()
            # Rediriger vers la liste des actionnaires après la suppression
            return redirect('liste_actionnaires')

        # Réduire le capital et les entrées du compte principal KHA
        statut_actif = get_object_or_404(Statuts, statut='Actif')
        princ = get_object_or_404(ComptePrincipale, statut=statut_actif)
        
        # Soustraire l'apport de l'actionnaire du capital et des entrées totales
        princ.capital -= actionnaire.apport
        princ.totalentree -= actionnaire.apport
        princ.totalgain = ( princ.totalentree - (princ.totalsortie + princ.totaldepenses))
        princ.datecapital = timezone.now()  # Mettre à jour la date de la dernière modification
        princ.save()

        # Si la méthode de la requête n'est pas POST, afficher la page de confirmation de suppression
        return render(request, 'Pages/Actionnaire/supprimer_actionnaire.html', {'agent': agent})

    except Http404:
        # Gérer l'erreur 404 si l'actionnaire n'est pas trouvé
        return render(request, '404/404.html', status=404)
    except Exception as e:
        # Gérer toutes les autres exceptions
        return render(request, '500/500.html', status=500)
#------------------------------------------------------------------------------------------------------------------------------------------------
def supprimer_actionnairen(request, actionnaire_id):
    try:
        # Récupérer l'actionnaire à supprimer
        agent = get_object_or_404(Actionnaire, pk=actionnaire_id)

        if request.method == 'POST':
            # Supprimer l'utilisateur associé à l'actionnaire
            agent.user.delete()
            # Calculer le total des apports après la suppression
            total_apport = Actionnaire.objects.aggregate(Sum('apport'))['apport__sum'] or 0
            # Recalculer les parts des actionnaires restants
            for actionnaire in Actionnaire.objects.all():
                actionnaire.pourcentage = (actionnaire.apport / total_apport) * 100 if total_apport != 0 else 0
                actionnaire.save()
            # Supprimer l'actionnaire lui-même
            agent.delete()
            # Rediriger vers la liste des actionnaires après la suppression
            return redirect('liste_actionnairesn')

        # Réduire le capital et les entrées du compte principal KHA
        statut_actif = get_object_or_404(Statuts, statut='Actif')
        princ = get_object_or_404(ComptePrincipale, statut=statut_actif)
        
        # Soustraire l'apport de l'actionnaire du capital et des entrées totales
        princ.capital -= actionnaire.apport
        princ.totalentree -= actionnaire.apport
        princ.totalgain = ( princ.totalentree - (princ.totalsortie + princ.totaldepenses))
        princ.datecapital = timezone.now()  # Mettre à jour la date de la dernière modification
        princ.save()

        
        # Si la méthode de la requête n'est pas POST, afficher la page de confirmation de suppression
        return render(request, 'Pages/Actionnaire/supprimer_actionnaire.html', {'agent': agent})

    except Http404:
        # Gérer l'erreur 404 si l'actionnaire n'est pas trouvé
        return render(request, '404/404.html', status=404)
    except Exception as e:
        # Gérer toutes les autres exceptions
        return render(request, '500/500.html', status=500)
# __________________________________________________________________________________________________________________________________________________________


from django.db.models import Sum

def courbe_transactions(request):
    # MAJ
    # Récupérer l'utilisateur connecté
    user = request.user

    from django.core.exceptions import ObjectDoesNotExist

    try:
        etudian = Actionnaire.objects.get(user=user.id)
        et = etudian.nom + " " + etudian.prenom
        # Obtenez tous les messages avec groupemsg='ALL' ou groupemsg égal à l'ID de l'actionnaire
        messag = Msg.objects.filter(groupemsg='ALL').order_by('-date_msg') | Msg.objects.filter(groupemsg=et).order_by('-date_msg')

        # Obtenez la date d'aujourd'hui
        date_aujourdhui = timezone.now().date()

        # Supposons que vous avez déjà votre requête pour filtrer les messages.
        messages = Msg.objects.filter(groupemsg='ALL').order_by('-date_msg') | Msg.objects.filter(groupemsg=et).order_by('-date_msg')

        # Filtrez les messages pour obtenir ceux qui ont la date d'aujourd'hui
        messages_aujourdhui = messages.filter(date_msg__date=date_aujourdhui)

        # Obtenez le nombre de messages à la date d'aujourd'hui
        nombre_messages_aujourdhui = messages_aujourdhui.count()
        badge_class = "badge rounded-pill" if nombre_messages_aujourdhui == 0 else "badge bg-danger rounded-pill"
    except ObjectDoesNotExist:
        # Gérer le cas où aucun objet Actionnaire n'est trouvé pour l'utilisateur actuel
        etudian = None
        et = ""
        messag = Msg.objects.all().order_by('-date_msg')
        # Obtenez la date d'aujourd'hui
        date_aujourdhui = timezone.now().date()

        # Supposons que vous avez déjà votre requête pour filtrer les messages.
        messages = Msg.objects.all().order_by('-date_msg')

        # Filtrez les messages pour obtenir ceux qui ont la date d'aujourd'hui
        messages_aujourdhui = messages.filter(date_msg__date=date_aujourdhui)

        # Obtenez le nombre de messages à la date d'aujourd'hui
        nombre_messages_aujourdhui = messages_aujourdhui.count()
        badge_class = "badge rounded-pill" if nombre_messages_aujourdhui == 0 else "badge bg-danger rounded-pill"
 
   


    

# Fin MAJ
    # Récupérer les décomptes du nombre d'enseignants de chaque genre depuis la base de données-------------
    male_countens = Clients.objects.filter(sexe='1').count()
    female_countens = Clients.objects.filter(sexe='2').count()

    # Récupérer
    date_today = datetime.now().date()
    date_un_mois_avant = date_today - timedelta(days=30)

    echeances = Echeancier.objects.filter(date_echeance__gte=date_un_mois_avant, date_echeance__lte=date_today)
    total_echeances = echeances.count()
    echeances_payees = echeances.filter(est_paye=True).count()
    echeances_non_payees = total_echeances - echeances_payees

     # Récupérer le nombre de transactions par type
    depot_count = TransactionEpargne.objects.filter(type_transaction='Depot').count()
    retrait_count = TransactionEpargne.objects.filter(type_transaction='Retrait').count()
    virement_count = TransactionEpargne.objects.filter(type_transaction='Virement').count()
    
    # Récupérer les montants des transactions par type-------------------------------
    depot_amount = TransactionEpargne.objects.filter(type_transaction='Depot').aggregate(total=Sum('montant'))['total'] or 0
    retrait_amount = TransactionEpargne.objects.filter(type_transaction='Retrait').aggregate(total=Sum('montant'))['total'] or 0
    virement_amount = TransactionEpargne.objects.filter(type_transaction='Virement').aggregate(total=Sum('montant'))['total'] or 0

    # Récupérer les données des transactions d'épargne------------------------------------
    # Calculer la date de début et la date de fin pour l'intervalle d'un mois
    aujourd_hui = datetime.today()
    mois_precedent = aujourd_hui - timedelta(days=30)  # Interval d'un mois environ

    # Récupérer les transactions d'épargne pour l'intervalle d'un mois
    transactions = TransactionEpargne.objects.filter(date_transaction__gte=mois_precedent)

    # Préparer les données pour le graphique à barres
    transactions_data = {}
    for transaction in transactions:
        date = transaction.date_transaction.strftime('%Y-%m-%d')
        if date not in transactions_data:
            transactions_data[date] = {'Depot': 0, 'Retrait': 0, 'Virement': 0}
        transactions_data[date][transaction.type_transaction] += float(transaction.montant)

    # Calculer la date de début et la date de fin pour l'intervalle d'un mois-------------------------
    aujourdhui = datetime.today()
    mois_precedent = aujourdhui - timedelta(days=30)

    # Récupérer les transactions de prêt pour l'intervalle d'un mois
    transactions_pret = TransactionPret.objects.filter(date_transaction__gte=mois_precedent)

    # Préparer les données pour le graphique à barres
    transactions_pret_data = {}
    for transaction in transactions_pret:
        date = transaction.date_transaction.strftime('%Y-%m-%d')
        if date not in transactions_pret_data:
            transactions_pret_data[date] = {'Depot': 0, 'Retrait': 0, 'Virement': 0}
        transactions_pret_data[date][transaction.type_transaction] += float(transaction.montant)

    # Récupérer-------------

    context = {
        'male_countens': male_countens,
        'female_countens': female_countens,

        'echeances_payees': echeances_payees,
        'echeances_non_payees': echeances_non_payees,

        'depot_amount': depot_amount,
        'retrait_amount': retrait_amount,
        'virement_amount': virement_amount,

        'depot_count': depot_count,
        'retrait_count': retrait_count,
        'virement_count': virement_count,

        'transactions_data': transactions_data,

        'transactions_pret_data': transactions_pret_data,
        # MAJ
        'messag':messag,
        'nombre_messages_aujourdhui':nombre_messages_aujourdhui,
        'badge_class':badge_class
        # Fin
    }
    
    return render(request, 'Pages/Dashboard/dashboard.html',context)

# MAJ 1
# message admin a un actionnaire
def soumettre_message(request, actionnaire_id):
    actionnaire = get_object_or_404(Actionnaire, id=actionnaire_id)

    if request.method == 'POST':
        form = MessagesForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.groupemsg = actionnaire  # Utilisez l'ID de l'actionnaire
            message.save()
            form = MessagesForm()  # Réinitialisez le formulaire
            return redirect('liste_actionnaires')
    else:
        form = MessagesForm()

    return render(request, 'Pages/Actionnaire/message.html', {'form': form})

# message admin a tous les actionnaires
def soumettre_messageact(request):
    
    if request.method == 'POST':
        form = MessagesForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.groupemsg = 'ALL'  # Utilisez l'ID de l'actionnaire
            message.save()
            form = MessagesForm()  # Réinitialisez le formulaire
            return redirect('listemessages')
    else:
        form = MessagesForm()

    return render(request, 'Pages/Actionnaire/messageact.html', {'form': form})

# message d'un actionnaire au gérant
def soumettre_messageactger(request):
    user = request.user

    # Vérifier si l'utilisateur est un actionnaire
    
    etudian = Actionnaire.objects.get(user=user.id)
    if request.method == 'POST':
        form = MessagesForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.groupemsg = etudian  # Utilisez l'ID de l'actionnaire
            message.save()
            form = MessagesForm()  # Réinitialisez le formulaire
            return redirect('menuact')
    else:
        form = MessagesForm()

    return render(request, 'Pages/Actionnaire/messageactger.html', {'form': form})

def listemessage(request):
    messages = Msg.objects.all()
    return render(request, 'Pages/Actionnaire/listemessages.html', {'messages': messages})

def modifiermessage(request, msg_id):
    msg = get_object_or_404(Msg, id=msg_id)

    if request.method == 'POST':
        form = MessagesForm(request.POST, instance=msg)
        if form.is_valid():
            form.save()
            return redirect('listemessages')
    else:
        form = MessagesForm(instance=msg)

    return render(request, 'Pages/Actionnaire/modifiermessage.html', {'form': form})


def supprimermessage(request, msg_id):
    try:
        agent = get_object_or_404(Msg, pk=msg_id)
        if request.method == 'POST':
            agent.delete()
            return redirect('listemessages')
        return render(request, 'Pages/Actionnaire/supprimermessage.html', {'agent': agent})
    
        # Votre logique de suppression d'actionnaire ici
    
    except Http404:
        return render(request, '404/404.html', status=404)
    except Exception as e:
        return render(request, '500/500.html', status=500)
    

# SPONSORS ____________________________________________________________________________________________________________________________________________________
# liste sponsor
def liste_sponsors(request):
    actionnaires = Sponsors.objects.filter(type_act='3')
    return render(request, 'Pages/Sponsors/liste_actionnairess.html', {'actionnaires': actionnaires})

# ajouter sponsor
def ajouter_actionnaires(request):
    if request.method == 'POST':
        form = SponsorForm(request.POST)
        if form.is_valid():
            # Créer un utilisateur avec les informations du formulaire
            userna = form.cleaned_data['nom']
            usernam = form.cleaned_data['prenom']
            FString = form.cleaned_data['telephone']
            username = FString
            role = "SPONSOR"
            statu = 'NON ACTIVE'
            password = 'P@ssword'
            encoded_password = make_password(password)
            email = form.cleaned_data['email']
            user = Utilisateurs.objects.create(
                statut=statu, 
                username=username, 
                last_name=usernam, 
                first_name=userna, 
                password=encoded_password, 
                email=email, 
                role=role
            )
            
            # Récupérer l'instance Typeactionnaire correspondant à type_act='3'
            try:
                type_actionnaire = Typeactionnaire.objects.get(type_act='Sponsor')
            except Typeactionnaire.DoesNotExist:
                # Gérer le cas où le type d'actionnaire n'existe pas
                return redirect('erreur_page')  # Redirigez vers une page d'erreur ou créez une instance par défaut

            actionnaire = form.save(commit=False)
            actionnaire.type_act = type_actionnaire
            actionnaire.user = user
            actionnaire.apport = 0
            #actionnaire.pourcentage = 0
            actionnaire.dividende = 0
            actionnaire.save()
            
            return redirect('liste_sponsors')
    else:
        form = SponsorForm()

    return render(request, 'Pages/Sponsors/ajouter_actionnaires.html', {'form': form})
# _____________________________________________________________________________________________________________________________________________________________


# CONTRAT SPONSORS _____________________________________________________________________________________________________________________________________________
def ajouter_contrat_pret(request, sponsor_id):
    try:
        typp = Typeprets.objects.get(id=3)
        statut_actif = Statuts.objects.get(statut='Actif')
        nat_client = Natclients.objects.get(nat_client='Sponsor')
    except (Typeprets.DoesNotExist, Statuts.DoesNotExist, Natclients.DoesNotExist):
        return redirect('erreur_page')

    if request.method == 'POST':
        form = ContratSponsorForm(request.POST)
        if form.is_valid():
            agent = None
            if request.user.is_authenticated and isinstance(request.user, Utilisateurs):
                agent = request.user

            # Création de l'utilisateur
            user = Utilisateurs.objects.create(
                statut='ACTIVE',
                username=form.cleaned_data['telephone'],
                last_name=form.cleaned_data['prenom'],
                first_name=form.cleaned_data['nom'],
                password=make_password('P@ssword'),
                email=form.cleaned_data['email'],
                role='CLIENT'
            )

            # Création du client
            client = Clients.objects.create(
                nom=form.cleaned_data['nom'],
                prenom=form.cleaned_data['prenom'],
                adresse=form.cleaned_data['adresse'],
                telephone=form.cleaned_data['telephone'],
                sexe=form.cleaned_data['sexe'],
                statut=statut_actif,
                email=form.cleaned_data['email'],
                date_inscription=timezone.now(),
                photo=form.cleaned_data['photo'],
                piece_identite_scan=form.cleaned_data['piece_identite_scan'],
                profession=form.cleaned_data['profession'],
                date_naissance=form.cleaned_data['date_naissance'],
                lieu_naissance=form.cleaned_data['lieu_naissance'],
                type_piece_identite=form.cleaned_data['type_piece_identite'],
                numero_piece_identite=form.cleaned_data['numero_piece_identite'],
                validite_piece_identite_debut=form.cleaned_data['validite_piece_identite_debut'],
                validite_piece_identite_fin=form.cleaned_data['validite_piece_identite_fin'],
                ville_village=form.cleaned_data['ville_village'],
                matrimoniale=form.cleaned_data['matrimoniale'],
                user=user,
                nat_client=nat_client
            )

            # Création du compte épargne
            CompteEpargnes.objects.create(
                client=client,
                numero_compte=f"CE{timezone.now().strftime('%Y%m%d%H%M%S')}",
                solde=Decimal('0.00'),
                statut=statut_actif,
                naturecompte=f"CLIENTSPONSOR"
            )

            # Calcul du solde et des intérêts
            somme_initiale = form.cleaned_data['somme_initiale']
            duree_en_mois = form.cleaned_data['duree_en_mois']
            taux_interet = form.cleaned_data['taux_interet'] / 100
            taux_garantie = 15 / 100
            statut_actif = get_object_or_404(Statuts, statut='Actif')
            Conf = Confconstantes.objects.filter(statut=statut_actif).first()
            taux_kha = Conf.partepargne
            taux_khaa = Conf.partfraisdos

            if typp.id == 1:  # TYPE DE PRET avec versement d’une garantie
                interets = somme_initiale * Decimal(taux_interet) * duree_en_mois
            elif typp.id == 2:  # TYPE DE PRET sans versement de la garantie au préalable
                interets = (somme_initiale * Decimal(taux_garantie)) + somme_initiale * Decimal(taux_interet) * 10  # 10 mois de remboursement par défaut
            elif typp.id == 3:  # TYPE DE PRET le client ayant un compte avec KHA
                interets = somme_initiale * Decimal(taux_interet) * duree_en_mois
            else:
                interets = 0

            duree_contrat = form.cleaned_data['duree_contrat']
            solde = somme_initiale + interets + (somme_initiale * Decimal(taux_kha)) + (somme_initiale * Decimal(taux_khaa))
            date_fin_pret = form.cleaned_data['date_debut_pret'] + timedelta(days=30 * duree_en_mois)
            date_fin_contrat = form.cleaned_data['date_debut_pret'] + timedelta(days=30 * duree_contrat)

            # Création du compte de prêt
            compte_pret = ComptePrets.objects.create(
                client=client,
                numero_compte=f"PR{timezone.now().strftime('%Y%m%d%H%M%S')}",
                solde=solde,
                taux_interet=form.cleaned_data['taux_interet'],
                duree_en_mois=duree_en_mois,
                date_debut_pret=form.cleaned_data['date_debut_pret'],
                agent=request.user,
                date_fin_pret=date_fin_pret,
                somme_initiale=somme_initiale,
                domicile_bancaire=form.cleaned_data['domicile_bancaire'],
                type_pret=typp,
                date_demande=timezone.now(),
                statut=statut_actif,
                type_client=form.cleaned_data['type_client'],
                com=form.cleaned_data['com'],
                naturecompte=f"CLIENTSPONSOR"
            )


            # Calculer les détails des échéances
            montant_echeance, montant_interet, montant_epargne, montant_adhesion = form.calculate_echeance(compte_pret, interets)

            # Sauvegarder l'instance de ComptePrets et créer les échéances
            #compte_pret.save()

            echeances = compte_pret.calculer_echeances()
            for echeance in echeances:
                Echeancier.objects.create(
                    compte_pret=compte_pret,  # Assurez-vous que ceci est bien l'instance de ComptePrets
                    date_echeance=echeance,
                    montant_echeance=montant_echeance,
                    montant_interet=montant_interet,
                    montant_epargne=montant_epargne,
                    montant_adhesion=montant_adhesion,
                )


            # Compte le sponor
            spon = get_object_or_404(Sponsors, id=sponsor_id)
            spon.apport += Decimal(somme_initiale )
            spon.dividende += somme_initiale + (somme_initiale * (Decimal(spon.pourcentage)/100))
            spon.save()

            # Enregistrement du formulaire
            form.instance.client = client
            form.instance.nat_client = nat_client
            form.instance.numero_compte = compte_pret.numero_compte
            form.instance.numero_contrat = f"SP{timezone.now().strftime('%Y%m%d%H%M%S')}"
            form.instance.date_demande = timezone.now()
            form.instance.date_inscription = timezone.now()
            form.instance.statut = statut_actif
            form.instance.solde = solde
            form.instance.date_fin_pret = date_fin_pret
            form.instance.date_fin_contrat = date_fin_contrat
            form.instance.soldecontrat = somme_initiale + (somme_initiale * (Decimal(spon.pourcentage)/100))
            form.save()

            return redirect('liste_sponsors')

    else:
        form = ContratSponsorForm(initial={'sponsor': sponsor_id, 'type_pret': typp})

    context = {
        'form': form,
        'client': sponsor_id,
        'etud': Sponsors.objects.filter(id=sponsor_id)
    }
    return render(request, 'Pages/Sponsors/creer_contrat.html', context)

# Contrat ancien client -------------------------------------------------------------------------------------------------------------
def ajouter_contrat_pretac(request, sponsor_id):
    print(f"Received request with sponsor_id: {sponsor_id}")
    try:
        typp = Typeprets.objects.get(id=3)
        statut_actif = Statuts.objects.get(statut='Actif')
        nat_client = Natclients.objects.get(nat_client='Sponsor')
    except (Typeprets.DoesNotExist, Statuts.DoesNotExist, Natclients.DoesNotExist):
        return redirect('erreur_page')

    if request.method == 'POST':
        form = ContratSponsoracForm(request.POST)
        if form.is_valid():
            agent = None

            if request.user.is_authenticated and isinstance(request.user, Utilisateurs):
                agent = request.user

            client = Clients.objects.get(id=form.cleaned_data['client'].id)
            
            
        
            # Création du compte épargne
            CompteEpargnes.objects.create(
                client=client,
                numero_compte=f"CE{timezone.now().strftime('%Y%m%d%H%M%S')}",
                solde=Decimal('0.00'),
                statut=statut_actif,
                naturecompte=f"CLIENTSPONSOR"
            )

            # Calcul du solde et des intérêts
            somme_initiale = form.cleaned_data['somme_initiale']
            duree_en_mois = form.cleaned_data['duree_en_mois']
            taux_interet = form.cleaned_data['taux_interet'] / 100
            taux_garantie = 15 / 100
            statut_actif = get_object_or_404(Statuts, statut='Actif')
            Conf = Confconstantes.objects.filter(statut=statut_actif).first()
            taux_kha = Conf.partepargne
            taux_khaa = Conf.partfraisdos

            if typp.id == 1:  # TYPE DE PRET avec versement d’une garantie
                interets = somme_initiale * Decimal(taux_interet) * duree_en_mois
            elif typp.id == 2:  # TYPE DE PRET sans versement de la garantie au préalable
                interets = (somme_initiale * Decimal(taux_garantie)) + somme_initiale * Decimal(taux_interet) * 10  # 10 mois de remboursement par défaut
            elif typp.id == 3:  # TYPE DE PRET le client ayant un compte avec KHA
                interets = somme_initiale * Decimal(taux_interet) * duree_en_mois
            else:
                interets = 0

            duree_contrat = form.cleaned_data['duree_contrat']
            solde = somme_initiale + interets + (somme_initiale * Decimal(taux_kha)) + (somme_initiale * Decimal(taux_khaa))
            date_fin_pret = form.cleaned_data['date_debut_pret'] + timedelta(days=30 * duree_en_mois)
            date_fin_contrat = form.cleaned_data['date_debut_pret'] + timedelta(days=30 * duree_contrat)

            # Création du compte de prêt
            compte_pret = ComptePrets.objects.create(
                client=client,
                numero_compte=f"PR{timezone.now().strftime('%Y%m%d%H%M%S')}",
                solde=solde,
                taux_interet=form.cleaned_data['taux_interet'],
                duree_en_mois=duree_en_mois,
                date_debut_pret=form.cleaned_data['date_debut_pret'],
                agent=request.user,
                date_fin_pret=date_fin_pret,
                somme_initiale=somme_initiale,
                domicile_bancaire=form.cleaned_data['domicile_bancaire'],
                type_pret=typp,
                date_demande=timezone.now(),
                statut=statut_actif,
                type_client=form.cleaned_data['type_client'],
                com=form.cleaned_data['com'],
                naturecompte=f"CLIENTSPONSOR"
            )


            # Calculer les détails des échéances
            montant_echeance, montant_interet, montant_epargne ,montant_adhesion = form.calculate_echeance(compte_pret, interets)

            # Sauvegarder l'instance de ComptePrets et créer les échéances
            #compte_pret.save()

            echeances = compte_pret.calculer_echeances()
            for echeance in echeances:
                Echeancier.objects.create(
                    compte_pret=compte_pret,  # Assurez-vous que ceci est bien l'instance de ComptePrets
                    date_echeance=echeance,
                    montant_echeance=montant_echeance,
                    montant_interet=montant_interet,
                    montant_epargne=montant_epargne,
                    montant_adhesion=montant_adhesion
                )


            # Compte le sponor
            spon = get_object_or_404(Sponsors, id=sponsor_id)
            spon.apport += Decimal(somme_initiale )
            spon.dividende += somme_initiale + (somme_initiale *  (Decimal(spon.pourcentage)/100))
            spon.save()


            nom=client.nom
            prenom=client.prenom
            adresse=client.adresse
            telephone=client.telephone
            sexe=client.sexe
            email=client.email
            photo=client.photo
            piece_identite_scan=client.piece_identite_scan
            profession=client.profession
            date_naissance=client.date_naissance
            lieu_naissance=client.lieu_naissance
            type_piece_identite=client.type_piece_identite
            numero_piece_identite=client.numero_piece_identite
            validite_piece_identite_debut=client.validite_piece_identite_debut
            validite_piece_identite_fin=client.validite_piece_identite_fin
            ville_village=client.ville_village
            matrimoniale=client.matrimoniale
            nat_client=nat_client
            # Enregistrement du formulaire
             #form.instance.client = client
            form.instance.nat_client = nat_client
            form.instance.numero_compte = compte_pret.numero_compte
            form.instance.numero_contrat = f"SP{timezone.now().strftime('%Y%m%d%H%M%S')}"
            form.instance.date_demande = timezone.now()
            form.instance.date_inscription = timezone.now()
            form.instance.statut = statut_actif
            form.instance.solde = solde
            form.instance.date_fin_pret = date_fin_pret
            form.instance.date_fin_contrat = date_fin_contrat
            form.instance.soldecontrat = somme_initiale + (somme_initiale * (Decimal(spon.pourcentage)/100))
            form.save()      

            return redirect('liste_sponsors')

    else:
        form = ContratSponsoracForm(initial={'sponsor': sponsor_id, 'type_pret': typp})

    context = {
        'form': form,
        'etud': Sponsors.objects.filter(id=sponsor_id)
    }
    return render(request, 'Pages/Sponsors/creer_contratac.html', context)
#______________________________________________________________________________________________________________________________________________________________


#__________________________________________________________________________________________________________________________________________________
from django.http import JsonResponse
from .models import Clients

def get_client_name(request):
    client_id = request.GET.get('client_id')
    if client_id:
        try:
            client = Clients.objects.get(id=client_id)
            return JsonResponse({'nom': client.nom})
        except Clients.DoesNotExist:
            return JsonResponse({'error': 'Client not found'}, status=404)
    return JsonResponse({'error': 'Client ID not provided'}, status=400)
#______________________________________________________________________________________________________________________________________________________________

# COMPTE PRET DES ACTIONNAIRES   _______________________________________________________________________________________________________________________________
def ajouter_compte_pretactT(request):
    user = request.user
    # Vérifier si l'utilisateur est un actionnaire
    etudian = Actionnaire.objects.get(user=user.id)
    typp = Typeprets.objects.get(id=3)
    nombre = ComptePretsact.objects.count()
    if request.method == 'POST':
        form = ComptePretactForm(request.POST)
        if form.is_valid():
            statut_actif = Statuts.objects.get(statut='Non Actif')
            typ = Typeprets.objects.get(id=3)
            form.instance.statut = statut_actif
            
            compte_pret = form.save(commit=False)
            compte_pret.client_id = etudian  # Associer le compte prêt au client spécifié par l'ID
            compte_pret.date_demande = date.today()
            compte_pret.numero_compte='HP' + str(nombre+1)
            
            # Calculer la date de fin en fonction de la date de début et de la durée en mois
            duree_en_mois = form.cleaned_data['duree_en_mois']
            compte_pret.date_fin_pret = compte_pret.date_debut_pret + timedelta(days=30 * duree_en_mois)

            # Calculer les intérêts en fonction du type de prêt
            somme_initiale = compte_pret.somme_initiale
            taux_interet = compte_pret.taux_interet / 100
            taux_garantie = 15 / 100
            taux_kha = 75 / 100
            duree_en_mois = compte_pret.duree_en_mois

            if compte_pret.type_pret_id == 1:  # TYPE DE PRET avec versement d’une garantie
                interets = somme_initiale * Decimal(taux_interet) * duree_en_mois
            elif compte_pret.type_pret_id == 2:  # TYPE DE PRET sans versement de la garantie au préalable
                interets = (somme_initiale *Decimal(taux_garantie))+somme_initiale * Decimal(taux_interet) * 10  # 10 mois de remboursement par défaut
            elif compte_pret.type_pret_id == 3:  # TYPE DE PRET le client ayant un compte avec KHA
                interets = somme_initiale * Decimal(taux_interet) * duree_en_mois
            else:
                interets = 0

            compte_pret.solde = somme_initiale + interets + (somme_initiale *Decimal(taux_kha))
            # Calcul des échéances
            compte_pret.save()
            
            return redirect('menuact')

    else:
        form = ComptePretactForm(initial={'actionnaire': etudian,'type_pret':typp})

    context = {
        'form': form,
        'actionnaire': etudian,  # Passer l'ID du client dans le contexte pour l'utiliser dans le formulaire
        
    }
    return render(request, 'Pages/Comptepretact/ajouter_compte_pret.html', context)


#------------------------------------------------------------------------------------------------------------------------------------------
def ajouter_compte_pretact(request):
    user = request.user
    
    # Vérifier si l'utilisateur est un actionnaire
    etudian = Actionnaire.objects.filter(user=user).first()
    if not etudian:
        return redirect('error_page')  # Rediriger vers une page d'erreur si l'utilisateur n'est pas un actionnaire

    typp = Typeprets.objects.filter(id=3).first()
    if not typp:
        return redirect('error_page')  # Rediriger vers une page d'erreur si le type de prêt n'est pas trouvé

    nombre = ComptePretsact.objects.count()

    if request.method == 'POST':
        form = ComptePretactForm(request.POST)
        if form.is_valid():
            statut_actif = Statuts.objects.filter(statut='Non Actif').first()
            if not statut_actif:
                return redirect('error_page')  # Rediriger vers une page d'erreur si le statut actif n'est pas trouvé

            form.instance.statut = statut_actif
            if request.user.is_authenticated and isinstance(request.user, Utilisateurs):
                agent = request.user

    
            form.instance.agent=request.user  # Assurez-vous que cela pointe vers l'utilisateur connecté

            compte_pret = form.save(commit=False)
            compte_pret.client = etudian  # Associer le compte prêt au client spécifié par l'ID
            compte_pret.date_demande = timezone.now()
            compte_pret.numero_compte = f"PR{timezone.now().strftime('%Y%m%d%H%M%S')}"
            
            # Calculer la date de fin en fonction de la date de début et de la durée en mois
            duree_en_mois = form.cleaned_data.get('duree_en_mois')
            if duree_en_mois:
                compte_pret.date_fin_pret = compte_pret.date_debut_pret + timedelta(days=30 * duree_en_mois)

            # Calculer les intérêts en fonction du type de prêt
            somme_initiale = compte_pret.somme_initiale
            taux_interet = compte_pret.taux_interet / 100
            taux_garantie = 15 / 100
            statut_actif = get_object_or_404(Statuts, statut='Actif')
            Conf = Confconstantes.objects.filter(statut=statut_actif).first()
            taux_kha = Conf.partepargnesous
            taux_khaa = Conf.partfraisdossous

            # Mise à jour du solde du compte portefeuilles KHA
            statut_actif = get_object_or_404(Statuts, statut='Actif')
            porte = get_object_or_404(ComptePortefeuilles, statut=statut_actif)
            porte.totalsortie += somme_initiale
            porte.totalreste = (porte.totalentree - somme_initiale)
            porte.save()

            # Mise à jour du solde du compte principal KHA
            statut_actif = get_object_or_404(Statuts, statut='Actif')
            princ = get_object_or_404(ComptePrincipale, statut=statut_actif)
            princ.totalsortie += somme_initiale
            princ.datesortie = timezone.now()  # Conserve la date avec fuseau horaire
            princ.save()

            if compte_pret.type_pret.id == 1:  # TYPE DE PRET avec versement d’une garantie
                interets = somme_initiale * Decimal(taux_interet) * duree_en_mois
            elif compte_pret.type_pret.id == 2:  # TYPE DE PRET sans versement de la garantie au préalable
                interets = (somme_initiale * Decimal(taux_garantie)) + somme_initiale * Decimal(taux_interet) * 10  # 10 mois de remboursement par défaut
            elif compte_pret.type_pret.id == 3:  # TYPE DE PRET le client ayant un compte avec KHA
                interets = somme_initiale * Decimal(taux_interet) * duree_en_mois
            else:
                interets = 0

            compte_pret.solde = somme_initiale + interets + (somme_initiale * Decimal(taux_kha)) + (somme_initiale * Decimal(taux_khaa))
            compte_pret.save()

            return redirect('menuact')

    else:
        form = ComptePretactForm(initial={'actionnaire': etudian, 'type_pret': typp})

    context = {
        'form': form,
        'actionnaire': etudian,
    }
    return render(request, 'Pages/Comptepretact/ajouter_compte_pret.html', context)


        #API___ Juillet 2


def liste_comptes_pretsact(request):
    comptes_prets = ComptePretsact.objects.all()
    return render(request, 'Pages/Comptepretact/liste_comptes_prets.html', {'comptes_prets': comptes_prets})

def liste_comptes_pretsactenc(request):
    comptes_prets = ComptePretsact.objects.filter(statut=2)
    return render(request, 'Pages/Comptepretact/liste_comptes_prets.html', {'comptes_prets': comptes_prets})

def liste_comptes_pretsactval(request):
    comptes_prets = ComptePretsact.objects.filter(statut=1)
    return render(request, 'Pages/Comptepretact/liste_comptes_prets.html', {'comptes_prets': comptes_prets})

def detail_compte_pretact(request, compte_pret_id):
    compte_pret = get_object_or_404(ComptePretsact, id=compte_pret_id)
    echeanciers = Echeancieract.objects.filter(compte_pretact=compte_pret)

    context = {
        'compte_pret': compte_pret,
        'echeanciers': echeanciers,
    }
    return render(request, 'Pages/Comptepretact/detail_compte_pret.html', context)


def supprimer_compte_pretact(request, pk):
    compte_pret = get_object_or_404(ComptePretsact, pk=pk)
    if request.method == 'POST':
        compte_pret.delete()
        return redirect('liste_comptes_pretsact')
    return render(request, 'Pages/Comptepretact/supprimer_compte_pret.html', {'compte_pret': compte_pret})

            #API___ Juillet 2
def modifier_compte_pretact(request, pk):
    compte_pret = get_object_or_404(ComptePretsact, pk=pk)
    ancisom = compte_pret.somme_initiale

    if request.method == 'POST':
        compte_pret_form = ComptePretactForm(request.POST, instance=compte_pret)

        if compte_pret_form.is_valid(): 
            statut_actif = Statuts.objects.get(statut='Actif')
            
            compte_pret_form.instance.statut = statut_actif
            if request.user.is_authenticated and isinstance(request.user, Utilisateurs):
                agent = request.user

    
            compte_pret_form.instance.agent=request.user  # Assurez-vous que cela pointe vers l'utilisateur connecté

            
            compte_pret = compte_pret_form.save()

            # Calculer la date de fin en fonction de la date de début et de la durée en mois
            duree_en_mois = compte_pret_form.cleaned_data['duree_en_mois']
            compte_pret.date_fin_pret = compte_pret.date_debut_pret + timedelta(days=30 * duree_en_mois) 

            if duree_en_mois:
                compte_pret.date_fin_pret = compte_pret.date_debut_pret + timedelta(days=30 * duree_en_mois)

            # Calculer les intérêts en fonction du type de prêt
            somme_initiale = compte_pret.somme_initiale
            taux_interet = compte_pret.taux_interet / 100
            statut_actif = get_object_or_404(Statuts, statut='Actif')
            Conf = Confconstantes.objects.filter(statut=statut_actif).first()
            taux_kha = Conf.partepargnesous
            taux_khaa = Conf.partfraisdossous
            taux_garantie = 15 / 100
            

            if compte_pret.type_pret.id == 1:  # TYPE DE PRET avec versement d’une garantie
                interets = somme_initiale * Decimal(taux_interet) * duree_en_mois
            elif compte_pret.type_pret.id == 2:  # TYPE DE PRET sans versement de la garantie au préalable
                interets = (somme_initiale * Decimal(taux_garantie)) + somme_initiale * Decimal(taux_interet) * 10  # 10 mois de remboursement par défaut
            elif compte_pret.type_pret.id == 3:  # TYPE DE PRET le client ayant un compte avec KHA
                interets = somme_initiale * Decimal(taux_interet) * duree_en_mois
            else:
                interets = 0

            compte_pret.solde = somme_initiale + interets + (somme_initiale * Decimal(taux_kha)) + (somme_initiale * Decimal(taux_khaa))
            compte_pret.save()

            # Mise à jour du solde du compte portefeuilles KHA
            statut_actif = get_object_or_404(Statuts, statut='Actif')
            porte = get_object_or_404(ComptePortefeuilles, statut=statut_actif)
            porte.totalsortie += somme_initiale
            porte.totalreste = porte.totalentree - porte.totalsortie
            porte.save()

            # Mise à jour du solde du compte principal KHA
            statut_actif = get_object_or_404(Statuts, statut='Actif')
            princ = get_object_or_404(ComptePrincipale, statut=statut_actif)
            princ.totalsortie += somme_initiale
            princ.datesortie = timezone.now()  # Conserve la date avec fuseau horaire
            princ.totalgain = ( princ.totalentree - (princ.totalsortie + princ.totaldepenses))
            princ.save()

            # Récupérer le compte prêt via son identifiant (pk)
            compte_pret = get_object_or_404(ComptePrets, pk=pk)

            # Vérifier si un rachat existe pour ce compte
            rach = Rachats.objects.filter(compte_pretnew=compte_pret).first()

            # Si un rachat existe, mettre à jour le montant
            if rach:
                rach.montant_new += (somme_initiale - ancisom)
                rach.save()

            # Une fois les modifications du compte prêt enregistrées, appelez la fonction de création/mise à jour de l'échéancier
             # Passez l'instance de compte_pret  create_echeanciersact(compte_pret)

            return redirect('liste_comptes_pretsact')
    else:
        compte_pret_form = ComptePretactForm(instance=compte_pret)

    return render(request, 'Pages/Comptepretact/modifier_compte_pret.html', {'compte_pret_form': compte_pret_form})

# MAJ API ___________________________________________________________
@receiver(post_save, sender=ComptePretsact)
def create_echeanciersactapi(sender, instance, created, **kwargs):
    if created:
        statut_actif = get_object_or_404(Statuts, statut='Actif')
        Conf = Confconstantes.objects.filter(statut=statut_actif).first()
        taux_kha = Decimal(Conf.partepargnesous)
        taux_khaa = Conf.partfraisdossous
        somme_initiale = instance.somme_initiale
        taux_interet = instance.taux_interet / Decimal('100')
        duree_en_mois = instance.duree_en_mois

        interets = somme_initiale * taux_interet * duree_en_mois
        instance.solde = somme_initiale + interets + (somme_initiale * taux_kha) + (somme_initiale * taux_khaa)
        instance.save()  # Sauvegarde les modifications apportées au solde

        if instance.type_client_id == 1:  # Pour un client avec des échéances chaque semaine
            montant_interet = interets / (duree_en_mois * 4)
            montant_epargne = (somme_initiale * taux_kha) / (duree_en_mois * 4)
            montant_adhesion = (somme_initiale * taux_kha) / duree_en_mois
            montant_echeance = ((somme_initiale + interets) / (duree_en_mois * 4)) + montant_epargne + montant_adhesion
        elif instance.type_client_id == 2:  # Pour un client avec des échéances chaque mois
            montant_interet = interets / duree_en_mois
            montant_epargne = (somme_initiale * taux_kha) / duree_en_mois
            montant_adhesion = (somme_initiale * taux_kha) / duree_en_mois
            montant_echeance = ((somme_initiale + interets) / duree_en_mois) + montant_epargne + montant_adhesion
        else:
            montant_epargne = Decimal('0')
            montant_interet = Decimal('0')
            montant_echeance = Decimal('0')
            montant_adhesion = Decimal('0')

        echeances = instance.calculer_echeances()
        for date_echeance in echeances:
            Echeancieract.objects.create(
                compte_pretact=instance,
                date_echeance=date_echeance,
                montant_echeance=montant_echeance,
                montant_interet=montant_interet,
                montant_epargne=montant_epargne,
                montant_adhesion=montant_adhesion
            )
# MAJ API ___________________________________________________________

@receiver(pre_save, sender=ComptePretsact)
def update_echeanciersact(sender, instance, **kwargs):
    if instance.pk is not None:
        somme_initiale = instance.somme_initiale
        taux_interet = instance.taux_interet / 100
        duree_en_mois = instance.duree_en_mois
        statut_actif = get_object_or_404(Statuts, statut='Actif')
        Conf = Confconstantes.objects.filter(statut=statut_actif).first()
        taux_kha = Conf.partepargnesous
        taux_khaa = Conf.partfraisdossous
        interets = somme_initiale * Decimal(taux_interet) * duree_en_mois
        instance.solde = somme_initiale + interets + (somme_initiale *Decimal(taux_kha)) + (somme_initiale * taux_khaa)

        
        if instance.type_client_id == 1:  # Pour un client avec des échéances chaque semaine
            montant_interet =  interets/(instance.duree_en_mois * 4)
            montant_epargne = (instance.somme_initiale *Decimal(taux_kha)) / (instance.duree_en_mois * 4)
            montant_adhesion = (instance.somme_initiale *Decimal(taux_khaa)) / (instance.duree_en_mois * 4)
            montant_echeance = ((instance.somme_initiale + interets) / (instance.duree_en_mois * 4)) + montant_epargne + montant_adhesion
        elif instance.type_client_id == 2:  # Pour un client avec des échéances chaque mois
            montant_interet =  interets/instance.duree_en_mois
            montant_epargne = (instance.somme_initiale *Decimal(taux_kha)) / instance.duree_en_mois
            montant_adhesion = (instance.somme_initiale *Decimal(taux_khaa)) / instance.duree_en_mois
            montant_echeance = ((instance.somme_initiale + interets) / instance.duree_en_mois) + montant_epargne + montant_adhesion
        else:
            montant_epargne = 0
            montant_adhesion = 0

        # Supprimer toutes les échéances existantes pour ce compte de prêt
        Echeancieract.objects.filter(compte_pretact=instance).delete()

        echeances = instance.calculer_echeances()
        for date_echeance in echeances:
            Echeancieract.objects.create(
                compte_pretact=instance,
                date_echeance=date_echeance,
                montant_echeance=montant_echeance,
                montant_interet=montant_interet,
                montant_epargne=montant_epargne,
                montant_adhesion=montant_adhesion
            )

                #API___ Juillet 2
# FIN MAJ
                #API___ Juillet 2
def modifier_est_payeact(request, actionnaire_id):
    echance = Echeancieract.objects.get(pk=actionnaire_id)
    echance.est_paye = 1
    echance.save()

    # Créez une nouvelle transaction de prêt pour indiquer le paiement de l'échéance
    if request.user.is_authenticated and isinstance(request.user, Agent):
                agent = request.user

    transaction_pret = TransactionPretact.objects.create(
        compte_pret=echance.compte_pretact,
        montant=echance.montant_echeance,
        type_transaction='Depot',  # Mettez le type de transaction approprié
        agent=request.user  # Assurez-vous que cela pointe vers l'utilisateur connecté
    )

    # Mise à jour du solde du compte épargne associé à l'actionnaire
    compte_pret = echance.compte_pretact
    clien = compte_pret.actionnaire
    epar = get_object_or_404(CompteEpargnesact, actionnaire=clien)
    epar.solde += echance.montant_epargne
    epar.save()

    # Vérifier si c'est la dernière échéance payée pour le compte prêt
    compte_pret = echance.compte_pretact
    #API___ Juillet 2
    statut_actif = Statuts.objects.get(statut='Actif')
    kha = get_object_or_404(CompteKha, statut=statut_actif)
    kha.soldeprecedent = kha.solde
    kha.dateprecedent = kha.datesolde
    kha.datesolde = timezone.now()
    kha.solde += echance.montant_epargne
    kha.save()

    transactionkha = TransactionKha.objects.create(
        comptekha=kha,
        montant=echance.montant_epargne,
        type_transaction='Virement',  # À adapter en fonction de votre logique
        agent=request.user #if isinstance(request.user, Agent) else None  # Assurez-vous que cela pointe vers l'utilisateur connecté
    )

    
    # Récupérer l'échéance en question
    # Vérifier si c'est la dernière échéance payée pour le compte prêt
    compte_pret = echance.compte_pretact
    dernier_echeance_payee = Echeancieract.objects.filter(compte_pretact=compte_pret, est_paye=False).order_by('date_echeance').first()
    if not dernier_echeance_payee:
        # Si aucune échéance impayée, mettre le statut du compte prêt en inactif
        compte_pret.statut = Statuts.objects.get(statut='Non Actif')
        compte_pret.save()
    
    # Associer le compte prêt au client spécifié par l'ID
    statut_actif = get_object_or_404(Statuts, statut='Actif')
    Conf = Confconstantes.objects.filter(statut=statut_actif).first()
    taux_com = Conf.partcom

    compte_pret = echance.compte_pretact
    comm = get_object_or_404(ComptePretsact, id=compte_pret.id)
    etudian = get_object_or_404(Agent, user=comm.agent)

    # Assurez-vous que la commission existe pour l'agent, sinon créez-la
    statut_actif = get_object_or_404(Statuts, statut='Actif')  
    commission, created = Commissions.objects.get_or_create(agent=etudian.user, defaults={
        'solde': 0,
        'soldeprecedent': 0,
        'datesolde': timezone.now(),
        'statut': statut_actif,
    })

    # Mettre à jour la commission
    commission.soldeprecedent = commission.solde
    commission.date_aide = commission.datesolde
    commission.datesolde = timezone.now()
    commission.solde += (echance.montant_interet * Decimal(taux_com))
    commission.save()

    # Créer une nouvelle transaction de prêt
    transactioncom = TransactionCommissionpretact.objects.create(
        commissionact=commission,
        echeance=echance,
        montant=(echance.montant_interet * Decimal(taux_com)),
        type_transaction='Virement',  # À adapter en fonction de votre logique
        agent=request.user  # Assurez-vous que cela pointe vers l'utilisateur connecté
    )
    
#
    # Mise à jour du solde du compte adhesion associé à l'actionnaire
    statut_actif = get_object_or_404(Statuts, statut='Actif')
    adh = get_object_or_404(CompteAdhesionkhas, statut=statut_actif)
    adh.soldeprecedent = adh.solde
    adh.dateprecedent = adh.datesolde
    adh.datesolde = timezone.now()  # Conserve la date avec fuseau horaire
    adh.solde += echance.montant_adhesion
    adh.save()

    # Mise à jour du solde du compte interet associé à l'actionnaire
    statut_actif = get_object_or_404(Statuts, statut='Actif')
    inter = get_object_or_404(CompteInterets, statut=statut_actif)
    inter.soldeprecedent = inter.solde
    inter.dateprecedent = inter.datesolde
    inter.datesolde = timezone.now()  # Conserve la date avec fuseau horaire
    inter.solde += echance.montant_interet
    inter.save()

    transactionint = TransactionInteret.objects.create(
        compteinteret=inter,
        montant=echance.montant_interet,
        type_transaction='Virement',  # À adapter en fonction de votre logique
    )

    # Mise à jour du solde du compte interet associé à l'actionnaire
    statut_actif = get_object_or_404(Statuts, statut='Actif')
    penal = get_object_or_404(ComptePenalites, statut=statut_actif)
    penal.soldeprecedent = penal.solde
    penal.dateprecedent = penal.datesolde
    penal.datesolde = timezone.now()  # Conserve la date avec fuseau horaire
    penal.solde += echance.montant_penalite
    penal.save()

    if echance.montant_penalite > 0:
        transactionpenal = TransactionPenaliteHist.objects.create(
            comptepenalite=penal,
            montant=echance.montant_penalite,
            type_transaction='Virement',  # À adapter en fonction de votre logique
        )

        # Créer une nouvelle transaction de prêt
        transactionpenalites = TransactionPenalite.objects.create(
            compte_pret=echance.compte_pret,
            echeance=echance,
            montant=echance.montant_penalite,
            type_transaction='Virement',  # À adapter en fonction de votre logique
        )
    
    # Mise à jour du solde du compte principal KHA
    statut_actif = get_object_or_404(Statuts, statut='Actif')
    princ = get_object_or_404(ComptePrincipale, statut=statut_actif)
    # princ.totalentree += (echance.montant_echeance - (echance.montant_interet + echance.montant_epargne + echance.montant_adhesion + echance.montant_penalite))
    princ.totalentree += echance.montant_echeance
    princ.dateentree = timezone.now()  # Conserve la date avec fuseau horaire
    princ.totalgain = ( princ.totalentree - (princ.totalsortie + princ.totaldepenses))
    princ.save()

    # Mise à jour du solde du compte portefeuilles KHA
    statut_actif = get_object_or_404(Statuts, statut='Actif')
    porte = get_object_or_404(ComptePortefeuilles, statut=statut_actif)
    porte.totalentree += echance.montant_echeance
    porte.totalreste =  porte.totalentree -  porte.totalsortie
    porte.save()
#

    return redirect('clients_proche_echeance')

def modifier_est_payereact(request, actionnaire_id):
    echance = Echeancieract.objects.get(pk=actionnaire_id)
    echance.est_paye = 1
    echance.save()

    # Créez une nouvelle transaction de prêt pour indiquer le paiement de l'échéance
    if request.user.is_authenticated and isinstance(request.user, Agent):
                agent = request.user

    transaction_pret = TransactionPretact.objects.create(
        compte_pret=echance.compte_pretact,
        montant=echance.montant_echeance,
        type_transaction='Depot',  # Mettez le type de transaction approprié
        agent=request.user  # Assurez-vous que cela pointe vers l'utilisateur connecté
    )

    # Mise à jour du solde du compte épargne associé à l'actionnaire
    compte_pret = echance.compte_pretact
    clien = compte_pret.actionnaire
    epar = get_object_or_404(CompteEpargnesact, actionnaire=clien)
    epar.solde += echance.montant_epargne
    epar.save()

    #API___ Juillet 2
    statut_actif = Statuts.objects.get(statut='Actif')
    kha = get_object_or_404(CompteKha, statut=statut_actif)
    kha.soldeprecedent = kha.solde
    kha.dateprecedent = kha.datesolde
    kha.datesolde = timezone.now()
    kha.solde += echance.montant_epargne
    kha.save()

    transactionkha = TransactionKha.objects.create(
        comptekha=kha,
        montant=echance.montant_epargne,
        type_transaction='Virement',  # À adapter en fonction de votre logique
        agent=request.user #if isinstance(request.user, Agent) else None  # Assurez-vous que cela pointe vers l'utilisateur connecté
    )

    
    # Récupérer l'échéance en question
    
    
    # Associer le compte prêt au client spécifié par l'ID
    statut_actif = get_object_or_404(Statuts, statut='Actif')
    Conf = Confconstantes.objects.filter(statut=statut_actif).first()
    taux_com = Conf.partcom

    compte_pret = echance.compte_pretact
    comm = get_object_or_404(ComptePretsact, id=compte_pret.id)
    etudian = get_object_or_404(Agent, user=comm.agent)

    # Assurez-vous que la commission existe pour l'agent, sinon créez-la
    statut_actif = get_object_or_404(Statuts, statut='Actif')
    commission, created = Commissions.objects.get_or_create(agent=etudian.user, defaults={
        'solde': 0,
        'soldeprecedent': 0,
        'datesolde': timezone.now(),
        'statut': statut_actif,
    })

    # Mettre à jour la commission
    commission.soldeprecedent = commission.solde
    commission.date_aide = commission.datesolde
    commission.datesolde = timezone.now()
    commission.solde += (echance.montant_interet * Decimal(taux_com))
    commission.save()

    # Créer une nouvelle transaction de prêt
    transactioncom = TransactionCommissionpretact.objects.create(
        commissionact=commission,
        echeance=echance,
        montant=(echance.montant_interet * Decimal(taux_com)),
        type_transaction='Virement',  # À adapter en fonction de votre logique
        agent=request.user  # Assurez-vous que cela pointe vers l'utilisateur connecté
    )

#
    # Mise à jour du solde du compte adhesion associé à l'actionnaire
    statut_actif = get_object_or_404(Statuts, statut='Actif')
    adh = get_object_or_404(CompteAdhesionkhas, statut=statut_actif)
    adh.soldeprecedent = adh.solde
    adh.dateprecedent = adh.datesolde
    adh.datesolde = timezone.now()  # Conserve la date avec fuseau horaire
    adh.solde += echance.montant_adhesion
    adh.save()

    # Mise à jour du solde du compte interet associé à l'actionnaire
    statut_actif = get_object_or_404(Statuts, statut='Actif')
    inter = get_object_or_404(CompteInterets, statut=statut_actif)
    inter.soldeprecedent = inter.solde
    inter.dateprecedent = inter.datesolde
    inter.datesolde = timezone.now()  # Conserve la date avec fuseau horaire
    inter.solde += echance.montant_interet
    inter.save()

    transactionint = TransactionInteret.objects.create(
        compteinteret=inter,
        montant=echance.montant_interet,
        type_transaction='Virement',  # À adapter en fonction de votre logique
    )

    # Mise à jour du solde du compte interet associé à l'actionnaire
    statut_actif = get_object_or_404(Statuts, statut='Actif')
    penal = get_object_or_404(ComptePenalites, statut=statut_actif)
    penal.soldeprecedent = penal.solde
    penal.dateprecedent = penal.datesolde
    penal.datesolde = timezone.now()  # Conserve la date avec fuseau horaire
    penal.solde += echance.montant_penalite
    penal.save()

    if echance.montant_penalite > 0:
        transactionpenal = TransactionPenaliteHist.objects.create(
            comptepenalite=penal,
            montant=echance.montant_penalite,
            type_transaction='Virement',  # À adapter en fonction de votre logique
        )

        # Créer une nouvelle transaction de prêt
        transactionpenalites = TransactionPenalite.objects.create(
            compte_pret=echance.compte_pret,
            echeance=echance,
            montant=echance.montant_penalite,
            type_transaction='Virement',  # À adapter en fonction de votre logique
        )
    
    # Mise à jour du solde du compte principal KHA
    statut_actif = get_object_or_404(Statuts, statut='Actif')
    princ = get_object_or_404(ComptePrincipale, statut=statut_actif)
    princ.totalentree += echance.montant_echeance
    princ.dateentree = timezone.now()  # Conserve la date avec fuseau horaire
    princ.totalgain = ( princ.totalentree - (princ.totalsortie + princ.totaldepenses))
    princ.save()

    # Mise à jour du solde du compte portefeuilles KHA
    statut_actif = get_object_or_404(Statuts, statut='Actif')
    porte = get_object_or_404(ComptePortefeuilles, statut=statut_actif)
    porte.totalentree += (echance.montant_echeance - (echance.montant_interet + echance.montant_epargne + echance.montant_adhesion + echance.montant_penalite))
    porte.totalreste = porte.totalentree - porte.totalsortie
    porte.save()
#
            #API___ Juillet 2
    # Vérifier si c'est la dernière échéance payée pour le compte prêt
    compte_pret = echance.compte_pretact
    dernier_echeance_payee = Echeancieract.objects.filter(compte_pretact=compte_pret, est_paye=False).order_by('date_echeance').first()
    if not dernier_echeance_payee:
        # Si aucune échéance impayée, mettre le statut du compte prêt en inactif
        compte_pret.statut = Statuts.objects.get(statut='Non Actif')
        compte_pret.save()
    return redirect('liste_echeances_non_payees')

from .forms import AideForm

#API___ Juillet 2
#AIDES _________________________________________________________________________________________________________________________________________________
# Créer une aide
def create_aide(request, client_id):
    client = get_object_or_404(Clients, id=client_id)
    nombre = Tontines.objects.count()

    if request.method == 'POST':
        form = AideForm(request.POST)
        if form.is_valid():
            # Créez une nouvelle transaction de prêt pour indiquer le paiement de l'échéance
            if request.user.is_authenticated and isinstance(request.user, Agent):
                agent = request.user
                
            form.instance.agent = request.user  # Assurez-vous que cela pointe vers l'utilisateur connecté

            statut_actif = Statuts.objects.get(statut='Actif')
            form.instance.statut = statut_actif
            
            # Calculer la date 90 jours à partir de maintenant
         # date_palier = timezone.now() + timedelta(days=90)
            numero_compte = f"TO{timezone.now().strftime('%Y%m%d%H%M%S')}"
            tontine, created = Tontines.objects.get_or_create(client=client, defaults={
                'client': client,
                'numero_tontine': numero_compte ,
                'solde': 0,
                'cotite': 0,
                'date_tontine': timezone.now(),
                'statut': statut_actif , # ou une valeur par défaut
                'agent': request.user , # ou une valeur par défaut
                'date_palier': timezone.now() + timedelta(days=90) ,
                'duree' : 0,
                'penaliteton' : 0,
                'montant_min' : 500,
            })



            
            etudian = get_object_or_404(Agent, user=tontine.agent)

            # Assurez-vous que la commission existe pour l'agent, sinon créez-la
            commission, created = Commissions.objects.get_or_create(agent=etudian.user, defaults={
                'solde': 0,
                'soldeprecedent': 0,
                'datesolde': timezone.now(),
                'statut': etudian.type_agent  # ou une valeur par défaut
            })

            # Supposons que vous avez des objets 'tontine', 'commission', et 'echance'
            statut_actif = get_object_or_404(Statuts, statut='Actif')
            Conf = Confconstantes.objects.filter(statut=statut_actif).first()
            taux_com = Conf.partcom
            # if tontine.duree <= 365 :
            #     # Mettre à jour la commission
            #     commission.soldeprecedent = commission.solde
            #     commission.date_aide = commission.datesolde
            #     commission.datesolde = timezone.now()
            #     commission.solde += (echance.montant_interet * Decimal(taux_com))
            #     commission.save()

            #     # Créer une nouvelle transaction de prêt
            #     transactioncom = TransactionCommissionpret.objects.create(
            #         commission=commission,
            #         echeance=echance,
            #         montant=(echance.montant_interet * Decimal(taux_com)),
            #         type_transaction='Virement',  # À adapter en fonction de votre logique
            #         agent=request.user  # Assurez-vous que cela pointe vers l'utilisateur connecté
            #     )

            if tontine.duree <= 90:
                taux_p = Conf.partpalierun
            elif 90 < tontine.duree <= 180:
                taux_p = Conf.partpalierd
            elif 180 < tontine.duree <= 270:
                taux_p = Conf.partparliert
            elif 270 < tontine.duree <= 365:
                taux_p = Conf.partparlierq

            # Compter le nombre d'aides dont a bénéficié le client
            nbreaide = Aides.objects.filter(client=client).count()
            tontine.nbreaide = nbreaide
            tontine.dateaide = timezone.now()
            tontine.montant_aide = form.instance.montant_aide
            tontine.date_tontine = timezone.now()
            tontine.solde -= form.instance.montant_aide

            # Ajuster la valeur de cotite selon la condition
            if tontine.solde < 0:
                tontine.cotite = 0
            else:
                tontine.cotite = tontine.solde + (tontine.solde * Decimal(taux_p))

            tontine.save()

            form.save()
            return redirect('aide_list')
    else:
        form = AideForm(initial={'client': client})

    return render(request, 'Pages/Aide/ajouter_aide.html', {'form': form})


# Lire toutes les aides
def aide_list(request):
    aides = Aides.objects.all()
    return render(request, 'Pages/Aide/liste_aide.html', {'aides': aides})

# Lire une aide spécifique
def aide_detail(request, pk):
    aide = get_object_or_404(Aides, pk=pk)
    return render(request, 'Pages/Aide/detail_aide.html', {'aide': aide})

# Mettre à jour une aide
def update_aide(request, pk):
    aide = get_object_or_404(Aides, pk=pk)
    if request.method == 'POST':
        form = AideForm(request.POST, instance=aide)
        if form.is_valid():
            form.save()
            return redirect('aide_list')
    else:
        form = AideForm(instance=aide)
    return render(request, 'Pages/Aide/modifier_aide.html', {'form': form})

# Supprimer une aide
def delete_aide(request, pk):
    aide = get_object_or_404(Aides, pk=pk)
    tontine = get_object_or_404(Tontines, client=aide.client)
    if request.method == 'POST':

        # Mettre à jour le solde de la tontine en fonction du type de transaction
        nbreaide = Aides.objects.filter(client=aide.client).count()
        tontine.nbreaide = nbreaide
        tontine.date_tontine = timezone.now()
        tontine.solde -= aide.montant

            # Ajuster la valeur de cotite selon la condition
        statut_actif = get_object_or_404(Statuts, statut='Actif')
        Conf = Confconstantes.objects.filter(statut=statut_actif).first()
        if tontine.duree <= 90:
            taux_p = Conf.partpalierun
        elif 90 < tontine.duree <= 180:
            taux_p = Conf.partpalierd
        elif 180 < tontine.duree <= 270:
            taux_p = Conf.partparliert
        elif 270 < tontine.duree <= 365:
            taux_p = Conf.partparlierq

            # Ajuster la valeur de cotite selon la condition
        if tontine.solde < 0:
            tontine.cotite = 0
        else:
            tontine.cotite = tontine.solde + (tontine.solde * Decimal(taux_p))
                
        tontine.save()

            
        # Supprimer la aide      
        aide.delete()
        return redirect('aide_list')
    return render(request, 'Pages/Aide/supprimer_aide.html', {'aide': aide})
# _________________________________________________________________________________________________________________________________________________________

#TONTINE _________________________________________________________________________________________________________________________________________________________
# Create
# views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from datetime import timedelta
from decimal import Decimal
from .models import Tontines, Clients, Statuts, Confconstantes, Commissions, Agent
from .forms import TontineAForm

def create_tontine(request, ton):
    client = get_object_or_404(Clients, id=ton)
    
    if request.method == 'POST':
        form = TontineAForm(request.POST)
        if form.is_valid():
            typ = form.cleaned_data['type_tontine']  # Cela retourne déjà l'objet Typetontines
            N = {'Journalière': 1, 'Hebdomadaire': 7, 'Bimensuelle': 15, 'Mensuelle': 30}.get(typ.type_tontine, 7)

            statut_actif = get_object_or_404(Statuts, statut='Actif')

            etudian = form.cleaned_data['com']  # 'com' contient l'ID de l'agent
            etudia = get_object_or_404(Agent, id=etudian.id)

            compte_tontine = form.save(commit=False)
            compte_tontine.client = client
            compte_tontine.date_tontine = timezone.now()
            compte_tontine.numero_tontine = f"TO{timezone.now().strftime('%Y%m%d%H%M%S')}"
            compte_tontine.solde += form.cleaned_data['montant_min']
            compte_tontine.statut = statut_actif
            compte_tontine.agent = request.user
            compte_tontine.nbreaide = 0
            compte_tontine.penaliteton = 0
            compte_tontine.date_palier = timezone.now() + relativedelta(months=3)
            compte_tontine.duree = 0
            compte_tontine.date_futurcotisation = timezone.now() + timedelta(days=N)
            
            Conf = get_object_or_404(Confconstantes, statut=statut_actif)
            partprelev = Conf.partprelev
            taux_p = Conf.partpalierun
            
            etudian = form.cleaned_data['com']  # 'com' contient l'ID de l'agent
            etudia = get_object_or_404(Agent, id=etudian.id)  # Récupère l'instance d'Agent via son ID
            commission = get_object_or_404(Commissions, agent=etudia.user)  # Utilise l'ID de l'utilisateur associé à l'agent
            commission.soldeprecedent = commission.solde
            commission.date_aide = commission.datesolde
            commission.datesolde = timezone.now()
            commission.solde += partprelev
            commission.save()

            compte_tontine.cotite = max(0, compte_tontine.solde + (compte_tontine.solde * Decimal(taux_p)))
            compte_tontine.save()

            cli = get_object_or_404(Clients, id=client.id)
            cli.statut = statut_actif
            cli.save()

            #Créer une nouvelle transaction de prêt
            transactionton = TransactionTontine.objects.create(
                tontine = compte_tontine,
                montant = form.cleaned_data['montant_min'],
                date_transaction = timezone.now(),
                type_transaction='Virement',  # À adapter en fonction de votre logique
                agent=request.user  # Assurez-vous que cela pointe vers l'utilisateur connecté
                )
            
            
            return redirect('tontine_list')  # Redirige vers une liste ou une autre page après la sauvegarde  liste_clientsa
    else:
        form = TontineAForm(initial={'client': client})
    
    return render(request, 'Pages/Cotisation/tontine_form.html', {'form': form, 'action': 'Créer'})


# -------------------------
def update_tontine(request, pk):
    tontine = get_object_or_404(Tontines, pk=pk)
    if request.method == 'POST':
        form = TontineAForm(request.POST, instance=tontine)
        if form.is_valid():
            form.save()
            return redirect('tontine_list')  # Redirige vers une liste ou une autre page après la sauvegarde
    else:
        form = TontineAForm(instance=tontine)
    return render(request, 'Pages/Cotisation/tontine_form.html', {'form': form, 'action': 'Modifier'})

# _________________________________________________________


def tontine_create(request):
    if request.method == 'POST':
        form = TontineForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('tontine_list')
    else:
        form = TontineForm()
    return render(request, 'Pages/Cotisation/tontine_form.html', {'form': form})

# Read - List
def tontine_list(request):
    tontines = Tontines.objects.all()
    return render(request, 'Pages/Cotisation/tontine_list.html', {'tontines': tontines})

# Read - Detail
def tontine_detail(request, id):
    tontine = get_object_or_404(Tontines, id=id)
    return render(request, 'Pages/Cotisation/tontine_detail.html', {'tontine': tontine})

# Update
def tontine_update(request, id):
    tontine = get_object_or_404(Tontines, id=id)
    if request.method == 'POST':
        form = TontineForm(request.POST, instance=tontine)
        if form.is_valid():
            form.save()
            return redirect('tontine_detail', id=id)
    else:
        form = TontineForm(instance=tontine)
    return render(request, 'Pages/Cotisation/tontine_form.html', {'form': form})

# Delete
def tontine_delete(request, id):
    tontine = get_object_or_404(Tontines, id=id)
    if request.method == 'POST':
        tontine.delete()
        return redirect('tontine_list')
    return render(request, 'Pages/Cotisation/tontine_confirm_delete.html', {'tontine': tontine})

#TRANSACTIONTONTINE ________________________________________________________________________________________________________________________________________
# Create
def transaction_tontine_create(request, ton):
    client = get_object_or_404(Clients, id=ton)
    nombre = Tontines.objects.count()
    if request.method == 'POST':
        form = TransactionTontineForm(request.POST)
        if form.is_valid():
            if request.user.is_authenticated and isinstance(request.user, Agent):
                agent = request.user

            form.instance.agent = request.user  # Assurez-vous que cela pointe vers l'utilisateur connecté

            statut_actif = Statuts.objects.get(statut='Actif')
            form.instance.statut = statut_actif

            tontine = get_object_or_404(Tontines, client=ton)
            client = tontine.client

            # Assurez-vous que le client est bien une instance de Clients
            if not isinstance(client, Clients):
                raise ValueError("Le client doit être une instance de Clients")

            numero_compte = f"TO{timezone.now().strftime('%Y%m%d%H%M%S')}"
            new_tontine, created = Tontines.objects.get_or_create(client=client, defaults={
                'client': client,
                'numero_tontine': numero_compte ,
                'solde': 0,
                'cotite': 0,
                'date_tontine': timezone.now(),
                'statut': statut_actif , # ou une valeur par défaut
                'agent': request.user , # ou une valeur par défaut
                'date_palier': timezone.now() + timedelta(days=90) ,
                'duree' : 0,
                'penaliteton' : 0,
                'montant_min' : 500,
            })

            # Transaction de tontine
            form.instance.tontine = new_tontine
            form.instance.type_transaction = 'Virement'  # À adapter en fonction de votre logique

            # Compter le nombre d'aides dont a bénéficié le client
            epar = get_object_or_404(Tontines, client=client)
            nbreaide = Aides.objects.filter(client=client).count()
            epar.nbreaide = nbreaide
            epar.date_tontine = timezone.now()
            epar.solde += form.instance.montant


            etudian = get_object_or_404(Agent, user=new_tontine.agent)

            # Assurez-vous que la commission existe pour l'agent, sinon créez-la
            commission, created = Commissions.objects.get_or_create(agent=etudian.user, defaults={
                'solde': 0,
                'soldeprecedent': 0,
                'datesolde': timezone.now(),
                'statut': etudian.type_agent  # ou une valeur par défaut
            })

            # Supposons que vous avez des objets 'tontine', 'commission', et 'echance'
            statut_actif = get_object_or_404(Statuts, statut='Actif')
            Conf = Confconstantes.objects.filter(statut=statut_actif).first()
            taux_com = Conf.partcom
            m = form.instance.montant
            if tontine.duree <= 365 :
                # Mettre à jour la commission
                commission.soldeprecedent = commission.solde
                commission.date_aide = commission.datesolde
                commission.datesolde = timezone.now()
                commission.solde += (m * Decimal(taux_com))
                commission.save()

            # Créer une nouvelle transaction de prêt
                # transactionton = TransactionTontine.objects.create(
                #     tontine=commission,
                #     echeance=echance,
                #     montant=(echance.montant_interet * Decimal(taux_com)),
                #     type_transaction='Virement',  # À adapter en fonction de votre logique
                #     agent=request.user  # Assurez-vous que cela pointe vers l'utilisateur connecté
                # )

            if tontine.duree <= 90:
                taux_p = Conf.partpalierun
            elif 90 < tontine.duree <= 180:
                taux_p = Conf.partpalierd
            elif 180 < tontine.duree <= 270:
                taux_p = Conf.partparliert
            elif 270 < tontine.duree <= 365:
                taux_p = Conf.partparlierq

            # Ajuster la valeur de cotite selon la condition
            if epar.solde < 0:
                epar.cotite = 0
            else:
                epar.cotite = epar.solde + (epar.solde * Decimal(taux_p))
                
            epar.save()

            form.save()
            return redirect('tontine_list')  #aide_list
    else:
        form = TransactionTontineForm(initial={'tontine': ton})
    return render(request, 'Pages/Cotisation/transaction_tontine_form.html', {'form': form})

# TRANSACTION TONTINE ----------------------------------------------------------------------------------------------
# Read - List
# Read - Detail
def transaction_tontine_detailclient(request, id):
    transactions = TransactionTontine.objects.filter(tontine=id)
    return render(request, 'Pages/Transactiontontine/liste_transactions.html', {'transactions': transactions})


def transaction_tontine_list(request):
    transactions = TransactionTontine.objects.all()
    return render(request, 'Pages/Transactiontontine/liste_transactions.html', {'transactions': transactions})

# Read - Detail
def transaction_tontine_detail(request, id):
    transaction = get_object_or_404(TransactionTontine, id=id)
    return render(request, 'Pages/Transactiontontine/liste.html', {'transaction': transaction})

@login_required
def transaction_tontine_update(request, id):
    transaction = get_object_or_404(TransactionTontine, id=id)
    type_avant_modification = transaction.type_transaction
    montant_avant_modification = transaction.montant

    if request.method == 'POST':
        form = TransactionTontineForm(request.POST, instance=transaction)
        if form.is_valid():
            transaction = form.save(commit=False)

            if request.user.is_authenticated and isinstance(request.user, Agent):
                transaction.agent = request.user

            montant_apres_modification = transaction.montant

            # Cas 1: Même type de transaction, montant modifié
            if type_avant_modification == transaction.type_transaction and montant_avant_modification != montant_apres_modification:
                ajustement_solde = montant_apres_modification - montant_avant_modification
                if type_avant_modification in ['Depot', 'Virement', 'Mobile money']:
                    transaction.tontine.solde += ajustement_solde
                elif type_avant_modification == 'Retrait':
                    transaction.tontine.solde -= ajustement_solde
                # Ajuster la valeur de cotite selon la condition
                if transaction.tontine.solde < 0:
                    transaction.tontine.cotite = 0
                else:
                    transaction.tontine.cotite = transaction.tontine.solde * 3
                transaction.tontine.date_tontine = timezone.now()
                
                transaction.tontine.save()

            # Cas 2: Même type de transaction, montant inchangé
            elif type_avant_modification == transaction.type_transaction and montant_avant_modification == montant_apres_modification:
                pass  # Aucun ajustement de solde nécessaire

            # Cas 3: Changement de type de transaction, montant inchangé
            elif type_avant_modification != transaction.type_transaction and montant_avant_modification == montant_apres_modification:
                if type_avant_modification in ['Depot', 'Virement', 'Mobile money']:
                    transaction.tontine.solde -= montant_avant_modification
                elif type_avant_modification == 'Retrait':
                    transaction.tontine.solde += montant_avant_modification
                # Ajuster la valeur de cotite selon la condition
                if transaction.tontine.solde < 0:
                    transaction.tontine.cotite = 0
                else:
                    transaction.tontine.cotite = transaction.tontine.solde * 3
                transaction.tontine.date_tontine = timezone.now()
                
                transaction.tontine.save()

                if transaction.type_transaction in ['Depot', 'Virement', 'Mobile money']:
                    transaction.tontine.solde += montant_apres_modification
                elif transaction.type_transaction == 'Retrait':
                    transaction.tontine.solde -= montant_apres_modification
                # Ajuster la valeur de cotite selon la condition
                if transaction.tontine.solde < 0:
                    transaction.tontine.cotite = 0
                else:
                    transaction.tontine.cotite = transaction.tontine.solde * 3
                transaction.tontine.date_tontine = timezone.now()
                
                transaction.tontine.save()

            # Cas 4: Changement de type de transaction et montant modifié
            elif type_avant_modification != transaction.type_transaction and montant_avant_modification != montant_apres_modification:
                ajustement_solde_montant = montant_apres_modification - montant_avant_modification
                ajustement_solde_type = 2 * montant_avant_modification  # ajustement pour le changement de type
                ajustement_solde_total = ajustement_solde_montant + ajustement_solde_type

                if transaction.type_transaction in ['Depot', 'Virement', 'Mobile money']:
                    transaction.tontine.solde += ajustement_solde_total
                elif transaction.type_transaction == 'Retrait':
                    transaction.tontine.solde -= ajustement_solde_total
                # Ajuster la valeur de cotite selon la condition
                if transaction.tontine.solde < 0:
                    transaction.tontine.cotite = 0
                else:
                    transaction.tontine.cotite = transaction.tontine.solde * 3
                transaction.tontine.date_tontine = timezone.now()
                
                transaction.tontine.save()

            transaction.save()
            return redirect(reverse('transaction_tontine_detailclient', args=[transaction.tontine.id]))
    else:
        form = TransactionTontineForm(instance=transaction)

    context = {
        'form': form,
        'id': id,
    }

    return render(request, 'Pages/Cotisation/transaction_tontine_form.html', context)

# Delete

def transaction_tontine_delete(request, id):
    transaction = get_object_or_404(TransactionTontine, id=id)
    tontine = transaction.tontine
    
    if request.method == 'POST':
        # Mettre à jour le solde de la tontine en fonction du type de transaction
        if transaction.type_transaction in ['Depot', 'Virement', 'Mobile money']:
            tontine.solde -= transaction.montant
        elif transaction.type_transaction == 'Retrait':
            tontine.solde += transaction.montant
        
        # Enregistrer les modifications de la tontine
        tontine.save()
        
        # Supprimer la transaction
        transaction.delete()
        
        return redirect('transaction_tontine_list')
    
    return render(request, 'Pages/Transactiontontine/transaction_tontine_confirm_delete.html', {'transaction': transaction})



# RACHAT ____________________________________________________________________________________________________________________________________________
def create_rachat(request):
    if request.method == 'POST':
        form = RachatForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('rachat_list')
    else:
        form = RachatForm()
    return render(request, 'Pages/Rachat/ajouter_rachat.html', {'form': form})

#def create_rachatpret(request,idpret):
#    statut_actif = Statuts.objects.get(statut='Actif')
#    pretactuel = get_object_or_404(ComptePrets, pk=idpret)
#    echeancepretactuel = Echeancier.objects.filter(compte_pret=idpret,est_paye=1)
#    echeancepretactuelre = Echeancier.objects.filter(compte_pret=idpret,est_paye=0)
#    reste = sum(echeancepretactuelr.montant_echeance for echeancepretactuelr in echeancepretactuelre)
#    if request.method == 'POST':
#        form = RachatForm(request.POST)
#        if form.is_valid():

            #executer le processus de creer de nouvelle pret

#            form.compte_pretnew = 2
#           form.save()
#            return redirect('rachat_list')
#    else:
#        form = RachatForm(initial={'compte_pretactuel': idpret,'reste_actuel':reste,'montant_actuel':pretactuel.somme_initiale,'client':pretactuel.client})
#    return render(request, 'Pages/Rachat/ajouter_rachat_compte_pret.html', {'form': form})

def create_rachatpret(request, idpret):
    statut_actif = Statuts.objects.get(statut='Actif')
    statut_nactif = get_object_or_404(Statuts, statut='Non Actif')
    pretactuel = get_object_or_404(ComptePrets, pk=idpret)
    echeancepretactuelre = Echeancier.objects.filter(compte_pret=idpret, est_paye=0)
    reste = sum(echeancepretactuelr.montant_echeance for echeancepretactuelr in echeancepretactuelre)

    client_id = pretactuel.client.id
    etud = Clients.objects.filter(id=client_id)
    nombre = ComptePrets.objects.count()
    typp = Typeprets.objects.get(id=3)

    etnon = Clients.objects.get(id=client_id)
    na = etnon.nat_client.nat_client   # Initialiser `na` pour éviter l'UnboundLocalError
    #na = None 
    if etnon:
        if na == 'Ordinaire':
            nat = 'CLIENTORDINAIRE'
        elif na == 'Sponsor':
            nat = 'CLIENTSPONSOR'
        elif na == 'Aide':
            nat = 'CLIENTAIDE'
    else:
        # Gérer le cas où aucun client n'est trouvé
        messages.error(request, "Aucun client trouvé avec cet ID.")

    # Vérifier si `na` a été défini correctement avant de l'utiliser
    if nat:
        # Utilisation de la variable `na`
        print(f"Client type: {nat}")
    else:
        # Gérer le cas où `na` est encore `None` (aucune condition `if` n'était remplie)
        messages.error(request, "Le type de client n'a pas pu être déterminé.")

    if request.method == 'POST':
        form = CompteRaPretForm(request.POST)
        if form.is_valid():
            compte_pret = form.save(commit=False)
            
            if request.user.is_authenticated and isinstance(request.user, Utilisateurs):
                agent = request.user
            
            compte_pret.agent = request.user
            compte_pret.type_pret = typp
            # statut_actif = Statuts.objects.get(statut='Actif')
            # form.instance.statut = statut_actif
            compte_pret.client_id = client_id
            compte_pret.date_demande = timezone.now()
            compte_pret.numero_compte = f"PR{timezone.now().strftime('%Y%m%d%H%M%S')}"

            duree_en_mois = form.cleaned_data['duree_en_mois']
            compte_pret.date_fin_pret = compte_pret.date_debut_pret + timedelta(days=30 * duree_en_mois)

            somme_initiale = compte_pret.somme_initiale
            #somme_initiale = compte_pret.somme_initiale - reste
            taux_interet = compte_pret.taux_interet / 100
            taux_garantie = 15 / 100
            statut_actif = get_object_or_404(Statuts, statut='Actif')
            Conf = Confconstantes.objects.filter(statut=statut_actif).first()
            taux_kha = Conf.partepargne
            taux_khaa = Conf.partfraisdos

            if compte_pret.type_pret_id == 1:  # TYPE DE PRET avec versement d’une garantie
                interets = somme_initiale * Decimal(taux_interet) * duree_en_mois
            elif compte_pret.type_pret_id == 2:  # TYPE DE PRET sans versement de la garantie au préalable
                interets = (somme_initiale * Decimal(taux_garantie)) + somme_initiale * Decimal(taux_interet) * 10
            elif compte_pret.type_pret_id == 3:  # TYPE DE PRET le client ayant un compte avec KHA
                interets = somme_initiale * Decimal(taux_interet) * duree_en_mois
            else:
                interets = 0

            
            compte_pret.solde = somme_initiale + interets + (somme_initiale * Decimal(taux_kha)) + (somme_initiale * Decimal(taux_khaa))
            

            Rachats.objects.create(
                client=pretactuel.client,
                date_rachat=timezone.now(),
                compte_pretactuel=pretactuel,
                montant_actuel=pretactuel.somme_initiale,
                reste_actuel=reste,
                compte_pretnew=compte_pret.numero_compte,
                montant_new=compte_pret.somme_initiale
            )

             # Créer une nouvelle transaction de prêt
            transactionpret = TransactionPret.objects.create(
                compte_pret=compte_pret,
                montant=somme_initiale,
                date_transaction=timezone.now(),
                type_transaction='Virement',  # À adapter en fonction de votre logique
                agent=request.user  # Assurez-vous que cela pointe vers l'utilisateur connecté
            )

            

            pretactuel.statut = statut_nactif
            pretactuel.save()

            compte_pret.somme_initiale = somme_initiale
            compte_pret.naturecompte = nat
            compte_pret.statut = statut_actif
            compte_pret.save()

            
#
            # Vérifier si la date de cotisation future est dépassée
            for echeancepretactuel in echeancepretactuelre:
                
                # Calculer la durée écoulée depuis la date de création de la tontine
                
                # Création de la transaction de prêt
                transaction_pret = TransactionPret.objects.create(
                    compte_pret=echeancepretactuel.compte_pret,
                    montant=echeancepretactuel.montant_echeance,
                    type_transaction='Depot',  # À adapter en fonction de votre logique
                    agent=request.user #if isinstance(request.user, Agent) else None  # Assurez-vous que cela pointe vers l'utilisateur connecté
                )

                compte_pret = echeancepretactuel.compte_pret
                clien = compte_pret.client
                epar = get_object_or_404(CompteEpargnes, client=clien)
                epar.solde += echeancepretactuel.montant_epargne
                epar.save()


                # Mise à jour du solde du compte adhesion associé à l'actionnaire
                statut_actif = get_object_or_404(Statuts, statut='Actif')
                adh = get_object_or_404(CompteAdhesionkhas, statut=statut_actif)
                adh.soldeprecedent = adh.solde
                adh.dateprecedent = adh.datesolde
                adh.datesolde = timezone.now()  # Conserve la date avec fuseau horaire
                adh.solde += echeancepretactuel.montant_adhesion
                adh.save()

                # Mise à jour du solde du compte interet associé à l'actionnaire
                statut_actif = get_object_or_404(Statuts, statut='Actif')
                inter = get_object_or_404(CompteInterets, statut=statut_actif)
                inter.soldeprecedent = inter.solde
                inter.dateprecedent = inter.datesolde
                inter.datesolde = timezone.now()  # Conserve la date avec fuseau horaire
                inter.solde += echeancepretactuel.montant_interet
                inter.save()

                transactionint = TransactionInteret.objects.create(
                    compteinteret=inter,
                    montant=echeancepretactuel.montant_interet,
                    type_transaction='Virement',  # À adapter en fonction de votre logique
                )

                # Mise à jour du solde du compte interet associé à l'actionnaire
                statut_actif = get_object_or_404(Statuts, statut='Actif')
                penal = get_object_or_404(ComptePenalites, statut=statut_actif)
                penal.soldeprecedent = penal.solde
                penal.dateprecedent = penal.datesolde
                penal.datesolde = timezone.now()  # Conserve la date avec fuseau horaire
                penal.solde += echeancepretactuel.montant_penalite
                penal.save()

                if echeancepretactuel.montant_penalite > 0:
                    transactionpenal = TransactionPenaliteHist.objects.create(
                        comptepenalite=penal,
                        montant=echeancepretactuel.montant_penalite,
                        type_transaction='Virement',  # À adapter en fonction de votre logique
                        agent=request.user  # Assurez-vous que cela pointe vers l'utilisateur connecté
                    )

                    # Créer une nouvelle transaction de prêt
                    transactionpenalites = TransactionPenalite.objects.create(
                        compte_pret=echeancepretactuel.compte_pret,
                        echeance=echeancepretactuel,
                        montant=echeancepretactuel.montant_penalite,
                        type_transaction='Virement',  # À adapter en fonction de votre logique
                        agent=request.user  # Assurez-vous que cela pointe vers l'utilisateur connecté
                    )
                
                # Mise à jour du solde du compte principal KHA
                statut_actif = get_object_or_404(Statuts, statut='Actif')
                princ = get_object_or_404(ComptePrincipale, statut=statut_actif)
                princ.totalentree += echeancepretactuel.montant_echeance
                princ.dateentree = timezone.now()  # Conserve la date avec fuseau horaire
                princ.totalgain = ( princ.totalentree - (princ.totalsortie + princ.totaldepenses))
                princ.save()

                # Mise à jour du solde du compte portefeuilles KHA
                statut_actif = get_object_or_404(Statuts, statut='Actif')
                porte = get_object_or_404(ComptePortefeuilles, statut=statut_actif)
                porte.totalentree += (echeancepretactuel.montant_echeance - (echeancepretactuel.montant_interet + echeancepretactuel.montant_epargne + echeancepretactuel.montant_adhesion + echeancepretactuel.montant_penalite))
                porte.totalreste = porte.totalentree - porte.totalsortie
                porte.save()
            #
                # Création de la transaction d'épargne
                transaction_epar = TransactionEpargne.objects.create(
                    compte_epargne=epar,
                    montant=echeancepretactuel.montant_epargne,
                    type_transaction='Virement',  # À adapter en fonction de votre logique
                    agent=request.user   # Assurez-vous que cela pointe vers l'utilisateur connecté
                )
                # MAJ FEV

                # Vérifier si c'est la dernière échéance payée pour le compte prêt
                compte_pret = echeancepretactuel.compte_pret
                dernier_echeance_payee = Echeancier.objects.filter(compte_pret=compte_pret, est_paye=False).order_by('date_echeance').first()
                if not dernier_echeance_payee:
                    # Si aucune échéance impayée, mettre le statut du compte prêt en inactif
                    compte_pret.statut = Statuts.objects.get(statut='Non Actif')
                    compte_pret.save()

                    # Mettre à jour le statut du contrat sponsor
                    try:
                        cont = Contratsponsor.objects.get(numero_compte=compte_pret.numero_compte)
                        cont.statut = Statuts.objects.get(statut='Non Actif')
                        cont.save()
                    except Contratsponsor.DoesNotExist:
                        # Gérer le cas où le contrat sponsor n'existe pas
                        pass


                        #API___ Juillet 2
                statut_actif = Statuts.objects.get(statut='Actif')
                kha = get_object_or_404(CompteKha, statut=statut_actif)
                kha.soldeprecedent = kha.solde
                kha.dateprecedent = kha.datesolde
                kha.datesolde = timezone.now()
                kha.solde += echeancepretactuel.montant_epargne
                kha.save()

                transactionkha = TransactionKha.objects.create(
                    comptekha=kha,
                    montant=echeancepretactuel.montant_epargne,
                    type_transaction='Virement',  # À adapter en fonction de votre logique
                    agent=request.user #if isinstance(request.user, Agent) else None  # Assurez-vous que cela pointe vers l'utilisateur connecté
                )

                transactionadh = TransactionAdhesionkha.objects.create(
                    compteAdhessionkha=adh,
                    montant=echeancepretactuel.montant_adhesion,
                    type_transaction='Virement',  # À adapter en fonction de votre logique
                    agent=request.user #if isinstance(request.user, Agent) else None  # Assurez-vous que cela pointe vers l'utilisateur connecté
                )

                # Associer le compte prêt au client spécifié par l'ID
                statut_actif = get_object_or_404(Statuts, statut='Actif')
                Conf = Confconstantes.objects.filter(statut=statut_actif).first()
                taux_kha = Conf.partepargne
                taux_com = Conf.partcom

                compte_pret = echeancepretactuel.compte_pret
                # Mettre à jour l'agent avec son ID
                comm = get_object_or_404(ComptePrets, id=compte_pret.id)
                com = get_object_or_404(Agent, id=comm.com.id)  # Utilisez .id pour obtenir l'ID de l'objet

                # Assurez-vous que la commission existe pour l'agent, sinon créez-la
                commission, created = Commissions.objects.get_or_create(agent=com.user, defaults={
                    'solde': 0,
                    'soldeprecedent': 0,
                    'datesolde': timezone.now(),
                    'statut': statut_actif.id  # ou une valeur par défaut
                })

                # Mettre à jour la commission
                commission.soldeprecedent = commission.solde
                commission.date_aide = commission.datesolde
                commission.datesolde = timezone.now()
                commission.solde += (echeancepretactuel.montant_interet * Decimal(taux_com))
                commission.save()

                # Créer une nouvelle transaction de prêt
                transactioncom = TransactionCommissionpret.objects.create(
                    commission=commission,
                    echeance=echeancepretactuel,
                    montant=(echeancepretactuel.montant_interet * Decimal(taux_com)),
                    type_transaction='Virement',  # À adapter en fonction de votre logique
                    agent=request.user  # Assurez-vous que cela pointe vers l'utilisateur connecté
                )
            # Mettre à jour toutes les échéances non payées en est_paye=1
            echeancepretactuelre.update(est_paye=1)

            return redirect('liste_comptes_prets')
    else:
        form = CompteRaPretForm(initial={
            'client': client_id,
            'statut': statut_actif,
            'type_pret': typp,
            'compte_pretactuel': idpret,
            'reste_actuel': reste,
            'montant_actuel': pretactuel.somme_initiale
        })

    context = {
        'form': form,
        'client': client_id,
        'etud': etud,
        'compte_pretactuel': idpret,
        'reste_actuel': reste,
        'montant_actuel': pretactuel.somme_initiale
    }
    return render(request, 'Pages/Rachat/ajouter_rachat_compte_pret.html', context)

# _______________________________________________________________________________________________________________________________________________________________
def create_rachatpretact(request, idpret):
    statut_actif = Statuts.objects.get(statut='Actif')
    statut_nactif = get_object_or_404(Statuts, statut='Non Actif')
    pretactuel = get_object_or_404(ComptePretsact, pk=idpret)
    echeancepretactuelre = Echeancieract.objects.filter(compte_pretact=idpret, est_paye=0)
    reste = sum(echeancepretactuelr.montant_echeance for echeancepretactuelr in echeancepretactuelre)

    client_id = pretactuel.actionnaire.id
    etud = Actionnaire.objects.filter(id=client_id)
    nombre = ComptePretsact.objects.count()
    typp = Typeprets.objects.get(id=3)



    if request.method == 'POST':
        form = CompteRaPretFormact(request.POST)
        if form.is_valid():
            compte_pret = form.save(commit=False)
            
            if request.user.is_authenticated and isinstance(request.user, Utilisateurs):
                agent = request.user
            
            compte_pret.agent = request.user
            compte_pret.type_pret = typp
            # statut_actif = Statuts.objects.get(statut='Actif')
            # form.instance.statut = statut_actif
            compte_pret.actionnaire_id = client_id
            compte_pret.date_demande = timezone.now()
            compte_pret.numero_compte = f"PR{timezone.now().strftime('%Y%m%d%H%M%S')}"

            duree_en_mois = form.cleaned_data['duree_en_mois']
            compte_pret.date_fin_pret = compte_pret.date_debut_pret + timedelta(days=30 * duree_en_mois)

            somme_initiale = compte_pret.somme_initiale
            #somme_initiale = compte_pret.somme_initiale - reste
            taux_interet = compte_pret.taux_interet / 100
            taux_garantie = 15 / 100
            statut_actif = get_object_or_404(Statuts, statut='Actif')
            Conf = Confconstantes.objects.filter(statut=statut_actif).first()
            taux_kha = Conf.partepargne
            taux_khaa = Conf.partfraisdos

            if compte_pret.type_pret_id == 1:  # TYPE DE PRET avec versement d’une garantie
                interets = somme_initiale * Decimal(taux_interet) * duree_en_mois
            elif compte_pret.type_pret_id == 2:  # TYPE DE PRET sans versement de la garantie au préalable
                interets = (somme_initiale * Decimal(taux_garantie)) + somme_initiale * Decimal(taux_interet) * 10
            elif compte_pret.type_pret_id == 3:  # TYPE DE PRET le client ayant un compte avec KHA
                interets = somme_initiale * Decimal(taux_interet) * duree_en_mois
            else:
                interets = 0

            
            compte_pret.solde = somme_initiale + interets + (somme_initiale * Decimal(taux_kha)) + (somme_initiale * Decimal(taux_khaa))
            

            Rachats.objects.create(
                actionnaire=pretactuel.actionnaire,
                date_rachat=timezone.now(),
                compte_pretactuel=pretactuel,
                montant_actuel=pretactuel.somme_initiale,
                reste_actuel=reste,
                compte_pretnew=compte_pret.numero_compte,
                montant_new=compte_pret.somme_initiale
            )

             # Créer une nouvelle transaction de prêt
            #transactionpret = TransactionPretact.objects.create(
            #    compte_pret=compte_pret,
            #    montant=somme_initiale,
            #    date_transaction=timezone.now(),
            #    type_transaction='Virement',  # À adapter en fonction de votre logique
            #    agent=request.user  # Assurez-vous que cela pointe vers l'utilisateur connecté
            #)

            

            pretactuel.statut = statut_nactif
            pretactuel.save()

            compte_pret.somme_initiale = somme_initiale
            compte_pret.statut = statut_actif
            compte_pret.save()

            
#
            # Vérifier si la date de cotisation future est dépassée
            for echeancepretactuel in echeancepretactuelre:
                
                # Calculer la durée écoulée depuis la date de création de la tontine
                
                # Création de la transaction de prêt
                transaction_pret = TransactionPretact.objects.create(
                    compte_pret=echeancepretactuel.compte_pret,
                    montant=echeancepretactuel.montant_echeance,
                    type_transaction='Depot',  # À adapter en fonction de votre logique
                    agent=request.user #if isinstance(request.user, Agent) else None  # Assurez-vous que cela pointe vers l'utilisateur connecté
                )

                compte_pret = echeancepretactuel.compte_pret
                clien = compte_pret.actionnaire
                epar = get_object_or_404(CompteEpargnesact, actionnaire=clien)
                epar.solde += echeancepretactuel.montant_epargne
                epar.save()


                # Mise à jour du solde du compte adhesion associé à l'actionnaire
                statut_actif = get_object_or_404(Statuts, statut='Actif')
                adh = get_object_or_404(CompteAdhesionkhas, statut=statut_actif)
                adh.soldeprecedent = adh.solde
                adh.dateprecedent = adh.datesolde
                adh.datesolde = timezone.now()  # Conserve la date avec fuseau horaire
                adh.solde += echeancepretactuel.montant_adhesion
                adh.save()

                # Mise à jour du solde du compte interet associé à l'actionnaire
                statut_actif = get_object_or_404(Statuts, statut='Actif')
                inter = get_object_or_404(CompteInterets, statut=statut_actif)
                inter.soldeprecedent = inter.solde
                inter.dateprecedent = inter.datesolde
                inter.datesolde = timezone.now()  # Conserve la date avec fuseau horaire
                inter.solde += echeancepretactuel.montant_interet
                inter.save()

                transactionint = TransactionInteret.objects.create(
                    compteinteret=inter,
                    montant=echeancepretactuel.montant_interet,
                    type_transaction='Virement',  # À adapter en fonction de votre logique
                )

                # Mise à jour du solde du compte interet associé à l'actionnaire
                statut_actif = get_object_or_404(Statuts, statut='Actif')
                penal = get_object_or_404(ComptePenalites, statut=statut_actif)
                penal.soldeprecedent = penal.solde
                penal.dateprecedent = penal.datesolde
                penal.datesolde = timezone.now()  # Conserve la date avec fuseau horaire
                penal.solde += echeancepretactuel.montant_penalite
                penal.save()

                if echeancepretactuel.montant_penalite > 0:
                    transactionpenal = TransactionPenaliteHist.objects.create(
                        comptepenalite=penal,
                        montant=echeancepretactuel.montant_penalite,
                        type_transaction='Virement',  # À adapter en fonction de votre logique
                        agent=request.user  # Assurez-vous que cela pointe vers l'utilisateur connecté
                    )

                    # Créer une nouvelle transaction de prêt
                    transactionpenalites = TransactionPenalite.objects.create(
                        compte_pret=echeancepretactuel.compte_pret,
                        echeance=echeancepretactuel,
                        montant=echeancepretactuel.montant_penalite,
                        type_transaction='Virement',  # À adapter en fonction de votre logique
                        agent=request.user  # Assurez-vous que cela pointe vers l'utilisateur connecté
                    )
                
                # Mise à jour du solde du compte principal KHA
                statut_actif = get_object_or_404(Statuts, statut='Actif')
                princ = get_object_or_404(ComptePrincipale, statut=statut_actif)
                princ.totalentree += echeancepretactuel.montant_echeance
                princ.dateentree = timezone.now()  # Conserve la date avec fuseau horaire
                princ.totalgain = ( princ.totalentree - (princ.totalsortie + princ.totaldepenses))
                princ.save()

                # Mise à jour du solde du compte portefeuilles KHA
                statut_actif = get_object_or_404(Statuts, statut='Actif')
                porte = get_object_or_404(ComptePortefeuilles, statut=statut_actif)
                porte.totalentree += (echeancepretactuel.montant_echeance - (echeancepretactuel.montant_interet + echeancepretactuel.montant_epargne + echeancepretactuel.montant_adhesion + echeancepretactuel.montant_penalite))
                porte.totalreste = porte.totalentree - porte.totalsortie
                porte.save()
            #
                # Création de la transaction d'épargne
                transaction_epar = TransactionEpargne.objects.create(
                    compte_epargne=epar,
                    montant=echeancepretactuel.montant_epargne,
                    type_transaction='Virement',  # À adapter en fonction de votre logique
                    agent=request.user   # Assurez-vous que cela pointe vers l'utilisateur connecté
                )
                # MAJ FEV

                # Vérifier si c'est la dernière échéance payée pour le compte prêt
                compte_pret = echeancepretactuel.compte_pret
                dernier_echeance_payee = Echeancier.objects.filter(compte_pret=compte_pret, est_paye=False).order_by('date_echeance').first()
                if not dernier_echeance_payee:
                    # Si aucune échéance impayée, mettre le statut du compte prêt en inactif
                    compte_pret.statut = Statuts.objects.get(statut='Non Actif')
                    compte_pret.save()

                    # Mettre à jour le statut du contrat sponsor
                    try:
                        cont = Contratsponsor.objects.get(numero_compte=compte_pret.numero_compte)
                        cont.statut = Statuts.objects.get(statut='Non Actif')
                        cont.save()
                    except Contratsponsor.DoesNotExist:
                        # Gérer le cas où le contrat sponsor n'existe pas
                        pass


                        #API___ Juillet 2
                statut_actif = Statuts.objects.get(statut='Actif')
                kha = get_object_or_404(CompteKha, statut=statut_actif)
                kha.soldeprecedent = kha.solde
                kha.dateprecedent = kha.datesolde
                kha.datesolde = timezone.now()
                kha.solde += echeancepretactuel.montant_epargne
                kha.save()

                transactionkha = TransactionKha.objects.create(
                    comptekha=kha,
                    montant=echeancepretactuel.montant_epargne,
                    type_transaction='Virement',  # À adapter en fonction de votre logique
                    agent=request.user #if isinstance(request.user, Agent) else None  # Assurez-vous que cela pointe vers l'utilisateur connecté
                )

                transactionadh = TransactionAdhesionkha.objects.create(
                    compteAdhessionkha=adh,
                    montant=echeancepretactuel.montant_adhesion,
                    type_transaction='Virement',  # À adapter en fonction de votre logique
                    agent=request.user #if isinstance(request.user, Agent) else None  # Assurez-vous que cela pointe vers l'utilisateur connecté
                )

                # Associer le compte prêt au client spécifié par l'ID
                statut_actif = get_object_or_404(Statuts, statut='Actif')
                Conf = Confconstantes.objects.filter(statut=statut_actif).first()
                taux_kha = Conf.partepargne
                taux_com = Conf.partcom

                compte_pret = echeancepretactuel.compte_pret
                # Mettre à jour l'agent avec son ID
                comm = get_object_or_404(ComptePretsact, id=compte_pret.id)
                com = get_object_or_404(Agent, id=comm.com.id)  # Utilisez .id pour obtenir l'ID de l'objet

                # Assurez-vous que la commission existe pour l'agent, sinon créez-la
                commission, created = Commissions.objects.get_or_create(agent=com.user, defaults={
                    'solde': 0,
                    'soldeprecedent': 0,
                    'datesolde': timezone.now(),
                    'statut': statut_actif.id  # ou une valeur par défaut
                })

                # Mettre à jour la commission
                commission.soldeprecedent = commission.solde
                commission.date_aide = commission.datesolde
                commission.datesolde = timezone.now()
                commission.solde += (echeancepretactuel.montant_interet * Decimal(taux_com))
                commission.save()

                # Créer une nouvelle transaction de prêt
                transactioncom = TransactionCommissionpret.objects.create(
                    commission=commission,
                    echeance=echeancepretactuel,
                    montant=(echeancepretactuel.montant_interet * Decimal(taux_com)),
                    type_transaction='Virement',  # À adapter en fonction de votre logique
                    agent=request.user  # Assurez-vous que cela pointe vers l'utilisateur connecté
                )
            # Mettre à jour toutes les échéances non payées en est_paye=1
            echeancepretactuelre.update(est_paye=1)

            return redirect('liste_comptes_prets')
    else:
        form = CompteRaPretFormact(initial={
            'actionnaire': client_id,
            'statut': statut_actif,
            'type_pret': typp,
            'compte_pretactuel': idpret,
            'reste_actuel': reste,
            'montant_actuel': pretactuel.somme_initiale
        })

    context = {
        'form': form,
        'actionnaire': client_id,
        'etud': etud,
        'compte_pretactuel': idpret,
        'reste_actuel': reste,
        'montant_actuel': pretactuel.somme_initiale
    }
    return render(request, 'Pages/Rachat/ajouter_rachat_compte_pretact.html', context)
#____________________________________________________________________________________________________________________________________________________________________

def create_or_update_rachatpret(request, idpret, idrachat=None):
    statut_actif = get_object_or_404(Statuts, statut='Actif')
    statut_nactif = get_object_or_404(Statuts, statut='Non Actif')
    pretactuel = get_object_or_404(ComptePrets, pk=idpret)
    echeancepretactuelre = Echeancier.objects.filter(compte_pret=idpret, est_paye=0)
    reste = sum(echeancepretactuelr.montant_echeance for echeancepretactuelr in echeancepretactuelre)
    
    client_id = pretactuel.client.id
    etud = Clients.objects.filter(id=client_id)
    nombre = ComptePrets.objects.count()
    typp = get_object_or_404(Typeprets, id=3)

    etnon = Clients.objects.get(id=client_id)
    na = etnon.nat_client.nat_client   # Initialiser `na` pour éviter l'UnboundLocalError
    #na = None 
    if etnon:
        if na == 'Ordinaire':
            nat = 'CLIENTORDINAIRE'
        elif na == 'Sponsor':
            nat = 'CLIENTSPONSOR'
        elif na == 'Aide':
            nat = 'CLIENTAIDE'
    else:
        # Gérer le cas où aucun client n'est trouvé
        messages.error(request, "Aucun client trouvé avec cet ID.")

    # Vérifier si `na` a été défini correctement avant de l'utiliser
    if nat:
        # Utilisation de la variable `na`
        print(f"Client type: {nat}")
    else:
        # Gérer le cas où `na` est encore `None` (aucune condition `if` n'était remplie)
        messages.error(request, "Le type de client n'a pas pu être déterminé.")


    if idrachat:
        rachat = get_object_or_404(Rachats, pk=idrachat)
        initial_data = {
            'client': rachat.client.id,
            'type_pret': typp,
            'compte_pretactuel': rachat.compte_pretactuel.id,
            'reste_actuel': rachat.reste_actuel,
            'montant_actuel': rachat.montant_actuel
        }
    else:
        rachat = None
        initial_data = {
            'client': client_id,
            'type_pret': typp,
            'compte_pretactuel': idpret,
            'reste_actuel': reste,
            'montant_actuel': pretactuel.somme_initiale
        }

    if request.method == 'POST':
        form = ComptePretForm(request.POST, instance=rachat.compte_pretnew if rachat else None)
        if form.is_valid():
            compte_pret = form.save(commit=False)
            
            if request.user.is_authenticated and hasattr(request.user, 'agent'):
                compte_pret.agent = request.user
            
            compte_pret.agent = request.user
            compte_pret.type_pret = typp
            compte_pret.statut = statut_actif
            compte_pret.client_id = client_id
            compte_pret.date_demande = timezone.now()
            compte_pret.numero_compte = f"PR{timezone.now().strftime('%Y%m%d%H%M%S')}"

            duree_en_mois = form.cleaned_data['duree_en_mois']
            compte_pret.date_fin_pret = compte_pret.date_debut_pret + timedelta(days=30 * duree_en_mois)

            somme_initiale = compte_pret.somme_initiale
            taux_interet = compte_pret.taux_interet / 100
            taux_garantie = 15 / 100
            statut_actif = get_object_or_404(Statuts, statut='Actif')
            Conf = Confconstantes.objects.filter(statut=statut_actif).first()
            taux_kha = Conf.partepargne
            taux_khaa = Conf.partfraisdos

            if compte_pret.type_pret_id == 1:  # TYPE DE PRET avec versement d’une garantie
                interets = somme_initiale * Decimal(taux_interet) * duree_en_mois
            elif compte_pret.type_pret_id == 2:  # TYPE DE PRET sans versement de la garantie au préalable
                interets = (somme_initiale * Decimal(taux_garantie)) + somme_initiale * Decimal(taux_interet) * 10
            elif compte_pret.type_pret_id == 3:  # TYPE DE PRET le client ayant un compte avec KHA
                interets = somme_initiale * Decimal(taux_interet) * duree_en_mois
            else:
                interets = 0

            compte_pret.solde = somme_initiale + interets + (somme_initiale * Decimal(taux_kha)) +  (somme_initiale * Decimal(taux_khaa))
            # compte_pret.save()

            if rachat:
                rachat.compte_pretnew = compte_pret
                rachat.montant_new = compte_pret.somme_initiale
                rachat.save()
            else:
                Rachats.objects.create(
                    client=pretactuel.client,
                    date_rachat=timezone.now(),
                    compte_pretactuel=pretactuel,
                    montant_actuel=pretactuel.somme_initiale,
                    reste_actuel=reste,
                    compte_pretnew=compte_pret,
                    montant_new=compte_pret.somme_initiale
                )

            # Créer une nouvelle transaction de prêt
            TransactionPret.objects.create(
                compte_pret=compte_pret,
                montant=somme_initiale,
                date_transaction=timezone.now(),
                type_transaction='Virement',  # À adapter en fonction de votre logique
                agent=request.user  # Assurez-vous que cela pointe vers l'utilisateur connecté
            )

            # Mettre à jour toutes les échéances non payées en est_paye=1 et rendre le prêt actuel non actif
            echeancepretactuelre.update(est_paye=1)
            pretactuel.statut = statut_nactif
            pretactuel.save()

            compte_pret.somme_initiale = somme_initiale - reste
            compte_pret.naturecompte = nat
            compte_pret.save()

            # Mettre à jour toutes les échéances non payées en est_paye=1
            # echeancepretactuelre.update(est_paye=1)

# Vérifier si la date de cotisation future est dépassée
            for echeancepretactuel in echeancepretactuelre:
                # Calculer la durée écoulée depuis la date de création de la tontine
                if request.user.is_authenticated and isinstance(request.user, Utilisateurs):
                    agent = request.user

                # Création de la transaction de prêt
                transaction_pret = TransactionPret.objects.create(
                    compte_pret=echeancepretactuel.compte_pret,
                    montant=echeancepretactuel.montant_echeance,
                    type_transaction='Depot',  # À adapter en fonction de votre logique
                    agent=request.user #if isinstance(request.user, Agent) else None  # Assurez-vous que cela pointe vers l'utilisateur connecté
                )

                compte_pret = echeancepretactuel.compte_pret
                clien = compte_pret.client
                epar = get_object_or_404(CompteEpargnes, client=clien)
                epar.solde += echeancepretactuel.montant_epargne
                epar.save()

#
                # Mise à jour du solde du compte adhesion associé à l'actionnaire
                statut_actif = get_object_or_404(Statuts, statut='Actif')
                adh = get_object_or_404(CompteAdhesionkhas, statut=statut_actif)
                adh.soldeprecedent = adh.solde
                adh.dateprecedent = adh.datesolde
                adh.datesolde = timezone.now()  # Conserve la date avec fuseau horaire
                adh.solde += echeancepretactuel.montant_adhesion
                adh.save()

                # Mise à jour du solde du compte interet associé à l'actionnaire
                statut_actif = get_object_or_404(Statuts, statut='Actif')
                inter = get_object_or_404(CompteInterets, statut=statut_actif)
                inter.soldeprecedent = inter.solde
                inter.dateprecedent = inter.datesolde
                inter.datesolde = timezone.now()  # Conserve la date avec fuseau horaire
                inter.solde += echeancepretactuel.montant_interet
                inter.save()

                transactionint = TransactionInteret.objects.create(
                    compteinteret=inter,
                    montant=echeancepretactuel.montant_interet,
                    type_transaction='Virement',  # À adapter en fonction de votre logique
                )

                # Mise à jour du solde du compte interet associé à l'actionnaire
                statut_actif = get_object_or_404(Statuts, statut='Actif')
                penal = get_object_or_404(ComptePenalites, statut=statut_actif)
                penal.soldeprecedent = penal.solde
                penal.dateprecedent = penal.datesolde
                penal.datesolde = timezone.now()  # Conserve la date avec fuseau horaire
                penal.solde += echeancepretactuel.montant_penalite
                penal.save()

                if echeancepretactuel.montant_penalite > 0:
                    transactionpenal = TransactionPenaliteHist.objects.create(
                        comptepenalite=penal,
                        montant=echeancepretactuel.montant_penalite,
                        type_transaction='Virement',  # À adapter en fonction de votre logique
                        agent=request.user  # Assurez-vous que cela pointe vers l'utilisateur connecté
                    )

                    # Créer une nouvelle transaction de prêt
                    transactionpenalites = TransactionPenalite.objects.create(
                        compte_pret=echeancepretactuel.compte_pret,
                        echeance=echeancepretactuel,
                        montant=echeancepretactuel.montant_penalite,
                        type_transaction='Virement',  # À adapter en fonction de votre logique
                        agent=request.user  # Assurez-vous que cela pointe vers l'utilisateur connecté
                    )
                
                # Mise à jour du solde du compte principal KHA
                statut_actif = get_object_or_404(Statuts, statut='Actif')
                princ = get_object_or_404(ComptePrincipale, statut=statut_actif)
                princ.totalentree += echeancepretactuel.montant_echeance
                princ.dateentree = timezone.now()  # Conserve la date avec fuseau horaire
                princ.totalgain = ( princ.totalentree - (princ.totalsortie + princ.totaldepenses))
                princ.save()

                # Mise à jour du solde du compte portefeuilles KHA
                statut_actif = get_object_or_404(Statuts, statut='Actif')
                porte = get_object_or_404(ComptePortefeuilles, statut=statut_actif)
                porte.totalentree += (echeancepretactuel.montant_echeance - (echeancepretactuel.montant_interet + echeancepretactuel.montant_epargne + echeancepretactuel.montant_adhesion + echeancepretactuel.montant_penalite))
                porte.totalreste = porte.totalentree - porte.totalsortie
                porte.save()
            #
                # Création de la transaction d'épargne
                transaction_epar = TransactionEpargne.objects.create(
                    compte_epargne=epar,
                    montant=echeancepretactuel.montant_epargne,
                    type_transaction='Virement',  # À adapter en fonction de votre logique
                    agent=request.user   # Assurez-vous que cela pointe vers l'utilisateur connecté
                )
                # MAJ FEV

                # Vérifier si c'est la dernière échéance payée pour le compte prêt
                compte_pret = echeancepretactuel.compte_pret
                dernier_echeance_payee = Echeancier.objects.filter(compte_pret=compte_pret, est_paye=False).order_by('date_echeance').first()
                if not dernier_echeance_payee:
                    # Si aucune échéance impayée, mettre le statut du compte prêt en inactif
                    compte_pret.statut = Statuts.objects.get(statut='Non Actif')
                    compte_pret.save()

                    # Mettre à jour le statut du contrat sponsor
                    try:
                        cont = Contratsponsor.objects.get(numero_compte=compte_pret.numero_compte)
                        cont.statut = Statuts.objects.get(statut='Non Actif')
                        cont.save()
                    except Contratsponsor.DoesNotExist:
                        # Gérer le cas où le contrat sponsor n'existe pas
                        pass


                        #API___ Juillet 2
                statut_actif = Statuts.objects.get(statut='Actif')
                kha = get_object_or_404(CompteKha, statut=statut_actif)
                kha.soldeprecedent = kha.solde
                kha.dateprecedent = kha.datesolde
                kha.datesolde = timezone.now()
                kha.solde += echeancepretactuel.montant_epargne
                kha.save()

                transactionkha = TransactionKha.objects.create(
                    comptekha=kha,
                    montant=echeancepretactuel.montant_epargne,
                    type_transaction='Virement',  # À adapter en fonction de votre logique
                    agent=request.user #if isinstance(request.user, Agent) else None  # Assurez-vous que cela pointe vers l'utilisateur connecté
                )

                transactionadh = TransactionAdhesionkha.objects.create(
                    compteAdhessionkha=adh,
                    montant=echeancepretactuel.montant_adhesion,
                    type_transaction='Virement',  # À adapter en fonction de votre logique
                    agent=request.user #if isinstance(request.user, Agent) else None  # Assurez-vous que cela pointe vers l'utilisateur connecté
                )

                # Associer le compte prêt au client spécifié par l'ID
                statut_actif = get_object_or_404(Statuts, statut='Actif')
                Conf = Confconstantes.objects.filter(statut=statut_actif).first()
                taux_kha = Conf.partepargne
                taux_com = Conf.partcom

                compte_pret = echeancepretactuel.compte_pret
                # Mettre à jour l'agent avec son ID
                comm = get_object_or_404(ComptePrets, id=compte_pret.id)
                com = get_object_or_404(Agent, id=comm.com.id)  # Utilisez .id pour obtenir l'ID de l'objet

                # Assurez-vous que la commission existe pour l'agent, sinon créez-la
                commission, created = Commissions.objects.get_or_create(agent=com.user, defaults={
                    'solde': 0,
                    'soldeprecedent': 0,
                    'datesolde': timezone.now(),
                    'statut': statut_actif.id  # ou une valeur par défaut
                })

                # Mettre à jour la commission
                commission.soldeprecedent = commission.solde
                commission.date_aide = commission.datesolde
                commission.datesolde = timezone.now()
                commission.solde += (echeancepretactuel.montant_interet * Decimal(taux_com))
                commission.save()

                # Créer une nouvelle transaction de prêt
                transactioncom = TransactionCommissionpret.objects.create(
                    commission=commission,
                    echeance=echeancepretactuel,
                    montant=(echeancepretactuel.montant_interet * Decimal(taux_com)),
                    type_transaction='Virement',  # À adapter en fonction de votre logique
                    agent=request.user  # Assurez-vous que cela pointe vers l'utilisateur connecté
                )

            return redirect('liste_comptes_prets')
    else:
        form = ComptePretForm(initial=initial_data)

    context = {
        'form': form,
        'client': client_id,
        'etud': etud,
        'compte_pretactuel': idpret,
        'reste_actuel': reste,
        'montant_actuel': pretactuel.somme_initiale
    }
    return render(request, 'Pages/Rachat/ajouter_rachat_compte_pret.html', context)




def create_or_update_rachatpretm(request, idpret, idrachat=None):
    statut_actif = get_object_or_404(Statuts, statut='Actif')
    pretactuel = get_object_or_404(ComptePrets, pk=idpret)
    echeancepretactuelre = Echeancier.objects.filter(compte_pret=idpret, est_paye=0)
    reste = sum(echeancepretactuelr.montant_echeance for echeancepretactuelr in echeancepretactuelre)

    client_id = pretactuel.client.id
    etud = Clients.objects.filter(id=client_id)
    nombre = ComptePrets.objects.count()
    typp = Typeprets.objects.get(id=3)

    if idrachat:
        rachat = get_object_or_404(Rachats, pk=idrachat)
        initial_data = {
            'client': rachat.client.id,
            'type_pret': typp,
            'compte_pretactuel': rachat.compte_pretactuel.id,
            'reste_actuel': rachat.reste_actuel,
            'montant_actuel': rachat.montant_actuel
        }
    else:
        initial_data = {
            'client': client_id,
            'type_pret': typp,
            'compte_pretactuel': idpret,
            'reste_actuel': reste,
            'montant_actuel': pretactuel.somme_initiale
        }

    if request.method == 'POST':
        form = ComptePretForm(request.POST, instance=rachat.compte_pretnew if idrachat else None)
        if form.is_valid():
            compte_pret = form.save(commit=False)
            
            if request.user.is_authenticated and isinstance(request.user, Agent):
                compte_pret.agent = request.user
            
            compte_pret.type_pret = typp
            statut_actif = Statuts.objects.get(statut='Actif')
            form.instance.statut = statut_actif.id
            compte_pret.client_id = client_id
            compte_pret.date_demande = timezone.now()
            compte_pret.numero_compte = f"PR{timezone.now().strftime('%Y%m%d%H%M%S')}"

            duree_en_mois = form.cleaned_data['duree_en_mois']
            compte_pret.date_fin_pret = compte_pret.date_debut_pret + timedelta(days=30 * duree_en_mois)

            somme_initiale = compte_pret.somme_initiale
            taux_interet = compte_pret.taux_interet / 100
            taux_garantie = 15 / 100
            statut_actif = get_object_or_404(Statuts, statut='Actif')
            Conf = Confconstantes.objects.filter(statut=statut_actif).first()
            taux_kha = Conf.partepargne
            taux_khaa = Conf.partfraisdos

            if compte_pret.type_pret_id == 1:  # TYPE DE PRET avec versement d’une garantie
                interets = somme_initiale * Decimal(taux_interet) * duree_en_mois
            elif compte_pret.type_pret_id == 2:  # TYPE DE PRET sans versement de la garantie au préalable
                interets = (somme_initiale * Decimal(taux_garantie)) + somme_initiale * Decimal(taux_interet) * 10
            elif compte_pret.type_pret_id == 3:  # TYPE DE PRET le client ayant un compte avec KHA
                interets = somme_initiale * Decimal(taux_interet) * duree_en_mois
            else:
                interets = 0

            compte_pret.solde = somme_initiale + interets + (somme_initiale * Decimal(taux_kha)) + (somme_initiale * Decimal(taux_khaa))
            compte_pret.save()

            if idrachat:
                rachat.compte_pretnew = compte_pret.numero_compte
                rachat.montant_new = compte_pret.somme_initiale
                rachat.save()
            else:
                Rachats.objects.create(
                    client=pretactuel.client,
                    date_rachat=timezone.now(),
                    compte_pretactuel=pretactuel,
                    montant_actuel=pretactuel.somme_initiale,
                    reste_actuel=reste,
                    compte_pretnew=compte_pret.numero_compte,
                    montant_new=compte_pret.somme_initiale
                )

            # Mettre à jour toutes les échéances non payées en est_paye=1
            echeancepretactuelre.update(est_paye=1)

# Vérifier si la date de cotisation future est dépassée
            for echeancepretactuel in echeancepretactuelre:
                # Calculer la durée écoulée depuis la date de création de la tontine
                if request.user.is_authenticated and isinstance(request.user, Utilisateurs):
                    agent = request.user

                # Création de la transaction de prêt
                transaction_pret = TransactionPret.objects.create(
                    compte_pret=echeancepretactuel.compte_pret,
                    montant=echeancepretactuel.montant_echeance,
                    type_transaction='Depot',  # À adapter en fonction de votre logique
                    agent=request.user #if isinstance(request.user, Agent) else None  # Assurez-vous que cela pointe vers l'utilisateur connecté
                )

                compte_pret = echeancepretactuel.compte_pret
                clien = compte_pret.client
                epar = get_object_or_404(CompteEpargnes, client=clien)
                epar.solde += echeancepretactuel.montant_epargne
                epar.save()

#
                # Mise à jour du solde du compte adhesion associé à l'actionnaire
                statut_actif = get_object_or_404(Statuts, statut='Actif')
                adh = get_object_or_404(CompteAdhesionkhas, statut=statut_actif)
                adh.soldeprecedent = adh.solde
                adh.dateprecedent = adh.datesolde
                adh.datesolde = timezone.now()  # Conserve la date avec fuseau horaire
                adh.solde += echeancepretactuel.montant_adhesion
                adh.save()

                # Mise à jour du solde du compte interet associé à l'actionnaire
                statut_actif = get_object_or_404(Statuts, statut='Actif')
                inter = get_object_or_404(CompteInterets, statut=statut_actif)
                inter.soldeprecedent = inter.solde
                inter.dateprecedent = inter.datesolde
                inter.datesolde = timezone.now()  # Conserve la date avec fuseau horaire
                inter.solde += echeancepretactuel.montant_interet
                inter.save()

                transactionint = TransactionInteret.objects.create(
                    compteinteret=inter,
                    montant=echeancepretactuel.montant_interet,
                    type_transaction='Virement',  # À adapter en fonction de votre logique
                )

                # Mise à jour du solde du compte interet associé à l'actionnaire
                statut_actif = get_object_or_404(Statuts, statut='Actif')
                penal = get_object_or_404(ComptePenalites, statut=statut_actif)
                penal.soldeprecedent = penal.solde
                penal.dateprecedent = penal.datesolde
                penal.datesolde = timezone.now()  # Conserve la date avec fuseau horaire
                penal.solde += echeancepretactuel.montant_penalite
                penal.save()

                if echeancepretactuel.montant_penalite > 0:
                    transactionpenal = TransactionPenaliteHist.objects.create(
                        comptepenalite=penal,
                        montant=echeancepretactuel.montant_penalite,
                        type_transaction='Virement',  # À adapter en fonction de votre logique
                        agent=request.user  # Assurez-vous que cela pointe vers l'utilisateur connecté
                    )

                    # Créer une nouvelle transaction de prêt
                    transactionpenalites = TransactionPenalite.objects.create(
                        compte_pret=echeancepretactuel.compte_pret,
                        echeance=echeancepretactuel,
                        montant=echeancepretactuel.montant_penalite,
                        type_transaction='Virement',  # À adapter en fonction de votre logique
                        agent=request.user  # Assurez-vous que cela pointe vers l'utilisateur connecté
                    )
                
                # Mise à jour du solde du compte principal KHA
                statut_actif = get_object_or_404(Statuts, statut='Actif')
                princ = get_object_or_404(ComptePrincipale, statut=statut_actif)
                princ.totalentree += echeancepretactuel.montant_echeance
                princ.dateentree = timezone.now()  # Conserve la date avec fuseau horaire
                princ.totalgain = ( princ.totalentree - (princ.totalsortie + princ.totaldepenses))
                princ.save()

                # Mise à jour du solde du compte portefeuilles KHA
                statut_actif = get_object_or_404(Statuts, statut='Actif')
                porte = get_object_or_404(ComptePortefeuilles, statut=statut_actif)
                porte.totalentree += (echeancepretactuel.montant_echeance - (echeancepretactuel.montant_interet + echeancepretactuel.montant_epargne + echeancepretactuel.montant_adhesion + echeancepretactuel.montant_penalite))
                porte.totalreste = porte.totalentree - porte.totalsortie
                porte.save()
            #
                # Création de la transaction d'épargne
                transaction_epar = TransactionEpargne.objects.create(
                    compte_epargne=epar,
                    montant=echeancepretactuel.montant_epargne,
                    type_transaction='Virement',  # À adapter en fonction de votre logique
                    agent=request.user   # Assurez-vous que cela pointe vers l'utilisateur connecté
                )
                # MAJ FEV

                # Vérifier si c'est la dernière échéance payée pour le compte prêt
                compte_pret = echeancepretactuel.compte_pret
                dernier_echeance_payee = Echeancier.objects.filter(compte_pret=compte_pret, est_paye=False).order_by('date_echeance').first()
                if not dernier_echeance_payee:
                    # Si aucune échéance impayée, mettre le statut du compte prêt en inactif
                    compte_pret.statut = Statuts.objects.get(statut='Non Actif')
                    compte_pret.save()

                    # Mettre à jour le statut du contrat sponsor
                    try:
                        cont = Contratsponsor.objects.get(numero_compte=compte_pret.numero_compte)
                        cont.statut = Statuts.objects.get(statut='Non Actif')
                        cont.save()
                    except Contratsponsor.DoesNotExist:
                        # Gérer le cas où le contrat sponsor n'existe pas
                        pass


                        #API___ Juillet 2
                statut_actif = Statuts.objects.get(statut='Actif')
                kha = get_object_or_404(CompteKha, statut=statut_actif)
                kha.soldeprecedent = kha.solde
                kha.dateprecedent = kha.datesolde
                kha.datesolde = timezone.now()
                kha.solde += echeancepretactuel.montant_epargne
                kha.save()

                transactionkha = TransactionKha.objects.create(
                    comptekha=kha,
                    montant=echeancepretactuel.montant_epargne,
                    type_transaction='Virement',  # À adapter en fonction de votre logique
                    agent=request.user #if isinstance(request.user, Agent) else None  # Assurez-vous que cela pointe vers l'utilisateur connecté
                )

                transactionadh = TransactionAdhesionkha.objects.create(
                    compteAdhessionkha=adh,
                    montant=echeancepretactuel.montant_adhesion,
                    type_transaction='Virement',  # À adapter en fonction de votre logique
                    agent=request.user #if isinstance(request.user, Agent) else None  # Assurez-vous que cela pointe vers l'utilisateur connecté
                )

                # Associer le compte prêt au client spécifié par l'ID
                statut_actif = get_object_or_404(Statuts, statut='Actif')
                Conf = Confconstantes.objects.filter(statut=statut_actif).first()
                taux_kha = Conf.partepargne
                taux_com = Conf.partcom

                compte_pret = echeancepretactuel.compte_pret
                # Mettre à jour l'agent avec son ID
                comm = get_object_or_404(ComptePrets, id=compte_pret.id)
                com = get_object_or_404(Agent, id=comm.com.id)  # Utilisez .id pour obtenir l'ID de l'objet

                # Assurez-vous que la commission existe pour l'agent, sinon créez-la
                commission, created = Commissions.objects.get_or_create(agent=com.user, defaults={
                    'solde': 0,
                    'soldeprecedent': 0,
                    'datesolde': timezone.now(),
                    'statut': statut_actif.id  # ou une valeur par défaut
                })

                # Mettre à jour la commission
                commission.soldeprecedent = commission.solde
                commission.date_aide = commission.datesolde
                commission.datesolde = timezone.now()
                commission.solde += (echeancepretactuel.montant_interet * Decimal(taux_com))
                commission.save()

                # Créer une nouvelle transaction de prêt
                transactioncom = TransactionCommissionpret.objects.create(
                    commission=commission,
                    echeance=echeancepretactuel,
                    montant=(echeancepretactuel.montant_interet * Decimal(taux_com)),
                    type_transaction='Virement',  # À adapter en fonction de votre logique
                    agent=request.user  # Assurez-vous que cela pointe vers l'utilisateur connecté
                )



            

            return redirect('liste_comptes_prets')
    else:
        form = ComptePretForm(initial=initial_data)

    context = {
        'form': form,
        'client': client_id,
        'etud': etud,
        'compte_pretactuel': idpret,
        'reste_actuel': reste,
        'montant_actuel': pretactuel.somme_initiale
    }
    return render(request, 'Pages/Comptepret/modifier_rachat_compte_pret.html', context)

def rachat_list(request):
    comptes_prets = ComptePrets.objects.all().select_related('client', 'statut', 'type_pret', 'agent')
    rachats = Rachats.objects.all().select_related('client', 'compte_pretactuel')

    context = {
        'comptes_prets': comptes_prets,
        'rachats': rachats
    }
    
    return render(request, 'Pages/Rachat/liste_rachatsp.html', context)

def rachat_listt(request):
    rachats = Rachats.objects.all()
    return render(request, 'Pages/Rachat/liste_rachats.html', {'rachats': rachats})

def update_rachat(request, pk):
    rachat = get_object_or_404(Rachats, pk=pk)
    if request.method == 'POST':
        form = RachatForm(request.POST, instance=rachat)
        if form.is_valid():
            form.save()
            return redirect('rachat_list')
    else:
        form = RachatForm(instance=rachat)
    return render(request, 'Pages/Rachat/modifier_rachat.html', {'form': form})

def delete_rachat(request, pk):
    rachat = get_object_or_404(Rachats, pk=pk)
    if request.method == 'POST':
        rachat.delete()
        return redirect('rachat_list')
    return render(request, 'Pages/Rachat/confirmer_suppression.html', {'rachat': rachat})


#DIVIDENDES  __________________________________________________________________________________________________________________________________________________

# CALCUL DES DIVIDENDES ET ENREGISTREMENTS
def dividende(request):
    # Récupérer les actionnaires et leurs informations
    actionnaires_type_1 = Actionnaire.objects.filter(type_act_id=1)
    actionnaires_type_2 = Actionnaire.objects.filter(type_act_id=2)

    # Récupérer le montant à répartir entre les actionnaires
    echeances_payees_mois = Echeancier.objects.filter(date_echeance__month=date.today().month, est_paye=True)
    echeances_payees_moisact = Echeancieract.objects.filter(date_echeance__month=date.today().month, est_paye=True)
    benefice_mois = sum(echeance.montant_interet for echeance in echeances_payees_mois) + sum(echeance.montant_interet for echeance in echeances_payees_moisact)
    depenses_mois = Depense.objects.filter(date__month=date.today().month).aggregate(Sum('montant'))['montant__sum'] or 0
    montant_a_repartir = benefice_mois - depenses_mois

    # Répartir les montants selon le type d'actionnaire
    montant_a_repartir_type_1 = montant_a_repartir * (2/3)
    montant_a_repartir_type_2 = montant_a_repartir * (1/3)

    # Calculer les parts et montants à payer pour les actionnaires de type 1
    total_apport_type_1 = sum(actionnaire.apport for actionnaire in actionnaires_type_1)
    for actionnaire in actionnaires_type_1:
        actionnaire.part = round((actionnaire.apport / total_apport_type_1) * 100, 2)
        actionnaire.montant_a_payer = round((actionnaire.part / 100) * montant_a_repartir_type_1, 2)
        actionnaire.dividende += actionnaire.montant_a_payer
        actionnaire.save()
        # Créer une nouvelle transaction de prêt
        TransactionRistourne.objects.create(
            actionnaire=actionnaire,
            montant=actionnaire.montant_a_payer,
            date_transaction=timezone.now(),
            type_transaction='Virement',  # À adapter en fonction de votre logique
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


    # Calculer les parts et montants à payer pour les actionnaires de type 2
    total_apport_type_2 = sum(actionnaire.apport for actionnaire in actionnaires_type_2)
    for actionnaire in actionnaires_type_2:
        actionnaire.part = round((actionnaire.apport / total_apport_type_2) * 100, 2)
        actionnaire.montant_a_payer = round((actionnaire.part / 100) * montant_a_repartir_type_2, 2)
        actionnaire.dividende += actionnaire.montant_a_payer
        actionnaire.save()
        # Créer une nouvelle transaction de prêt
        TransactionRistourne.objects.create(
            actionnaire=actionnaire,
            montant=actionnaire.montant_a_payer,
            date_transaction=timezone.now(),
            type_transaction='Retrait',  # À adapter en fonction de votre logique
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

    return render(request, 'dividende.html', {'actionnaires': actionnaires_type_1.union(actionnaires_type_2)})


# Dans votre fichier views.py
def calcul_dividendes1(request):
    # Récupérer les actionnaires et leurs informations
    actionnaires_type_1 = Actionnaire.objects.filter(type_act_id=1)
    actionnaires_type_2 = Actionnaire.objects.filter(type_act_id=2)

    # Récupérer le montant à répartir entre les actionnaires
    echeances_payees_mois = Echeancier.objects.filter(date_echeance__month=date.today().month, est_paye=True)
    echeances_payees_moisact = Echeancieract.objects.filter(date_echeance__month=date.today().month, est_paye=True)
    benefice_mois = sum(echeance.montant_interet for echeance in echeances_payees_mois) + sum(echeance.montant_interet for echeance in echeances_payees_moisact)
    depenses_mois = Depense.objects.filter(date__month=date.today().month).aggregate(Sum('montant'))['montant__sum'] or 0
    montant_a_repartir = benefice_mois - depenses_mois

    # Répartir les montants selon le type d'actionnaire
    # Répartir les montants selon le type d'actionnaire
    montant_a_repartir_type_1 = montant_a_repartir * Decimal('2.0') / Decimal('3.0')
    montant_a_repartir_type_2 = montant_a_repartir * Decimal('1.0') / Decimal('3.0')


    # Calculer les parts et montants à payer pour les actionnaires de type 1
    total_apport_type_1 = sum(actionnaire.apport for actionnaire in actionnaires_type_1)
    for actionnaire in actionnaires_type_1:
        actionnaire.part = round((actionnaire.apport / total_apport_type_1) * 100, 2)
        actionnaire.montant_a_payer = round((actionnaire.part / 100) * montant_a_repartir_type_1, 2)
        actionnaire.dividende += actionnaire.montant_a_payer
        actionnaire.save()
        # Créer une nouvelle transaction de prêt
        TransactionRistourne.objects.create(
            actionnaire=actionnaire,
            montant=actionnaire.montant_a_payer,
            date_transaction=timezone.now(),
            type_transaction='Virement',  # À adapter en fonction de votre logique
        )

    # Calculer les parts et montants à payer pour les actionnaires de type 2
    total_apport_type_2 = sum(actionnaire.apport for actionnaire in actionnaires_type_2)
    for actionnaire in actionnaires_type_2:
        actionnaire.part = round((actionnaire.apport / total_apport_type_2) * 100, 2)
        actionnaire.montant_a_payer = round((actionnaire.part / 100) * montant_a_repartir_type_2, 2)
        actionnaire.dividende += actionnaire.montant_a_payer
        actionnaire.save()

        # Créer une nouvelle transaction de prêt
        TransactionRistourne.objects.create(
            actionnaire=actionnaire,
            montant=actionnaire.montant_a_payer,
            date_transaction=timezone.now(),
            type_transaction='Virement',  # À adapter en fonction de votre logique
        )

    # Retourner les informations mises à jour en JSON
    actionnaires = actionnaires_type_1.union(actionnaires_type_2)
    data = [
        {
            'id': actionnaire.id,
            'nom': actionnaire.nom,
            'prenom': actionnaire.prenom,
            'telephone': actionnaire.telephone,
            'dividende': float(actionnaire.dividende),
        }
        for actionnaire in actionnaires
    ]

    return JsonResponse(data, safe=False)

#-----------------------------------------
from django.utils import timezone
from datetime import date
def calcul_dividendes(request):

   # Récupérer
    statut_actif = get_object_or_404(Statuts, statut='Actif')
    Conf = Confconstantes.objects.filter(statut=statut_actif).first()
    dureecoopa = Conf.dureecoopa
    dureecoopn = Conf.dureecoopn
    date_today = datetime.now().date()
    date_un_mois_actif = date_today - timedelta(days=dureecoopa)
    date_un_mois_passif = date_today - timedelta(days=dureecoopn)  

    # Récupérer les actionnaires et leurs informations
    actionnaires_type_1 = Actionnaire.objects.filter(type_act_id=1, date_adhesion__gte=date_un_mois_actif)
    #actionnaires_type_2 = Actionnaire.objects.filter(type_act_id=2, date_adhesion__gte=date_un_mois_passif)
    #actionnaires_type_2 = Actionnaire.objects.filter(type_act_id=2)
    statut_actif = Statuts.objects.get(statut='Actif')
    actionnaires_type_2 = Actionnaire.objects.filter(
    type_act_id=2, date_adhesion__gte=date_un_mois_passif ,
    comptepretsact__isnull=True, 
    # comptepretsact__statut__statut=statut_actif
    )


    # Récupérer le montant à répartir entre les actionnaires
    echeances_payees_mois = Echeancier.objects.filter(date_echeance__month=date.today().month, est_paye=True)
    echeances_payees_moisact = Echeancieract.objects.filter(date_echeance__month=date.today().month, est_paye=True)
    benefice_mois = sum(echeance.montant_interet for echeance in echeances_payees_mois) + sum(echeance.montant_interet for echeance in echeances_payees_moisact)
    #depenses_mois = Depense.objects.filter(date__month=date.today().month).aggregate(Sum('montant'))['montant__sum'] or 0
    


    today = timezone.localtime(timezone.now()).date()
    depenses_mois = Depense.objects.filter(date__month=date.today().month)
    print(depenses_mois)  # Cela vous montrera quelles entrées sont prises en compte.
    total_montant = depenses_mois.aggregate(Sum('montant'))['montant__sum'] or 0
    print(total_montant)




    today = timezone.localtime(timezone.now()).date()
    depenses_mois = Depense.objects.filter(date__month=today.month, date__year=today.year).aggregate(Sum('montant'))['montant__sum'] or 0
    montant_a_repartir = benefice_mois - depenses_mois

    # Répartir les montants selon le type d'actionnaire
    # Répartir les montants selon le type d'actionnaire
    statut_actif = get_object_or_404(Statuts, statut='Actif')
    Conf = Confconstantes.objects.filter(statut=statut_actif).first()
    #montant_a_repartir_type_1 = montant_a_repartir * Decimal('2.0') / Decimal('3.0')
    #montant_a_repartir_type_2 = montant_a_repartir * Decimal('1.0') / Decimal('3.0')
    montant_a_repartir_type_1 = montant_a_repartir * Decimal(Conf.partactif)
    montant_a_repartir_type_chef = montant_a_repartir * Decimal(Conf.partnonactif)* Decimal(Conf.partrespo)
    #montant_a_repartir_type_2 = montant_a_repartir * Decimal(Conf.partnonactif)
    montant_a_repartir_type_2 = (montant_a_repartir * Decimal(Conf.partnonactif)) - montant_a_repartir_type_chef

    print(depenses_mois)
    # Compter le nombre d'aides dont a bénéficié le client
    chef = get_object_or_404(CompteFondateur, statut=statut_actif)
    chef.dateprecedent= chef.datesolde
    chef.soldeprecedent = chef.solde
    chef.datesolde = timezone.now()
    chef.solde += montant_a_repartir_type_chef
    chef.save()

   

    # Calculer les parts et montants à payer pour les actionnaires de type 1
    total_apport_type_1 = sum(actionnaire.apport for actionnaire in actionnaires_type_1)
    for actionnaire in actionnaires_type_1:
        actionnaire.part = round((actionnaire.apport / total_apport_type_1) * 100, 2)
        actionnaire.montant_a_payer = round((actionnaire.part / 100) * montant_a_repartir_type_1, 2)
        actionnaire.dividende += actionnaire.montant_a_payer
        actionnaire.save()
        # Créer une nouvelle transaction de prêt
        TransactionRistourne.objects.create(
            actionnaire=actionnaire,
            montant=actionnaire.montant_a_payer,
            date_transaction=timezone.now(),
            type_transaction='Virement',  # À adapter en fonction de votre logique
        )

    # Calculer les parts et montants à payer pour les actionnaires de type 2
    total_apport_type_2 = sum(actionnaire.apport for actionnaire in actionnaires_type_2)
    for actionnaire in actionnaires_type_2:
        actionnaire.part = round((actionnaire.apport / total_apport_type_2) * 100, 2)
        actionnaire.montant_a_payer = round((actionnaire.part / 100) * montant_a_repartir_type_2, 2)
        actionnaire.dividende += actionnaire.montant_a_payer
        actionnaire.save()

        # Créer une nouvelle transaction de prêt
        TransactionRistourne.objects.create(
            actionnaire=actionnaire,
            montant=actionnaire.montant_a_payer,
            date_transaction=timezone.now(),
            type_transaction='Virement',  # À adapter en fonction de votre logique
        )

    # Retourner les informations mises à jour en JSON
    actionnaires = actionnaires_type_1.union(actionnaires_type_2)
    data = [
        {
            'id': actionnaire.id,
            'nom': actionnaire.nom,
            'prenom': actionnaire.prenom,
            'telephone': actionnaire.telephone,
            'dividende': float(actionnaire.dividende),
        }
        for actionnaire in actionnaires
    ]

    return JsonResponse(data, safe=False)
#______________________________________________________________________________________________________________________________________________________


# CALCUL DES PENALITE ________________________________________________________________________________________________________________________________ 
from django.shortcuts import render
from datetime import date
from .models import Echeancier, Echeancieract

def penalite(request):
    # Récupérer les échéances non payées dans le passé
    echeances_non_payees = Echeancier.objects.filter(date_echeance__lt=date.today(), est_paye=False)
    echeances_non_payeesact = Echeancieract.objects.filter(date_echeance__lt=date.today(), est_paye=False)
    
    # Définir le taux de pénalité
    taux_penalite = Decimal('0.017')  # 1.7%

    # Calculer la pénalité et mettre à jour le montant pour chaque échéance
    for echeance in echeances_non_payees:
        penalite = echeance.montant_echeance * taux_penalite
        echeance.montant_echeance += penalite
        echeance.save()  # Enregistrer les modifications dans la base de données
        # Créer une nouvelle transaction de prêt

        TransactionPenalite.objects.create(
            compte_pret=echeance.compte_pret.id,
            echeance=echeance.id,
            montant=penalite,
            date_transaction=timezone.now(),
            type_transaction='Virement',  # À adapter en fonction de votre logique
        )
    
    for echeanceact in echeances_non_payeesact:
        penalite = echeanceact.montant_echeance * taux_penalite
        echeanceact.montant_echeance += penalite
        echeanceact.save()  # Enregistrer les modifications dans la base de données

        TransactionPenaliteact.objects.create(
            compte_pretact=echeanceact.compte_pretact.id,
            echeance=echeanceact.id,
            montant=penalite,
            date_transaction=timezone.now(),
            type_transaction='Virement',  # À adapter en fonction de votre logique
        )

    # Récupérer les échéances mises à jour pour le contexte du rendu
    echeances_non_payees = Echeancier.objects.filter(date_echeance__lt=date.today(), est_paye=False)
    echeances_non_payeesact = Echeancieract.objects.filter(date_echeance__lt=date.today(), est_paye=False)

    context = {
        'echeances_non_payees': echeances_non_payees,
        'echeances_non_payeesact': echeances_non_payeesact
    }

    return render(request, 'Pages/Comptepret/listeecheancenon.html', context)
# __________________________________________________________________________________________________________________________________________________________

# __________________________________________________________________________________________________________________________________________________________
from django.http import JsonResponse
from django.utils import timezone
from datetime import date
from .models import Echeancier, Echeancieract, TransactionPenalite, TransactionPenaliteact

def penalitejson(request):
    # Récupérer les échéances non payées dans le passé
    echeances_non_payees = Echeancier.objects.filter(date_echeance__lt=date.today(), est_paye=False)
    echeances_non_payeesact = Echeancieract.objects.filter(date_echeance__lt=date.today(), est_paye=False)
    
    # Définir le taux de pénalité
    # taux_penalite = Decimal('0.017')  # 1.7%
    statut_actif = get_object_or_404(Statuts, statut='Actif')
    Conf = Confconstantes.objects.filter(statut=statut_actif).first()
    taux_penalite = Conf.partpenalite

    # Calculer la pénalité et mettre à jour le montant pour chaque échéance
    for echeance in echeances_non_payees:
        penalite = echeance.montant_echeance * taux_penalite
        echeance.ancien_echeance = echeance.montant_echeance
        echeance.montant_penalite = penalite
        echeance.montant_echeance += penalite
        echeance.save()  # Enregistrer les modifications dans la base de données
        
        # Créer une nouvelle transaction de pénalité
        TransactionPenalite.objects.create(
            compte_pret=echeance.compte_pret,
            echeance=echeance,
            montant=penalite,
            date_transaction=timezone.now(),
            type_transaction='Virement',  # À adapter en fonction de votre logique
        )
    
    for echeanceact in echeances_non_payeesact:
        penalite = echeanceact.montant_echeance * taux_penalite
        echeanceact.ancien_echeance = echeanceact.montant_echeance
        echeanceact.montant_penalite = penalite
        echeanceact.montant_echeance += penalite
        echeanceact.save()  # Enregistrer les modifications dans la base de données
        
        # Créer une nouvelle transaction de pénalité
        TransactionPenaliteact.objects.create(
            compte_pret=echeanceact.compte_pretact,
            echeance=echeanceact,
            montant=penalite,
            date_transaction=timezone.now(),
            type_transaction='Virement',  # À adapter en fonction de votre logique
        )

    # Préparer les données pour la réponse JSON
    echeances_non_payees_data = list(echeances_non_payees.values('id', 'date_echeance', 'montant_echeance'))
    echeances_non_payeesact_data = list(echeances_non_payeesact.values('id', 'date_echeance', 'montant_echeance'))

    response_data = {
        'echeances_non_payees': echeances_non_payees_data,
        'echeances_non_payeesact': echeances_non_payeesact_data
    }

    return JsonResponse(response_data)
# __________________________________________________________________________________________________________________________________________________________

# __________________________________________________________________________________________________________________________________________________________
from datetime import date, timedelta
from decimal import Decimal
from django.utils import timezone
from django.http import JsonResponse

def penalite_tontines1(request):
    # Récupérer toutes les tontines dont la date de cotisation future est dépassée
    tontines_en_tout = Tontines.objects.filter()
    tontines_en_retard = Tontines.objects.filter(date_futurcotisation__lt=date.today())

    for tontine in tontines_en_retard:
               # Calculer la pénalité en fonction de la différence entre aujourd'hui et la prochaine cotisation prévue
        penaliteton = (date.today() - tontine.date_futurcotisation).days
        if penaliteton > 0:

            # Mise à jour du champ 'penaliteton'
            tontine.penaliteton += penaliteton

        # Mise à jour du solde et de la date_palier
            #tontine.solde -= montant_penalite
            tontine.date_palier += timedelta(days=penaliteton)  # Ajoute les jours de pénalité à la date du palier

        # Sauvegarder les modifications dans la base de données
        tontine.save()

    for tontinetout in tontines_en_tout:
        # Calculer la durée écoulée depuis la date de création de la tontine
        duree = (date.today() - tontinetout.date_tontine).days        

        # Sauvegarder les modifications dans la base de données
        tontinetout.duree = duree
        tontinetout.save()

    # Préparer les données pour la réponse JSON
    tontines_data = list(tontines_en_retard.values('id', 'numero_tontine', 'duree', 'penaliteton', 'solde', 'date_palier'))

    return JsonResponse({'tontines': tontines_data})

from datetime import date, timedelta
from django.http import JsonResponse

def penalite_tontines(request):
    # Récupérer toutes les tontines
    tontines = Tontines.objects.all()

    # Définir le taux de pénalité (si nécessaire)
    # taux_penalite = Decimal('0.017')  # Exemple de taux de pénalité (1.7%)

    # Parcourir toutes les tontines et calculer la durée et les pénalités
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

    # Préparer les données pour la réponse JSON
    tontines_data = list(tontines.values('id', 'numero_tontine', 'duree', 'penaliteton', 'solde', 'date_palier'))

    # Retourner les données JSON
    return JsonResponse({'tontines': tontines_data})

# __________________________________________________________________________________________________________________________________________________________


# PRESENTATION_____________________________________________________________________________________________________________________________________________
def liste_presentation(request):
    presents = Presentation.objects.filter()
    return render(request, 'Pages/Presentations/liste_presentation.html', {'presents': presents})

# Vue pour creer une PresentationForm
def create_presentation(request):
    if request.method == 'POST':
        form = PresentationForm(request.POST, request.FILES)
        if form.is_valid():
        # Enregistrement du formulaire
            form.save()

            # Redirection après création
            return redirect('liste_presentation')
        else:
            # Si le formulaire n'est pas valide, imprime les erreurs
            print("Formulaire invalide :", form.errors)
    else:
        form = PresentationForm()
    
    return render(request, 'Pages/Presentations/create_presentation.html', {'form': form})

def modifier_presentation(request, pk):
    presentation = get_object_or_404(Presentation, pk=pk)
    if request.method == 'POST':
        form = PresentationForm(request.POST, request.FILES, instance=presentation)
        if form.is_valid():
            form.save()
            return redirect('liste_presentation')
    else:
        form = PresentationForm(instance=presentation)
    
    return render(request, 'Pages/Presentations/create_presentation.html', {'form': form})
#______________________________________________________________________________________________________________________________________________

#AFFICHER HISTORIQUES __________________________________________________________________________________________________________________________
def liste_echeances_cli_payees(request):
    # Récupérer les échéances non payées dans le passé
    echeances_non_payees = Echeancier.objects.filter(est_paye=True)

    context = {
        'echeances_non_payees': echeances_non_payees
    }

    return render(request, 'Pages/Historiques/listeecheancecli.html', context)

def liste_echeances_act_payees(request):
    # Récupérer les échéances non payées dans le passé
    echeances_non_payeesact = Echeancieract.objects.filter(est_paye=True)

    context = {
        'echeances_non_payeesact': echeances_non_payeesact
    }

    return render(request, 'Pages/Historiques/listeecheanceact.html', context)

# MARQUER UNE ÉCHÉANCE COMME NON PAYÉE (ANNULATION DE PAIEMENT) CLIENT ------------------------------------------------------------------
@login_required  # Décorateur pour s'assurer que l'utilisateur est connecté
def annuler_est_payere(request, actionnaire_id):
    echance = get_object_or_404(Echeancier, pk=actionnaire_id)
    
    # Vérifier que l'échéance est déjà payée avant de continuer
    if echance.est_paye:
        # Marquer l'échéance comme non payée
        echance.est_paye = False
        echance.save()

        if request.user.is_authenticated and isinstance(request.user, Utilisateurs):
            agent = request.user

        # Mise à jour des soldes du compte épargne associé à l'actionnaire
        compte_pret = echance.compte_pret
        clien = compte_pret.client
        epar = get_object_or_404(CompteEpargnes, client=clien)

        # Déduire le montant de l'épargne de l'échéance du solde d'épargne
        epar.solde -= echance.montant_epargne
        epar.save()

        # Mise à jour du solde du compte adhésion associé à l'actionnaire
        statut_actif = get_object_or_404(Statuts, statut='Actif')
        adh = get_object_or_404(CompteAdhesionkhas, statut=statut_actif)
        adh.soldeprecedent += adh.solde
        adh.dateprecedent = adh.datesolde
        adh.datesolde = timezone.now()  # Conserve la date avec fuseau horaire
        adh.solde -= echance.montant_epargne
        adh.save()

        # Annuler la transaction de prêt associée à cette échéance
        TransactionPret.objects.filter(compte_pret=compte_pret, montant=echance.montant_echeance, agent=request.user).delete()

        # Annuler la transaction d'épargne associée
        TransactionEpargne.objects.filter(compte_epargne=epar, montant=echance.montant_epargne, agent=request.user).delete()

        # Annuler les transactions KHA et adhésion
        TransactionKha.objects.filter(comptekha__statut=statut_actif, montant=echance.montant_epargne, agent=request.user).delete()
        TransactionAdhesionkha.objects.filter(compteAdhessionkha__statut=statut_actif, montant=echance.montant_adhesion, agent=request.user).delete()

        # Mise à jour de la commission de l'agent
        Conf = Confconstantes.objects.filter(statut=statut_actif).first()
        taux_com = Conf.partcom

        comm = get_object_or_404(ComptePrets, id=compte_pret.id)
        com = get_object_or_404(Agent, id=comm.com.id)

        # Mise à jour ou création de la commission
        commission = Commissions.objects.filter(agent=com.user).first()
        if commission:
            commission.soldeprecedent = commission.solde
            commission.datesolde = timezone.now()
            commission.solde -= (echance.montant_interet * Decimal(taux_com))
            commission.save()

            # Annuler la transaction de commission associée à cette échéance
            TransactionCommissionpret.objects.filter(commission=commission, echeance=echance, montant=(echance.montant_interet * Decimal(taux_com)), agent=request.user).delete()

        #messages.success(request, 'L\'échéance a été annulée avec succès.')
    
    return redirect('liste_echeances_cli_payees')

# MARQUER NON PAYEES DANS HISTORIQUE POUR SOUS COOP ----------------------------------------------------------------------------
def modifier_est_non_payereact(request, actionnaire_id):
    echance = Echeancieract.objects.get(pk=actionnaire_id)
    echance.est_paye = 0  # Marquer l'échéance comme non payée
    echance.save()

    # Supprimer ou ajuster la transaction de prêt créée pour le paiement de l'échéance
    if request.user.is_authenticated and isinstance(request.user, Agent):
        agent = request.user

    # Supprimer la transaction de prêt associée à cette échéance (si nécessaire)
    TransactionPretact.objects.filter(compte_pret=echance.compte_pretact, montant=echance.montant_echeance, type_transaction='Depot').delete()

    statut_actif = Statuts.objects.get(statut='Actif')
    kha = get_object_or_404(CompteKha, statut=statut_actif)
    kha.soldeprecedent = kha.solde
    kha.dateprecedent = kha.datesolde
    kha.datesolde = timezone.now()
    kha.solde -= echance.montant_epargne  # Réduire le solde du montant d'épargne précédemment ajouté
    kha.save()

    # Supprimer la transaction Kha associée à cette échéance
    TransactionKha.objects.filter(comptekha=kha, montant=echance.montant_epargne, type_transaction='Virement').delete()

    # Récupérer l'échéance en question

    # Annuler ou ajuster la commission associée à cette échéance
    statut_actif = get_object_or_404(Statuts, statut='Actif')
    Conf = Confconstantes.objects.filter(statut=statut_actif).first()
    taux_com = Conf.partcom

    compte_pret = echance.compte_pretact
    comm = get_object_or_404(ComptePretsact, id=compte_pret.id)
    etudian = get_object_or_404(Agent, user=comm.agent)

    # Supprimer ou ajuster la commission existante pour l'agent
    commission = Commissions.objects.filter(agent=etudian.user).first()
    if commission:
        commission.soldeprecedent = commission.solde
        commission.date_aide = commission.datesolde
        commission.datesolde = timezone.now()
        commission.solde -= (echance.montant_interet * Decimal(taux_com))  # Réduire le solde de la commission
        commission.save()

        # Supprimer la transaction de commission de prêt associée à cette échéance
        TransactionCommissionpret.objects.filter(commission=commission, echeance=echance, montant=(echance.montant_interet * Decimal(taux_com)), type_transaction='Virement').delete()

    # Vérifier si c'est la dernière échéance non payée pour le compte prêt
    compte_pret = echance.compte_pretact
    dernier_echeance_payee = Echeancieract.objects.filter(compte_pretact=compte_pret, est_paye=False).order_by('date_echeance').first()
    if dernier_echeance_payee:
        # Si une échéance impayée existe, remettre le statut du compte prêt en actif
        compte_pret.statut = Statuts.objects.get(statut='Actif')
        compte_pret.save()

    return redirect('liste_echeances_act_payees')  # Rediriger vers la liste des échéances payées
#______________________________________________________________________________________


# AFFICHER DETAIL UN COMPTE INTERET _________________________________________________________________________________________________________________________________
def detail_compte_interet (request):
    statut_actif = get_object_or_404(Statuts, statut='Actif')
    compte_pret = get_object_or_404(CompteInterets, statut=statut_actif)
    echeanciers = TransactionInteret.objects.filter(compteinteret=compte_pret).order_by('-date_transaction')

    context = {
        'compte_pret': compte_pret,
        'echeanciers': echeanciers,
    }
    return render(request, 'Pages/Compteentreprise/detail_compte_interet.html', context)

# Create ----------------------------------------------------------------------------------------------------------------
def transaction_cpteint(request, id):
    cpte = get_object_or_404(CompteInterets, id=id)
    if request.method == 'POST':
        form = TransactionretraitcpteintForm(request.POST)
        if form.is_valid():
            if request.user.is_authenticated and isinstance(request.user, Agent):
                agent = request.user

            form.instance.agent = request.user  # Assurez-vous que cela pointe vers l'utilisateur connecté           
            form.instance.compteinteret = cpte
            form.instance.type_transaction = 'Retrait'  # À adapter en fonction de votre logique

            # Compter le nombre d'aides dont a bénéficié le client
            epar = get_object_or_404(CompteInterets, id=id)
            epar.soldeprecedent = epar.solde
            epar.dateprecedent = epar.datesolde
            epar.datesolde = timezone.now()
            epar.solde -= form.cleaned_data['montant']
                
            epar.save()

            form.save()
            return redirect('detail_compte_interet')  #aide_list
    else:
        form = TransactionretraitcpteintForm()
    return render(request, 'Pages/Compteentreprise/transaction_cptekha_form.html', {'form': form})

# modifier ----------------------------------------------------------------------------------------------------------------
def modifier_transaction_cpteint(request, transaction_id):
    transaction = get_object_or_404(TransactionInteret, id=transaction_id)
    cpte = transaction.compteinteret
    ancien_montant = transaction.montant

    if request.method == 'POST':
        form = TransactionretraitcpteintForm(request.POST, instance=transaction)
        if form.is_valid():
            if request.user.is_authenticated and isinstance(request.user, Agent):
                agent = request.user

            form.instance.agent = request.user

            # Récupération des anciens et nouveaux montants
            
            nouveau_montant = form.cleaned_data['montant']

            print(f"Ancien montant: {ancien_montant}, Nouveau montant: {nouveau_montant}")

            # Mise à jour des champs du compte
            cpte.soldeprecedent = cpte.solde
            cpte.dateprecedent = cpte.datesolde
            cpte.datesolde = timezone.now()

            # Réajuster le solde
            cpte.solde += ancien_montant
            cpte.solde -= nouveau_montant

            # Sauvegarde du compte après réajustement
            cpte.save()
            print(f"Solde mis à jour: {cpte.solde}")

            # Sauvegarde de la transaction modifiée
            form.save()

            return redirect('detail_compte_interet')
        else:
            print(form.errors)
    else:
        form = TransactionretraitcpteintForm(instance=transaction)

    return render(request, 'Pages/Compteentreprise/transaction_cptekha_form.html', {'form': form})
#____________________________________________________________________________________________________________________________________________________________________


# AFFICHER DETAIL UN COMPTE KHA _________________________________________________________________________________________________________________________________
def detail_compte_kha (request):
    statut_actif = get_object_or_404(Statuts, statut='Actif')
    compte_pret = get_object_or_404(CompteKha, statut=statut_actif)
    echeanciers = TransactionKha.objects.filter(comptekha=compte_pret).order_by('-date_transaction')

    context = {
        'compte_pret': compte_pret,
        'echeanciers': echeanciers,
    }
    return render(request, 'Pages/Compteentreprise/detail_compte_kha.html', context)

# Create ----------------------------------------------------------------------------------------------------------------
def transaction_cptekha(request, id):
    cpte = get_object_or_404(CompteKha, id=id)
    if request.method == 'POST':
        form = TransactionretraitcptekhaForm(request.POST)
        if form.is_valid():
            if request.user.is_authenticated and isinstance(request.user, Agent):
                agent = request.user

            form.instance.agent = request.user  # Assurez-vous que cela pointe vers l'utilisateur connecté           
            form.instance.comptekha = cpte
            form.instance.type_transaction = 'Retrait'  # À adapter en fonction de votre logique

            # Compter le nombre d'aides dont a bénéficié le client
            epar = get_object_or_404(CompteKha, id=id)
            epar.soldeprecedent = epar.solde
            epar.dateprecedent = epar.datesolde
            epar.datesolde = timezone.now()
            epar.solde -= form.cleaned_data['montant']
                
            epar.save()

            form.save()
            return redirect('detail_compte_kha')  #aide_list
    else:
        form = TransactionretraitcptekhaForm()
    return render(request, 'Pages/Compteentreprise/transaction_cptekha_form.html', {'form': form})

# modifier ----------------------------------------------------------------------------------------------------------------
def modifier_transaction_cptekha(request, transaction_id):
    transaction = get_object_or_404(TransactionKha, id=transaction_id)
    cpte = transaction.comptekha
    ancien_montant = transaction.montant

    if request.method == 'POST':
        form = TransactionretraitcptekhaForm(request.POST, instance=transaction)
        if form.is_valid():
            if request.user.is_authenticated and isinstance(request.user, Agent):
                agent = request.user

            form.instance.agent = request.user

            # Récupération des anciens et nouveaux montants
            
            nouveau_montant = form.cleaned_data['montant']

            print(f"Ancien montant: {ancien_montant}, Nouveau montant: {nouveau_montant}")

            # Mise à jour des champs du compte
            cpte.soldeprecedent = cpte.solde
            cpte.dateprecedent = cpte.datesolde
            cpte.datesolde = timezone.now()

            # Réajuster le solde
            cpte.solde += ancien_montant
            cpte.solde -= nouveau_montant

            # Sauvegarde du compte après réajustement
            cpte.save()
            print(f"Solde mis à jour: {cpte.solde}")

            # Sauvegarde de la transaction modifiée
            form.save()

            return redirect('detail_compte_kha')
        else:
            print(form.errors)
    else:
        form = TransactionretraitcptekhaForm(instance=transaction)

    return render(request, 'Pages/Compteentreprise/transaction_cptekha_form.html', {'form': form})
#____________________________________________________________________________________________________________________________________________________________________

# AFFICHER DETAIL UN COMPTE ADHESION _________________________________________________________________________________________________________________________________
def detail_compte_adhesion (request):
    statut_actif = get_object_or_404(Statuts, statut='Actif')
    compte_pret = get_object_or_404(CompteAdhesionkhas, statut=statut_actif)
    echeanciers = TransactionAdhesionkha.objects.filter(compteAdhessionkha=compte_pret).order_by('-date_transaction')

    context = {
        'compte_pret': compte_pret,
        'echeanciers': echeanciers,
    }
    return render(request, 'Pages/Compteentreprise/detail_compte_adhesion.html', context)

# Create ----------------------------------------------------------------------------------------------------------------
def transaction_cpteadhesion(request, id):
    cpte = get_object_or_404(CompteAdhesionkhas, id=id)
    if request.method == 'POST':
        form = TransactionretraitcpteadhForm(request.POST)
        if form.is_valid():
            if request.user.is_authenticated and isinstance(request.user, Agent):
                agent = request.user

            form.instance.agent = request.user  # Assurez-vous que cela pointe vers l'utilisateur connecté           
            form.instance.compteAdhessionkha = cpte
            form.instance.type_transaction = 'Retrait'  # À adapter en fonction de votre logique

            # Compter le nombre d'aides dont a bénéficié le client
            epar = get_object_or_404(CompteAdhesionkhas, id=id)
            epar.soldeprecedent = epar.solde
            epar.dateprecedent = epar.datesolde
            epar.datesolde = timezone.now()
            epar.solde -= form.cleaned_data['montant']
                
            epar.save()

            form.save()
            return redirect('detail_compte_adhesion')  #aide_list
    else:
        form = TransactionretraitcpteadhForm()
    return render(request, 'Pages/Compteentreprise/transaction_cptekha_form.html', {'form': form})

# modifier ----------------------------------------------------------------------------------------------------------------
def modifier_transaction_cpteadhesion(request, transaction_id):
    transaction = get_object_or_404(TransactionAdhesionkha, id=transaction_id)
    cpte = transaction.compteAdhessionkha
    ancien_montant = transaction.montant

    if request.method == 'POST':
        form = TransactionretraitcpteadhForm(request.POST, instance=transaction)
        if form.is_valid():
            if request.user.is_authenticated and isinstance(request.user, Agent):
                agent = request.user

            form.instance.agent = request.user

            # Récupération des anciens et nouveaux montants
            
            nouveau_montant = form.cleaned_data['montant']

            print(f"Ancien montant: {ancien_montant}, Nouveau montant: {nouveau_montant}")

            # Mise à jour des champs du compte
            cpte.soldeprecedent = cpte.solde
            cpte.dateprecedent = cpte.datesolde
            cpte.datesolde = timezone.now()

            # Réajuster le solde
            cpte.solde += ancien_montant
            cpte.solde -= nouveau_montant

            # Sauvegarde du compte après réajustement
            cpte.save()
            print(f"Solde mis à jour: {cpte.solde}")

            # Sauvegarde de la transaction modifiée
            form.save()

            return redirect('detail_compte_adhesion')
        else:
            print(form.errors)
    else:
        form = TransactionretraitcpteadhForm(instance=transaction)

    return render(request, 'Pages/Compteentreprise/transaction_cptekha_form.html', {'form': form})
#____________________________________________________________________________________________________________________________________________________________________

# AFFICHER DETAIL UN COMPTE FONDATEUR _________________________________________________________________________________________________________________________________
def detail_compte_fond (request):
    statut_actif = get_object_or_404(Statuts, statut='Actif')
    compte_pret = get_object_or_404(CompteFondateur, statut=statut_actif)
    echeanciers = TransactionFondateur.objects.filter(comptefond=compte_pret).order_by('-date_transaction')

    context = {
        'compte_pret': compte_pret,
        'echeanciers': echeanciers,
    }
    return render(request, 'Pages/Compteentreprise/detail_compte_fond.html', context)

# Create ----------------------------------------------------------------------------------------------------------------
def transaction_cptefond(request, id):
    cpte = get_object_or_404(CompteFondateur, id=id)
    if request.method == 'POST':
        form = TransactionretraitcptefondForm(request.POST)
        if form.is_valid():
            if request.user.is_authenticated and isinstance(request.user, Agent):
                agent = request.user

            form.instance.agent = request.user  # Assurez-vous que cela pointe vers l'utilisateur connecté           
            form.instance.comptefond = cpte
            form.instance.type_transaction = 'Retrait'  # À adapter en fonction de votre logique

            # Compter le nombre d'aides dont a bénéficié le client
            epar = get_object_or_404(CompteFondateur, id=id)
            epar.soldeprecedent = epar.solde
            epar.dateprecedent = epar.datesolde
            epar.datesolde = timezone.now()
            epar.solde -= form.cleaned_data['montant']
                
            epar.save()

            form.save()
            return redirect('detail_compte_fond')  #aide_list
    else:
        form = TransactionretraitcptefondForm()
    return render(request, 'Pages/Compteentreprise/transaction_cptekha_form.html', {'form': form})

# modifier ----------------------------------------------------------------------------------------------------------------
def modifier_transaction_cptefond(request, transaction_id):
    transaction = get_object_or_404(TransactionFondateur, id=transaction_id)
    cpte = transaction.comptekha
    ancien_montant = transaction.montant

    if request.method == 'POST':
        form = TransactionretraitcptefondForm(request.POST, instance=transaction)
        if form.is_valid():
            if request.user.is_authenticated and isinstance(request.user, Agent):
                agent = request.user

            form.instance.agent = request.user

            # Récupération des anciens et nouveaux montants
            
            nouveau_montant = form.cleaned_data['montant']

            print(f"Ancien montant: {ancien_montant}, Nouveau montant: {nouveau_montant}")

            # Mise à jour des champs du compte
            cpte.soldeprecedent = cpte.solde
            cpte.dateprecedent = cpte.datesolde
            cpte.datesolde = timezone.now()

            # Réajuster le solde
            cpte.solde += ancien_montant
            cpte.solde -= nouveau_montant

            # Sauvegarde du compte après réajustement
            cpte.save()
            print(f"Solde mis à jour: {cpte.solde}")

            # Sauvegarde de la transaction modifiée
            form.save()

            return redirect('detail_compte_fond')
        else:
            print(form.errors)
    else:
        form = TransactionretraitcptefondForm(instance=transaction)

    return render(request, 'Pages/Compteentreprise/transaction_cptekha_form.html', {'form': form})
#____________________________________________________________________________________________________________________________________________________________________

# AFFICHER DETAIL UN COMPTE ADHESION _________________________________________________________________________________________________________________________________
def detail_compte_penalite (request):
    statut_actif = get_object_or_404(Statuts, statut='Actif')
    compte_pret = get_object_or_404(ComptePenalites, statut=statut_actif)
    echeanciers = TransactionPenaliteHist.objects.filter(comptepenalite=compte_pret).order_by('-date_transaction')

    context = {
        'compte_pret': compte_pret,
        'echeanciers': echeanciers,
    }
    return render(request, 'Pages/Compteentreprise/detail_compte_penalite.html', context)

# Create ----------------------------------------------------------------------------------------------------------------
def transaction_cptepenalite(request, id):
    cpte = get_object_or_404(ComptePenalites, id=id)
    if request.method == 'POST':
        form = TransactionretraitcptepenForm(request.POST)
        if form.is_valid():
            if request.user.is_authenticated and isinstance(request.user, Agent):
                agent = request.user
       
            form.instance.comptepenalite = cpte
            form.instance.type_transaction = 'Retrait'  # À adapter en fonction de votre logique

            # Compter le nombre d'aides dont a bénéficié le client
            epar = get_object_or_404(ComptePenalites, id=id)
            epar.soldeprecedent = epar.solde
            epar.dateprecedent = epar.datesolde
            epar.datesolde = timezone.now()
            epar.solde -= form.cleaned_data['montant']
                
            epar.save()


           

            form.save()
            return redirect('detail_compte_penalite')  #aide_list
    else:
        form = TransactionretraitcptepenForm()
    return render(request, 'Pages/Compteentreprise/transaction_cptekha_form.html', {'form': form})

# modifier ----------------------------------------------------------------------------------------------------------------
def modifier_transaction_cptepenalite(request, transaction_id):
    transaction = get_object_or_404(TransactionPenaliteHist, id=transaction_id)
    cpte = transaction.comptepenalite
    ancien_montant = transaction.montant

    if request.method == 'POST':
        form = TransactionretraitcptepenForm(request.POST, instance=transaction)
        if form.is_valid():
            if request.user.is_authenticated and isinstance(request.user, Agent):
                agent = request.user

            form.instance.agent = request.user

            # Récupération des anciens et nouveaux montants
            
            nouveau_montant = form.cleaned_data['montant']

            print(f"Ancien montant: {ancien_montant}, Nouveau montant: {nouveau_montant}")

            # Mise à jour des champs du compte
            cpte.soldeprecedent = cpte.solde
            cpte.dateprecedent = cpte.datesolde
            cpte.datesolde = timezone.now()

            # Réajuster le solde
            cpte.solde += ancien_montant
            cpte.solde -= nouveau_montant

            # Sauvegarde du compte après réajustement
            cpte.save()
            print(f"Solde mis à jour: {cpte.solde}")

            # Sauvegarde de la transaction modifiée
            form.save()

            return redirect('detail_compte_penalite')
        else:
            print(form.errors)
    else:
        form = TransactionretraitcptepenForm(instance=transaction)

    return render(request, 'Pages/Compteentreprise/transaction_cptekha_form.html', {'form': form})
#____________________________________________________________________________________________________________________________________________________________________

# AFFICHER DETAIL UN COMPTE KHA _________________________________________________________________________________________________________________________________
def detail_compte_principal (request):
    statut_actif = get_object_or_404(Statuts, statut='Actif')
    compte_pret = get_object_or_404(ComptePrincipale, statut=statut_actif)

    context = {
        'compte_pret': compte_pret
    }
    return render(request, 'Pages/Compteentreprise/detail_compte_principal.html', context)
#____________________________________________________________________________________________________________________________________________________________________

# AFFICHER DETAIL UN COMPTE COMMISSION _________________________________________________________________________________________________________________________________
def detail_compte_portefeuille (request):
    statut_actif = get_object_or_404(Statuts, statut='Actif')
    compte_pret = get_object_or_404(ComptePortefeuilles, statut=statut_actif)

    context = {
        'compte_pret': compte_pret
    }
    return render(request, 'Pages/Compteentreprise/detail_compte_portefeuille.html', context)
#____________________________________________________________________________________________________________________________________________________________________

# AFFICHER DETAIL UN COMPTE COMMERCIAL _________________________________________________________________________________________________________________________________
from itertools import chain

def detail_compte_commercial(request, id):
    statut_actif = get_object_or_404(Statuts, statut='Actif')
    com = get_object_or_404(Agent, id=id)
    compte_pret = get_object_or_404(Commissions, statut=statut_actif, agent=com.user)

    # Récupérer les deux listes d'échéanciers
    echeanciers_pret = TransactionCommissionpret.objects.filter(commission=compte_pret).order_by('-date_transaction')
    echeanciers_pretact = TransactionCommissionpretact.objects.filter(commissionact=compte_pret).order_by('-date_transaction')
    retrait = TransactionRetraitcommercial.objects.filter(com=compte_pret).order_by('-date_transaction')

    # Combiner les deux listes en une seule
    echeanciers_combined = list(chain(echeanciers_pret, echeanciers_pretact,retrait))

    context = {
        'compte_pret': compte_pret,
        'echeanciers': echeanciers_combined,  # Une seule liste combinée
    }

    return render(request, 'Pages/Agent/detail_commission.html', context)


# Create ----------------------------------------------------------------------------------------------------------------
from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
from .forms import TransactionretraitcomForm
from .models import Commissions, TransactionRetraitcommercial

def transaction_cptecommercial(request, id):
    cpte = get_object_or_404(Commissions, id=id)  # Récupérer le compte de commission

    if request.method == 'POST':
        form = TransactionretraitcomForm(request.POST)
        if form.is_valid():
            # Vérification du solde suffisant
            form.instance.montant = form.cleaned_data['montant']
            montant = form.cleaned_data['montant']
                # Initialisation des champs du formulaire
            form.instance.com = cpte
            form.instance.type_transaction = 'Retrait'  # Type de transaction fixé à 'Retrait'
            form.instance.Motif = form.cleaned_data['Motif']

                # Mise à jour des soldes
            cpte.soldeprecedent = cpte.solde  # Enregistrer le solde précédent
            cpte.datesolde = timezone.now()  # Mettre à jour la date du solde
            cpte.solde -= montant  # Déduire le montant du solde actuel

                # Sauvegarder les changements dans la base de données
            cpte.save()
            form.save()

            
            cuser = get_object_or_404(Utilisateurs, id=cpte.agent.id)
            com = get_object_or_404(Agent, user=cuser.id)

            return redirect('detail_compte_commercial', id=com.id) 
    else:
        form = TransactionretraitcomForm()

    return render(request, 'Pages/Retraits/transaction_cptekha_form.html', {'form': form})



# modifier ----------------------------------------------------------------------------------------------------------------
def modifier_transaction_cptecommercial (request, transaction_id):
    transaction = get_object_or_404(TransactionRetraitcommercial, id=transaction_id)
    cpte = transaction.com
    ancien_montant = transaction.montant

    if request.method == 'POST':
        form = TransactionretraitcomForm(request.POST, instance=transaction)
        if form.is_valid():
            if request.user.is_authenticated and isinstance(request.user, Agent):
                agent = request.user

            form.instance.agent = request.user
            form.instance.date_transaction = timezone.now() 

            # Récupération des anciens et nouveaux montants
            
            nouveau_montant = form.cleaned_data['montant']

            print(f"Ancien montant: {ancien_montant}, Nouveau montant: {nouveau_montant}")

            # Mise à jour des champs du compte
            cpte.soldeprecedent = cpte.solde
            cpte.datesolde = timezone.now()

            # Réajuster le solde
            cpte.solde += ancien_montant
            cpte.solde -= nouveau_montant

            # Sauvegarde du compte après réajustement
            cpte.save()
            print(f"Solde mis à jour: {cpte.solde}")

            # Sauvegarde de la transaction modifiée
            form.save()

            cuser = get_object_or_404(Utilisateurs, id=cpte.agent.id)
            com = get_object_or_404(Agent, user=cuser.id)

            return redirect('detail_compte_commercial', id=com.id) 
        else:
            print(form.errors)
    else:
        form = TransactionretraitcomForm(instance=transaction)

    return render(request, 'Pages/Retraits/transaction_cptekha_form.html', {'form': form})
# ______________________________________________________________________________________________________________________________________________________

# AFFICHER DETAIL UN COMPTE DEMARCHEUR _________________________________________________________________________________________________________________________________
from itertools import chain

def detail_compte_demarcheur(request, id):
    statut_actif = get_object_or_404(Statuts, statut='Actif')
    com = get_object_or_404(Agent, id=id)
    compte_pret = get_object_or_404(Commissions, statut=statut_actif, agent=com.user)

    # Récupérer les deux listes d'échéanciers
    #echeanciers_pret = TransactionCommissionpret.objects.filter(commission=compte_pret)
    #echeanciers_pretact = TransactionCommissionpretact.objects.filter(commissionact=compte_pret)
    retrait = TransactionRetraitdemarcheur.objects.filter(dem=compte_pret).order_by('-date_transaction')

    # Combiner les deux listes en une seule
    #echeanciers_combined = list(chain(echeanciers_pret, echeanciers_pretact,retrait))
    echeanciers_combined = list(retrait)
    context = {
        'compte_pret': compte_pret,
        'echeanciers': echeanciers_combined,  # Une seule liste combinée
    }

    return render(request, 'Pages/Agent/detail_demarcheur.html', context)


# Create ----------------------------------------------------------------------------------------------------------------

def transaction_cptedemarcheur(request, id):
    cpte = get_object_or_404(Commissions, id=id)  # Récupérer le compte de commission

    if request.method == 'POST':
        form = TransactionretraitdemForm(request.POST)
        if form.is_valid():
            # Vérification du solde suffisant
            form.instance.montant = form.cleaned_data['montant']
            montant = form.cleaned_data['montant']
                # Initialisation des champs du formulaire
            form.instance.dem = cpte
            form.instance.type_transaction = 'Retrait'  # Type de transaction fixé à 'Retrait'
            form.instance.Motif = form.cleaned_data['Motif']

                # Mise à jour des soldes
            cpte.soldeprecedent = cpte.solde  # Enregistrer le solde précédent
            cpte.datesolde = timezone.now()  # Mettre à jour la date du solde
            cpte.solde -= montant  # Déduire le montant du solde actuel

                # Sauvegarder les changements dans la base de données
            cpte.save()
            form.save()

            
            cuser = get_object_or_404(Utilisateurs, id=cpte.agent.id)
            com = get_object_or_404(Agent, user=cuser.id)

            return redirect('detail_compte_demarcheur', id=com.id) 
    else:
        form = TransactionretraitdemForm()

    return render(request, 'Pages/Retraits/transaction_cptekha_form.html', {'form': form})



# modifier ----------------------------------------------------------------------------------------------------------------
def modifier_transaction_cptedemarcheur (request, transaction_id):
    transaction = get_object_or_404(TransactionRetraitdemarcheur, id=transaction_id)
    cpte = transaction.dem
    ancien_montant = transaction.montant

    if request.method == 'POST':
        form = TransactionretraitdemForm(request.POST, instance=transaction)
        if form.is_valid():
            if request.user.is_authenticated and isinstance(request.user, Agent):
                agent = request.user

            form.instance.agent = request.user
            form.instance.date_transaction = timezone.now() 

            # Récupération des anciens et nouveaux montants
            
            nouveau_montant = form.cleaned_data['montant']

            print(f"Ancien montant: {ancien_montant}, Nouveau montant: {nouveau_montant}")

            # Mise à jour des champs du compte
            cpte.soldeprecedent = cpte.solde
            cpte.datesolde = timezone.now()

            # Réajuster le solde
            cpte.solde += ancien_montant
            cpte.solde -= nouveau_montant

            # Sauvegarde du compte après réajustement
            cpte.save()
            print(f"Solde mis à jour: {cpte.solde}")

            # Sauvegarde de la transaction modifiée
            form.save()

            cuser = get_object_or_404(Utilisateurs, id=cpte.agent.id)
            com = get_object_or_404(Agent, user=cuser.id)

            return redirect('detail_compte_demarcheur', id=com.id) 
        else:
            print(form.errors)
    else:
        form = TransactionretraitdemForm(instance=transaction)

    return render(request, 'Pages/Retraits/transaction_cptekha_form.html', {'form': form})
# ______________________________________________________________________________________________________________________________________________________


# AFFICHER DETAIL UN COMPTE SPONSOR _________________________________________________________________________________________________________________________________
def detail_compte_sponsor (request,id):
    statut_actif = get_object_or_404(Statuts, statut='Actif')
    compte_pret = get_object_or_404(Sponsors,  id=id)
    echeanciers = TransactionRetraitsponsor.objects.filter(gain=compte_pret).order_by('-date_transaction')

    context = {
        'compte_pret': compte_pret,
        'echeanciers': echeanciers,
    }
    return render(request, 'Pages/Sponsors/detail_gain.html', context)

# Create ----------------------------------------------------------------------------------------------------------------
def transaction_cptesponsor(request, id):
    cpte = get_object_or_404(Sponsors, id=id)
    if request.method == 'POST':
        form = TransactionretraitspoForm(request.POST)
        if form.is_valid():
            if request.user.is_authenticated and isinstance(request.user, Agent):
                agent = request.user
       
            form.instance.gain = cpte
            form.instance.type_transaction = 'Retrait'  # À adapter en fonction de votre logique

            # Compter le nombre d'aides dont a bénéficié le client
            epar = get_object_or_404(Sponsors, id=id)
            epar.dividende -= form.cleaned_data['montant']
                
            epar.save()

            form.save()
            # Redirection avec l'ID du sponsor
            return redirect('detail_compte_sponsor', id=cpte.id) 
    else:
        form = TransactionretraitspoForm()
    return render(request, 'Pages/Retraits/transaction_cptekha_form.html', {'form': form})

# modifier ----------------------------------------------------------------------------------------------------------------
def modifier_transaction_cptesponsor(request, transaction_id):
    transaction = get_object_or_404(TransactionRetraitsponsor, id=transaction_id)
    cpte = transaction.gain
    ancien_montant = transaction.montant

    if request.method == 'POST':
        form = TransactionretraitspoForm(request.POST, instance=transaction)
        if form.is_valid():
            if request.user.is_authenticated and isinstance(request.user, Agent):
                agent = request.user

            form.instance.agent = request.user
            form.instance.date_transaction = timezone.now() 

            # Récupération des anciens et nouveaux montants
            
            nouveau_montant = form.cleaned_data['montant']

            print(f"Ancien montant: {ancien_montant}, Nouveau montant: {nouveau_montant}")

            # Mise à jour des champs du compte

            # Réajuster le solde
            cpte.dividende += ancien_montant
            cpte.dividende -= nouveau_montant

            # Sauvegarde du compte après réajustement
            cpte.save()
            print(f"Solde mis à jour: {cpte.dividende}")

            # Sauvegarde de la transaction modifiée
            form.save()

            return redirect('detail_compte_sponsor', id=cpte.id) 
        else:
            print(form.errors)
    else:
        form = TransactionretraitspoForm(instance=transaction)

    return render(request, 'Pages/Retraits/transaction_cptekha_form.html', {'form': form})
#____________________________________________________________________________________________________________________________________________________________________

# AFFICHER DETAIL UN COMPTE COOPERATEUR _________________________________________________________________________________________________________________________________
from itertools import chain

def detail_compte_cooperateur(request, id):
    compte_pret = get_object_or_404(Actionnaire, id=id)

    # Récupérer les deux listes d'échéanciers
    retrait = TransactionRistourne.objects.filter(actionnaire=compte_pret).order_by('-date_transaction')

    # Combiner les deux listes en une seule
    echeanciers_combined = list(chain(retrait))

    context = {
        'compte_pret': compte_pret,
        'echeanciers': echeanciers_combined,  # Une seule liste combinée
    }

    return render(request, 'Pages/Actionnaire/detail_compte_actionnaire.html', context)


# Create ----------------------------------------------------------------------------------------------------------------

def transaction_cpteactionnaire(request, id):
    cpte = get_object_or_404(Actionnaire, id=id)  # Récupérer le compte de commission

    if request.method == 'POST':
        form = TransactionretraitactForm(request.POST)
        if form.is_valid():
            # Vérification du solde suffisant
            form.instance.montant = form.cleaned_data['montant']
            form.instance.actionnaire = cpte
            montant = form.cleaned_data['montant']
                # Initialisation des champs du formulaire
            form.instance.com = cpte
            form.instance.type_transaction = 'Retrait'  # Type de transaction fixé à 'Retrait'

                # Mise à jour des soldes
            #cpte.apport -= montant  # Déduire le montant du solde actuel  
            cpte.dividende -= montant  # Déduire le montant du solde actuel

                # Sauvegarder les changements dans la base de données
            cpte.save()
            form.save()


            return redirect('detail_compte_cooperateur', id=id) 
    else:
        form = TransactionretraitactForm()

    return render(request, 'Pages/Actionnaire/transaction_cptekha_form.html', {'form': form})



# modifier ----------------------------------------------------------------------------------------------------------------
def modifier_transaction_cpteactionnaire (request, transaction_id):
    transaction = get_object_or_404(TransactionRistourne, id=transaction_id)
    cpte = transaction.actionnaire
    ancien_montant = transaction.montant

    if request.method == 'POST':
        form = TransactionretraitactForm(request.POST, instance=transaction)
        if form.is_valid():

            form.instance.date_transaction = timezone.now() 

            # Récupération des anciens et nouveaux montants
            
            nouveau_montant = form.cleaned_data['montant']

            print(f"Ancien montant: {ancien_montant}, Nouveau montant: {nouveau_montant}")

            # Mise à jour des champs du compte
            # Réajuster le solde
            cpte.dividende += ancien_montant
            cpte.dividende -= nouveau_montant

            # Sauvegarde du compte après réajustement
            cpte.save()
            print(f"Solde mis à jour: {cpte.dividende}")

            # Sauvegarde de la transaction modifiée
            form.save()
            return redirect('detail_compte_cooperateur', id=id) 
        else:
            print(form.errors)
    else:
        form = TransactionretraitactForm(instance=transaction)

    return render(request, 'Pages/Actionnaire/transaction_cptekha_form.html', {'form': form})
# ______________________________________________________________________________________________________________________________________________________

# CONFIGURATION _________________________________________________________________________________________________________________________________
from django.shortcuts import render, get_object_or_404, redirect
from .models import Confconstantes
from .forms import ConfconstantesForm

def liste_confconstantes(request):
    confconstantes = Confconstantes.objects.all()
    return render(request, 'Pages/Confconstantes/liste_confconstantes.html', {'confconstantes': confconstantes})


def modifier_confconstantes(request, id):
    confconstante = get_object_or_404(Confconstantes, id=id)
    
    if request.method == "POST":
        form = ConfconstantesForm(request.POST, instance=confconstante)
        if form.is_valid():
            form.save()
            return redirect('detail_confconstantes', id=confconstante.id)  # Redirection après la soumission
    else:
        form = ConfconstantesForm(instance=confconstante)
    
    return render(request, 'Pages/Confconstantes/modifier_confconstantes.html', {'form': form})

def detail_confconstantes(request, id):
    confconstante = get_object_or_404(Confconstantes, id=id)
    return render(request, 'Pages/Confconstantes/detail_confconstantes.html', {'confconstante': confconstante})



#API___ Juillet 2

# finance/views.py






















#API____________________________________________________________________________ MOBILE ________________________________________________________________________
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import json
from rest_framework import status # type: ignore
from rest_framework.response import Response # type: ignore
from rest_framework.views import APIView # type: ignore
from .models import Clients, CompteEpargnes, Statuts
from finances.serializers import ClientSerializer


from django.http import JsonResponse





@csrf_exempt
@require_POST
def votre_vue(request):
    # Traitez les données de la requête POST ici
    # Exemple : récupérer des données du corps de la requête
    data = json.loads(request.body)

    # Effectuez des opérations avec les données
    # ...

    # Renvoyez une réponse JSON
    response_data = {'message': 'Traitement réussi', 'result': 'quelque chose'}
    return JsonResponse(response_data)


def liste_clientsapi(request):
    # Assuming Clients is a Django model with fields like name, email, etc.
    clients = Clients.objects.all().values()  # Retrieve all clients as dictionaries

    # You might want to convert QuerySet to a list for JsonResponse
    clients_list = list(clients)

    return JsonResponse(clients_list, safe=False)


# ALERTE COMPTE PRETS
def liste_echeances_non_payeesapi(request):
    # Récupérer les échéances non payées dans le passé
    echeances_non_payees = Echeancier.objects.filter(date_echeance__lt=date.today(), est_paye=False).values('id',
        'compte_pret_id',
        'date_echeance',
        'montant_echeance',
        'montant_interet',
        'est_paye',
        'compte_pret__client__nom',        # Replace 'client' with the actual related field name
        'compte_pret__client__prenom',     # Replace 'client' with the actual related field name
        'compte_pret__client__sexe__sexe',       # Replace 'client' with the actual related field name
        'compte_pret__client__telephone',)
    echeances_non_payeesact = Echeancieract.objects.filter(date_echeance__lt=date.today(), est_paye=False).values()

    context =  list(echeances_non_payees),
    return JsonResponse(context, safe=False)

# AJOUT CLIENTS
class CreerClientAPI(APIView):
    def post(self, request, format=None):
        serializer = ClientSerializer(data=request.data)
        if serializer.is_valid():
            statut_actif = Statuts.objects.get(statut='Actif')
            serializer.validated_data['statut'] = statut_actif
            client = serializer.save()
            CompteEpargnes.objects.create(client=client, solde=0, numero_compte='EP' + str(client.id), statut=statut_actif)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#API___ Juin 2
# RECHERCHER CLIENT PAR TYPE __________________________________________________________________________________________________________________________________
from django.http import JsonResponse
from .models import Clients

def search_clients(request):
    query = request.GET.get('query', '')
    clients = Clients.objects.filter(nat_client='1',nom__icontains=query) | Clients.objects.filter(nat_client='1',prenom__icontains=query)
    clients_data = [
        {
            'id': client.id,
            'nom': client.nom,
            'prenom': client.prenom,
            'sexe': client.sexe.sexe,  # Assuming `libelle` is the field name in `Genres`
            'telephone': client.telephone,
            'ville': client.ville_village,
            'prof': client.profession,
            'photo': request.build_absolute_uri(client.photo.url) if client.photo else None,  # Get the absolute URL of the photo
        }
        for client in clients
    ]
    return JsonResponse(clients_data, safe=False)

# Client Aide -----------------------------------------------------------------------------------------------
def search_clientsai(request):
    query = request.GET.get('query', '')
    clients = Clients.objects.filter(nat_client='2',nom__icontains=query) | Clients.objects.filter(nat_client='2',prenom__icontains=query)
    clients_data = [
        {
            'id': client.id,
            'nom': client.nom,
            'prenom': client.prenom,
            'sexe': client.sexe.sexe,  # Assuming `libelle` is the field name in `Genres`
            'telephone': client.telephone,
            'ville': client.ville_village,
            'prof': client.profession,
            'photo': request.build_absolute_uri(client.photo.url) if client.photo else None,  # Get the absolute URL of the photo
        }
        for client in clients
    ]
    return JsonResponse(clients_data, safe=False)

# Client Sponsor -----------------------------------------------------------------------------------------------
def search_clientssp(request):
    query = request.GET.get('query', '')
    clients = Clients.objects.filter(nat_client='3',nom__icontains=query) | Clients.objects.filter(nat_client='3',prenom__icontains=query)
    clients_data = [
        {
            'id': client.id,
            'nom': client.nom,
            'prenom': client.prenom,
            'sexe': client.sexe.sexe,  # Assuming `libelle` is the field name in `Genres`
            'telephone': client.telephone,
            'ville': client.ville_village,
            'prof': client.profession,
            'photo': request.build_absolute_uri(client.photo.url) if client.photo else None,  # Get the absolute URL of the photo
        }
        for client in clients
    ]
    return JsonResponse(clients_data, safe=False)
#__________________________________________________________________________________________________________________________________________________________


# RECHERCHER ACTIONNAIRE PAR TYPE _________________________________________________________________________________________________________________________
# Actif
def search_actionnaire(request):
    query = request.GET.get('query', '')
    actionnaires = Actionnaire.objects.filter(type_act='1',nom__icontains=query) | Actionnaire.objects.filter(type_act='1',prenom__icontains=query)
    actionnaires_data = [
        {
            'id': actionnaire.id,
            'nom': actionnaire.nom,
            'prenom': actionnaire.prenom,
            'apport': actionnaire.apport,  # Assuming `libelle` is the field name in `Genres`
            'telephone': actionnaire.telephone,
            'part': actionnaire.pourcentage,
            'type': actionnaire.type_act.type_act,    # Get the absolute URL of the photo
        }
        for actionnaire in actionnaires
    ]
    return JsonResponse(actionnaires_data, safe=False)

# Passif
def search_actionnairepa(request):
    query = request.GET.get('query', '')
    actionnaires = Actionnaire.objects.filter(type_act='2',nom__icontains=query) | Actionnaire.objects.filter(type_act='2',prenom__icontains=query)
    actionnaires_data = [
        {
            'id': actionnaire.id,
            'nom': actionnaire.nom,
            'prenom': actionnaire.prenom,
            'apport': actionnaire.apport,  # Assuming `libelle` is the field name in `Genres`
            'telephone': actionnaire.telephone,
            'part': actionnaire.pourcentage,
            'type': actionnaire.type_act.type_act,    # Get the absolute URL of the photo
        }
        for actionnaire in actionnaires
    ]
    return JsonResponse(actionnaires_data, safe=False)

# Sponsor
def search_actionnairesp(request):
    query = request.GET.get('query', '')
    actionnaires = Sponsors.objects.filter(nom__icontains=query) | Sponsors.objects.filter(prenom__icontains=query)
    actionnaires_data = [
        {
            'id': actionnaire.id,
            'nom': actionnaire.nom,
            'prenom': actionnaire.prenom,
            'apport': actionnaire.apport,  # Assuming `libelle` is the field name in `Genres`
            'telephone': actionnaire.telephone,
            'part': actionnaire.pourcentage,
            'type': actionnaire.type_act.type_act,    # Get the absolute URL of the photo
        }
        for actionnaire in actionnaires
    ]
    return JsonResponse(actionnaires_data, safe=False)
#_______________________________________________________________________________________________________________________________________________________________
# Liste echeances
from datetime import timedelta
from django.utils.timezone import now
from django.http import JsonResponse
from .models import Echeancier, Echeancieract


def clients_proche_echeance_api(request):
    date_actuelle = now().date()
    date_une_semaine_plus_tard = date_actuelle + timedelta(days=3)

    clients_proche_echeance = Echeancier.objects.filter(
        date_echeance__gte=date_actuelle,
        date_echeance__lte=date_une_semaine_plus_tard,
        est_paye=False
    ).values(
        'compte_pret__client__nom',
        'compte_pret__client__prenom',
        'compte_pret__client__telephone',
        'compte_pret__numero_compte',
        'montant_echeance',
        'date_echeance',
        'id'
    )

    actionnaire_proche_echeance = Echeancieract.objects.filter(
        date_echeance__gte=date_actuelle,
        date_echeance__lte=date_une_semaine_plus_tard,
        est_paye=False
    ).values(
        'compte_pretact__actionnaire__nom',
        'compte_pretact__actionnaire__prenom',
        'compte_pretact__actionnaire__telephone',
        'compte_pretact__numero_compte',
        'montant_echeance',
        'date_echeance',
        'id'
    )

    resultats = list(clients_proche_echeance) + list(actionnaire_proche_echeance)

    return JsonResponse(resultats, safe=False)

def liste_echeances_non_payees_api(request):
    echeances_non_payees = Echeancier.objects.filter(
        est_paye=False,date_echeance__lt=timezone.now()
    ).values(
        'compte_pret__client__nom',
        'compte_pret__client__prenom',
        'compte_pret__client__telephone',
        'compte_pret__numero_compte',
        'montant_echeance',
        'date_echeance',
        'id'
    )

    actionnaire_non_payees = Echeancieract.objects.filter(
        est_paye=False,date_echeance__lt=timezone.now()
        
    ).values(
        'compte_pretact__actionnaire__nom',
        'compte_pretact__actionnaire__prenom',
        'compte_pretact__actionnaire__telephone',
        'compte_pretact__numero_compte',
        'montant_echeance',
        'date_echeance',
        'id'
    )

    resultats = list(echeances_non_payees) + list(actionnaire_non_payees)

    return JsonResponse(resultats, safe=False)


# CLIENT ApI coté_______________________________________________________________________________________________________________________________________________

def clients_proche_echeance_apiclient(request):
    date_actuelle = now().date()
    date_une_semaine_plus_tard = date_actuelle + timedelta(days=3)

    clients_proche_echeance = Echeancier.objects.filter(
        date_echeance__gte=date_actuelle,
        date_echeance__lte=date_une_semaine_plus_tard,
        est_paye=False
    ).values(
        'compte_pret__client__nom',
        'compte_pret__client__prenom',
        'compte_pret__client__telephone',
        'compte_pret__client__email',
        'compte_pret__numero_compte',
        'montant_echeance',
        'ancien_echeance',
        'montant_penalite',
        'date_echeance',
        'id'
    )


    resultats = list(clients_proche_echeance)

    return JsonResponse(resultats, safe=False)

# liste cote client
def liste_echeances_non_payees_apiclient(request):
    echeances_non_payees = Echeancier.objects.filter(
        est_paye=False,date_echeance__lt=timezone.now()
    ).values(
        'compte_pret__client__nom',
        'compte_pret__client__prenom',
        'compte_pret__client__telephone',
        'compte_pret__client__email',
        'compte_pret__numero_compte',
        'montant_echeance',
        'ancien_echeance',
        'montant_penalite',
        'date_echeance',
        'id'
    )

    resultats = list(echeances_non_payees)

    return JsonResponse(resultats, safe=False)
# liste ok
def clients_proche_echeanced(request):
    echeances_proche = Echeancier.objects.all().values(
        'compte_pret__client__nom',
        'compte_pret__client__prenom',
        'compte_pret__client__telephone',
        'compte_pret__numero_compte',
        'montant_echeance',
        'ancien_echeance',
        'montant_penalite',
        'date_echeance',
        'id'
    )

    actionnaires_proche = Echeancieract.objects.all().values(
        'compte_pretact__actionnaire__nom',
        'compte_pretact__actionnaire__prenom',
        'compte_pretact__actionnaire__telephone',
        'compte_pretact__numero_compte',
        'montant_echeance',
        'ancien_echeance',
        'montant_penalite',
        'date_echeance',
        'id'
    )

    resultats = list(echeances_proche) + list(actionnaires_proche)
    return JsonResponse(resultats, safe=False)

# Liste des compte

def liste_comptes_json(request):
    # Récupération des comptes épargne avec email du client
    comptes_epargne = CompteEpargnes.objects.all().values('numero_compte', 'solde', 'statut', 'client__email')

    # Récupération des comptes prêt avec email du client
    comptes_pret = ComptePrets.objects.all().values('numero_compte', 'solde', 'statut', 'client__email')

    # Vous pouvez maintenant passer ces trois listes à votre réponse JSON
    data = {
        'comptes_epargne': list(comptes_epargne),
        'comptes_pret': list(comptes_pret),
         #'comptes_pret_act': list(comptes_pret_act),
    }

    return JsonResponse(data, safe=False)


# Liste des transactions aides
from django.http import JsonResponse
from .models import Tontines, Aides, TransactionTontine

def client_trans_aide(request):
    # Récupérer toutes les tontines avec les champs nécessaires
    tontine_aide = list(Tontines.objects.all().values(
        'client__id',
        #'client__nom',  # Nom du client
        'client__email',  # Email du client
        'numero_tontine',
        'date_tontine',
        'solde',
        'cotite',
        'agent__id',  # ID de l'agent
        'agent__first_name',  # Nom de l'agent
        'statut__id',  # ID du statut
        #'statut__nom',  # Nom du statut
        'nbreaide',
        'dateaide',
        'montant_aide',
        'id'
    ))

    # Récupérer toutes les aides avec les champs nécessaires
    aide_aide = list(Aides.objects.all().values(
        'client__id',
        'client__nom',  # Nom du client
        'client__prenom',  # Nom du client
        'client__email',  # Email du client
        'date_aide',
        'montant_aide',
        'statut__id',  # ID du statut
        #'statut__nom',  # Nom du statut
        'id'
    ))

    # Récupérer toutes les transactions de tontine avec les champs nécessaires
    trans_aide = list(TransactionTontine.objects.all().values(
        'type_transaction',
        'date_transaction',
        'montant',
        'agent__id',  # ID de l'agent
        'agent__first_name',  # Nom de l'agent
        'tontine__id',  # ID de la tontine
        'tontine__numero_tontine',  # Numéro de la tontine
        'tontine__client__email',  # Email du client associé à la tontine
        'tontine__client__nom',
        'tontine__client__prenom',
        #'tontine__client__nom',  # Nom du client associé à la tontine
        'id'
    ))

    # Combiner les résultats
    resultats = {
        'tontines': tontine_aide,
        'aides': aide_aide,
        'transactions': trans_aide
    }

    # Retourner les résultats en format JSON
    return JsonResponse(resultats, safe=False)

# liste des echeances client 
from django.core.serializers.json import DjangoJSONEncoder 
class CustomJSONEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, date):
            return obj.strftime('%Y-%m-%d')
        return super().default(obj) 
    
def clients_echeance_api(request):
    date_actuelle = now().date()
    date_une_semaine_plus_tard = date_actuelle + timedelta(days=3)

    clients_proche_echeance = Echeancier.objects.filter(
        date_echeance__gte=date_actuelle,
        date_echeance__lte=date_une_semaine_plus_tard,
        est_paye=False
    ).values(
        'compte_pret__client__nom',
        'compte_pret__client__prenom',
        'compte_pret__client__telephone',
        'compte_pret__client__email',
        'compte_pret__client__photo',
        'compte_pret__numero_compte',
        'montant_echeance',
        'ancien_echeance',
        'montant_penalite',
        'date_echeance',
        'id'
    )
    echeances_non_payees = Echeancier.objects.filter(
        est_paye=False,date_echeance__lt=timezone.now()
    ).values(
        'compte_pret__client__nom',
        'compte_pret__client__prenom',
        'compte_pret__client__telephone',
        'compte_pret__client__email',
        'compte_pret__client__photo',
        'compte_pret__numero_compte',
        'montant_echeance',
        'ancien_echeance',
        'montant_penalite',
        'date_echeance',
        'id'
    )
    # Convertir les dates en format YYYY-MM-DD
    clients_proche_echeance = list(clients_proche_echeance)
    for item in clients_proche_echeance:
        if 'date_echeance' in item:
            item['date_echeance'] = item['date_echeance'].strftime('%Y-%m-%d')

    echeances_non_payees = list(echeances_non_payees)
    for item in echeances_non_payees:
        if 'date_echeance' in item:
            item['date_echeance'] = item['date_echeance'].strftime('%Y-%m-%d')

    resultats = list(clients_proche_echeance) + list(echeances_non_payees)

    return JsonResponse(resultats, safe=False, encoder=CustomJSONEncoder)

# liste des transactions pret -------------------------------------------
from django.http import JsonResponse
from django.db.models import Sum

def client_trans_pret(request):
    # Récupérer le statut 'Actif'
    statut_actif = Statuts.objects.get(statut='Actif')
    
    # Récupérer tous les comptes de prêt avec le statut 'Actif'
    comptes_pret = list(ComptePrets.objects.filter(statut=statut_actif).values(
        'numero_compte', 'solde', 'statut__statut', 'client__email'))

    # Initialiser une liste pour stocker les informations des prêts avec les échéances
    pret_pret = []

    # Parcourir chaque compte de prêt actif
    for compte in ComptePrets.objects.filter(statut=statut_actif):
        # Récupérer toutes les échéances non payées pour ce compte
        echeances_non_payees = Echeancier.objects.filter(compte_pret=compte, est_paye=False)
        # Récupérer toutes les échéances payées pour ce compte
        echeances_payees = Echeancier.objects.filter(compte_pret=compte, est_paye=True)

        # Calculer le montant total des échéances restantes à payer
        montant_total_echeances_restantes = echeances_non_payees.aggregate(total=Sum('montant_echeance'))['total'] or 0

        # Calculer le montant total déjà payé
        montant_total_payee = echeances_payees.aggregate(total=Sum('montant_echeance'))['total'] or 0

        # Ajouter les informations du compte et des échéances dans la liste
        pret_pret.append({
            'numero_compte': compte.numero_compte,
            'somme_initiale': compte.somme_initiale,
            'email_client': compte.client.email,
            'date_demande': compte.date_demande,
            'solde': compte.solde,
            'statut': compte.statut.statut,
            'duree_en_mois': compte.duree_en_mois,
            'montant_total_echeances_restantes': montant_total_echeances_restantes,
            'montant_total_payee': montant_total_payee,
        })

    # Récupérer toutes les transactions de prêt avec les champs nécessaires
    trans_pret = list(TransactionPret.objects.all().values(
        'type_transaction',
        'date_transaction',
        'montant',
        'agent__id',  # ID de l'agent
        'agent__first_name',  # Nom de l'agent
        'compte_pret__id',  # ID du compte prêt
        'compte_pret__client__email',  # Email du client associé au prêt
        'id'
    )[:5])

    # Combiner les résultats
    resultats = {
        'comptepret': comptes_pret,
        'prets': pret_pret,
        'transactions': trans_pret
    }

    # Retourner les résultats en format JSON
    return JsonResponse(resultats, safe=False)


def client_trans_pret1(request):
    # Récupérer toutes les tontines avec les champs nécessaires
    statut_actif = Statuts.objects.get(statut='Actif')
    comptes_pret = list(ComptePrets.objects.filter(statut=statut_actif).values('numero_compte', 'solde', 'statut', 'client__email'))

    # Récupérer toutes les aides avec les champs nécessaires
    pret_pret = list(ComptePrets.objects.all().values(
        'numero_compte',
        'somme_initiale',  # Nom du client
        'client__email',  # Email du client
        'date_demande',
        'solde',
        'statut',  # ID du statut
        'duree_en_mois',  # Nom du statut
        'id'
    ))

    # Récupérer toutes les transactions de tontine avec les champs nécessaires
    trans_pret = list(TransactionPret.objects.all().values(
        'type_transaction',
        'date_transaction',
        'montant',
        'agent__id',  # ID de l'agent
        'agent__first_name',  # Nom de l'agent
        'compte_pret__id',  # ID de la tontine
        'compte_pret__client__email',  # Email du client associé à la tontine
        #'tontine__client__nom',  # Nom du client associé à la tontine
        'id'
    ))

    # Combiner les résultats
    resultats = {
        'comptepret': comptes_pret,
        'prets': pret_pret,
        'transactions': trans_pret
    }

    # Retourner les résultats en format JSON
    return JsonResponse(resultats, safe=False)

# liste des credits epargne -------------------------------------------
from django.http import JsonResponse
from django.db.models import Sum

def client_trans_credit(request):
    # Récupérer le statut 'Actif'
    statut_actif = Statuts.objects.get(statut='Actif')
    
    # Récupérer tous les comptes de prêt avec le statut 'Actif'
    comptes_pret = list(ComptePrets.objects.filter(statut=statut_actif).values(
        'numero_compte', 'solde', 'statut__statut', 'client__email'))

    # Initialiser une liste pour stocker les informations des prêts avec les échéances
    pret_pret = []

    # Parcourir chaque compte de prêt actif
    for compte in ComptePrets.objects.all():
    #for compte in ComptePrets.objects.filter(statut=statut_actif):
        # Récupérer toutes les échéances non payées pour ce compte
        echeances_non_payees = Echeancier.objects.filter(compte_pret=compte, est_paye=False)
        # Récupérer toutes les échéances payées pour ce compte
        echeances_payees = Echeancier.objects.filter(compte_pret=compte, est_paye=True)

        # Calculer le montant total des échéances restantes à payer
        montant_total_echeances_restantes = echeances_non_payees.aggregate(total=Sum('montant_echeance'))['total'] or 0

        # Calculer le montant total déjà payé
        montant_total_payee = echeances_payees.aggregate(total=Sum('montant_echeance'))['total'] or 0

        # Ajouter les informations du compte et des échéances dans la liste
        pret_pret.append({
            'numero_compte': compte.numero_compte,
            'somme_initiale': compte.somme_initiale,
            'email_client': compte.client.email,
            'date_demande': compte.date_demande,
            'solde': compte.solde,
            'statut': compte.statut.statut,
            'duree_en_mois': compte.duree_en_mois,
            'montant_total_echeances_restantes': montant_total_echeances_restantes,
            'montant_total_payee': montant_total_payee,
        })

    
    # Combiner les résultats
    resultats = { 
        'prets': pret_pret,
    }

    # Retourner les résultats en format JSON
    return JsonResponse(resultats, safe=False)

# liste des transactions epargne -------------------------------------------
def decimal_to_float(obj):
    """Convertit un objet Decimal en float pour la sérialisation JSON."""
    if isinstance(obj, Decimal):
        return float(obj)
    raise TypeError(f'Type {obj.__class__.__name__} not serializable')

    
def client_trans_epargne(request):
    # Récupérer toutes les tontines avec les champs nécessaires
    statut_actif = Statuts.objects.get(statut='Actif')
    comptes_epargne = list(CompteEpargnes.objects.filter(statut=statut_actif).values('numero_compte', 'solde', 'statut', 'client__email'))

    # Récupérer toutes les aides avec les champs nécessaires
    epargne_epargne = list(CompteEpargnes.objects.all().values(
        'numero_compte',
        'client__email',  # Email du client
        'solde',
        'statut',  # ID du statut
        'id'
    ))

    # Récupérer toutes les transactions de tontine avec les champs nécessaires
    current_date = timezone.now()
    current_month = current_date.month
    current_year = current_date.year

    start_date = timezone.make_aware(datetime(current_year, current_month, 1))
    end_date = timezone.make_aware(datetime(current_year, current_month + 1, 1))
    trans_epargne = list(TransactionEpargne.objects.filter(
        date_transaction__gte=start_date,
        date_transaction__lt=end_date
    ).order_by('-date_transaction').values(
        'type_transaction',
        'date_transaction',
        'montant',
        'agent__id',  # ID de l'agent
        'agent__first_name',  # Nom de l'agent
        'compte_epargne__id',  # ID de la tontine
        'compte_epargne__client__email',  # Email du client associé à la tontine
        'id'
    ))

    # Récupérer toutes les transactions de tontine avec les champs nécessaires
    trans_pret = list(TransactionPret.objects.filter(
        date_transaction__gte=start_date,
        date_transaction__lt=end_date
    ).order_by('-date_transaction').values(
        'type_transaction',
        'date_transaction',
        'montant',
        'agent__id',  # ID de l'agent
        'agent__first_name',  # Nom de l'agent
        'compte_pret__id',  # ID de la tontine
        'compte_pret__client__email',  # Email du client associé à la tontine
        #'tontine__client__nom',  # Nom du client associé à la tontine
        'id'
    ))

    # Combiner les résultats des transactions
    transactions_combined = list(chain(trans_pret, trans_epargne))

    # Convertir les dates en chaînes
    for transaction in transactions_combined:
        transaction['date_transaction'] = transaction['date_transaction'].strftime('%Y-%m-%d %H:%M:%S')

    # Vérifier s'il y a des transactions
    if transactions_combined:
        print("Transactions récupérées :")
        print(json.dumps(transactions_combined, indent=4, ensure_ascii=False, default=decimal_to_float))
    else:
        print("Aucune transaction pour le mois en cours.")   
    # Combiner les résultats
    resultats = {
        'compteepargne': comptes_epargne,
        'epargne': epargne_epargne,
        'transactions': trans_epargne,
        'echeanciers': transactions_combined
    }

    # Retourner les résultats en format JSON
    return JsonResponse(resultats, safe=False)

# ACTIONNAIRE API ______________________________________________________________________________________________________________________________________________

def clients_proche_echeance_apiact(request):
    date_actuelle = now().date()
    date_une_semaine_plus_tard = date_actuelle + timedelta(days=3)

    actionnaire_proche_echeance = Echeancieract.objects.filter(
        date_echeance__gte=date_actuelle,
        date_echeance__lte=date_une_semaine_plus_tard,
        est_paye=False
    ).values(
        'compte_pretact__actionnaire__nom',
        'compte_pretact__actionnaire__prenom',
        'compte_pretact__actionnaire__telephone',
        'compte_pretact__actionnaire__email',
        'compte_pretact__numero_compte',
        'montant_echeance',
        'date_echeance',
        'id'
    )

    resultats = list(actionnaire_proche_echeance)

    return JsonResponse(resultats, safe=False)

# ACTIONS COOPERATEURS SUR LE MOBILE______________________________________________________________________________________________________________________________________
# AFFICHER LE TABLEAU DE BORD POUR LE COOPERATEURS SUR MOBILE------------------------------------------------------------------------------------------------------------------------------------------
from django.http import JsonResponse
from django.utils import timezone
from datetime import datetime, timedelta
from django.db.models import Sum
from django.utils.timezone import make_aware
from .models import Clients, Echeancier, TransactionEpargne, TransactionPret

def courbe_transactionsapi(request):
    # Déterminer la date actuelle
    date_aujourdhui = timezone.now().date()

    # Décomptes du nombre de clients de chaque genre
    male_countens = Clients.objects.filter(sexe='1').count()
    female_countens = Clients.objects.filter(sexe='2').count()

    # Échéances
    date_today = timezone.now().date()
    date_un_mois_avant = date_today - timedelta(days=30)
    echeances = Echeancier.objects.filter(date_echeance__gte=date_un_mois_avant, date_echeance__lte=date_today)
    total_echeances = echeances.count()
    echeances_payees = echeances.filter(est_paye=True).count()
    echeances_non_payees = total_echeances - echeances_payees

    # Transactions par type
    depot_count = TransactionEpargne.objects.filter(type_transaction='Depot').count()
    retrait_count = TransactionEpargne.objects.filter(type_transaction='Retrait').count()
    virement_count = TransactionEpargne.objects.filter(type_transaction='Virement').count()

    # Montants des transactions par type
    depot_amount = TransactionEpargne.objects.filter(type_transaction='Depot').aggregate(total=Sum('montant'))['total'] or 0
    retrait_amount = TransactionEpargne.objects.filter(type_transaction='Retrait').aggregate(total=Sum('montant'))['total'] or 0
    virement_amount = TransactionEpargne.objects.filter(type_transaction='Virement').aggregate(total=Sum('montant'))['total'] or 0

    # Transactions d'épargne pour l'intervalle d'un mois
    aujourd_hui = make_aware(datetime.today())
    mois_precedent = aujourd_hui - timedelta(days=30)
    transactions = TransactionEpargne.objects.filter(date_transaction__gte=mois_precedent)
    transactions_data = {}
    for transaction in transactions:
        date = transaction.date_transaction.strftime('%Y-%m-%d')
        if date not in transactions_data:
            transactions_data[date] = {'Depot': 0, 'Retrait': 0, 'Virement': 0}
        transactions_data[date][transaction.type_transaction] += float(transaction.montant or 0)

    # Transactions de prêt pour l'intervalle d'un mois
    transactions_pret = TransactionPret.objects.filter(date_transaction__gte=mois_precedent)
    transactions_pret_data = {}
    for transaction in transactions_pret:
        date = transaction.date_transaction.strftime('%Y-%m-%d')
        if date not in transactions_pret_data:
            transactions_pret_data[date] = {'Depot': 0, 'Retrait': 0, 'Virement': 0}
        transactions_pret_data[date][transaction.type_transaction] += float(transaction.montant or 0)

    # Préparer les données à retourner
    data = {
    'male_countens': male_countens,
    'female_countens': female_countens,
    'echeances_payees': echeances_payees,
    'echeances_non_payees': echeances_non_payees,
    'depot_amount': depot_amount if depot_amount is not None else 0.0,
    'retrait_amount': retrait_amount if retrait_amount is not None else 0.0,
    'virement_amount': virement_amount if virement_amount is not None else 0.0,
    'depot_count': depot_count,
    'retrait_count': retrait_count,
    'virement_count': virement_count,
    'transactions_data': transactions_data,
    'transactions_pret_data': transactions_pret_data,
}


    return JsonResponse(data, safe=False)
#__________________________________________________________________________________________________________________________________________________________


# AFFICHAGE DES ECHEANCES ENCOURS ET EN RETARD DU COOPERATEUR SUR LE MOBILE ________________________________________________________________________________
# liste des echeances actionnaire  
def actionnaire_echeance_api(request):
    date_actuelle = now().date()
    date_une_semaine_plus_tard = date_actuelle + timedelta(days=3)

    clients_proche_echeance = Echeancieract.objects.filter(
        date_echeance__gte=date_actuelle,
        date_echeance__lte=date_une_semaine_plus_tard,
        est_paye=False
    ).values(
        'compte_pretact__actionnaire__nom',
        'compte_pretact__actionnaire__prenom',
        'compte_pretact__actionnaire__telephone',
        'compte_pretact__actionnaire__email',
        'compte_pretact__numero_compte',
        'montant_echeance',
        'date_echeance',
        'id'
    )
    echeances_non_payees = Echeancieract.objects.filter(
        est_paye=False,date_echeance__lt=timezone.now()
    ).values(
        'compte_pretact__actionnaire__nom',
        'compte_pretact__actionnaire__prenom',
        'compte_pretact__actionnaire__telephone',
        'compte_pretact__actionnaire__email',
        'compte_pretact__numero_compte',
        'montant_echeance',
        'date_echeance',
        'id'
    )

    resultats = list(clients_proche_echeance) + list(echeances_non_payees)

    return JsonResponse(resultats, safe=False)
#_________________________________________________________________________________________________________________________________________________________


# AFFICHAGE DES DIVIDENDES SUR LE MOBILE _______________________________________________________________________________________________________________
# Récupérer les dividende
def actionnaire_dividendebon(request):

    # Déterminer la date actuelle
    date_aujourdhui = timezone.now().date()

    # Décomptes du nombre de clients de chaque genre
    male_countens = Clients.objects.filter(sexe='1').count()
    female_countens = Clients.objects.filter(sexe='2').count()

    # Échéances
    date_todayy = timezone.now().date()
    date_un_mois_avant = date_todayy - timedelta(days=30)
    echeances = Echeancier.objects.filter(date_echeance__gte=date_un_mois_avant, date_echeance__lte=date_todayy)
    total_echeances = echeances.count()
    echeances_payees = echeances.filter(est_paye=True).count()
    echeances_non_payees = total_echeances - echeances_payees

    # Transactions par type
    depot_count = TransactionEpargne.objects.filter(type_transaction='Depot').count()
    retrait_count = TransactionEpargne.objects.filter(type_transaction='Retrait').count()
    virement_count = TransactionEpargne.objects.filter(type_transaction='Virement').count()

    # Montants des transactions par type
    depot_amount = TransactionEpargne.objects.filter(type_transaction='Depot').aggregate(total=Sum('montant'))['total'] or 0
    retrait_amount = TransactionEpargne.objects.filter(type_transaction='Retrait').aggregate(total=Sum('montant'))['total'] or 0
    virement_amount = TransactionEpargne.objects.filter(type_transaction='Virement').aggregate(total=Sum('montant'))['total'] or 0

    # Transactions d'épargne pour l'intervalle d'un mois
    aujourd_hui = make_aware(datetime.today())
    mois_precedent = aujourd_hui - timedelta(days=30)
    transactions = TransactionEpargne.objects.filter(date_transaction__gte=mois_precedent)
    transactions_data = {}
    for transaction in transactions:
        date = transaction.date_transaction.strftime('%Y-%m-%d')
        if date not in transactions_data:
            transactions_data[date] = {'Depot': 0, 'Retrait': 0, 'Virement': 0}
        transactions_data[date][transaction.type_transaction] += float(transaction.montant or 0)

    # Transactions de prêt pour l'intervalle d'un mois
    transactions_pret = TransactionPret.objects.filter(date_transaction__gte=mois_precedent)
    transactions_pret_data = {}
    for transaction in transactions_pret:
        date = transaction.date_transaction.strftime('%Y-%m-%d')
        if date not in transactions_pret_data:
            transactions_pret_data[date] = {'Depot': 0, 'Retrait': 0, 'Virement': 0}
        transactions_pret_data[date][transaction.type_transaction] += float(transaction.montant or 0)

    # Préparer les données à retourner
    data = {
    'male_countens': male_countens,
    'female_countens': female_countens,
    'echeances_payees': echeances_payees,
    'echeances_non_payees': echeances_non_payees,
    'depot_amount': depot_amount if depot_amount is not None else 0.0,
    'retrait_amount': retrait_amount if retrait_amount is not None else 0.0,
    'virement_amount': virement_amount if virement_amount is not None else 0.0,
    'depot_count': depot_count,
    'retrait_count': retrait_count,
    'virement_count': virement_count,
    'transactions_data': transactions_data,
    'transactions_pret_data': transactions_pret_data,
    }


# montant a repatir
    # Récupérer les actionnaires et leurs informations
    # Récupérer
    statut_actif = get_object_or_404(Statuts, statut='Actif')
    Conf = Confconstantes.objects.filter(statut=statut_actif).first()
    dureecoopa = Conf.dureecoopa
    dureecoopn = Conf.dureecoopn
    date_today = datetime.now().date()
    date_un_mois_actif = date_today - timedelta(days=dureecoopa)
    date_un_mois_passif = date_today - timedelta(days=dureecoopn)

    # Récupérer les actionnaires et leurs informations
    actionnaires_type_1 = Actionnaire.objects.filter(type_act_id=1, date_adhesion__gte=date_un_mois_actif)
    actionnaires_type_2 = Actionnaire.objects.filter(type_act_id=2, date_adhesion__gte=date_un_mois_passif)

    # Récupérer le montant à répartir entre les actionnaires
    echeances_payees_mois = Echeancier.objects.filter(date_echeance__month=date.today().month, est_paye=True)
    echeances_payees_moisact = Echeancieract.objects.filter(date_echeance__month=date.today().month, est_paye=True)
    benefice_mois = sum(echeance.montant_interet for echeance in echeances_payees_mois) + sum(echeance.montant_interet for echeance in echeances_payees_moisact)
    #depenses_mois = Depense.objects.filter(date__month=date.today().month).aggregate(Sum('montant'))['montant__sum'] or 0
    


    today = timezone.localtime(timezone.now()).date()
    depenses_mois = Depense.objects.filter(date__month=date.today().month)
    print(depenses_mois)  # Cela vous montrera quelles entrées sont prises en compte.
    total_montant = depenses_mois.aggregate(Sum('montant'))['montant__sum'] or 0
    print(total_montant)
    print(benefice_mois)

    today = timezone.localtime(timezone.now()).date()
    depenses_mois = Depense.objects.filter(date__month=today.month, date__year=today.year).aggregate(Sum('montant'))['montant__sum'] or 0
    montant_a_repartir = benefice_mois - depenses_mois

    # Répartir les montants selon le type d'actionnaire
    # Répartir les montants selon le type d'actionnaire
    statut_actif = get_object_or_404(Statuts, statut='Actif')
    Conf = Confconstantes.objects.filter(statut=statut_actif).first()
    #montant_a_repartir_type_1 = montant_a_repartir * Decimal('2.0') / Decimal('3.0')
    #montant_a_repartir_type_2 = montant_a_repartir * Decimal('1.0') / Decimal('3.0')
    montant_a_repartir_type_1 = montant_a_repartir * Decimal(Conf.partactif)
    montant_a_repartir_type_chef = montant_a_repartir * Decimal(Conf.partnonactif)* Decimal(Conf.partrespo)
    #montant_a_repartir_type_2 = montant_a_repartir * Decimal(Conf.partnonactif)
    montant_a_repartir_type_2 = (montant_a_repartir * Decimal(Conf.partnonactif)) - montant_a_repartir_type_chef


    # Récupérer toutes les tontines avec les champs nécessaires
    compteactionnaire = list(Actionnaire.objects.all().values(
        'apport',
        'pourcentage',  # Email du client
        'dividende',
        'email',
        'date_adhesion',
        'id',
        'type_act'
    ))

    # Récupérer toutes les transactions de tontine avec les champs nécessaires
    trans_ris = list(TransactionRistourne.objects.all().values(
        'type_transaction',
        'date_transaction',
        'actionnaire',
        #'agent__id',  # ID de l'agent
        #'agent__first_name',  # Nom de l'agent
        'actionnaire__id',  # ID de la tontine
        'actionnaire__email',  # Email du client associé à la tontine
        'actionnaire__nom',
        'actionnaire__prenom',
        'id'
    ))

    # Combiner les résultats
    resultats = {
        'tontines': compteactionnaire,
        'transactions': trans_ris,
        'depenses_mois' : depenses_mois,
        'benefice_mois' : benefice_mois,
        'montant_a_repartir' : montant_a_repartir,
        'montant_a_repartir_type_1' : montant_a_repartir_type_1,
        'montant_a_repartir_type_2' : montant_a_repartir_type_2,
        'montant_a_repartir_type_chef' : montant_a_repartir_type_chef,



        'male_countens': male_countens,
        'female_countens': female_countens,
        'echeances_payees': echeances_payees,
        'echeances_non_payees': echeances_non_payees,
        'depot_amount': depot_amount if depot_amount is not None else 0.0,
        'retrait_amount': retrait_amount if retrait_amount is not None else 0.0,
        'virement_amount': virement_amount if virement_amount is not None else 0.0,
        'depot_count': depot_count,
        'retrait_count': retrait_count,
        'virement_count': virement_count,
        'transactions_data': transactions_data,
        'transactions_pret_data': transactions_pret_data,
    }

    # Retourner les résultats en format JSON
    return JsonResponse(resultats, safe=False)



from datetime import datetime, timedelta
from django.utils.timezone import make_aware
from django.db.models import Sum
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Actionnaire, TransactionEpargne, TransactionPret, Echeancier, Echeancieract, Clients, Depense, Statuts, Confconstantes, TransactionRistourne

def actionnaire_dividende(request):
    # Déterminer la date actuelle
    date_aujourdhui = timezone.now().date()

    # Décomptes du nombre de clients de chaque genre
    male_countens = Clients.objects.filter(sexe='1').count()
    female_countens = Clients.objects.filter(sexe='2').count()

    # Échéances
    date_todayy = timezone.now().date()
    date_un_mois_avant = date_todayy - timedelta(days=30)
    echeances = Echeancier.objects.filter(date_echeance__gte=date_un_mois_avant, date_echeance__lte=date_todayy)
    total_echeances = echeances.count()
    echeances_payees = echeances.filter(est_paye=True).count()
    echeances_non_payees = total_echeances - echeances_payees

    # Transactions par type
    depot_count = TransactionEpargne.objects.filter(type_transaction='Depot').count()
    retrait_count = TransactionEpargne.objects.filter(type_transaction='Retrait').count()
    virement_count = TransactionEpargne.objects.filter(type_transaction='Virement').count()

    # Montants des transactions par type
    depot_amount = TransactionEpargne.objects.filter(type_transaction='Depot').aggregate(total=Sum('montant'))['total'] or 0
    retrait_amount = TransactionEpargne.objects.filter(type_transaction='Retrait').aggregate(total=Sum('montant'))['total'] or 0
    virement_amount = TransactionEpargne.objects.filter(type_transaction='Virement').aggregate(total=Sum('montant'))['total'] or 0

    # Transactions d'épargne pour l'intervalle d'un mois
    aujourd_hui = make_aware(datetime.today())
    mois_precedent = aujourd_hui - timedelta(days=30)
    transactions = TransactionEpargne.objects.filter(date_transaction__gte=mois_precedent)
    transactions_data = {}
    for transaction in transactions:
        date = transaction.date_transaction.strftime('%Y-%m-%d')
        if date not in transactions_data:
            transactions_data[date] = {'Depot': 0, 'Retrait': 0, 'Virement': 0}
        transactions_data[date][transaction.type_transaction] += float(transaction.montant or 0)

    # Transactions de prêt pour l'intervalle d'un mois
    transactions_pret = TransactionPret.objects.filter(date_transaction__gte=mois_precedent)
    transactions_pret_data = {}
    for transaction in transactions_pret:
        date = transaction.date_transaction.strftime('%Y-%m-%d')
        if date not in transactions_pret_data:
            transactions_pret_data[date] = {'Depot': 0, 'Retrait': 0, 'Virement': 0}
        transactions_pret_data[date][transaction.type_transaction] += float(transaction.montant or 0)

    # Préparer les données à retourner
    data = {
        'male_countens': male_countens,
        'female_countens': female_countens,
        'echeances_payees': echeances_payees,
        'echeances_non_payees': echeances_non_payees,
        'depot_amount': depot_amount if depot_amount is not None else 0.0,
        'retrait_amount': retrait_amount if retrait_amount is not None else 0.0,
        'virement_amount': virement_amount if virement_amount is not None else 0.0,
        'depot_count': depot_count,
        'retrait_count': retrait_count,
        'virement_count': virement_count,
        'transactions_data': transactions_data,
        'transactions_pret_data': transactions_pret_data,
    }
    print(data)
    # Montant à répartir entre les actionnaires
    statut_actif = get_object_or_404(Statuts, statut='Actif')
    Conf = Confconstantes.objects.filter(statut=statut_actif).first()
    dureecoopa = Conf.dureecoopa
    dureecoopn = Conf.dureecoopn
    date_today = datetime.now().date()
    date_un_mois_actif = date_today - timedelta(days=dureecoopa)
    date_un_mois_passif = date_today - timedelta(days=dureecoopn)

    # Récupérer les actionnaires et leurs informations
    actionnaires_type_1 = Actionnaire.objects.filter(type_act_id=1, date_adhesion__gte=date_un_mois_actif)
    actionnaires_type_2 = Actionnaire.objects.filter(type_act_id=2, date_adhesion__gte=date_un_mois_passif)

    # Récupérer le montant à répartir
    echeances_payees_mois = Echeancier.objects.filter(date_echeance__month=datetime.now().month, est_paye=True)
    echeances_payees_moisact = Echeancieract.objects.filter(date_echeance__month=datetime.now().month, est_paye=True)
    benefice_mois = sum(echeance.montant_interet for echeance in echeances_payees_mois) + sum(echeance.montant_interet for echeance in echeances_payees_moisact)

    today = timezone.localtime(timezone.now()).date()
    depenses_mois = Depense.objects.filter(date__month=today.month).aggregate(Sum('montant'))['montant__sum'] or 0
    montant_a_repartir = benefice_mois - depenses_mois

    # Répartir les montants selon le type d'actionnaire
    montant_a_repartir_type_1 = montant_a_repartir * Decimal(Conf.partactif)
    montant_a_repartir_type_chef = montant_a_repartir * Decimal(Conf.partnonactif) * Decimal(Conf.partrespo)
    montant_a_repartir_type_2 = montant_a_repartir * Decimal(Conf.partnonactif) - montant_a_repartir_type_chef

    # Combiner les résultats
    resultats = {
        'tontines': list(Actionnaire.objects.all().values('apport', 'pourcentage', 'dividende', 'email', 'date_adhesion', 'id', 'type_act')),
        'transactions': list(TransactionRistourne.objects.all().values('type_transaction', 'date_transaction', 'actionnaire__email', 'actionnaire__nom', 'actionnaire__prenom', 'id')),
        'depenses_mois': depenses_mois,
        'benefice_mois': benefice_mois,
        'montant_a_repartir': montant_a_repartir,
        'montant_a_repartir_type_1': montant_a_repartir_type_1,
        'montant_a_repartir_type_2': montant_a_repartir_type_2,
        'montant_a_repartir_type_chef': montant_a_repartir_type_chef,
        'male_countens': male_countens,
        'female_countens': female_countens,
        'echeances_payees': echeances_payees,
        'echeances_non_payees': echeances_non_payees,
        'depot_amount': depot_amount if depot_amount is not None else 0.0,
        'retrait_amount': retrait_amount if retrait_amount is not None else 0.0,
        'virement_amount': virement_amount if virement_amount is not None else 0.0,
        'depot_count': depot_count,
        'retrait_count': retrait_count,
        'virement_count': virement_count,
        }
    print(resultats)

    # Retourner les résultats en format JSON
    return JsonResponse(resultats, safe=False)

#______________________________________________________________________________________________________________________________________________________


#AFFICHAGE DES INFORMATIONS DES PRETS SUR LE MOBILE____________________________________________________________________________________________________
# liste des transactions pret -----------------------------------------------------------------------------------------------------------------------------
from django.http import JsonResponse
from django.db.models import Sum

def actionnaire_trans_pret(request):
    # Récupérer le statut 'Actif'
    statut_actif = Statuts.objects.get(statut='Actif')
    
    # Récupérer tous les comptes de prêt avec le statut 'Actif'
    comptes_pret = list(ComptePretsact.objects.filter(statut=statut_actif).values(
        'numero_compte', 'solde', 'statut__statut', 'actionnaire__email'))

    # Initialiser une liste pour stocker les informations des prêts avec les échéances
    pret_pret = []

    # Parcourir chaque compte de prêt actif
    for compte in ComptePretsact.objects.filter(statut=statut_actif):
        # Récupérer toutes les échéances non payées pour ce compte
        echeances_non_payees = Echeancieract.objects.filter(compte_pretact=compte, est_paye=False)
        # Récupérer toutes les échéances payées pour ce compte
        echeances_payees = Echeancieract.objects.filter(compte_pretact=compte, est_paye=True)

        # Calculer le montant total des échéances restantes à payer
        montant_total_echeances_restantes = echeances_non_payees.aggregate(total=Sum('montant_echeance'))['total'] or 0

        # Calculer le montant total déjà payé
        montant_total_payee = echeances_payees.aggregate(total=Sum('montant_echeance'))['total'] or 0

        # Ajouter les informations du compte et des échéances dans la liste
        pret_pret.append({
            'numero_compte': compte.numero_compte,
            'somme_initiale': compte.somme_initiale,
            'email_client': compte.actionnaire.email,
            'date_demande': compte.date_demande,
            'solde': compte.solde,
            'statut': compte.statut.statut,
            'duree_en_mois': compte.duree_en_mois,
            'montant_total_echeances_restantes': montant_total_echeances_restantes,
            'montant_total_payee': montant_total_payee,
        })

    # Récupérer toutes les transactions de prêt avec les champs nécessaires
    trans_pret = list(TransactionPretact.objects.all().values(
        'type_transaction',
        'date_transaction',
        'montant',
        'agent__id',  # ID de l'agent
        'agent__first_name',  # Nom de l'agent
        'compte_pret__id',  # ID de la tontine
        'compte_pret__actionnaire__email',  # Email du client associé à la tontine
        #'tontine__client__nom',  # Nom du client associé à la tontine
        'id'
    ))

    # Combiner les résultats
    resultats = {
        'comptepret': comptes_pret,
        'prets': pret_pret,
        'transactions': trans_pret
    }

    # Retourner les résultats en format JSON
    return JsonResponse(resultats, safe=False)

def actionnaire_trans_pret1(request):
    # Récupérer toutes les tontines avec les champs nécessaires
    statut_actif = Statuts.objects.get(statut='Actif')
    comptes_pret = list(ComptePretsact.objects.filter(statut=statut_actif).values('numero_compte', 'solde', 'statut', 'actionnaire__email'))

    # Récupérer toutes les aides avec les champs nécessaires
    pret_pret = list(ComptePretsact.objects.all().values(
        'numero_compte',
        'somme_initiale',  # Nom du client
        'actionnaire__email',  # Email du client
        'date_demande',
        'solde',
        'statut',  # ID du statut
        'duree_en_mois',  # Nom du statut
        'id'
    ))

    # Récupérer toutes les transactions de tontine avec les champs nécessaires
    trans_pret = list(TransactionPretact.objects.all().values(
        'type_transaction',
        'date_transaction',
        'montant',
        'agent__id',  # ID de l'agent
        'agent__first_name',  # Nom de l'agent
        'compte_pret__id',  # ID de la tontine
        'compte_pret__actionnaire__email',  # Email du client associé à la tontine
        #'tontine__client__nom',  # Nom du client associé à la tontine
        'id'
    ))

    # Combiner les résultats
    resultats = {
        'comptepret': comptes_pret,
        'prets': pret_pret,
        'transactions': trans_pret
    }

    # Retourner les résultats en format JSON
    return JsonResponse(resultats, safe=False)

# liste des transactions epargne -------------------------------------------
def actionnaire_trans_epargne(request):
    # Récupérer toutes les tontines avec les champs nécessaires
    statut_actif = Statuts.objects.get(statut='Actif')
    comptes_epargne = list(CompteEpargnesact.objects.filter(statut=statut_actif).values('numero_compte', 'solde', 'statut', 'actionnaire__email'))

    # Récupérer toutes les aides avec les champs nécessaires
    epargne_epargne = list(CompteEpargnesact.objects.all().values(
        'numero_compte',
        'actionnaire__email',  # Email du client
        'solde',
        'statut',  # ID du statut
        'id'
    ))

    # Récupérer toutes les transactions de tontine avec les champs nécessaires
    trans_epargne = list(TransactionEpargneact.objects.all().values(
        'type_transaction',
        'date_transaction',
        'montant',
        'agent__id',  # ID de l'agent
        'agent__first_name',  # Nom de l'agent
        'compte_epargne__id',  # ID de la tontine
        'compte_epargne__actionnaire__email',  # Email du client associé à la tontine
        #'tontine__client__nom',  # Nom du client associé à la tontine
        'id'
    ))

    # Récupérer toutes les transactions de tontine avec les champs nécessaires
    trans_cpte = list(TransactionRistourne.objects.all().values(
        'type_transaction',
        'date_transaction',
        'montant',
        'actionnaire__email',  # ID de l'agent
        'actionnaire__dividende',
        'id'
    ))

    # Combiner les résultats
    resultats = {
        'compteepargne': comptes_epargne,
        'epargne': epargne_epargne,
        'transactions': trans_epargne,
        'trans_cpte' : trans_cpte
    }

    # Retourner les résultats en format JSON
    return JsonResponse(resultats, safe=False)


# liste ok
def clients_proche_echeancea(request):
    echeances_proche = Echeancier.objects.all().values(
        'compte_pret__client__nom',
        'compte_pret__client__prenom',
        'compte_pret__client__telephone',
        'compte_pret__numero_compte',
        'montant_echeance',
        'date_echeance',
        'id'
    )

    actionnaires_proche = Echeancieract.objects.all().values(
        'compte_pretact__actionnaire__nom',
        'compte_pretact__actionnaire__prenom',
        'compte_pretact__actionnaire__telephone',
        'compte_pretact__numero_compte',
        'montant_echeance',
        'date_echeance',
        'id'
    )

    resultats = list(echeances_proche) + list(actionnaires_proche)
    return JsonResponse(resultats, safe=False)
#________________________________________________________________________________________________________________________________________________________________


# SPONSOR API COTE ________________________________________________________________________________________________________________________________________
# Récupérer les dividende
def sponsor_dividende(request):
    # Récupérer toutes les tontines avec les champs nécessaires
    compteactionnaire = list(Sponsors.objects.all().values(
        'apport',
        'pourcentage',  # Email du client
        'dividende',
        'email',
        'date_adhesion',
        'id'
    ))

    # Récupérer toutes les transactions de tontine avec les champs nécessaires
    trans_ris = list(Contratsponsor.objects.all().values(
        'numero_contrat',
        'somme_initiale',
        'duree_contrat',
        'date_demande',  # ID de l'agent
        #'agent__first_name',  # Nom de l'agent
        'date_fin_contrat',  # ID de la tontine
        'sponsor__email',  # Email du client associé à la tontine
        'soldecontrat',
        'id'
    ))[:5]

    trans_rist = list(Contratsponsor.objects.all().values(
    'numero_contrat',
    'somme_initiale',
    'duree_contrat',
    'statut__statut',
    'date_fin_contrat',
    'date_demande',
    'sponsor__email',
    'soldecontrat',
    'id'    
    ).order_by('-date_demande'))  # Trier par 'date_fin_contrat' en ordre décroissant


    # Combiner les résultats
    resultats = {
        'tontines': compteactionnaire,
        'transactions': trans_ris,
        'transactionst': trans_rist
    }

    # Retourner les résultats en format JSON
    return JsonResponse(resultats, safe=False)
# _________________________________________________________________________________________________________________________________________________________

# COMMERCIAL API coté____________________________________________________________________________________________________________________________________
# Liste des trans paiement
from django.http import JsonResponse
from django.utils import timezone
from datetime import timedelta, datetime
from .models import Statuts, Commissions, TransactionCommissionpret, TransactionCommissioninves, Clients, TransactionRetraitcommercial, TransactionCommissionpretact
from django.db.models import Prefetch
from itertools import chain
import json
from decimal import Decimal

def decimal_to_float(obj):
    """Convertit un objet Decimal en float pour la sérialisation JSON."""
    if isinstance(obj, Decimal):
        return float(obj)
    raise TypeError(f'Type {obj.__class__.__name__} not serializable')

    


def commercial_trans_pret(request):
    # Récupérer le statut 'Actif'
    statut_actif = Statuts.objects.get(statut='Actif')
    
    # Récupérer toutes les commissions actives
    com = list(Commissions.objects.filter(statut=statut_actif).values(
        'solde', 'datesolde', 'soldeprecedent', 'date_aide', 'agent__email', 'agent__first_name'
    ))

    # Déterminer l'intervalle de la semaine passée
    now = timezone.now()
    one_week_ago = now - timedelta(days=7)

    # Récupérer les transactions de commission prêt et investissement de la semaine passée
    trans_pret = list(TransactionCommissionpret.objects.filter(date_transaction__range=(one_week_ago, now)).values(
        'type_transaction',
        'date_transaction',
        'montant',
        'agent__id',
        'agent__first_name',
        'commission__id',
        'commission__agent__email',
        'id'
    )[:5])

    trans_inv = list(TransactionCommissioninves.objects.filter(date_transaction__range=(one_week_ago, now)).values(
        'type_transaction',
        'date_transaction',
        'montant',
        'agent__id',
        'agent__first_name',
        'commissioninv__id',
        'commissioninv__agent__email',
        'id'
    ))

    # Filtrer les clients ayant un ComptePrets avec un statut 'Actif'
    clients = Clients.objects.prefetch_related(
        Prefetch(
            'compteprets_set',
            queryset=ComptePrets.objects.select_related('com').filter(statut=statut_actif),
            to_attr='active_compteprets'
        )
    )

    clients_data = []
    client_ids = set()  # Ensemble pour stocker les IDs des clients déjà ajoutés

    for client in clients:
        for compte_pret in client.active_compteprets:
            if client.id not in client_ids:  # Vérifier si le client a déjà été ajouté
                clients_data.append({
                    'nom': client.nom,
                    'prenom': client.prenom,
                    'sexe': client.sexe.sexe if client.sexe else 'Non défini',
                    'telephone': client.telephone,
                    'numero_compte': compte_pret.numero_compte,
                    'solde': compte_pret.solde,
                    'agent_nom': compte_pret.com.nom if compte_pret.com else 'Non défini',
                    'agent_email': compte_pret.com.email if compte_pret.com else 'Non défini',
                })
                client_ids.add(client.id)  # Ajouter l'ID du client à l'ensemble pour éviter les doublons


    current_date = timezone.now()
    current_month = current_date.month
    current_year = current_date.year

    start_date = timezone.make_aware(datetime(current_year, current_month, 1))
    end_date = timezone.make_aware(datetime(current_year, current_month + 1, 1))

    retrait = list(TransactionRetraitcommercial.objects.filter(
        date_transaction__gte=start_date,
        date_transaction__lt=end_date
    ).order_by('-date_transaction').values(
        'type_transaction',
        'date_transaction',
        'montant',
        'com__id',
        'com__agent__email',
        'id'
    ))

    echeanciers_pret = list(TransactionCommissionpret.objects.filter(
        date_transaction__gte=start_date,
        date_transaction__lt=end_date
    ).order_by('-date_transaction').values(
        'type_transaction',
        'date_transaction',
        'montant',
        'commission__id',
        'commission__agent__email',
        'id'
    ))

    echeanciers_pretact = list(TransactionCommissionpretact.objects.filter(
        date_transaction__gte=start_date,
        date_transaction__lt=end_date
    ).order_by('-date_transaction').values(
        'type_transaction',
        'date_transaction',
        'montant',
        'commissionact_id',
        'commissionact__agent__email',
        'id'
    ))

    # Combiner les résultats des transactions
    transactions_combined = list(chain(retrait, echeanciers_pret, echeanciers_pretact))

    # Convertir les dates en chaînes
    for transaction in transactions_combined:
        transaction['date_transaction'] = transaction['date_transaction'].strftime('%Y-%m-%d %H:%M:%S')

    # Vérifier s'il y a des transactions
    if transactions_combined:
        print("Transactions récupérées :")
        print(json.dumps(transactions_combined, indent=4, ensure_ascii=False, default=decimal_to_float))
    else:
        print("Aucune transaction pour le mois en cours.")   

    # Combiner les résultats
    resultats = {
        'comptecom': com,
        'transactionsinv': trans_inv,
        'transactions': trans_pret,
        'clients': clients_data,
        'echeanciers': transactions_combined
    }

    return JsonResponse(resultats, safe=False)


from django.http import JsonResponse
from django.utils import timezone
from datetime import timedelta
from .models import Statuts, Commissions, TransactionCommissionpret, TransactionCommissioninves, Clients
from django.db.models import Prefetch

from itertools import chain
from django.http import JsonResponse
from django.utils import timezone
from datetime import timedelta
from datetime import datetime
from django.http import JsonResponse
from django.utils import timezone
from datetime import datetime, timedelta
import json
from decimal import Decimal

def decimal_to_float(obj):
    """Convertit un objet Decimal en float pour la sérialisation JSON."""
    if isinstance(obj, Decimal):
        return float(obj)
    raise TypeError(f'Type {obj.__class__.__name__} not serializable')

def commercial_trans_pret4(request):
    # Récupérer le statut 'Actif'
    statut_actif = Statuts.objects.get(statut='Actif')
    
    # Récupérer toutes les commissions actives
    com = list(Commissions.objects.filter(statut=statut_actif).values(
        'solde', 'datesolde', 'soldeprecedent', 'date_aide', 'agent__email', 'agent__first_name'
    ))

    # Déterminer l'intervalle de la semaine passée
    now = timezone.now()
    one_week_ago = now - timedelta(days=7)

    # Récupérer les transactions de commission prêt de la semaine passée
    trans_pret = list(TransactionCommissionpret.objects.filter(date_transaction__range=(one_week_ago, now)).values(
        'type_transaction',
        'date_transaction',
        'montant',
        'agent__id',
        'agent__first_name',
        'commission__id',
        'commission__agent__email',
        'id'
    )[:5])

    # Récupérer les transactions de commission investissement de la semaine passée
    trans_inv = list(TransactionCommissioninves.objects.filter(date_transaction__range=(one_week_ago, now)).values(
        'type_transaction',
        'date_transaction',
        'montant',
        'agent__id',
        'agent__first_name',
        'commissioninv__id',
        'commissioninv__agent__email',
        'id'
    ))

    # Filtrer les clients ayant un ComptePrets avec un statut 'Actif'
    clients = Clients.objects.prefetch_related(
        Prefetch(
            'compteprets_set',
            queryset=ComptePrets.objects.select_related('com').filter(statut=statut_actif),
            to_attr='active_compteprets'
        )
    )

    clients_data = []
    for client in clients:
        for compte_pret in client.active_compteprets:
            clients_data.append({
                'nom': client.nom,
                'prenom': client.prenom,
                'sexe': client.sexe.sexe if client.sexe else 'Non défini',
                'telephone': client.telephone,
                'numero_compte': compte_pret.numero_compte,
                'solde': compte_pret.solde,
                'agent_nom': compte_pret.com.nom if compte_pret.com else 'Non défini',
                'agent_email': compte_pret.com.email if compte_pret.com else 'Non défini',
            })

    
    # Obtenir la date actuelle
    current_date = timezone.now()
    current_month = current_date.month
    current_year = current_date.year

    start_date = timezone.make_aware(datetime(current_year, current_month, 1))
    end_date = timezone.make_aware(datetime(current_year, current_month + 1, 1))

    retrait = TransactionRetraitcommercial.objects.filter(
        date_transaction__gte=start_date,
        date_transaction__lt=end_date
    ).order_by('-date_transaction')

    echeanciers_pret = TransactionCommissionpret.objects.filter(
        date_transaction__gte=start_date,
        date_transaction__lt=end_date
    ).order_by('-date_transaction')

    echeanciers_pretact = TransactionCommissionpretact.objects.filter(
        date_transaction__gte=start_date,
        date_transaction__lt=end_date
    ).order_by('-date_transaction')

    transactions_combined = list(
        chain(echeanciers_pret, echeanciers_pretact,retrait).values(
            'type_transaction',
            'date_transaction',
            'montant',
            'com__id',
            'com__agent__email',
            'id'
        )
    )

    # Convertir les dates en chaînes
    for transaction in transactions_combined:
        transaction['date_transaction'] = transaction['date_transaction'].strftime('%Y-%m-%d %H:%M:%S')

    # Vérifier s'il y a des transactions
    if transactions_combined:
        print("Transactions récupérées :")
        print(json.dumps(transactions_combined, indent=4, ensure_ascii=False, default=decimal_to_float))
    else:
        print("Aucune transaction pour le mois en cours.")

    print(transactions_combined)

    # Combiner les résultats
    resultats = {
        'comptecom': com,
        'transactionsinv': trans_inv,
        'transactions': trans_pret,
        'clients': clients_data,
        'echeanciers': transactions_combined
    }

    # Retourner les résultats en format JSON
    return JsonResponse(resultats, safe=False)

def commercial_trans_pret3(request):
    # Récupérer le statut 'Actif'
    statut_actif = Statuts.objects.get(statut='Actif')
    
    # Récupérer toutes les commissions actives
    com = list(Commissions.objects.filter(statut=statut_actif).values(
        'solde', 'datesolde', 'soldeprecedent', 'date_aide', 'agent__email', 'agent__first_name'
    ))

    # Déterminer l'intervalle de la semaine passée
    now = timezone.now()
    one_week_ago = now - timedelta(days=7)

    # Récupérer les transactions de commission prêt de la semaine passée
    trans_pret = list(TransactionCommissionpret.objects.filter(date_transaction__range=(one_week_ago, now)).values(
        'type_transaction',
        'date_transaction',
        'montant',
        'agent__id',
        'agent__first_name',
        'commission__id',
        'commission__agent__email',
        'id'
    )[:5])

    # Récupérer les transactions de commission investissement de la semaine passée
    trans_inv = list(TransactionCommissioninves.objects.filter(date_transaction__range=(one_week_ago, now)).values(
        'type_transaction',
        'date_transaction',
        'montant',
        'agent__id',
        'agent__first_name',
        'commissioninv__id',
        'commissioninv__agent__email',
        'id'
    ))

    # Filtrer les clients ayant un ComptePrets avec un statut 'Actif'
    clients = Clients.objects.prefetch_related(
        Prefetch(
            'compteprets_set',
            queryset=ComptePrets.objects.select_related('com').filter(statut=statut_actif),
            to_attr='active_compteprets'
        )
    )

    clients_data = []
    for client in clients:
        for compte_pret in client.active_compteprets:
            clients_data.append({
                'nom': client.nom,
                'prenom': client.prenom,
                'sexe': client.sexe.sexe if client.sexe else 'Non défini',
                'telephone': client.telephone,
                'numero_compte': compte_pret.numero_compte,
                'solde': compte_pret.solde,
                'agent_nom': compte_pret.com.nom if compte_pret.com else 'Non défini',
                'agent_email': compte_pret.com.email if compte_pret.com else 'Non défini',
            })

     # Obtenir la date actuelle
        # Obtenir la date actuelle
    current_date = timezone.now()
    current_month = current_date.month
    current_year = current_date.year

    # Imprimer les valeurs pour le débogage
    print("Current date:", current_date)
    print("Current month:", current_month)
    print("Current year:", current_year)

    # Filtrer les transactions de retrait du mois en cours
    start_date = datetime(current_year, current_month, 1)
    end_date = datetime(current_year, current_month + 1, 1)  # Premier jour du mois suivant
    retrait = TransactionRetraitcommercial.objects.filter(
        date_transaction__gte=start_date,
        date_transaction__lt=end_date
    ).order_by('-date_transaction')

    # Utiliser chain et values pour extraire les champs spécifiques
    transactions_combined = list(
        retrait.values(
            'type_transaction',
            'date_transaction',
            'montant',
            'com__id',
            'com__agent__email',  # Utiliser 'com__agent__email' pour l'email de l'agent lié à la commission
            'id'
        )
    )

    # Vérifier s'il y a des transactions
    if transactions_combined:
        print("Transactions récupérées :")
        print(json.dumps(transactions_combined, indent=4, ensure_ascii=False))
    else:
        print("Aucune transaction pour le mois en cours.")



    print(transactions_combined)


    # Combiner les résultats
    resultats = {
        'comptecom': com,
        'transactionsinv': trans_inv,
        'transactions': trans_pret,
        'clients': clients_data,
        'echeanciers': transactions_combined
    }

    # Retourner les résultats en format JSON
    return JsonResponse(resultats, safe=False)


def commercial_trans_pret2(request):
    # Récupérer le statut 'Actif'
    statut_actif = Statuts.objects.get(statut='Actif')
    
    # Récupérer toutes les commissions actives
    com = list(Commissions.objects.filter(statut=statut_actif).values(
        'solde', 'datesolde', 'soldeprecedent', 'date_aide', 'agent__email', 'agent__first_name'
    ))

    # Déterminer l'intervalle de la semaine passée
    now = timezone.now()
    one_week_ago = now - timedelta(days=7)

    # Récupérer les transactions de commission prêt de la semaine passée
    trans_pret = list(TransactionCommissionpret.objects.filter(date_transaction__range=(one_week_ago, now)).values(
        'type_transaction',
        'date_transaction',
        'montant',
        'agent__id',
        'agent__first_name',
        'commission__id',
        'commission__agent__email',
        'id'
    )[:5])

    # Récupérer les transactions de commission investissement de la semaine passée
    trans_inv = list(TransactionCommissioninves.objects.filter(date_transaction__range=(one_week_ago, now)).values(
        'type_transaction',
        'date_transaction',
        'montant',
        'agent__id',
        'agent__first_name',
        'commissioninv__id',
        'commissioninv__agent__email',
        'id'
    ))

   # Filtrer les clients ayant un ComptePrets avec un statut 'Actif'
    clients = Clients.objects.prefetch_related(
        Prefetch( 
            'compteprets_set',  # Relation inverse de ComptePrets vers Clients
            queryset=ComptePrets.objects.select_related('com').filter(statut=statut_actif),
            to_attr='active_compteprets'  # Attribut personnalisé pour accéder aux comptes actifs
        )
    )

    clients_data = []
    for client in clients:
        for compte_pret in client.active_compteprets:
            # Construction des données du client et du compte prêt
            clients_data.append({
                'nom': client.nom,
                'prenom': client.prenom,
                'sexe': client.sexe.sexe if client.sexe else 'Non défini',  # Gérer les valeurs nulles pour sexe
                'telephone': client.telephone,
                'numero_compte': compte_pret.numero_compte,
                'solde': compte_pret.solde,
                'agent_nom': compte_pret.com.nom if compte_pret.com else 'Non défini',  # Gérer les cas où com est nul
                'agent_email': compte_pret.com.email if compte_pret.com else 'Non défini',
            })

    
    compte_pret = get_object_or_404(Commissions, statut=statut_actif)

    echeanciers_pret = TransactionCommissionpret.objects.filter(commission=compte_pret).order_by('-date_transaction')
    echeanciers_pretact = TransactionCommissionpretact.objects.filter(commissionact=compte_pret).order_by('-date_transaction')
    retrait = TransactionRetraitcommercial.objects.filter(com=compte_pret).order_by('-date_transaction')

    # Combiner les transactions
    echeanciers_combined = list(chain(echeanciers_pret, echeanciers_pretact, retrait))


    # Serializer les transactions
    transactions_serialized = [
        {
            'description': str(ech),
            'date_transaction': ech.date_transaction,
            'agent__email' : ech.agent__email,
            'montant': ech.montant,
            'statut': 'retrait' if isinstance(ech, TransactionRetraitcommercial) else 'autre'
        } for ech in echeanciers_combined
    ]
    # Combiner les résultats
    resultats = {
        'comptecom': com,
        'transactionsinv': trans_inv,
        'transactions': trans_pret,
        'clients': clients_data,
        'echeanciers': transactions_serialized
    }

    # Retourner les résultats en format JSON
    return JsonResponse(resultats, safe=False)

def commercial_trans_pret1(request):
    # Récupérer le statut actif
    statut_actif = Statuts.objects.get(statut='Actif')
    
    # Récupérer toutes les commissions actives avec les champs nécessaires
    com = list(Commissions.objects.filter(statut=statut_actif).values(
        'solde', 'datesolde', 'soldeprecedent', 'date_aide', 'agent__email','agent__first_name'
    ))

    # Déterminer l'intervalle de la semaine passée
    now = timezone.now()
    one_week_ago = now - timedelta(days=7)

    # Récupérer toutes les transactions de commission prêt de la semaine passée avec les champs nécessaires
    trans_pret = list(TransactionCommissionpret.objects.filter(date_transaction__range=(one_week_ago, now)).values(
        'type_transaction',
        'date_transaction',
        'montant',
        'agent__id',  # ID de l'agent
        'agent__first_name',  # Prénom de l'agent
        'commission__id',  # ID de la commission
        'commission__agent__email',  # Email du client associé à la commissioncommission__agent__email
        'id'
    ))

    # Récupérer toutes les transactions de commission investissement de la semaine passée avec les champs nécessaires
    trans_inv = list(TransactionCommissioninves.objects.filter(date_transaction__range=(one_week_ago, now)).values(
        'type_transaction',
        'date_transaction',
        'montant',
        'agent__id',  # ID de l'agent
        'agent__first_name',  # Prénom de l'agent
        'commissioninv__id',  # ID de la commission
        'commissioninv__agent__email',  # Email du client associé à la commission
        'id'
    ))

    # Récupérer le statut 'Actif'
    statut_actif = Statuts.objects.get(statut='Actif')
    
    # Filtrer les clients ayant un ComptePrets avec le statut 'Actif'
    clients = Clients.objects.filter(compteprets__statut=statut_actif).prefetch_related('compteprets__com')

    clients_data = []
    for client in clients:
        # Récupérer le premier compte prêt actif du client (s'il en a plusieurs)
        compte_pret = client.compteprets.filter(statut=statut_actif).first()
        
        if compte_pret:
            # Construction des données du client
            clients_data.append({
                'nom': client.nom,
                'prenom': client.prenom,
                'sexe': client.sexe.sexe if client.sexe else 'Non défini',  # Gérer les valeurs nulles pour sexe
                'telephone': client.telephone,
                'email_com': compte_pret.com.email if compte_pret.com else 'Non défini',  # Gérer le cas où com est nul
            })

    

    # Combiner les résultats
    resultats = {
        'comptecom': com,
        'transactionsinv': trans_inv,
        'transactions': trans_pret,
        'clients': clients_data
    }

    # Retourner les résultats en format JSON
    return JsonResponse(resultats, safe=False)

#____________________________________________________________________________________________________________________________________________________________

# liste des echeances client pour le commercial 

def clients_echeance_apicom(request):
    date_actuelle = now().date()
    date_une_semaine_plus_tard = date_actuelle + timedelta(days=3)

    clients_proche_echeance = list(Echeancier.objects.filter(
        date_echeance__gte=date_actuelle,
        date_echeance__lte=date_une_semaine_plus_tard,
        est_paye=False
    ).values(
        'compte_pret__client__nom',
        'compte_pret__client__prenom',
        'compte_pret__client__telephone',
        'compte_pret__client__email',
        'compte_pret__client__photo',
        'compte_pret__com__email',
        'compte_pret__numero_compte',
        'montant_echeance',
        'date_echeance',
        'id'
    ))

    echeances_non_payees = list(Echeancier.objects.filter(
        est_paye=False,
        date_echeance__lt=now()
    ).values(
        'compte_pret__client__nom',
        'compte_pret__client__prenom',
        'compte_pret__client__telephone',
        'compte_pret__client__email',
        'compte_pret__client__photo',
        'compte_pret__com__email',
        'compte_pret__numero_compte',
        'montant_echeance',
        'date_echeance',
        'id'
    ))

    # Combiner les résultats
    resultats = {
        'echproche': clients_proche_echeance,
        'echretard': echeances_non_payees,
    }

    # Retourner les résultats en format JSON
    return JsonResponse(resultats, safe=False)

# COMPTE KHA______________________________________________________________________________________________________________________________________ 
# Récupérer les dividende
def kha(request):
# montant a repatir
    # Récupérer les actionnaires et leurs informations
    actionnaires_type_1 = Actionnaire.objects.filter(type_act_id=1)
    actionnaires_type_2 = Actionnaire.objects.filter(type_act_id=2)

    # Récupérer le montant à répartir entre les actionnaires
    echeances_payees_mois = Echeancier.objects.filter(date_echeance__month=date.today().month, est_paye=True)
    echeances_payees_moisact = Echeancieract.objects.filter(date_echeance__month=date.today().month, est_paye=True)
    benefice_mois = sum(echeance.montant_interet for echeance in echeances_payees_mois) + sum(echeance.montant_interet for echeance in echeances_payees_moisact)
    #depenses_mois = Depense.objects.filter(date__month=date.today().month).aggregate(Sum('montant'))['montant__sum'] or 0
    


    today = timezone.localtime(timezone.now()).date()
    depenses_mois = Depense.objects.filter(date__month=date.today().month)
    print(depenses_mois)  # Cela vous montrera quelles entrées sont prises en compte.
    total_montant = depenses_mois.aggregate(Sum('montant'))['montant__sum'] or 0
    print(total_montant)
    print(benefice_mois)

    today = timezone.localtime(timezone.now()).date()
    depenses_mois = Depense.objects.filter(date__month=today.month, date__year=today.year).aggregate(Sum('montant'))['montant__sum'] or 0
    montant_a_repartir = benefice_mois - depenses_mois

    # Répartir les montants selon le type d'actionnaire
    # Répartir les montants selon le type d'actionnaire
    statut_actif = get_object_or_404(Statuts, statut='Actif')
    Conf = Confconstantes.objects.filter(statut=statut_actif).first()
    #montant_a_repartir_type_1 = montant_a_repartir * Decimal('2.0') / Decimal('3.0')
    #montant_a_repartir_type_2 = montant_a_repartir * Decimal('1.0') / Decimal('3.0')
    montant_a_repartir_type_1 = montant_a_repartir * Decimal(Conf.partactif)
    montant_a_repartir_type_chef = montant_a_repartir * Decimal(Conf.partnonactif)* Decimal(Conf.partrespo)
    #montant_a_repartir_type_2 = montant_a_repartir * Decimal(Conf.partnonactif)
    montant_a_repartir_type_2 = (montant_a_repartir * Decimal(Conf.partnonactif)) - montant_a_repartir_type_chef
#_____________________________________

    # Récupérer toutes les tontines avec les champs nécessaires
    comptekha = list(CompteKha.objects.all().values(
        'solde',
        'datesolde',  # Email du client
        'soldeprecedent',
        'dateprecedent',
        'statut'
    ))

    # Récupérer toutes les transactions de tontine avec les champs nécessaires
    trans_kha = list(TransactionKha.objects.all().values(
        'type_transaction',
        'date_transaction',
        'comptekha',
        #'agent__id',  # ID de l'agent
        'agent__first_name',  # Nom de l'agent
        'agent__id',  # ID de la tontine
        'agent__email',  # Email du client associé à la tontin
        'id'
    ))

    # Récupérer toutes les tontines avec les champs nécessaires
    comptekhaad = list(CompteAdhesionkhas.objects.all().values(
        'solde',
        'datesolde',  # Email du client
        'soldeprecedent',
        'dateprecedent',
        'statut'
    ))

    # Récupérer toutes les transactions de tontine avec les champs nécessaires
    trans_khaad = list(TransactionAdhesionkha.objects.all().values(
        'type_transaction',
        'date_transaction',
        'compteAdhessionkha',
        #'agent__id',  # ID de l'agent
        'agent__first_name',  # Nom de l'agent
        'agent__id',  # ID de la tontine
        'agent__email',  # Email du client associé à la tontin
        'id'
    ))

    # Combiner les résultats
    resultats = {
        'cptekha': comptekha,
        'transactions': trans_kha,
        'cptekhaad': comptekhaad,
        'transactionsad': trans_khaad,
        'depenses_mois' : depenses_mois,
        'benefice_mois' : benefice_mois,
        'montant_a_repartir' : montant_a_repartir,
        'montant_a_repartir_type_1' : montant_a_repartir_type_1,
        'montant_a_repartir_type_2' : montant_a_repartir_type_2,
        'montant_a_repartir_type_chef' : montant_a_repartir_type_chef
    }

    # Retourner les résultats en format JSON
    return JsonResponse(resultats, safe=False)

# somme AIDE
from django.http import JsonResponse
from django.db.models import Sum
from datetime import datetime, time

def kha_trans_aide(request):
    # Récupérer le statut actif
    statut_actif = Statuts.objects.get(statut='Actif')
    dateactuelle = now().date()

    # Count active savings accounts from CompteEpargnes
    count_aide = Aides.objects.filter(statut=statut_actif).count()
    # Récupérer toutes les tontines actives avec les champs nécessaires et effectuer l'agrégation
    tontine_aide = Tontines.objects.filter(statut=statut_actif).values(
        'client__id',
        'client__email',
        'numero_tontine',
        'date_tontine',
        'agent__id',
        'agent__first_name',
        'statut__id',
        'dateaide',
        'montant_aide',
        'id'
    ).annotate(
        total_nbreaide=Sum('nbreaide'),
        total_solde=Sum('solde'),
        total_cotite=Sum('cotite')
    )

    # Convertir le QuerySet en liste de dictionnaires
    tontine_aide = list(tontine_aide)

    # Récupérer toutes les aides avec les champs nécessaires
    start_of_day = datetime.combine(dateactuelle, time.min)
    end_of_day = datetime.combine(dateactuelle, time.max)

    aide_aide = list(Aides.objects.filter(date_aide__range=(start_of_day, end_of_day)).values(
        'client__id',
        'client__nom',
        'client__prenom',
        'client__email',
        'date_aide',
        'montant_aide',
        'statut__id',
        'id'
    ))

    # Récupérer toutes les transactions de tontine avec les champs nécessaires
    trans_aide = list(TransactionTontine.objects.filter(date_transaction__range=(start_of_day, end_of_day)).values(
        'type_transaction',
        'date_transaction',
        'montant',
        'agent__id',
        'agent__first_name',
        'tontine__id',
        'tontine__numero_tontine',
        'tontine__client__email',
        'tontine__client__nom',
        'tontine__client__prenom',
        'id'
    ))

    # Combiner les résultats
    resultats = {
        'tontines': tontine_aide,
        'aides': aide_aide,
        'transactions': trans_aide,
        'count_aide' : count_aide
    }

    # Retourner les résultats en format JSON
    return JsonResponse(resultats, safe=False)

# ______________________________________________________________________________________________________________________________________________________
from django.http import JsonResponse
from django.db.models import Sum
from datetime import datetime, time

def kha_trans_pret(request):
    # Récupérer le statut actif
    statut_actif = Statuts.objects.get(statut='Actif')
    dateactuelle = now().date()
    
    # Récupérer les comptes de prêt actifs avec les champs nécessaires
    comptes_pret = ComptePrets.objects.filter(statut=statut_actif).values(
        'numero_compte', 'solde', 'somme_initiale'
    )
    
    comptes_pretact = ComptePretsact.objects.filter(statut=statut_actif).values(
        'numero_compte', 'solde', 'somme_initiale'
    )

    # Calculer la somme totale des champs solde et somme_initiale
    total_solde_pret = comptes_pret.aggregate(total_solde=Sum('solde'))['total_solde'] or 0
    total_somme_initiale_pret = comptes_pret.aggregate(total_somme_initiale=Sum('somme_initiale'))['total_somme_initiale'] or 0

    total_solde_pretact = comptes_pretact.aggregate(total_solde=Sum('solde'))['total_solde'] or 0
    total_somme_initiale_pretact = comptes_pretact.aggregate(total_somme_initiale=Sum('somme_initiale'))['total_somme_initiale'] or 0

    # Additionner les totaux des deux groupes
    total_solde = total_solde_pret + total_solde_pretact
    total_somme_initiale = total_somme_initiale_pret + total_somme_initiale_pretact

    comptes_pret = list(comptes_pret) + list(comptes_pretact)

    # Récupérer toutes les aides avec les champs nécessaires
    pret_pret = list(ComptePrets.objects.filter(date_demande=dateactuelle).values(
        'numero_compte',
        'somme_initiale', # Email du client
        'date_demande',
        'solde',
        'statut',  # ID du statut
        'duree_en_mois',  # Nom du statut
        'id'
    ))

    start_of_day = datetime.combine(dateactuelle, time.min)
    end_of_day = datetime.combine(dateactuelle, time.max)

    # Récupérer toutes les transactions de prêt avec les champs nécessaires
    trans_pret = list(TransactionPret.objects.filter(
    date_transaction__range=(start_of_day, end_of_day)).values(
        'type_transaction',
        'date_transaction',
        'montant',
        'agent__id',  # ID de l'agent
        'agent__first_name',  # Nom de l'agent
        'compte_pret__id',  # Email du client associé à la tontine
        'id'
    ))

    trans_pretact = list(TransactionPretact.objects.filter(
    date_transaction__range=(start_of_day, end_of_day)).values(
        'type_transaction',
        'date_transaction',
        'montant',
        'agent__id',  # ID de l'agent
        'agent__first_name',  # Nom de l'agent
        'compte_pret__id',   # Email du client associé à la tontine
        'id'
    ))

    trans_pret += trans_pretact
        # nbre = len(trans_pret)
    # Combiner les résultats
    resultats = {
        'comptepret': comptes_pret,
        'prets': pret_pret,
        'transactions': trans_pret,
        'total_solde': total_solde,
        'total_somme_initiale': total_somme_initiale,
            # //'nbre' : nbre
    }

    # Retourner les résultats en format JSON
    return JsonResponse(resultats, safe=False)


from django.http import JsonResponse
from django.db.models import Sum

def kha_trans_epargne(request):
    # Récupérer le statut actif
    statut_actif = Statuts.objects.get(statut='Actif')
    
    # Récupérer les comptes d'épargne actifs avec les champs nécessaires
    comptes_epargne = CompteEpargnes.objects.filter(statut=statut_actif).values(
        'numero_compte', 'solde', 'statut'
    )
    
    comptes_epargneact = CompteEpargnesact.objects.filter(statut=statut_actif).values(
        'numero_compte', 'solde', 'statut'
    )

    # Count active savings accounts from CompteEpargnes
    count_comptes_epargne = CompteEpargnes.objects.filter(statut=statut_actif).count()

    # Count active savings accounts from CompteEpargnesact
    count_comptes_epargneact = CompteEpargnesact.objects.filter(statut=statut_actif).count()

    # Optionally, sum up the total count
    total_count = count_comptes_epargne + count_comptes_epargneact


    # Calculer la somme totale des champs solde
    total_solde_epargne = comptes_epargne.aggregate(total_solde=Sum('solde'))['total_solde'] or 0
    total_solde_epargneact = comptes_epargneact.aggregate(total_solde=Sum('solde'))['total_solde'] or 0

    # Additionner les totaux des deux groupes
    total_solde = total_solde_epargne + total_solde_epargneact

    comptes_epargne = list(comptes_epargne) + list(comptes_epargneact)

    # Récupérer toutes les aides avec les champs nécessaires
    epargne_epargne = list(CompteEpargnes.objects.all().values(
        'numero_compte',  # Email du client
        'solde',
        'statut',  # ID du statut
        'id'
    ))

    dateactuelle = now().date()
    start_of_day = datetime.combine(dateactuelle, time.min)
    end_of_day = datetime.combine(dateactuelle, time.max)
    # Récupérer toutes les transactions d'épargne avec les champs nécessaires
    trans_epargne = list(TransactionEpargne.objects.filter(
    date_transaction__range=(start_of_day, end_of_day)).values(
        'type_transaction',
        'date_transaction',
        'montant',
        'agent__id',  # ID de l'agent
        'agent__first_name',  # Nom de l'agent
        'compte_epargne__id',  # Email du client associé à la tontine
        'id'
    ))

    trans_epargneact = list(TransactionEpargneact.objects.filter(
    date_transaction__range=(start_of_day, end_of_day)).values(
        'type_transaction',
        'date_transaction',
        'montant',
        'agent__id',  # ID de l'agent
        'agent__first_name',  # Nom de l'agent
        'compte_epargne__id',  # Email du client associé à la tontine
        'id'
    ))

    trans_epargne += trans_epargneact
        # nbre = len(trans_epargne)
    # Combiner les résultats
    resultats = {
        'compteepargne': comptes_epargne,
        'epargne': epargne_epargne,
        'transactions': trans_epargne,
        'total_solde': total_solde,
        'total_count' : total_count
    }

    # Retourner les résultats en format JSON
    return JsonResponse(resultats, safe=False)

from django.utils.timezone import make_aware, get_current_timezone
from datetime import datetime, time

def decimal_to_float(obj):
    """Convertit un objet Decimal en float pour la sérialisation JSON."""
    if isinstance(obj, Decimal):
        return float(obj)
    raise TypeError(f'Type {obj.__class__.__name__} not serializable')


def kha_trans_solde(request):
    # Récupérer le statut actif
    statut_actif = Statuts.objects.get(statut='Actif')
    
    comptes_epargne = list(CompteKha.objects.filter(statut=statut_actif).values('solde', 'statut'))
    comptes_adhesion = list(CompteAdhesionkhas.objects.filter(statut=statut_actif).values('solde', 'statut'))
    comptes_interet = list(CompteInterets.objects.filter(statut=statut_actif).values('solde', 'statut'))
    comptes_penalite = list(ComptePenalites.objects.filter(statut=statut_actif).values('solde', 'statut'))

    current_date = timezone.now()
    current_month = current_date.month
    current_year = current_date.year

    start_date = timezone.make_aware(datetime(current_year, current_month, 1))
    end_date = timezone.make_aware(datetime(current_year, current_month + 1, 1))
    
    trans_adh = list(TransactionAdhesionkha.objects.filter(
        date_transaction__gte=start_date,
        date_transaction__lt=end_date
    ).order_by('-date_transaction').values('type_transaction', 'date_transaction', 'montant', 'agent__first_name', 'agent__last_name'))

    trans_fond = list(TransactionFondateur.objects.filter(
        date_transaction__gte=start_date,
        date_transaction__lt=end_date
    ).order_by('-date_transaction').values('type_transaction', 'date_transaction', 'montant', 'agent__first_name', 'agent__last_name'))

    trans_ris = list(TransactionRistourne.objects.filter(
       date_transaction__gte=start_date,
        date_transaction__lt=end_date
    ).order_by('-date_transaction').values('type_transaction', 'date_transaction', 'montant', 'actionnaire__nom', 'actionnaire__prenom'))

    trans_int = list(TransactionInteret.objects.filter(
    date_transaction__gte=start_date,
        date_transaction__lt=end_date
    ).order_by('-date_transaction').values('type_transaction', 'date_transaction', 'montant'))

    trans_pen = list(TransactionPenalite.objects.filter(
    date_transaction__gte=start_date,
        date_transaction__lt=end_date
    ).order_by('-date_transaction').values('type_transaction', 'date_transaction', 'montant'))

    trans_penact = list(TransactionPenaliteact.objects.filter(
    date_transaction__gte=start_date,
        date_transaction__lt=end_date
    ).order_by('-date_transaction').values('type_transaction', 'date_transaction', 'montant'))

    trans_epargne = trans_adh + trans_penact + trans_pen + trans_int + trans_ris + trans_fond

    print(trans_epargne)

    resultats = {
        'comptes_epargne': comptes_epargne,
        'comptes_adhesion': comptes_adhesion,
        'comptes_interet': comptes_interet,
        'comptes_penalite': comptes_penalite,
        'transactions': trans_epargne,
    }

    return JsonResponse(resultats, safe=False)



# COMPTE KHA_______________________________________________________________________________________________________________________________________

# Liste des compte
from django.http import JsonResponse
from .models import CompteEpargnes, ComptePrets, ComptePretsact

def liste_comptesact_json(request):
   
    # Récupération des comptes prêt act avec email de l'actionnaire
    comptes_pret_act = ComptePretsact.objects.values('numero_compte', 'solde', 'statut', 'actionnaire__email')

    # Vous pouvez maintenant passer ces trois listes à votre réponse JSON
    data = {
        
        'comptes_pret_act': list(comptes_pret_act),
    }

    return JsonResponse(data, safe=False)

#API___ Juillet 2
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def payment_notify(request):
    if request.method == 'POST':
        data = request.POST
        # Traitez les données reçues de CinetPay ici
        print(data)
        # Répondez à CinetPay que la notification a été reçue
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'failed'}, status=400)


# DOCUMENTS ESPACE ENSEIGNANT------------------------------------------------------------------------------------------------------------
# DOCUMENT DE CLASSE------------------------------------------------------------------------------------------------------------
# Liste Document 
@login_required()
def listedoc(request):
   
    # Récupérer les données triées en fonction de l'objet
    queryse = Documents.objects.all()

    # Passer les données triées en contexte au template
    context = {'queryse': queryse}
    return render(request, 'Pages/documents/listedoc.html', context)

# Ajouter Document
#@login_required()
#def add_document(request):
    
#    if request.method == 'POST':
        
#        form = DocumentForm(request.POST, request.FILES)
#        if form.is_valid():
 #           Fil = form.cleaned_data['Cours']
  #          Typ = Typedocuments.objects.get(Matiere=Fil)
   #         File = form.cleaned_data['File']
    #        Title = form.cleaned_data['Title']
     #       ids = form.cleaned_data['Salle']
      #      student = form.save(commit=False)
       #     userm = Documents.objects.create(Cours=Fil,File=File,Title=Title,Salle=ids,Typematiere=Typ.Typematiere)
        #    userm.save()
            
         #   return redirect('documentlist')
    #else:
        
     #   form = DocumentForm()
    #return render(request, 'Pages/documents/ajoutdoc.html', {'form': form,'annee': statuta})

@login_required()
def add_document(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('documentlist')
    else:
        form = DocumentForm()
    return render(request, 'Pages/documents/ajoutdoc.html', {'form': form})

# modifier
@login_required()
def docmodif(request, id):
    if request.method == 'POST':
        pi = Documents.objects.get(pk=id)
        fm = DocumentForm(request.POST, instance=pi)
        if fm.is_valid():
            fm.save()
            return redirect('documentlist')
    else:
        pi = Documents.objects.get(pk=id)
        fm = DocumentForm(instance=pi)
    return render(request, 'Pages/documents/modif.html',{'form':fm})

# supprimer
@login_required()
def delete_doc(request, id):
    doc = Documents.objects.get(pk=id)
    doc.delete()
    return redirect('documentlist')

# Detail
#@login_required()
def document_detail(request, document_id):
    document = Documents.objects.get(id=document_id)
    return FileResponse(document.File)


# Telecharger
# views.py

def document_detaill(request, document_id):
    document = get_object_or_404(Documents, id=document_id)
    response_data = {
        'pdf_url': document.File.url  # Assurez-vous que le champ `file` pointe vers le bon champ dans votre modèle
    }
    return JsonResponse(response_data)


#@login_required()
def document_download(request, document_id):
    document = Documents.objects.get(id=document_id)
    response = HttpResponse(document.File, content_type='application/force-download')
    response['Content-Disposition'] = f'attachment; filename="{document.File.name}"'
    return response


#API___ Juillet  2  pour AJOUTTER PRET ACTIONNAIRE
# AJOUTER PRET ACTIONNAIRE __________________________________________________________________________________________________________________________________
from .models import ComptePretsact
from .serializers import ComptePretsactSerializer

from datetime import datetime, timedelta
from rest_framework.decorators import api_view # type: ignore
from django.http import JsonResponse
import json

from django.http import JsonResponse
from datetime import datetime, timedelta
from .models import Actionnaire, Typeprets, Statuts, ComptePretsact
from .serializers import ComptePretsactSerializer

@api_view(['POST'])
def ajouter_compte_pretappi(request):
    data = json.loads(request.body)
    actionnaire_email = data.get('actionnaire')
    date_debut_pret_str = data.get('date_debut_pret')
    taux_interet = data.get('taux_interet')
    duree_en_mois = data.get('duree_en_mois')
    somme_initiale = data.get('somme_initiale')
    domicile_bancaire = data.get('domicile_bancaire')
    type_client_id = data.get('type_client')

    try:
        date_debut_pret = datetime.strptime(date_debut_pret_str, '%Y-%m-%d').date()
    except ValueError:
        return JsonResponse({'error': 'Date de début du prêt invalide'}, status=400)

    actionnaire = Actionnaire.objects.filter(email=actionnaire_email).first()
    if not actionnaire:
        return JsonResponse({'error': 'Actionnaire non trouvé'}, status=400)

    typp = Typeprets.objects.filter(id=3).first()
    if not typp:
        return JsonResponse({'error': 'Type de prêt non trouvé'}, status=400)

    statut_actif = Statuts.objects.filter(statut='Non Actif').first()
    if not statut_actif:
        return JsonResponse({'error': 'Statut non trouvé'}, status=400)

    numero_compte = f"PR{timezone.now().strftime('%Y%m%d%H%M%S')}"
    date_fin_pret = date_debut_pret + timedelta(days=30 * int(duree_en_mois))

    # Créez un dictionnaire de données pour la création de l'objet
    compte_pret_data = {
        'actionnaire': actionnaire.pk,
        'numero_compte': numero_compte,
        'solde': 0,
        'taux_interet': float(taux_interet),
        'duree_en_mois': int(duree_en_mois),
        'date_debut_pret': date_debut_pret,
        'date_fin_pret': date_fin_pret,
        'somme_initiale': float(somme_initiale),
        'domicile_bancaire': domicile_bancaire,
        'type_pret': typp.pk,
        'statut': statut_actif.pk,
        'type_client': int(type_client_id)
    }

    serializer = ComptePretsactSerializer(data=compte_pret_data)
    if serializer.is_valid():
        compte_pret = serializer.save()
        # Calculer et mettre à jour le solde
        compte_pret.solde = compte_pret.somme_initiale + compte_pret.calculer_interets()
        compte_pret.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

from django.db.models.signals import post_save
from django.dispatch import receiver
from decimal import Decimal
from .models import ComptePretsact, Echeancieract

@receiver(post_save, sender=ComptePretsact)
def create_echeanciersactapi(sender, instance, created, **kwargs):
    statut_actif = get_object_or_404(Statuts, statut='Actif')
    Conf = Confconstantes.objects.filter(statut=statut_actif).first()
    taux_kha = Conf.partepargne
    taux_khaa = Conf.partfraisdos
    if created:
        statut_actif = get_object_or_404(Statuts, statut='Actif')
        Conf = Confconstantes.objects.filter(statut=statut_actif).first()
        taux_kha = Conf.partepargne
        taux_khaa = Conf.partfraisdos
        somme_initiale = instance.somme_initiale
        taux_interet = instance.taux_interet / Decimal('100')
        duree_en_mois = instance.duree_en_mois

        interets = somme_initiale * taux_interet * duree_en_mois
        instance.solde = somme_initiale + interets + (somme_initiale * taux_kha) + (somme_initiale * taux_khaa)
        instance.save()  # Sauvegarde les modifications apportées au solde

        if instance.type_client_id == 1:  # Pour un client avec des échéances chaque semaine
            montant_interet = interets / (duree_en_mois * 4)
            montant_epargne = (somme_initiale * taux_kha) / (duree_en_mois * 4)
            montant_adhesion = (somme_initiale * taux_khaa) / (duree_en_mois * 4)
            montant_echeance = ((somme_initiale + interets) / (duree_en_mois * 4)) + montant_epargne + montant_adhesion
        elif instance.type_client_id == 2:  # Pour un client avec des échéances chaque mois
            montant_interet = interets / duree_en_mois
            montant_epargne = (somme_initiale * taux_kha) / duree_en_mois
            montant_adhesion = (somme_initiale * taux_khaa) / duree_en_mois
            montant_echeance = ((somme_initiale + interets) / duree_en_mois) + montant_epargne + montant_adhesion
        else:
            montant_epargne = Decimal('0')
            montant_adhesion = Decimal('0')
            montant_interet = Decimal('0')
            montant_echeance = Decimal('0')


        echeances = instance.calculer_echeances()
        for date_echeance in echeances:
            Echeancieract.objects.create(
                compte_pretact=instance,
                date_echeance=date_echeance,
                montant_echeance=montant_echeance,
                montant_interet=montant_interet,
                montant_epargne=montant_epargne,
                montant_adhesion=montant_adhesion
            )
# _______________________________________________________________________________________________________________________________________________


#API___ Juillet  2  






from .models import Echeancieract, TransactionPretact
from .serializers import EcheancieractSerializer, TransactionPretactSerializer
from django.shortcuts import get_object_or_404
from django.utils import timezone
from decimal import Decimal

@api_view(['POST'])
def process_payment(request):
    data = request.data
    echeancier_id = data.get('echeancier_id')
    amount = data.get('amount')
    description = data.get('description')

    if not echeancier_id:
        return Response({'error': 'Echeancier ID is required'}, status=status.HTTP_400_BAD_REQUEST)
    
    echeance = get_object_or_404(Echeancieract, pk=echeancier_id)
    
    # Marquer l'échéance comme payée
    echeance.est_paye = True
    echeance.save()
    
    # Créer une nouvelle transaction de prêt pour indiquer le paiement de l'échéance
    agent = request.user if request.user.is_authenticated and isinstance(request.user, Agent) else None
    
    transaction_pret = TransactionPretact.objects.create(
        compte_pret=echeance.compte_pretact,
        montant=echeance.montant_echeance,
        type_transaction='Depot',  # Mettez le type de transaction approprié
        agent=agent
    )
    
    # Mise à jour du compte KHA
    statut_actif = Statuts.objects.get(statut='Actif')
    kha = get_object_or_404(CompteKha, statut=statut_actif)
    kha.soldeprecedent = kha.solde
    kha.dateprecedent = kha.datesolde
    kha.datesolde = timezone.now()
    kha.solde += echeance.montant_epargne
    kha.save()
    
    transaction_kha = TransactionKha.objects.create(
        comptekha=kha,
        montant=echeance.montant_epargne,
        type_transaction='Virement',
        agent=agent
    )
    
    # Mettre à jour la commission de l'agent
    taux_com = 1.5 / 100
    commission, created = Commissions.objects.get_or_create(agent=agent, defaults={
        'solde': 0,
        'soldeprecedent': 0,
        'datesolde': timezone.now(),
        'statut': agent.type_agent if agent else 'Default'
    })
    
    commission.soldeprecedent = commission.solde
    commission.datesolde = timezone.now()
    commission.solde += (echeance.montant_interet * Decimal(taux_com))
    commission.save()
    
    transaction_com = TransactionCommissionpret.objects.create(
        commission=commission,
        echeance=echeance,
        montant=(echeance.montant_interet * Decimal(taux_com)),
        type_transaction='Virement',
        agent=agent
    )
    
    # Vérifier si c'est la dernière échéance payée pour le compte prêt
    compte_pret = echeance.compte_pretact
    dernier_echeance_payee = Echeancieract.objects.filter(compte_pretact=compte_pret, est_paye=False).order_by('date_echeance').first()
    if not dernier_echeance_payee:
        # Si aucune échéance impayée, mettre le statut du compte prêt en inactif
        compte_pret.statut = Statuts.objects.get(statut='Non Actif')
        compte_pret.save()
        
    return Response({'message': 'Payment processed successfully'}, status=status.HTTP_201_CREATED)


#API___ Aout
# HISTORISQUE APPELS DES COMMERCIAUX______________________________________________________________________________________________________________________________
from .models import CallHistory
from .serializers import CallHistorySerializer

@api_view(['POST'])
def add_call_history(request):
    if request.method == 'POST':
        serializer = CallHistorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# ________________________________________________________________________________________________________________________________________________________________


# AFFICHER PAGE PRESENTATION_______________________________________________________________________________________________________________________________________
from rest_framework.permissions import AllowAny # type: ignore

class PresentationAPIView(APIView):
    permission_classes = [AllowAny] 
    def get(self, request):
        # Suppose we have only one presentation data entry
        presentation_data = Presentation.objects.first()
        if presentation_data:
            serializer = PresentationSerializer(presentation_data)
            return Response(serializer.data)
        else:
            return Response({"error": "No presentation data found"}, status=404)
# ________________________________________________________________________________________________________________________________________________________________


# CONTACT CLIENT AVEC KHA________________________________________________________________________________________________________________________________________
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Msg
import json

@csrf_exempt
def create_msg(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        titre = data.get('titre')
        message = data.get('message')
        groupemsg = data.get('groupemsg')

        if titre and message and groupemsg:
            Msg.objects.create(titre=titre, message=message, groupemsg=groupemsg)
            return JsonResponse({'status': 'success', 'message': 'Message enregistré avec succès'}, status=201)
        else:
            return JsonResponse({'status': 'error', 'message': 'Tous les champs sont requis'}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Méthode non autorisée'}, status=405)
# _______________________________________________________________________________________________________________________________________________________________


# CONTACT CLIENT AVEC UNE DEMANDES_________________________________________________________________________________________________________________________________
from rest_framework import generics # type: ignore
from .models import Demandes
from .serializers import DemandesSerializer

class DemandesCreateView(generics.CreateAPIView):
    queryset = Demandes.objects.all()
    serializer_class = DemandesSerializer

# liste
from rest_framework.views import APIView # type: ignore
from rest_framework.response import Response # type: ignore
from .models import Demandes
from .serializers import DemandesSerializer

class RecentDemandesView(APIView):
    def get(self, request):
        demandes = Demandes.objects.all().order_by('-date_dde')[:10]  # Récupère les 10 dernières demandes
        serializer = DemandesSerializer(demandes, many=True)
        return Response(serializer.data)
# ________________________________________________________________________________________________________________________________________________________________


# DOCUMENTS A TELECHARGER PAR UTILISATEUR_________________________________________________________________________________________________________________________________
from django.http import JsonResponse, FileResponse
from .models import Documents

def document_list(request):
    documents = Documents.objects.all().values('id', 'Title', 'File')
    return JsonResponse(list(documents), safe=False)

def document_download(request, document_id):
    document = Documents.objects.get(id=document_id)
    response = FileResponse(document.File.open(), as_attachment=True)
    return response
# ________________________________________________________________________________________________________________________________________________________________


# NOTIFICATIONS ______________________________________________________________________________________________________________________________________
from django.http import JsonResponse
from .models import Msg

def recent_msgs(request):
    msgs = Msg.objects.all().order_by('-date_msg')[:10]  # Récupère les 10 messages les plus récents
    msg_list = list(msgs.values('date_msg', 'titre', 'message', 'groupemsg'))
    return JsonResponse(msg_list, safe=False)

def recent_msgss(request):
    msgs = Msg.objects.filter(groupemsg='ALL').order_by('-date_msg')[:10]  # Récupère les 10 messages les plus récents
    msg_list = list(msgs.values('date_msg', 'titre', 'message', 'groupemsg'))
    return JsonResponse(msg_list, safe=False)
# ________________________________________________________________________________________________________________________________________________________________


# CONTRAT A PROVISIONNEL ______________________________________________________________________________________________________________________________________
from datetime import date
from django.shortcuts import render
from .models import Contratsponsor

def get_expiring_contrats(request):
    current_month = date.today().month
    current_year = date.today().year
    expiring_contrats = Contratsponsor.objects.filter(date_fin_contrat__year=current_year, date_fin_contrat__month=current_month)
    contrats_data = [
        {
            'nom_prenoms': f"{contrat.sponsor.nom} {contrat.sponsor.prenom}",
            'date_fin_contrat': contrat.date_fin_contrat,
            'somme_initiale': contrat.somme_initiale,
            'solde': contrat.solde
        }
        for contrat in expiring_contrats
    ]
    return JsonResponse(contrats_data, safe=False)
# ___________________________________________________________________________________________________________________________________________________

#  AJOUT DEPENSE API____________________________________________________________________________________________________________________________________________
from rest_framework import status # type: ignore
from rest_framework.decorators import api_view # type: ignore
from rest_framework.response import Response # type: ignore
from .models import Depense
from .serializers import DepenseSerializer

@api_view(['POST'])
def save_depense(request):
    if request.method == 'POST':
        serializer = DepenseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# ___________________________________________________________________________________________________________________________________________________

# API CREATION COOPERATEURS_____________________________________________________________________________________________________________________________________________
# Vue pour l'Actionnaire
from .models import Actionnaire, Typeactionnaire
from .serializers import ActionnaireSerializer
from rest_framework import viewsets # type: ignore


from django.contrib.auth.hashers import make_password
from .models import Actionnaire, Typeactionnaire, Utilisateurs
from .serializers import ActionnaireSerializer
from django.utils import timezone

class ActionnaireViewSet(viewsets.ModelViewSet):
    queryset = Actionnaire.objects.all()
    serializer_class = ActionnaireSerializer

    def create(self, request, *args, **kwargs):
        type_act_value = request.data.get('type_act')
        
        # Déterminer l'ID du type d'actionnaire en fonction de la valeur
        if type_act_value == 'Actif':
            type_act_id = 1
        elif type_act_value == 'Passif':
            type_act_id = 2
        else:
            return Response({'error': 'Type d\'actionnaire invalide.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            type_act_obj = Typeactionnaire.objects.get(id=type_act_id)
        except Typeactionnaire.DoesNotExist:
            return Response({'error': 'Type d\'actionnaire non trouvé.'}, status=status.HTTP_400_BAD_REQUEST)

        # Créer un utilisateur associé à l'actionnaire
        telephone = request.data.get('telephone')
        email = request.data.get('email')
        nom = request.data.get('nom')
        prenom = request.data.get('prenom')

        username = f"{telephone}"
        password = 'P@ssword'
        encoded_password = make_password(password)
        role = 'ACTIONNAIRE'
        statut = 'NON ACTIVE'

        user = Utilisateurs.objects.create(
            username=username,
            first_name=prenom,
            last_name=nom,
            password=encoded_password,
            email=email,
            role=role,
            statut=statut
        )

        # Préparer les données pour la création de l'actionnaire
        actionnaire_data = {
            'nom': nom,
            'prenom': prenom,
            'adresse': request.data.get('adresse', ''),
            'telephone': telephone,
            'email': email,
            'apport': request.data.get('apport', 0),
            'pourcentage': request.data.get('pourcentage', 0),
            'type_act': type_act_obj.id,
            'dividende': 0,  # Valeur par défaut
            'date_adhesion': timezone.now()  # Date du jour
        }

        # Créer l'instance de l'actionnaire
        serializer = self.get_serializer(data=actionnaire_data)
        if serializer.is_valid():
            actionnaire = serializer.save(user=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# ___________________________________________________________________________________________________________________________________________________________

#API___ Aout