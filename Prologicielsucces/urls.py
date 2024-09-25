"""Prologicielsucces URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from Prologicielsucces import settings
import accounts
from finances import views 
from accounts.views import PasswordResetRequestView, PasswordResetConfirmView,login_user,logout_user,login_usera,LoginAPIView,change_passwordsp,change_usernamesp,change_username,change_password,change_usernamecl,change_passwordcl,change_usernameag,change_passwordag
from finances.views import ActionnaireViewSet, PresentationAPIView
from django.conf.urls.static import static
from finances.views import PresentationAPIView,DemandesCreateView,RecentDemandesView
  #API____________________________________________________________________________________________________________________________________________________
from finances.views import CreerClientAPI, payment_notify, process_payment
from accounts.views import login_usera,get_csrf_token
#API__2 Juin 
from accounts.views import login_userbank,logout_userbank,profile_view

urlpatterns = [
    path('candidates/', views.CandidateListView.as_view(), name='candidate_list'),
    
    path("admin/", admin.site.urls),
    path('accounts/', login_user, name='login'),
    path('accounts/log', logout_user, name='signup'),
    path('administration/menu', views.menu, name='menu'),
    path('actionnaire/menu', views.afficher_dashboard, name='menuact'),
    path('profile/', profile_view, name='profile'),

    
# URL pour la liste des genres
    path('genres/', views.liste_genres, name='liste_genres'),
    # URL pour ajouter un genre
    path('genres/ajouter/', views.creer_genre, name='ajouter_genre'),
    # URL pour modifier un genre
    path('genres/modifier/<int:pk>/', views.modifier_genre, name='modifier_genre'),
    # URL pour supprimer un genre
    path('genres/supprimer/<int:pk>/', views.supprimer_genre, name='supprimer_genre'),
    
    # URL pour la liste des matrimoniales
    path('matrimoniales/', views.liste_matrimoniales, name='liste_matrimoniales'),
    # URL pour ajouter une matrimoniales
    path('matrimoniales/ajouter/', views.creer_matrimoniale, name='ajouter_matrimoniales'),
    # URL pour modifier une matrimoniales
    path('matrimoniales/modifier/<int:pk>/', views.modifier_matrimoniale, name='modifier_matrimoniales'),
    # URL pour supprimer une matrimoniales
    path('matrimoniales/supprimer/<int:pk>/', views.supprimer_matrimoniale, name='supprimer_matrimoniales'),
    
    # URL pour la liste des types de prêts
    path('typeprets/', views.liste_typeprets, name='liste_typeprets'),
    # URL pour ajouter un type de prêt
    path('typeprets/ajouter/', views.creer_typepret, name='ajouter_typeprets'),
    # URL pour modifier un type de prêt
    path('typeprets/modifier/<int:pk>/', views.modifier_typepret, name='modifier_typeprets'),
    # URL pour supprimer un type de prêt
    path('typeprets/supprimer/<int:pk>/', views.supprimer_typepret, name='supprimer_typeprets'),
# URL pour la liste des clients
    path('clients/', views.liste_clients, name='liste_clients'),
    path('clientsponsor/', views.liste_clientss, name='liste_clientss'),
    path('clientsaide/', views.liste_clientsa, name='liste_clientsa'),
    path('clients/<int:client_id>/detail', views.detail_clients, name='detail_clients'),
    path('clientsaide/<int:client_id>/detail', views.detail_clientsa, name='detail_clientsa'),
    # URL pour ajouter un client
    path('clients/ajouter/', views.creer_client, name='ajouter_client'),
    path('clientsponsor/ajouter/', views.creer_clients, name='ajouter_clients'),
    path('clientsaide/ajouter/', views.creer_clienta, name='ajouter_clienta'),
    # URL pour modifier un client
    path('clients/modifier/<int:pk>/', views.modifier_client, name='modifier_client'),
    # URL pour supprimer un client
    path('clients/supprimer/<int:pk>/', views.supprimer_client, name='supprimer_client'),
    
    # URL pour la liste des comptes épargnes
    path('comptes_epargnes/', views.liste_comptes_epargne, name='liste_comptes_epargnes'),
    path('comptes_epargnessponsor/', views.liste_comptes_epargnes, name='liste_comptes_epargness'),
    path('comptes_epargnessous/', views.liste_comptes_epargnec, name='liste_comptes_epargnesc'),
    path('comptes_epargne/<int:compte_epargne_id>/', views.detail_compte_epargne, name='detail_compte_epargne'),
    # URL pour ajouter un compte épargne
    path('comptes_epargnes/ajouter/', views.creer_compte_epargne, name='ajouter_compte_epargne'),
    # URL pour modifier un compte épargne
    path('comptes_epargnes/modifier/<int:pk>/', views.modifier_compte_epargne, name='modifier_compte_epargne'),
    # URL pour supprimer un compte épargne
    path('comptes_epargnes/supprimer/<int:pk>/', views.supprimer_compte_epargne, name='supprimer_compte_epargne'),
    
    # URL pour la liste des comptes prêts
    path('comptes_prets/', views.liste_comptes_prets, name='liste_comptes_prets'),
    path('comptes_pretssponsor/', views.liste_comptes_pretss, name='liste_comptes_pretss'),
    path('comptes_pretsnon/', views.liste_comptes_pretsna, name='liste_comptes_pretsna'),
    path('comptes_pretssponsornon/', views.liste_comptes_pretssna, name='liste_comptes_pretssna'),
    path('compte_pret/<int:compte_pret_id>/', views.detail_compte_pret, name='detail_compte_pret'),
    # URL pour la liste des comptes prêts
    path('comptes_prets/echeances', views.clients_proche_echeance, name='clients_proche_echeance'),
    path('sous-cooperateur/comptes_prets/echeances', views.clients_proche_echeancesous, name='clients_proche_echeanceact'),
    # URL pour la liste des comptes prêts
    path('comptes_prets/echeancesnon', views.liste_echeances_non_payees, name='liste_echeances_non_payees'),
    path('sous-cooperateur/comptes_prets/echeancesnon', views.liste_echeances_non_payeesact, name='liste_echeances_non_payeesact'),
    # URL pour ajouter un compte prêt
    path('comptes_prets/<int:client_id>/ajouter/', views.ajouter_compte_pret, name='ajouter_compte_pret'),
    # URL pour modifier un compte prêt
    path('comptes_prets/modifier/<int:pk>/', views.modifier_compte_pret, name='modifier_compte_pret'),
    # URL pour supprimer un compte prêt
    path('comptes_prets/supprimer/<int:pk>/', views.supprimer_compte_pret, name='supprimer_compte_pret'),
    path('comptes_prets/modifier/<int:pk>/', views.modifier_compte_pret, name='modifier_compte_pret'),
    # URL pour la liste des agents
        #API___ Juillet 2
    path('agents/personnel/', views.liste_agents, name='liste_agents'),
    path('agents/tout-personnels/', views.liste_agentstout, name='liste_agentstout'),
    path('agents/conseillers/', views.liste_agentcons, name='liste_agentcons'),
    path('agentstout/ajouter/', views.ajouter_agenttout, name='ajouter_agenttout'),
    path('agentsconseiller/ajouter/', views.ajouter_agentcons, name='ajouter_agentcons'),
    path('agents/commercial/', views.liste_com, name='liste_com'),
    path('agents/demarcheur/', views.liste_dem, name='liste_dem'),
    # URL pour ajouter un agent
    path('agents/ajouter/', views.ajouter_agent, name='ajouter_agent'),
    path('agents/c/ajouter/', views.ajouter_com, name='ajouter_com'),
    path('agents/d/ajouter/', views.ajouter_dem, name='ajouter_dem'),
    # URL pour modifier un agent
    path('agents/modifier/<int:pk>/', views.modifier_agent, name='modifier_agent'),
    # URL pour supprimer un agent
    path('agents/supprimer/<int:pk>/', views.supprimer_agent, name='supprimer_agent'),
    path('modifier_est_paye/<int:actionnaire_id>/', views.modifier_est_paye, name='modifier_est_paye'),
    path('modifier_est_payeretard/<int:actionnaire_id>/', views.modifier_est_payere, name='modifier_est_payere'),
        #API___ Juillet 2

    # URL pour la liste des transactions client
    path('creer_transaction_epargne/<int:id>/<int:idd>', views.creer_transaction_epargne, name='creer_transaction_epargne'),
    path('creer_transaction_pret/', views.creer_transaction_pret, name='creer_transaction_pret'),
    path('modifier_transaction_pret/<int:pk>/', views.modifier_transaction_pret, name='modifier_transaction_pret'),
    # Vue pour la modification d'une transaction d'épargne
    path('modifier_transaction_epargne/<int:transaction_id>/', views.modifier_transaction_epargne, name='modifier_transaction_epargne'),

    # Vue pour la suppression d'une transaction d'épargne
    path('supprimer_transaction_epargne/<int:transaction_id>/', views.supprimer_transaction_epargne, name='supprimer_transaction_epargne'),
    path('liste_transactions/epargnes', views.liste_transactions, name='liste_transactionsepargne'),
    path('liste_transactions/prets', views.liste_transactionss, name='liste_transactionspret'),

    # URL pour la liste des transactions sous cooperateur
    path('creer_transaction_epargnesous/<int:id>/<int:idd>', views.creer_transaction_epargnesous, name='creer_transaction_epargnesous'),
    path('modifier_transaction_epargnesous/<int:transaction_id>/', views.modifier_transaction_epargnesous, name='modifier_transaction_epargnesous'),
    path('supprimer_transaction_epargnesous/<int:transaction_id>/', views.supprimer_transaction_epargnesous, name='supprimer_transaction_epargnesous'),
    path('liste_transactions/epargnessous', views.liste_transactionsous, name='liste_transactionsepargnesous'),

    # URL pour la liste des depenses
    path('liste_depenses/', views.liste_depenses, name='liste_depenses'),
    path('ajouter_depense/', views.ajouter_depense, name='ajouter_depense'),
    path('modifier_depense/<int:depense_id>/', views.modifier_depense, name='modifier_depense'),
    path('supprimer_depense/<int:depense_id>/', views.supprimer_depense, name='supprimer_depense'),

# URL pour HISTORIQUE
    path('stories/comptes_prets/echeancesclient', views.liste_echeances_cli_payees, name='liste_echeances_cli_payees'),
    path('stories/comptes_prets/echeancessouscoop', views.liste_echeances_act_payees, name='liste_echeances_act_payees'),
    path('stories/modifier_est_paye/<int:actionnaire_id>/', views.annuler_est_payere, name='annuler_est_payere'),
    path('stories/modifier_est_payeretard/<int:actionnaire_id>/', views.modifier_est_non_payereact, name='modifier_est_non_payereact'),

    # URL pour la liste des actionnaires
    path('resultats/', views.afficher_resultats, name='afficher_resultats'),
    path('actionnaires/', views.liste_actionnaires, name='liste_actionnaires'),
    path('actionnaire-passif/', views.liste_actionnairesn, name='liste_actionnairesn'),
    path('sponsors/', views.liste_sponsors, name='liste_sponsors'),
    path('detail_actionnaire/<int:actionnaire_id>/', views.detail_actionnaire, name='detail_actionnaire'),
    path('actionnaires/ajouter/', views.ajouter_actionnaire, name='ajouter_actionnaire'),
    path('actionnairesn/ajouter/', views.ajouter_actionnairen, name='ajouter_actionnairen'),
    path('sponsor/ajouter/', views.ajouter_actionnaires, name='ajouter_actionnaires'),
    path('actionnaires/modifier/<int:actionnaire_id>/', views.modifier_actionnaire, name='modifier_actionnaire'),
    path('actionnaires-passifs/modifier/<int:actionnaire_id>/', views.modifier_actionnairen, name='modifier_actionnairen'),
    path('actionnaires/supprimer/<int:actionnaire_id>/', views.supprimer_actionnaire, name='supprimer_actionnaire'),
    path('actionnaires-passifs/supprimer/<int:actionnaire_id>/', views.supprimer_actionnairen, name='supprimer_actionnairen'),
    path('courbe_transactions/', views.courbe_transactions, name='courbe_transactions'),
        # MAJ
    path('actionnaires/message/<int:actionnaire_id>/', views.soumettre_message, name='message_actionnaire'),
    path('actionnaires/message/diffusion/', views.soumettre_messageact, name='message_actionnairetous'),
    path('actionnaires/message/gerant>/', views.soumettre_messageactger, name='message_actionnaireger'),

    path('messages/', views.listemessage, name='listemessages'),
    path('messages/modifier/<int:msg_id>/', views.modifiermessage, name='modifiermessages'),
    path('messages/supprimer/<int:msg_id>/', views.supprimermessage, name='supprimermessages'),
     # MAJ 2
    # URL pour ajouter un compte prêt
    path('actionnaires/comptepret/ajouterapi/', views.ajouter_compte_pretappi, name='ajouter_compte_pretappi'),
    path('actionnaires/comptepret/ajouter/', views.ajouter_compte_pretact, name='ajouter_compte_pretact'),
    path('actionnaires/comptepret/', views.liste_comptes_pretsact, name='liste_comptes_pretsact'),
    path('actionnaires/comptepretencours/', views.liste_comptes_pretsactenc, name='liste_comptes_pretsactenc'),
    path('actionnaires/comptepretvalide/', views.liste_comptes_pretsactval, name='liste_comptes_pretsactval'),
    path('actionnaires/comptepret/<int:compte_pret_id>/', views.detail_compte_pretact, name='detail_compte_pretact'),
    path('actionnaires/comptepret/supprimer/<int:pk>/', views.supprimer_compte_pretact, name='supprimer_compte_pretact'),
    path('actionnaires/comptepret/modifier/<int:pk>/', views.modifier_compte_pretact, name='modifier_compte_pretact'),
        # Fin MAJ
    path('modifier_est_payeact/<int:actionnaire_id>/', views.modifier_est_payeact, name='modifier_est_payeact'),
    path('modifier_est_payeretardact/<int:actionnaire_id>/', views.modifier_est_payereact, name='modifier_est_payereact'),

    #API___ Juillet 2
    # URL pour la liste des presentations
    path('presentations/', views.liste_presentation, name='liste_presentation'),
    path('presentations/create/', views.create_presentation, name='create_presentation'),
    path('presentations/<int:pk>/m/', views.modifier_presentation, name='modifier_presentation'),
    path('confconstantes/liste/', views.liste_confconstantes, name='liste_confconstantes'),
    path('confconstantes/modifier/<int:id>/', views.modifier_confconstantes, name='modifier_confconstantes'),
    path('confconstantes/detail/<int:id>/', views.detail_confconstantes, name='detail_confconstantes'),

    #API___ Juillet 2  

    # URL pour ajouter un contrat prêt
    path('contrat_prets/<int:sponsor_id>/ajouter/', views.ajouter_contrat_pret, name='ajouter_contrat_pret'),
    path('contrat_pretsac/<int:sponsor_id>/ajouter/', views.ajouter_contrat_pretac, name='ajouter_contrat_pretac'),
    path('get-client-name/', views.get_client_name, name='get_client_name'),


        #API____________________________________________________________________________________________________________________________________________________


    path('votre_point_de_terminaison/', views.votre_vue, name='votre_vue'),
    path('chemin_vers_votre_vue/', views.liste_clientsapi, name='liste_clients_api'),
    path('echeance/', views.liste_echeances_non_payeesapi, name='liste_echeances_non_payeesapi'),
    path('api/creer_client/', CreerClientAPI.as_view(), name='creer_client_api'),
   
    path('loginaa/', login_usera, name='loginaa'),

    # Ajoutez l'URL pour récupérer le jeton CSRF
    path('get_csrf_token/', get_csrf_token, name='get_csrf_token'),
    # Autres URLs de votre application

     
    #
    path('logf/login_user/', login_userbank, name='login_userbank'),
    path('logout_userbank', logout_userbank, name='logout_userbank'),
    path('search_clients/', views.search_clients, name='search_clients'),
    path('search_clientsai/', views.search_clientsai, name='search_clientsai'),
    path('search_clientssp/', views.search_clientssp, name='search_clientssp'),
    path('search_actionnaires/', views.search_actionnaire, name='search_actionnaires'),
    path('search_actionnairespa/', views.search_actionnairepa, name='search_actionnairespa'),
    path('search_actionnairessp/', views.search_actionnairesp, name='search_actionnairessp'),

    path('clients-proche-echeance/', views.clients_proche_echeance_api, name='clients_proche_echeance_api'),
    path('liste-echeances-non-payees/', views.liste_echeances_non_payees_api, name='liste_echeances_non_payees_api'),
    # KHA
    path('kha/', views.kha, name='kha'),
    path('kha_trans_aide/', views.kha_trans_aide, name='kha_trans_aide'),
    path('kha_trans_pret/', views.kha_trans_pret, name='kha_trans_pret'),
    path('kha_trans_epargne/', views.kha_trans_epargne, name='kha_trans_epargne'),
    path('kha_trans_solde/', views.kha_trans_solde, name='kha_trans_solde'),
    # client
    path('clients-proche-echeanceclient/', views.clients_proche_echeance_apiclient, name='clients_proche_echeance_apiclient'),
    path('echeances-non-payeesclient/', views.liste_echeances_non_payees_apiclient, name='liste_echeances_non_payees_apiclient'),
    path('echeances-non-liste_comptes_json/', views.liste_comptes_json, name='liste_comptes_json'),
    path('client_trans_aide/', views.client_trans_aide, name='client_trans_aide'),
    path('clients_echeance_api/', views.clients_echeance_api, name='clients_echeance_api'),
    path('client_trans_pret/', views.client_trans_pret, name='client_trans_pret'),
    path('client_trans_credit/', views.client_trans_credit, name='client_trans_credit'),
    path('client_trans_epargne/', views.client_trans_epargne, name='client_trans_epargne'),
    # actionnaire
    path('actionnaire_echeance_api/', views.actionnaire_echeance_api, name='actionnaire_echeance_api'),
    path('actionnaire_dividende/', views.actionnaire_dividende, name='actionnaire_dividende'),
    path('actionnaire_trans_pret/', views.actionnaire_trans_pret, name='actionnaire_trans_pret'),
    path('actionnaire_trans_epargne/', views.actionnaire_trans_epargne, name='actionnaire_trans_epargne'),
    path('courbe_transactionsapi/', views.courbe_transactionsapi, name='courbe_transactionsapi'),

    path('actionnaire-compte/detail/<int:id>', views.detail_compte_cooperateur, name='detail_compte_cooperateur'),
    path('actionnaire-compte/detail/<int:id>/retrait/', views.transaction_cpteactionnaire, name='transaction_cpteactionnaire'),
    path('actionnaire-compte/detail/<int:transaction_id>/modifier/', views.modifier_transaction_cpteactionnaire, name='modifier_transaction_cpteactionnaire'),
    # commercial
    path('commercial_trans_pret/', views.commercial_trans_pret, name='commercial_trans_pret'),
    path('clients_echeance_apicom/', views.clients_echeance_apicom, name='clients_echeance_apicom'),
    # Autres URLs de votre application Django
    path('clients-proche-echeanced/', views.clients_proche_echeanced, name='clients_proche_echeanced'),
    #Sponsor
    path('sponsor_dividende/', views.sponsor_dividende, name='sponsor_dividende'),

    #API___2 Juin
    #API___ Juillet 2

    #API___ Juillet 2
    path('aides/', views.aide_list, name='aide_list'),
    path('aides/<int:pk>/', views.aide_detail, name='aide_detail'),
    path('aides/<int:client_id>/create/', views.create_aide, name='create_aide'),
    path('aides/<int:pk>/edit/', views.update_aide, name='update_aide'),
    path('aides/<int:pk>/delete/', views.delete_aide, name='delete_aide'),

    path('tontines/', views.tontine_list, name='tontine_list'),
    path('tontines/create/', views.tontine_create, name='tontine_create'),
    path('tontines/<int:id>/', views.tontine_detail, name='tontine_detail'),
    path('tontines/<int:id>/update/', views.tontine_update, name='tontine_update'),
    path('tontines/<int:id>/delete/', views.tontine_delete, name='tontine_delete'),

    path('tontine/<int:ton>/create/', views.create_tontine, name='create_tontine'),
    path('tontine/update/<int:pk>/', views.update_tontine, name='update_tontine'),

    path('transactions_tontine/', views.transaction_tontine_list, name='transaction_tontine_list'),
    path('transactions_tontine/<int:ton>/create/', views.transaction_tontine_create, name='transaction_tontine_create'),
    path('transactions_tontine/<int:id>/client', views.transaction_tontine_detailclient, name='transaction_tontine_detailclient'),
    path('transactions_tontine/<int:id>/', views.transaction_tontine_detail, name='transaction_tontine_detail'),
    path('transactions_tontine/<int:id>/update/', views.transaction_tontine_update, name='transaction_tontine_update'),
    path('transactions_tontine/<int:id>/delete/', views.transaction_tontine_delete, name='transaction_tontine_delete'),

    path('rachats/', views.rachat_list, name='rachat_list'),
    path('rachats/create/', views.create_rachat, name='create_rachat'),
    path('rachats/<int:idpret>/create/', views.create_rachatpret, name='create_rachatpret'),
    path('rachatssous/<int:idpret>/create/', views.create_rachatpretact, name='create_rachatpretact'),
    #path('rachats/<int:pk>/update/', views.update_rachat, name='update_rachat'),
    path('rachats/<int:pk>/delete/', views.delete_rachat, name='delete_rachat'),
    path('rachat/<int:idpret>/', views.create_or_update_rachatpret, name='create_rachatprett'),
    path('rachat/<int:idpret>/<int:idrachat>/', views.create_or_update_rachatpretm, name='update_rachatpret'),

# SCRIPT
    path('calcul-dividende/', views.calcul_dividendes, name='calcul_dividende'),
    path('penalitejson/', views.penalitejson, name='penalitejson'),
    path('penalitetontinejson/', views.penalite_tontines, name='penalitetontinejson'),
# SCRIPT
    # modifier login et mot de passe
    path('change-username/<int:idact>/', change_username, name='change_username'),
    path('change-password/<int:idact>/', change_password, name='change_password'),
    path('change-usernamecl/<int:idact>/', change_usernamecl, name='change_usernamecl'),
    path('change-passwordcl/<int:idact>/', change_passwordcl, name='change_passwordcl'),
    path('change-usernamesp/<int:idact>/', change_usernamesp, name='change_usernamesp'),
    path('change-passwordsp/<int:idact>/', change_passwordsp, name='change_passwordsp'),
    path('change-usernameag/<int:idact>/', change_usernameag, name='change_usernameag'),
    path('change-passwordag/<int:idact>/', change_passwordag, name='change_passwordag'),

# Gestion des compte Entreprises
    path('tresor-comptekha/detail/', views.detail_compte_kha, name='detail_compte_kha'),
    path('tresor-comptekha/detail/<int:id>/retrait/', views.transaction_cptekha, name='transaction_cptekha'),
    path('tresor-comptekha/detail/<int:transaction_id>/modifier/', views.modifier_transaction_cptekha, name='modifier_transaction_cptekha'),

    path('tresor-comptgerant/detail/', views.detail_compte_fond, name='detail_compte_fond'),
    path('tresor-comptgerant/detail/<int:id>/retrait/', views.transaction_cptefond, name='transaction_cptefond'),
    path('tresor-comptgerant/detail/<int:transaction_id>/modifier/', views.modifier_transaction_cptefond, name='modifier_transaction_cptefond'),

    path('tresor-compteadh/detail/', views.detail_compte_adhesion, name='detail_compte_adhesion'),
    path('tresor-compteadh/detail/<int:id>/retrait/', views.transaction_cpteadhesion, name='transaction_cpteadhesion'),
    path('tresor-compteadh/detail/<int:transaction_id>/modifier/', views.modifier_transaction_cpteadhesion, name='modifier_transaction_cpteadhesion'),

    path('tresor-compteint/detail/', views.detail_compte_interet, name='detail_compte_interet'),
    path('tresor-compteint/detail/<int:id>/retrait/', views.transaction_cpteint, name='transaction_cpteint'),
    path('tresor-compteint/detail/<int:transaction_id>/modifier/', views.modifier_transaction_cpteint, name='modifier_transaction_cpteint'),

    path('tresor-comptepen/detail/', views.detail_compte_penalite, name='detail_compte_penalite'),
    path('tresor-comptepen/detail/<int:id>/retrait/', views.transaction_cptepenalite, name='transaction_cptepenalite'),
    path('tresor-comptepen/detail/<int:transaction_id>/modifier/', views.modifier_transaction_cptepenalite, name='modifier_transaction_cptepenalite'),

    path('tresor-compteprincipal/detail/', views.detail_compte_principal, name='detail_compte_principal'),
    path('tresor-compteportefeuille/detail/', views.detail_compte_portefeuille, name='detail_compte_portefeuille'),

    path('agent/commission/<int:id>/', views.detail_compte_commercial, name='detail_compte_commercial'),
    path('agent/commission/detail/<int:id>/retrait/', views.transaction_cptecommercial, name='transaction_cptecommercial'),
    path('agent/commission/detail/<int:transaction_id>/modifier/', views.modifier_transaction_cptecommercial, name='modifier_transaction_cptecommercial'),

    path('agent-demarcheur/commission/<int:id>/', views.detail_compte_demarcheur, name='detail_compte_demarcheur'),
    path('agent-demarcheur/commission/detail/<int:id>/retrait/', views.transaction_cptedemarcheur, name='transaction_cptedemarcheur'),
    path('agent-demarcheur/commission/detail/<int:transaction_id>/modifier/', views.modifier_transaction_cptedemarcheur, name='modifier_transaction_cptedemarcheur'),

    path('tresor-comptesponsor/detail/<int:id>', views.detail_compte_sponsor, name='detail_compte_sponsor'),
    path('tresor-comptesponsor/detail/<int:id>/retrait/', views.transaction_cptesponsor, name='transaction_cptesponsor'),
    path('tresor-comptesponsor/detail/<int:transaction_id>/modifier/', views.modifier_transaction_cptesponsor, name='modifier_transaction_cptesponsor'),


    path('notify/', payment_notify, name='payment_notify'),
    
    path('process_payment/', process_payment, name='process_payment'),
    #API___ Juillet 2
    path('document/add/>', views.add_document, name='documentadd'),
    path('document/liste', views.listedoc, name='documentlist'),
    path('document/<int:document_id>/', views.document_detail, name='document_detail'),
    path('document/<int:document_id>/download/', views.document_download, name='document_download'),
    path('document/<int:id>/supprimer/', views.delete_doc, name='delete_doc'),
    path('document/<int:id>/docmodification', views.docmodif, name='docmodif'),
    #API___ Aout
    path('api/call-history/', views.add_call_history, name='add_call_history'),

    # AFFICHER LA PAGE DE PRESENTATION______________________________________________________________
    path('presentationapi/', PresentationAPIView.as_view(), name='presentationapi'),

    # CONTACT KHA______________________________________________________________
    path('api/create_msg/', views.create_msg, name='create_msg'),

    # DEMANDE EN LIGNE______________________________________________________________
    path('demandesenligne/', DemandesCreateView.as_view(), name='demandes-create'),
    path('recent_demandes/', RecentDemandesView.as_view(), name='recent_demandes'),

    # DOCUMENT  EN LIGNE CLIENT______________________________________________________________
    path('documents/', views.document_list, name='document_list'),
    path('documents/<int:document_id>/download/', views.document_download, name='document_download'),

    # REINSTIALISER MOT DE PASSE EN LIGNE______________________________________________________________
    path('password-reset-request/', PasswordResetRequestView.as_view(), name='password_reset_request'),
    path('password-reset-confirm/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),

     # NOTIFICATION ______________________________________________________________
    path('recent_msgs/', views.recent_msgs, name='recent_msgs'),
    path('recent_msgss/', views.recent_msgss, name='recent_msgss'),
    
    # PROVISION CONTRAT______________________________________________________________
    path('expiring_contrats/', views.get_expiring_contrats, name='get_expiring_contrats'),

    # DEPENSE EN LIGNE API______________________________________________________________
    path('save_depense/', views.save_depense, name='save_depense'),

    # AJOUTER COOPERATEUR EN LIGNE______________________________________________________________
    path('api/actionnaires/', ActionnaireViewSet.as_view({
        'get': 'list',  # Liste tous les actionnaires
        'post': 'create',  # Crée un nouvel actionnaire
    }), name='actionnaire-list'),
    
    #API___ Aout
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)