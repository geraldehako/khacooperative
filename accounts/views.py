from django.shortcuts import get_object_or_404, render
from django.contrib.auth import login
from django.shortcuts import redirect, render
from django.contrib.auth import logout
from django.contrib.auth import authenticate
from finances.models import Actionnaire, Agent, Clients,Sponsors

# Create your views here.
# AUTHENTIFICATION--------------------------------------------------------------------------------------------
# Create your views here.

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_active:
            login(request, user)
            if request.user.role == 'ADMINISTRATEUR':
                return redirect('menu')
            elif request.user.role == 'ACTIONNAIRE':
                return redirect('menuact')
            elif request.user.role == 'ASSISTANT':
                return redirect('courbe_transactions')
            elif request.user.role == 'CONSEILLER':
                return redirect('courbe_transactions')
            elif request.user.role == 'ADMINISTRATEURSUPER':
                return redirect('menu')

    return render(request,'Pages/Log/login.html')

def logout_user(request):
    logout(request)
    return redirect('login')


#API___ Juillet 2------------------------------------------------------------------------------
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from .models import Utilisateurs

@csrf_exempt
def login_userbank(request):
    if request.method == "POST":
        print("Requête POST reçue")
        print(request.POST)  # Ajouter un log pour voir les données reçues
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if not username or not password:
            print("Nom d'utilisateur ou mot de passe manquant")
            return JsonResponse({'success': False, 'error': 'Missing username or password'}, status=400)
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                # Assurez-vous que l'utilisateur a un profil associé avec un rôle défini
                profile = Utilisateurs.objects.get(pk=user.id)  # Adapté à votre modèle Utilisateurs
                role = profile.role if profile else 'unknown'
                visite = profile.last_login if profile else 'unknown'
                email = profile.email if profile else 'unknown'
                first_name = profile.first_name if profile else 'unknown'
                last_name = profile.last_name if profile else 'unknown'
                print(f"Utilisateur authentifié: {username}, rôle: {role} , Nom: {first_name}")
                response = {
                    'success': True,
                    'role': role,'visite':visite,'email':email,'first_name':first_name,'last_name':last_name
                }
                return JsonResponse(response)
            else:
                print("Compte utilisateur inactif")
                return JsonResponse({'success': False, 'error': 'Inactive account'}, status=400)
        else:
            print("Identifiants invalides")
            return JsonResponse({'success': False, 'error': 'Invalid credentials'}, status=400)
    else:
        print("Méthode de requête non autorisée")
        return JsonResponse({'error': 'Invalid request method'}, status=405)

@csrf_exempt
def logout_userbank(request):
    if request.method == 'POST':
        logout(request)
        return JsonResponse({'success': True})
    return JsonResponse({'success': False}, status=400)


# CHANGER LES IDENTIFIANTS ET MOT DE PASSE _______________________________________________________________________________________________________________________
#update mot de passe et login actionnaire
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash

# Importations spécifiques au projet
from .forms import UsernameChangeForm, CustomPasswordChangeForm
from finances.models import Actionnaire, Utilisateurs

@login_required
def change_username(request, idact):
    """
    Fonction pour changer le nom d'utilisateur de l'utilisateur connecté.
    """
    action = get_object_or_404(Actionnaire, user=idact)
    Util = get_object_or_404(Utilisateurs, pk=action.user.id)
    
    if request.method == 'POST':
        form = UsernameChangeForm(request.POST, instance=Util)
        if form.is_valid():
            form.save()
            messages.success(request, 'Votre nom d\'utilisateur a été mis à jour avec succès.')
            return redirect('liste_actionnaires')
    else:
        form = UsernameChangeForm(instance=Util)
    
    return render(request, 'Pages/Utilisateur/change_username.html', {'form': form})

@login_required
def change_password(request, idact):
    """
    Fonction pour changer le mot de passe de l'utilisateur connecté.
    """
    action = get_object_or_404(Actionnaire, user=idact)
    Util = get_object_or_404(Utilisateurs, pk=action.user.id)
    
    if request.method == 'POST':
        form = CustomPasswordChangeForm(Util, request.POST)
        if form.is_valid():
            #user = form.save()
            form.save()
            #update_session_auth_hash(request, user)  # Important pour maintenir l'utilisateur connecté après le changement de mot de passe
            messages.success(request, 'Votre mot de passe a été mis à jour avec succès.')
            return redirect('liste_actionnaires')
    else:
        form = CustomPasswordChangeForm(Util)
    
    return render(request, 'Pages/Utilisateur/change_password.html', {'form': form})

#update mot de passe et login client 
@login_required
def change_usernamecl(request, idact):
    """
    Fonction pour changer le nom d'utilisateur de l'utilisateur connecté.
    """
    action = get_object_or_404(Clients, user=idact)
    Util = get_object_or_404(Utilisateurs, pk=action.user.id)
    
    if request.method == 'POST':
        form = UsernameChangeForm(request.POST, instance=Util)
        if form.is_valid():
            form.save()
            messages.success(request, 'Votre nom d\'utilisateur a été mis à jour avec succès.')
            return redirect('liste_clients')
    else:
        form = UsernameChangeForm(instance=Util)
    
    return render(request, 'Pages/Utilisateur/change_username.html', {'form': form})

@login_required
def change_passwordcl(request, idact):
    """
    Fonction pour changer le mot de passe de l'utilisateur connecté.
    """
    action = get_object_or_404(Clients, user=idact)
    Util = get_object_or_404(Utilisateurs, pk=action.user.id)
    
    if request.method == 'POST':
        form = CustomPasswordChangeForm(Util, request.POST)
        if form.is_valid():
            #user = form.save()
            form.save()
            #update_session_auth_hash(request, user)  # Important pour maintenir l'utilisateur connecté après le changement de mot de passe
            messages.success(request, 'Votre mot de passe a été mis à jour avec succès.')
            return redirect('liste_clients')
    else:
        form = CustomPasswordChangeForm(Util)
    
    return render(request, 'Pages/Utilisateur/change_password.html', {'form': form})

#update mot de passe et login sponsor
@login_required
def change_usernamesp(request, idact):
    """
    Fonction pour changer le nom d'utilisateur de l'utilisateur connecté.
    """
    action = get_object_or_404(Sponsors, user=idact)
    Util = get_object_or_404(Utilisateurs, pk=action.user.id)
    
    if request.method == 'POST':
        form = UsernameChangeForm(request.POST, instance=Util)
        if form.is_valid():
            form.save()
            messages.success(request, 'Votre nom d\'utilisateur a été mis à jour avec succès.')
            return redirect('liste_clients')
    else:
        form = UsernameChangeForm(instance=Util)
    
    return render(request, 'Pages/Utilisateur/change_username.html', {'form': form})

@login_required
def change_passwordsp(request, idact):
    """
    Fonction pour changer le mot de passe de l'utilisateur connecté.
    """
    action = get_object_or_404(Sponsors, user=idact)
    Util = get_object_or_404(Utilisateurs, pk=action.user.id)
    
    if request.method == 'POST':
        form = CustomPasswordChangeForm(Util, request.POST)
        if form.is_valid():
            #user = form.save()
            form.save()
            #update_session_auth_hash(request, user)  # Important pour maintenir l'utilisateur connecté après le changement de mot de passe
            messages.success(request, 'Votre mot de passe a été mis à jour avec succès.')
            return redirect('liste_clients')
    else:
        form = CustomPasswordChangeForm(Util)
    
    return render(request, 'Pages/Utilisateur/change_password.html', {'form': form})

#update mot de passe et login agent
@login_required
def change_usernameag(request, idact):
    """
    Fonction pour changer le nom d'utilisateur de l'utilisateur connecté.
    """
    action = get_object_or_404(Agent, user=idact)
    Util = get_object_or_404(Utilisateurs, pk=action.user.id)
    
    if request.method == 'POST':
        form = UsernameChangeForm(request.POST, instance=Util)
        if form.is_valid():
            form.save()
            messages.success(request, 'Votre nom d\'utilisateur a été mis à jour avec succès.')
            return redirect('liste_agents')
    else:
        form = UsernameChangeForm(instance=Util)
    
    return render(request, 'Pages/Utilisateur/change_username.html', {'form': form})

@login_required
def change_passwordag(request, idact):
    """
    Fonction pour changer le mot de passe de l'utilisateur connecté.
    """
    action = get_object_or_404(Agent, user=idact)
    Util = get_object_or_404(Utilisateurs, pk=action.user.id)
    
    if request.method == 'POST':
        form = CustomPasswordChangeForm(Util, request.POST)
        if form.is_valid():
            #user = form.save()
            form.save()
            #update_session_auth_hash(request, user)  # Important pour maintenir l'utilisateur connecté après le changement de mot de passe
            messages.success(request, 'Votre mot de passe a été mis à jour avec succès.')
            return redirect('liste_agents')
    else:
        form = CustomPasswordChangeForm(Util)
    
    return render(request, 'Pages/Utilisateur/change_password.html', {'form': form})

from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def profile_view(request):
    return render(request, 'Pages/Utilisateur/profile.html', {'user': request.user})
# __________________________________________________________________________________________________________________________________________________________
# #API___ Juillet 2 ---




#API____________________________________________________________________________________________________________________________________________________
# Authentification
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework import status


from django.middleware.csrf import get_token
from django.http import JsonResponse

def get_csrf_token(request):
    # Obtenez le jeton CSRF en appelant la fonction get_token
    csrf_token = get_token(request)
    
    # Retournez le jeton CSRF dans la réponse JSON
    return JsonResponse({'csrf_token': csrf_token})



@method_decorator(csrf_exempt, name='dispatch')
class LoginAPIView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            role = user.role  # Supposons que le rôle de l'utilisateur soit stocké dans un champ de modèle
            return JsonResponse({'success': True, 'role': role})
        else:
            return JsonResponse({'success': False, 'message': 'Nom d\'utilisateur ou mot de passe incorrect.'}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        # Répondez à la requête GET avec une erreur "Method Not Allowed"
        return JsonResponse({'message': 'Method Not Allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

from django.views.decorators.http import require_POST
from django.contrib.auth import authenticate, login
from django.http import JsonResponse

@require_POST
def login_usera(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Authentification réussie
            login(request, user)
            role = user.role  # Supposons que le rôle de l'utilisateur soit stocké dans un champ de modèle
            return JsonResponse({'success': True, 'role': role})
        else:
            # Échec de l'authentification
            return JsonResponse({'success': False, 'message': 'Nom d\'utilisateur ou mot de passe incorrect.'})

    else:
        # Requête non autorisée
        return JsonResponse({'success': False, 'message': 'Méthode non autorisée. Utilisez POST pour vous connecter.'})

# REINTIALISATION DU MOT DE PASSE CLIENT____________________________________________________________________________________________________________________________________________________
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.mail import send_mail
from .models import Utilisateurs
from .serializers import PasswordResetRequestSerializer, PasswordResetConfirmSerializer
from django.contrib.auth.hashers import make_password

class PasswordResetRequestView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = PasswordResetRequestSerializer(data=request.data)
        if serializer.is_valid():
            phone_number = serializer.validated_data['phone_number']
            user = Utilisateurs.objects.filter(phone_number=phone_number).first()
            if user:
                # Logique d'envoi de code de vérification par e-mail ou SMS
                return Response({'detail': 'Un code de vérification a été envoyé.'}, status=status.HTTP_200_OK)
            return Response({'detail': 'Utilisateur non trouvé.'}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PasswordResetConfirmView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        if serializer.is_valid():
            phone_number = serializer.validated_data['phone_number']
            new_password = serializer.validated_data['new_password']
            user = Utilisateurs.objects.filter(phone_number=phone_number).first()
            if user:
                user.password = make_password(new_password)
                user.save()
                return Response({'detail': 'Mot de passe réinitialisé avec succès.'}, status=status.HTTP_200_OK)
            return Response({'detail': 'Utilisateur non trouvé.'}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#API____________________________________________________________________________________________________________________________________________________