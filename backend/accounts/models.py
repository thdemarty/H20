from django.contrib.auth.models import AbstractUser
from django.shortcuts import reverse
from django.db import models


import datetime, json, requests

CIV_CHOICES = [
    ("I", "Indéterminé"),
    ("F", "Féminin"),
    ("M", "Masculin"),
]

STATUT_CHOICES = [
    ("P", "Provisoire"),
    ("R", "Récupérée"),
    ("V", "Vérifiée"),
    ("Q", "Qualifiée")
]

STATUT_COMPL_CHOICES = [
    ("H", "Homonyme"),
    ("F", "Fictive"),
    ("D", "Douteuse"),
]

class Utilisateur(AbstractUser):
    pass

class Patient(models.Model):
    statut = models.CharField(max_length=1, choices=STATUT_CHOICES, verbose_name="Statut d'identité")
    statut_compl = models.CharField(max_length=1, choices=STATUT_COMPL_CHOICES, blank=True, verbose_name="Statut d'identité complémentaire")
    ins = models.CharField(max_length=15, verbose_name="Matricule INS")
    oid = models.CharField(max_length=20, verbose_name="Object identifier")
    # Identité secondaire
    used_fname = models.CharField(max_length=100, verbose_name="Prénom utilisé")
    used_lname = models.CharField(max_length=100, verbose_name="Nom utilisé")
    # Identité primaire
    civilite = models.CharField(max_length=2, choices=CIV_CHOICES, verbose_name="civilité")
    birth_lname = models.CharField(max_length=100, verbose_name="Nom de naissance")
    birth_fnames = models.CharField(max_length=100, verbose_name="Prénom(s) de naissance")
    birth_fname = models.CharField(max_length=100, verbose_name="Premier prénom de naissance")
    birth_date = models.DateField(verbose_name="Date de naissance")
    birth_insee = models.CharField(max_length=5, verbose_name="Commune de naissance - code INSEE")
    
    def get_absolute_url(self):
        return reverse("accounts:patient_identity", kwargs={"pk": self.pk})
    
    def get_age(self):
        today = datetime.datetime.now()
        diff = abs((today-self.birth_date))
        return diff

    def get_commune(self):
        # FIXME Temporary solution => Urgent fixe
        cities_json = requests.get("http://127.0.0.1:8000/static/utils/commune2021.json").json()
        cities_name = [x for x in cities_json if x['INSEE'] == str(self.birth_insee)]
        return cities_name[0].get("Nom").upper()

    def __str__(self):
        return "{} {} - Né le {}".format(self.birth_lname.upper(), self.birth_fnames, self.birth_date.strftime("%d %B %Y"))

    class Meta:
        permissions = [
            ("can_change_qualify_identity", "Can change qualify identity"),
            ("can_set_statut_provisoire", "Can set identities status to temporary"),
            ("can_view_detail_patient", "Can view patient detail"),
        ]