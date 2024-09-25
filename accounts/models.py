from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser,AbstractBaseUser


class Utilisateurs(AbstractUser):
    
    GESTIONNAIRE = 'GESTIONNAIRE'
    ACTIONNAIRE = 'ACTIONNAIRE'
    ADMINISTRATEUR = 'ADMINISTRATEUR'
    ADMINISTRATEURSUPER = 'ADMINISTRATEURSUPER'

    ROLE_CHOICES = (
        (GESTIONNAIRE, 'Gestionnaire'),
        (ACTIONNAIRE,'Actionnaire'),
        (ADMINISTRATEUR, 'Administrateur'),
        (ADMINISTRATEURSUPER, 'Administrateur Super'),
    )
    PHONE_NUMBER = 'PHONE_NUMBER'

    phone_number = models.CharField(max_length=15, unique=True, null=True, blank=True)
    photo = models.ImageField(verbose_name='photo de profil', upload_to='Mediatheques/', null=True, blank=True)
    role = models.CharField(max_length=30, choices=ROLE_CHOICES, verbose_name='rôle')
    statut = models.CharField(max_length=10, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.get_role_display()}"
    

