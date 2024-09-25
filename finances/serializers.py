# finances/serializers.py
from decimal import Decimal
from rest_framework import serializers # type: ignore
from .models import Actionnaire, Clients, CompteEpargnes, Statuts,Presentation

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clients
        fields = '__all__'

from rest_framework import serializers # type: ignore
from .models import Echeancier, Echeancieract

class EcheancierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Echeancier
        fields = '__all__'

class EcheancieractSerializer(serializers.ModelSerializer):
    class Meta:
        model = Echeancieract
        fields = '__all__'



from rest_framework import serializers # type: ignore
from .models import Echeancieract, TransactionPretact

class EcheancieractSerializer(serializers.ModelSerializer):
    class Meta:
        model = Echeancieract
        fields = ['id', 'compte_pretact', 'date_echeance', 'montant_echeance', 'montant_interet', 'est_paye', 'montant_epargne','montant_adhesion']

class TransactionPretactSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionPretact
        fields = ['id', 'compte_pret', 'montant', 'type_transaction', 'date_transaction', 'agent']


from rest_framework import serializers # type: ignore
from .models import ComptePretsact

class ComptePretsactSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComptePretsact
        fields = '__all__'

    def validate(self, data):
        data['taux_interet'] = Decimal(data.get('taux_interet', 1))
        data['solde'] = Decimal(data.get('solde', 0))
        data['duree_en_mois'] = int(data.get('duree_en_mois', 12))
        return data

#API___ Aout
from .models import CallHistory

class CallHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CallHistory
        fields = '__all__'

class PresentationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Presentation
        #fields = ['logo', 'contact', 'presentation_text', 'welcome_message', 'video_url']
        fields = ['logo', 'contact', 'presentation_text', 'welcome_message', 'video_url','site','pub','email','whatsapp','facebook']


from .models import Demandes

class DemandesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Demandes
        fields = '__all__'



class DemandesSerializerr(serializers.ModelSerializer):
    class Meta:
        model = Demandes
        fields = ['Nom_prenoms', 'typedde', 'montant', 'phone_number']


from rest_framework import serializers # type: ignore
from .models import Depense

class DepenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Depense
        fields = '__all__'

# Serializer pour l'Actionnaire
class ActionnaireSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actionnaire
        fields = ['nom', 'prenom', 'adresse', 'telephone', 'email', 'apport', 'type_act']

#API___ Aout